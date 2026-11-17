# Match FEC individual contributions (to current GOP members' principal/authorized committees) to the selected 300 people.
import json,csv,re,sys,datetime,collections
from nicks import NICK
NOW=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
S=list(csv.DictReader(open('selected_top300.csv')))
STOPW={'THE','LLC','LLP','INC','GROUP','GOVERNMENT','RELATIONS','STRATEGIES','PARTNERS','AFFAIRS','PUBLIC','CONSULTING','ASSOCIATES','AND','COMPANY','LAW','CAPITOL','POLICY','ADVISORS','STRATEGY','STRATEGIC','SOLUTIONS','FIRM','OF'}
idx=collections.defaultdict(list)
for r in S:
  p=r['name'].split(); last=p[-1] if p[-1] not in ('JR','JR.','II','III','IV','SR') else p[-2]
  last=last.replace('.','')
  fs={p[0]}|set(NICK.get(p[0],[]))|{k for k,v in NICK.items() if p[0] in v}
  regw={w for reg in r['registrants'].split(';') for w in re.findall(r"[A-Z0-9']{3,}",reg.upper()) if w not in STOPW and w!=last}
  phr={' '.join(re.findall(r"[A-Z0-9']+",reg.upper())[:2]) for reg in r['registrants'].split(';')}
  regw=(regw,phr)
  for f in fs: idx[(last,f)].append((r,regw))
LOBW=re.compile(r'LOBBY|GOVERNMENT RELATIONS|GOV(ERNMENT|\'T)? AFFAIRS|PUBLIC (AFFAIRS|POLICY)|ADVOCA|LEGISLATIVE|POLICY',re.I)
PROW=re.compile(r'CONSULT|ATTORNEY|LAWYER|COUNSEL|PARTNER|PRINCIPAL|PRESIDENT|CEO|OWNER|EXECUTIVE|DIRECTOR|FOUNDER|MANAGING|VICE',re.I)
out=[];stat=collections.Counter()
for cyc in sys.argv[1:]:
  seen=set()
  for line in __import__('gzip').open(f'fec_indiv{cyc}_gopmember_poolname.jsonl.gz','rt'):
    d=json.loads(line)
    if d['sub_id'] in seen: continue
    seen.add(d['sub_id'])
    last,rest=d['name'].split(',',1); last=last.strip().replace('.','')
    toks=[t for t in re.split(r'[\s\.]+',rest) if t and t not in ('MR','MS','MRS','DR','HON')]
    if not toks: continue
    cands=idx.get((last,toks[0]),[])
    if not cands: continue
    stat['name_hit']+=1
    ew=set(re.findall(r"[A-Z0-9']{3,}",(d['emp']+' '+d['occ']).upper()))
    best=None
    for r,regw in cands:
      ws,phr=regw; empn=' '.join(re.findall(r"[A-Z0-9']+",(d['emp']).upper()))
      if (ws & ew) or any(p and p in empn for p in phr): conf='high_employer_matches_registrant'
      elif LOBW.search(d['emp']+' '+d['occ']): conf='medium_lobbying_occupation'
      elif PROW.search(d['occ']) and d['st'] in ('DC','VA','MD'): conf='low_dc_area_professional'
      else: conf=None
      if conf and (best is None or conf<best[1]): best=(r,conf)
    if not best: stat['rejected_employer_occ']+=1; continue
    r,conf=best
    if len([c for c in cands])>1 and not conf.startswith('high'): stat['ambiguous_dropped']+=1; continue
    stat[conf]+=1
    dt=d['dt']; iso=f"{dt[4:8]}-{dt[0:2]}-{dt[2:4]}" if len(dt)==8 else dt
    if iso<'2023-01-01': stat['pre2023']+=1; continue
    out.append(dict(person_id=r['lda_lobbyist_id'],lobbyist=r['name'],bioguide=d['bio'],fec_committee_id=d['cmte'],fec_contributor_name=d['name'],city=d['city'],state=d['st'],employer=d['emp'],occupation=d['occ'],
      date=iso,amount=d['amt'],transaction_tp=d['tp'],memo_cd=d['memo'],memo_text=d['memo_text'],fec_sub_id=d['sub_id'],fec_image_num=d['image'],
      fec_url=f"https://docquery.fec.gov/cgi-bin/fecimg/?{d['image']}",match_confidence=conf,cycle='20'+cyc,computed_at=NOW))
w=csv.DictWriter(open('edges_money_fec_raw.csv','w'),fieldnames=list(out[0]));w.writeheader();w.writerows(out)
print(stat,len(out),'rows',len({o['person_id'] for o in out}),'people')
