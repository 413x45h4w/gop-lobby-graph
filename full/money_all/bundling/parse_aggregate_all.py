# Parse SA3L (bundled-contribution) lines from every Form 3L .fec file (cycles 2024+2026 + member all-time query, cov. end >= 2023) and match bundlers to EVERY person in people_all.csv.
# Individual bundlers: (last, first/nickname) -> people; confidence 1 high = employer shares a distinctive registrant word (or 2-word registrant phrase), 2 medium = name + DC/VA/MD address, 3 low = name only (never scored).
#   Several same-name people tied at the best tier -> ambiguous (not scored).
# Org/PAC bundlers: normalized org name == normalized LDA registrant name -> registrant-level edge; credited to that registrant's people in the universe split equally (same as GOP build).
# Aggregation as before: most-recent versions only; per (committee, bundler, half-year) total = max(sum of period amounts, max semi-annual cumulative).
import json,csv,re,sys,datetime,collections,gzip,glob
sys.path.insert(0,'../..'); from nicks import NICK
NOW=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
R={r['file_number']:r for r in json.load(open('f3l_filings_union.json'))}
G={r['committee_id']:r for r in csv.DictReader(open('member_committees_all.csv'))}
P={r['person_id']:r for r in csv.DictReader(open('../people_all.csv'))}
lid2p={i:r['person_id'] for r in P.values() for i in r['person_key'].split('|')}
SUF={'JR','SR','II','III','IV'}
def cl(s): return ' '.join(x for x in re.split(r'[\s\.]+',(s or '').upper().strip()) if x and x not in SUF)
names=collections.defaultdict(set); regs=collections.defaultdict(set)
for fn in glob.glob('../../../lda/ld2_universe/*.jsonl.gz'):
  for line in gzip.open(fn,'rt'):
    d=json.loads(line)
    for a in d['acts']:
      for lid,fi,la,_ in a['lob']:
        if str(lid) in lid2p and fi and la: names[lid2p[str(lid)]].add((cl(la),fi.upper().split()[0].strip('.'))); regs[lid2p[str(lid)]].add(d['rn'])
for fn in glob.glob('../../../lda/ld203_universe/*.jsonl.gz'):
  for line in gzip.open(fn,'rt'):
    d=json.loads(line)
    if str(d.get('lid')) in lid2p and d.get('fn') and d.get('ln'): names[lid2p[str(d['lid'])]].add((cl(d['ln']),d['fn'].upper().split()[0].strip('.'))); regs[lid2p[str(d['lid'])]].add(d['rn'] or '')
STOPW={'&','THE','LLC','LLP','INC','GROUP','GOVERNMENT','RELATIONS','STRATEGIES','PARTNERS','AFFAIRS','PUBLIC','CONSULTING','ASSOCIATES','AND','COMPANY','LAW','CAPITOL','POLICY','ADVISORS','STRATEGY','STRATEGIC','SOLUTIONS','FIRM','OF','PLLC','LTD','CORP','CORPORATION','CO','FOR','USA','US','PAC','POLITICAL','ACTION','COMMITTEE'}
W=lambda s:re.findall(r"[A-Z0-9&']{3,}",(s or '').upper())
allregs={r for s in regs.values() for r in s}
df=collections.Counter(w for r in allregs for w in set(W(r)))
DIST=lambda w: w not in STOPW and df[w]<=25
def normorg(s): return ' '.join(w for w in re.findall(r"[A-Z0-9&']+",(s or '').upper()) if w not in STOPW)
reg2p=collections.defaultdict(set)
for pid,rs in regs.items():
  for rg in rs:
    if normorg(rg): reg2p[normorg(rg)].add(pid)
regname={normorg(rg):rg for rg in allregs}
idx=collections.defaultdict(dict)
for pid,ns in names.items():
  rw=set(); phr=set()
  for rg in regs[pid]:
    rw|={w for w in W(rg) if DIST(w)}
    t=re.findall(r"[A-Z0-9&']+",rg.upper())[:2]
    if len(t)==2 and any(DIST(x) for x in t): phr.add(' '.join(t))
  rw-={w for l,_ in ns for w in l.split()}
  for la,fi in ns:
    for f in {fi}|set(NICK.get(fi,[]))|{k for k,v in NICK.items() if fi in v}: idx[(la,f)][pid]=(rw,phr)
# Org/PAC bundler -> LDA registrant, resolved per FEC PAC id (so spelling variants of one PAC resolve identically):
# candidates = FEC cm connected-org name, FEC cm committee name, every org string reported for that PAC id; each with PAC suffixes/parentheticals stripped.
# Match = exact normalized (or space-free) equality with a registrant name, else the longest registrant name (>=2 words, >=1 distinctive word) that is a whole-word prefix.
CMN={}
for yy in ('24','26'):
  for line in open(f'../raw/fec_bulk/cm{yy}.txt',encoding='latin-1'):
    q=line.rstrip('\n').split('|'); CMN[q[0]]=(q[1],q[13])
