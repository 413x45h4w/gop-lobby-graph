# Match FEC individual contributions (to ALL current members' committees) to EVERY person in people_all.csv.
# Same rules as full/fec_match.py, with extra false-positive safeguards needed at full-universe scale:
#  * employer->registrant matching uses only DISTINCTIVE registrant words (appearing in <=25 of all LDA registrant names), so 'AMERICAN','NATIONAL','ASSOCIATION' etc. cannot create a high match
#  * several same-name candidates tied at the best confidence -> ambiguous file (old code took the first)
#  * medium (lobbying occupation) match whose employer is exactly a DIFFERENT LDA registrant -> ambiguous file
import json,csv,re,sys,datetime,collections,gzip,glob
sys.path.insert(0,'..'); from nicks import NICK
NOW=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
P={r['person_id']:r for r in csv.DictReader(open('people_all.csv'))}
lid2p={i:r['person_id'] for r in P.values() for i in r['person_key'].split('|')}
SUF={'JR','SR','II','III','IV'}
def cl(s): return ' '.join(x for x in re.split(r'[\s\.]+',(s or '').upper().strip()) if x and x not in SUF)
names=collections.defaultdict(set); regs=collections.defaultdict(set)
for fn in glob.glob('../../lda/ld2_universe/*.jsonl.gz'):
  for line in gzip.open(fn,'rt'):
    d=json.loads(line)
    for a in d['acts']:
      for lid,fi,la,_ in a['lob']:
        if str(lid) in lid2p and fi and la: names[lid2p[str(lid)]].add((cl(la),fi.upper().split()[0].strip('.'))); regs[lid2p[str(lid)]].add(d['rn'])
for fn in glob.glob('../../lda/ld203_universe/*.jsonl.gz'):
  for line in gzip.open(fn,'rt'):
    d=json.loads(line)
    if str(d.get('lid')) in lid2p and d.get('fn') and d.get('ln'): names[lid2p[str(d['lid'])]].add((cl(d['ln']),d['fn'].upper().split()[0].strip('.'))); regs[lid2p[str(d['lid'])]].add(d['rn'] or '')
STOPW={'THE','LLC','LLP','INC','GROUP','GOVERNMENT','RELATIONS','STRATEGIES','PARTNERS','AFFAIRS','PUBLIC','CONSULTING','ASSOCIATES','AND','COMPANY','LAW','CAPITOL','POLICY','ADVISORS','STRATEGY','STRATEGIC','SOLUTIONS','FIRM','OF','PLLC','LTD','CORP','CORPORATION','CO','FOR','USA','US'}
W=lambda s:re.findall(r"[A-Z0-9']{3,}",(s or '').upper())
allregs={r for s in regs.values() for r in s}
df=collections.Counter(w for r in allregs for w in set(W(r)))
DIST=lambda w: w not in STOPW and df[w]<=25
def normorg(s): return ' '.join(w for w in W(s) if w not in STOPW)
regnorm={normorg(r):r for r in allregs if normorg(r)}
idx=collections.defaultdict(list)
for pid,ns in names.items():
  rw=set(); phr=set()
  for rg in regs[pid]:
    ws=W(rg); rw|={w for w in ws if DIST(w)}
    t=re.findall(r"[A-Z0-9']+",rg.upper())[:2]
    if len(t)==2 and any(DIST(x) for x in t): phr.add(' '.join(t))
  lasts={l for l,_ in ns}
  rw-= {w for l in lasts for w in l.split()}
  for la,fi in ns:
    for f in {fi}|set(NICK.get(fi,[]))|{k for k,v in NICK.items() if fi in v}: idx[(la,f)].append((pid,rw,phr,{normorg(r) for r in regs[pid]}))