PACSUF=re.compile(r"\(.*?\)|\b(POLITICAL ACTION (COMMITTEE|FUND)|CIVIC ACTION COMMITTEE|COMMITTEE FOR EFFECTIVE GOVERNMENT|POLITICAL|PAC|FEDERAL|AKA)\b",re.I)
def strip_pac(s): return normorg(PACSUF.sub(' ',s or ''))
regkeys={k:v for k,v in reg2p.items()}
compact={k.replace(' ',''):k for k in regkeys}
def resolve(cands):
  for c in cands:
    if c in regkeys: return c,'exact'
    if c.replace(' ','') in compact: return compact[c.replace(' ','')],'exact_spacefree'
  best=None
  for c in cands:
    for k in regkeys:
      kt=k.split()
      if len(kt)>=2 and any(DIST(w) for w in kt) and (c+' ').startswith(k+' ') and (best is None or len(k)>len(best)): best=k
  return (best,'prefix') if best else (None,'')
orgnames=collections.defaultdict(set)
for fn,rec in R.items():
  try: txt=open(f'fecfiles/{fn}.fec','rb').read().decode('latin-1')
  except FileNotFoundError: continue
  for line in txt.replace('\r','').split('\n'):
    q=line.split('\x1c')+['']*40
    if q[0]=='SA3L' and q[5]!='IND': orgnames[(q[25] or '').upper().strip() or 'NOID:'+q[6].upper()].add(q[6])
PACRES={}
for pid_,ns in orgnames.items():
  cands=[]
  if pid_ in CMN: cands+= [strip_pac(CMN[pid_][1]), strip_pac(CMN[pid_][0])]
  cands+=[strip_pac(n) for n in sorted(ns)]
  PACRES[pid_]=resolve([c for c in cands if c])
with open('org_bundler_resolution.csv','w') as fo:
  wq=csv.writer(fo); wq.writerow(['fec_pac_id','reported_names','fec_cm_name','fec_connected_org','resolved_registrant','method','n_people_in_universe','computed_at'])
  for k,(r_,m_) in sorted(PACRES.items()): wq.writerow([k,' | '.join(sorted(orgnames[k])),CMN.get(k,('',''))[0],CMN.get(k,('',''))[1],regname.get(r_,'') if r_ else '',m_,len(reg2p[r_]) if r_ else 0,NOW])
lines=[]
for fn,rec in R.items():
  try: txt=open(f'fecfiles/{fn}.fec','rb').read().decode('latin-1')
  except FileNotFoundError: continue
  for line in txt.replace('\r','').split('\n'):
    f=line.split('\x1c')
    if f[0]!='SA3L': continue
    f+=['']*40
    ent=f[5]; org=f[6]; last=cl(f[7]); first=f[8].upper().replace('.','').strip(); emp,occ=f[23],f[24]
    try: amt=float(f[20] or 0)
    except: amt=0.0
    try: semi=float(f[21] or 0)
    except: semi=0.0
    match=[];conf='';amb='';orgreg=''
    if ent=='IND':
      fk=first.split()[0] if first else ''
      cand=[]
      ew=set(W(emp)); empraw=' '.join(re.findall(r"[A-Z0-9&']+",emp.upper()))
      for pid,(rw,phr) in idx.get((last,fk),{}).items():
        if (ew & rw) or any(p in empraw for p in phr): c='1_high_employer_matches_registrant'
        elif f[15] in ('DC','VA','MD'): c='2_medium_name_dc_area'
        else: c='3_low_name_only'
        cand.append((c,pid))
      if cand:
        best=min(c for c,_ in cand); match=sorted({i for c,i in cand if c==best}); conf=best[2:]
        if len(match)>1: amb=f'{len(match)} same-name LDA people tie at {conf}'
        elif len(cand)>1 and not best.startswith('1'): amb=f'{len(cand)} same-name LDA people, best only {conf}'
    else:
      rk,meth=PACRES.get((f[25] or '').upper().strip() or 'NOID:'+org.upper(),(None,''))
      if rk: match=sorted(reg2p[rk]); conf=f'org_pac_to_registrant_{meth}'; orgreg=regname.get(rk,'')
    g=G.get(rec['committee_id'])
    lines.append(dict(file_number=fn,committee_id=rec['committee_id'],committee_name=rec['committee_name'],member_bioguide=g['bioguide'] if g else '',member=g['member'] if g else '',member_party=g['party'] if g else '',committee_link=g['link_type'] if g else '',
      cycle=rec.get('cycle'),report_type=rec.get('report_type'),coverage_start=(rec.get('coverage_start_date') or '')[:10],coverage_end=(rec.get('coverage_end_date') or '')[:10],receipt_date=(rec.get('receipt_date') or '')[:10],
      amendment_indicator=rec.get('amendment_indicator'),most_recent=rec.get('most_recent'),bundler_entity=ent,bundler_org=org,bundler_last=f[7],bundler_first=f[8],bundler_city=f[14],bundler_state=f[15],
      bundler_employer=emp,bundler_occupation=occ,bundler_pac_id=f[25] if ent!='IND' else '',period_bundled_usd=amt,semiannual_bundled_usd=semi,
      matched_person_ids='|'.join(match),match_confidence=conf,ambiguous_reason=amb,matched_registrant=orgreg,pdf_url=rec.get('pdf_url'),fec_url=rec.get('fec_url'),computed_at=NOW))