for k in idx: idx[k]=list({c[0]:c for c in idx[k]}.values())
print('indexed people',len(names),'keys',len(idx),file=sys.stderr)
LOBW=re.compile(r'LOBBY|GOVERNMENT RELATIONS|GOV(ERNMENT|\'T)? AFFAIRS|PUBLIC (AFFAIRS|POLICY)|ADVOCA|LEGISLATIVE|POLICY',re.I)
PROW=re.compile(r'CONSULT|ATTORNEY|LAWYER|COUNSEL|PARTNER|PRINCIPAL|PRESIDENT|CEO|OWNER|EXECUTIVE|DIRECTOR|FOUNDER|MANAGING|VICE',re.I)
RANK={'high_employer_matches_registrant':0,'medium_lobbying_occupation':1,'low_dc_area_professional':2}
out=[];amb=[];stat=collections.Counter();rej=collections.Counter()
for cyc in ('24','26'):
  seen=set()
  for line in gzip.open(f'raw/fec_indiv{cyc}_allmember_poolname.jsonl.gz','rt'):
    d=json.loads(line)
    if d['sub_id'] in seen: continue
    seen.add(d['sub_id'])
    last,rest=d['name'].split(',',1); last=cl(last)
    toks=[t for t in re.split(r'[\s\.]+',rest) if t and t not in ('MR','MS','MRS','DR','HON')]
    if not toks: continue
    cands=idx.get((last,toks[0]),[])
    if not cands: continue
    stat['name_hit']+=1
    dt=d['dt']; iso=f"{dt[4:8]}-{dt[0:2]}-{dt[2:4]}" if len(dt)==8 else dt
    if iso<'2023-01-01': stat['pre2023']+=1; continue
    ew=set(W(d['emp']+' '+d['occ'])); empn=' '.join(re.findall(r"[A-Z0-9']+",d['emp'].upper())); en=normorg(d['emp'])
    scored=[]
    for pid,rw,phr,rn in cands:
      if (rw & ew) or any(p in empn for p in phr): c='high_employer_matches_registrant'
      elif LOBW.search(d['emp']+' '+d['occ']): c='medium_lobbying_occupation'
      elif PROW.search(d['occ']) and d['st'] in ('DC','VA','MD'): c='low_dc_area_professional'
      else: c=None
      if c: scored.append((RANK[c],c,pid,rn))
    base=dict(bioguide=d['bio'],committee_link=d['link'],fec_committee_id=d['cmte'],fec_contributor_name=d['name'],city=d['city'],state=d['st'],employer=d['emp'],occupation=d['occ'],
      date=iso,amount=d['amt'],transaction_tp=d['tp'],memo_cd=d['memo'],memo_text=d['memo_text'],fec_sub_id=d['sub_id'],fec_image_num=d['image'],
      fec_url=f"https://docquery.fec.gov/cgi-bin/fecimg/?{d['image']}",cycle='20'+cyc,computed_at=NOW)
    if not scored: rej['no_employer_or_occupation_evidence']+=1; continue
    best=min(s[0] for s in scored); top=[s for s in scored if s[0]==best]
    reason=''
    if len(top)>1: reason=f'{len(top)} same-name LDA people tie at {top[0][1]}'
    elif len(cands)>1 and best>0: reason=f'{len(cands)} same-name LDA people and best evidence only {top[0][1]}'
    elif best==1 and en and en in regnorm and en not in top[0][3]: reason=f'lobbying occupation but employer is a different LDA registrant ({regnorm[en]})'
    if reason:
      amb.append(dict(candidate_person_ids='|'.join(s[2] for s in top),candidate_names='|'.join(P[s[2]]['name'] for s in top),candidate_firms='|'.join(P[s[2]]['main_registrant'] for s in top),reason=reason,**base)); stat['ambiguous']+=1; continue
    s=top[0]; stat[s[1]]+=1
    out.append(dict(person_id=s[2],lobbyist=P[s[2]]['name'],lobbyist_firm=P[s[2]]['main_registrant'],match_confidence=s[1],**base))
w=csv.DictWriter(open('edges_fec_all.csv','w'),fieldnames=list(out[0]));w.writeheader();w.writerows(out)
w=csv.DictWriter(open('fec_ambiguous_all.csv','w'),fieldnames=list(amb[0]));w.writeheader();w.writerows(amb)
json.dump(dict(computed_at=NOW,stats=stat,rejected=rej,rows=len(out),people=len({o['person_id'] for o in out}),ambiguous_rows=len(amb)),open('fec_match_stats.json','w'),indent=1)
print(stat,rej,len(out),'rows',len({o['person_id'] for o in out}),'people')