w=csv.DictWriter(open('f3l_sa3l_lines_all.csv','w'),fieldnames=list(lines[0]));w.writeheader();w.writerows(lines)
O=[o for o in lines if o['most_recent'] in (True,'True') and '2023-01-01'<=o['coverage_end']<='2026-12-31']
def half(d): return d[:4]+('H1' if d[5:7]<='06' else 'H2')
def key(o): return (o['committee_id'],o['bundler_entity'],(o['bundler_last']+','+o['bundler_first']).upper() if o['bundler_entity']=='IND' else o['bundler_org'].upper(),half(o['coverage_end']))
gp=collections.defaultdict(list)
for o in O: gp[key(o)].append(o)
agg=[]
for k,rows in gp.items():
  per=sum(float(r['period_bundled_usd']) for r in rows); semi=max(float(r['semiannual_bundled_usd']) for r in rows); r0=rows[0]
  ids=[i for i in r0['matched_person_ids'].split('|') if i]
  agg.append(dict(scope='member_pcc_jfc_or_lpac' if r0['member_bioguide'] else 'nonmember_committee_context',committee_id=k[0],committee_name=r0['committee_name'],member_bioguide=r0['member_bioguide'],member=r0['member'],member_party=r0['member_party'],committee_link=r0['committee_link'],
    half_year=k[3],bundler_entity=k[1],bundler=k[2],bundler_employer=r0['bundler_employer'],bundler_city=r0['bundler_city'],bundler_state=r0['bundler_state'],
    bundled_usd=round(max(per,semi),2),sum_period_usd=round(per,2),max_semiannual_usd=round(semi,2),n_lines=len(rows),
    matched_person_ids='|'.join(ids),matched_lobbyists='|'.join(P[i]['name'] for i in ids),matched_firms='|'.join(dict.fromkeys(P[i]['main_registrant'] for i in ids)),matched_registrant=r0['matched_registrant'],match_confidence=r0['match_confidence'],ambiguous_reason=r0['ambiguous_reason'],
    scored=bool(r0['member_bioguide'] and ids and not r0['ambiguous_reason'] and not r0['match_confidence'].startswith('low')),
    fec_file_numbers='|'.join(sorted({str(r['file_number']) for r in rows})),pdf_urls='|'.join(sorted({r['pdf_url'] or '' for r in rows})),computed_at=NOW))
F=list(agg[0])
def wr(fn,rows): 
  w=csv.DictWriter(open(fn,'w'),fieldnames=F);w.writeheader();w.writerows(sorted(rows,key=lambda a:-a['bundled_usd']))
wr('../edges_bundling_all.csv',[a for a in agg if a['scope'].startswith('member')])
wr('bundling_matched_nonmember_committees_context.csv',[a for a in agg if a['matched_person_ids'] and not a['member_bioguide']])
wr('bundling_ambiguous_or_low.csv',[a for a in agg if a['matched_person_ids'] and (a['ambiguous_reason'] or a['match_confidence'].startswith('low'))])
ins=[a for a in agg if a['scope'].startswith('member')]
S=dict(computed_at=NOW,filings=len(R),sa3l_lines=len(lines),lines_most_recent_2023_26=len(O),agg_rows=len(agg),member_rows=len(ins),member_usd=round(sum(a['bundled_usd'] for a in ins),2),
  member_usd_by_party={p:round(sum(a['bundled_usd'] for a in ins if a['member_party']==p),2) for p in {a['member_party'] for a in ins}},
  member_committees_filing=len({a['committee_id'] for a in ins}),members_filing=len({a['member_bioguide'] for a in ins}),
  scored_rows=sum(1 for a in ins if a['scored']),scored_usd=round(sum(a['bundled_usd'] for a in ins if a['scored']),2),
  scored_usd_by_party={p:round(sum(a['bundled_usd'] for a in ins if a['scored'] and a['member_party']==p),2) for p in {a['member_party'] for a in ins}},
  scored_ind_usd=round(sum(a['bundled_usd'] for a in ins if a['scored'] and a['bundler_entity']=='IND'),2),scored_org_usd=round(sum(a['bundled_usd'] for a in ins if a['scored'] and a['bundler_entity']!='IND'),2),
  context_nonmember_matched_usd=round(sum(a['bundled_usd'] for a in agg if a['matched_person_ids'] and not a['member_bioguide'] and not a['ambiguous_reason'] and not a['match_confidence'].startswith('low')),2))
json.dump(S,open('bundling_summary_all.json','w'),indent=1); print(json.dumps(S,indent=1))
