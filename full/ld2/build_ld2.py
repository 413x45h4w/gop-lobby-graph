# Build LD-2 layer from raw/ld2full_*.jsonl.gz (2023Q1..2026Q3 original quarterly reports; amendments not crawled).
import gzip,json,glob,re,csv,collections,datetime,os,sys
NOW=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
OUTLIER=5_000_000
# --- person map (all-party universe) ---
pid_of={}; pname={}
for r in csv.DictReader(open('../money_all/people_all.csv')):
  for lid in r['person_key'].split('|'): pid_of[int(lid)]=r['person_id']
  pname[r['person_id']]=r['name']
scored={r['lda_lobbyist_id'] for r in csv.DictReader(open('../lobbyist_universe_scored.csv'))}
# --- bill regex ---
BILL=re.compile(r"(?<![A-Za-z0-9])(H\.?\s?R\.?|S\.?|H\.?\s?RES\.?|S\.?\s?RES\.?|H\.?\s?J\.?\s?RES\.?|S\.?\s?J\.?\s?RES\.?|H\.?\s?CON\.?\s?RES\.?|S\.?\s?CON\.?\s?RES\.?)\s?(?:NO\.?\s?)?(\d{1,5})(?![\d,]*\s?(?:%|PERCENT|MILLION|BILLION))\b",re.I)
CONG=re.compile(r"\b(11[5-9])(?:TH)?\s+CONGRESS",re.I)
def btype(s):
  s=re.sub(r'[^A-Z]','',s.upper()); return {'HR':'hr','S':'s','HRES':'hres','SRES':'sres','HJRES':'hjres','SJRES':'sjres','HCONRES':'hconres','SCONRES':'sconres'}.get(s)
def bills_in(text,year):
  out=set(); T=text or ''
  cm=CONG.findall(T); cg_default=118 if year<=2024 else 119
  for m in BILL.finditer(T):
    ty=btype(m.group(1)); n=int(m.group(2))
    if not ty or n==0: continue
    pre=T[max(0,m.start()-2):m.start()]
    if ty=='s' and re.search(r'U\.?$',T[max(0,m.start()-2):m.start()].upper()): continue   # 'U.S. 1'
    if ty=='s' and not re.match(r'S\.\s?\d|S\s\d|S\d',m.group(0).upper()): continue
    out.add((f'{ty}{n}-{cg_default}','explicit_congress' if cm else 'congress_inferred_from_filing_year'))
  return out
BILLS={}
for r in csv.DictReader(gzip.open('bills/bills.csv.gz','rt') if os.path.exists('bills/bills.csv.gz') else open('bills/bills.csv')): BILLS[r['bill_id']]=r['title']
SUF=re.compile(r'\b(INC|INCORPORATED|LLC|L L C|LLP|LP|CORP|CORPORATION|CO|COMPANY|THE|LTD|PLC|AND)\b')
def ckey(n):
  t=re.sub(r'\(.*?\)','',(n or '').upper()); t=re.sub(r'\b(ON BEHALF OF|OBO|FKA|F/K/A|DBA|D/B/A)\b.*$','',t)
  t=re.sub(r'[^A-Z0-9& ]',' ',t).replace('&',' AND '); k=' '.join(w for w in SUF.sub(' ',t).split())
  return k or ' '.join(t.split())
QS={'Q1':'03-31','Q2':'06-30','Q3':'09-30','Q4':'12-31'}
LC=collections.defaultdict(lambda:{'n':0,'usd':0.0,'q':set(),'iss':collections.Counter(),'reg':set(),'filings':[]})
CB=collections.defaultdict(lambda:{'n':0,'usd':0.0,'q':set(),'reg':set(),'iss':collections.Counter(),'conf':set(),'filings':[]})
LB=collections.defaultdict(lambda:{'n':0,'q':set(),'clients':set(),'filings':[]})
LA=collections.defaultdict(lambda:{'n':0,'q':set(),'clients':set()})
CA=collections.defaultdict(lambda:{'n':0,'usd':0.0,'q':set(),'reg':set()})
LN={}; CL={}; CK={}; CIDS=collections.defaultdict(set); FI=[]; seen=set(); outl=[]; stats=collections.Counter(); pulled=set()
for fn in sorted(glob.glob('raw/ld2full_*.jsonl.gz')):
  for line in gzip.open(fn,'rt'):
    try: d=json.loads(line)
    except: stats['bad_json']+=1; continue
    if d['uuid'] in seen: continue
    seen.add(d['uuid']); pulled.add(d['f'][:10])
    q=f"{d['y']}{d['t'][:2]}"; inc=float(d['inc'] or 0); exp=float(d['exp'] or 0); amt=inc or exp
    if inc>=OUTLIER: outl.append(d['uuid']); amt=exp if not inc else 0   # outlier rule applies to outside-firm income only (as in money_all/universe_all.py)
    ck=ckey(d['cn']); CIDS[ck].add(d['cid'])
    lobs={}; bills=set(); ents=set(); iss=set()
    for a in d['acts']:
      iss.add(a['i']); bs=bills_in(a['d'],d['y']); bills|=bs
      for e in a['e']: ents.add(e)
      for l in a['l']:
        lobs.setdefault(l[0],[l[1],l[2],set(),set(),set()]); lobs[l[0]][2].add(a['i']); lobs[l[0]][3]|={b for b,_ in bs}; lobs[l[0]][4]|=set(a['e'])
    FI.append([d['uuid'],d['y'],d['t'],d.get('posted') or '',d['rid'],d['rn'],d['cid'],ck,d['cn'],d['inc'] or '',d['exp'] or '',int(amt),len(d['acts']),len(lobs),'|'.join(sorted(iss)),len(bills),'|'.join(sorted(b for b,_ in bills))[:500],len(ents),len(d.get('fe') or []),d['f']])
    CL.setdefault(ck,(d['cn'],d.get('cdesc') or '',d.get('cst') or '',d.get('cco') or ''))
    nl=len(lobs) or 1
    for lid,(fi,la,li,lb,le) in lobs.items():
      LN[lid]=f"{(fi or '').strip()} {(la or '').strip()}".strip().upper()
      k=(lid,d['rid'],d['cid']); CK[d['cid']]=ck; x=LC[k]; x['n']+=1; x['usd']+=amt/nl; x['q'].add(q); x['iss'].update(li); x['reg'].add(d['rn'])
      if len(x['filings'])<3: x['filings'].append(d['uuid'])
      for b in lb:
        y=LB[(lid,b)]; y['n']+=1; y['q'].add(q); y['clients'].add(d['cn'])
        if len(y['filings'])<3: y['filings'].append(d['uuid'])
      for e in le:
        y=LA[(lid,e)]; y['n']+=1; y['q'].add(q); y['clients'].add(d['cn'])
    for b,conf in bills:
      y=CB[(ck,b)]; y['n']+=1; y['usd']+=amt; y['q'].add(q); y['reg'].add(d['rn']); y['conf'].add(conf)
      if len(y['filings'])<3: y['filings'].append(d['uuid'])
    for e in ents:
      y=CA[(ck,e)]; y['n']+=1; y['usd']+=amt; y['q'].add(q); y['reg'].add(d['rn'])
    stats['filings']+=1; stats['with_bills']+=bool(bills)
lname={}
for fn in sorted(glob.glob('raw/ld2full_*.jsonl.gz')): pass
def W(name,hdr,rows,gz=False):
  gz=gz or name.endswith('.gz')
  op=(lambda p:gzip.open(p,'wt',newline='')) if gz else (lambda p:open(p,'w',newline=''))
  with op(name) as f:
    w=csv.writer(f); w.writerow(hdr); n=0
    for r in rows: w.writerow(r); n+=1
  print(name,n,file=sys.stderr); return n
cnt={}
cnt['ld2_filings']=W('ld2_filings.csv.gz',['filing_uuid','year','period','posted','registrant_id','registrant','client_id','client_key','client','income','expenses','amount_usd_used','n_activities','n_lobbyists','issue_codes','n_bills','bill_ids','n_gov_entities','n_foreign_entities','pulled_at'],FI,gz=True)
qs=lambda s:(min(s),max(s))
names={}
for fn in sorted(glob.glob('raw/ld2full_*.jsonl.gz')):
  pass
cnt['edges_lobbyist_client']=W('edges_lobbyist_client.csv.gz',['person_id','lda_lobbyist_id','lobbyist','in_lobbyist_universe_scored','registrant_id','registrants','client_id','client_key','client','n_filings','attributed_usd','first_quarter','last_quarter','issue_codes','sample_filing_uuids','computed_at'],
  ([pid_of.get(l,''),l,LN.get(l,''),str(l) in scored,r,'|'.join(sorted(x['reg'])),c,CK[c],CL[CK[c]][0],x['n'],round(x['usd']),*qs(x['q']),'|'.join(k for k,_ in x['iss'].most_common()),'|'.join(x['filings']),NOW] for (l,r,c),x in LC.items()),gz=True)
cnt['edges_client_bill']=W('edges_client_bill.csv.gz',['client_key','client','lda_client_ids','bill_id','bill_in_billstatus','bill_title','n_filings','sum_filing_usd_mentioning_bill','n_registrants','registrants','first_quarter','last_quarter','bill_id_confidence','sample_filing_uuids','computed_at'],
  ([c,CL[c][0],'|'.join(map(str,sorted(CIDS[c])))[:200],b,b in BILLS,BILLS.get(b,'')[:120],x['n'],round(x['usd']),len(x['reg']),'|'.join(sorted(x['reg']))[:300],*qs(x['q']),'|'.join(sorted(x['conf'])),'|'.join(x['filings']),NOW] for (c,b),x in CB.items()))
cnt['edges_lobbyist_bill']=W('edges_lobbyist_bill.csv.gz',['person_id','lda_lobbyist_id','lobbyist','in_lobbyist_universe_scored','bill_id','bill_in_billstatus','n_filings','n_clients','clients','first_quarter','last_quarter','sample_filing_uuids','computed_at'],
  ([pid_of.get(l,''),l,LN.get(l,''),str(l) in scored,b,b in BILLS,x['n'],len(x['clients']),'|'.join(sorted(x['clients']))[:300],*qs(x['q']),'|'.join(x['filings']),NOW] for (l,b),x in LB.items()),gz=True)
cnt['edges_lobbyist_agency']=W('edges_lobbyist_agency.csv.gz',['person_id','lda_lobbyist_id','lobbyist','in_lobbyist_universe_scored','government_entity','n_filings','n_clients','first_quarter','last_quarter','computed_at'],
  ([pid_of.get(l,''),l,LN.get(l,''),str(l) in scored,e,x['n'],len(x['clients']),*qs(x['q']),NOW] for (l,e),x in LA.items()),gz=True)
cnt['edges_client_agency']=W('edges_client_agency.csv.gz',['client_key','client','government_entity','n_filings','sum_filing_usd','n_registrants','first_quarter','last_quarter','computed_at'],
  ([c,CL[c][0],e,x['n'],round(x['usd']),len(x['reg']),*qs(x['q']),NOW] for (c,e),x in CA.items()))
cnt['clients']=W('clients.csv',['client_key','client','general_description','state','country','lda_client_ids','computed_at'],([c,*v,'|'.join(map(str,sorted(CIDS[c]))),NOW] for c,v in CL.items()))
# ---- bills -> committees of jurisdiction -> current members; bills -> sponsors/cosponsors ----
import yaml
CM=yaml.safe_load(open('../../raw/committee-membership-current.yaml'))
LC_=json.load(open('../../raw/legislators-current.json')); CUR={l['id']['bioguide']:(l['name'].get('official_full') or l['name']['first']+' '+l['name']['last'],l['terms'][-1]['party'][0]) for l in LC_}
BC=collections.defaultdict(set); BCN={}
for r in csv.DictReader(gzip.open('bills/bill_committees.csv.gz','rt') if os.path.exists('bills/bill_committees.csv.gz') else open('bills/bill_committees.csv')):
  code=r['committee_code'].upper(); tid=code[:4] if code.endswith('00') else code[:4]+code[4:]
  BC[r['bill_id']].add(tid); BCN[tid]=r['committee_name']
BS=collections.defaultdict(list)
for r in csv.DictReader(gzip.open('bills/bill_sponsors.csv.gz','rt') if os.path.exists('bills/bill_sponsors.csv.gz') else open('bills/bill_sponsors.csv')): BS[r['bill_id']].append((r['bioguide'],r['role']))
lobbied={b for (_,b) in CB}
cnt['edges_bill_committee']=W('edges_bill_committee.csv',['bill_id','committee_id','committee_name','is_subcommittee','computed_at'],([b,t,BCN.get(t,''),len(t)>4,NOW] for b in sorted(lobbied) for t in sorted(BC.get(b,()))))
cnt['edges_bill_sponsor_member']=W('edges_bill_sponsor_member.csv.gz',['bill_id','bioguide','role','member_current','computed_at'],([b,bio,role,bio in CUR,NOW] for b in sorted(lobbied) for bio,role in BS.get(b,())))
# client -> committee (via bills) and client -> member reach (committee members of full committees of jurisdiction; sponsors/cosponsors)
CC=collections.defaultdict(lambda:{'bills':set(),'usd':0.0})
CMR=collections.defaultdict(lambda:{'via_committee':set(),'via_sponsor':set(),'via_cosponsor':set()})
for (c,b),x in CB.items():
  for t in BC.get(b,()):
    if len(t)!=4: continue
    y=CC[(c,t)]; y['bills'].add(b); y['usd']+=x['usd']
    for m in CM.get(t,[]):
      if m.get('bioguide'): CMR[(c,m['bioguide'])]['via_committee'].add(t)
  for bio,role in BS.get(b,()):
    if bio in CUR: CMR[(c,bio)]['via_'+role].add(b)
cnt['edges_client_committee']=W('edges_client_committee.csv.gz',['client_key','client','committee_id','committee_name','n_bills','bills','sum_filing_usd_mentioning_bills','computed_at'],
  ([c,CL[c][0],t,BCN.get(t,''),len(y['bills']),'|'.join(sorted(y['bills']))[:300],round(y['usd']),NOW] for (c,t),y in CC.items()))
cnt['edges_client_member_reach']=W('edges_client_member_reach.csv.gz',['client_key','client','bioguide','member','member_party','via_committees','n_sponsored_bills_lobbied','n_cosponsored_bills_lobbied','sponsored_bills','computed_at'],
  ([c,CL[c][0],bio,CUR[bio][0],CUR[bio][1],'|'.join(sorted(y['via_committee'])),len(y['via_sponsor']),len(y['via_cosponsor']),'|'.join(sorted(y['via_sponsor']))[:200],NOW] for (c,bio),y in CMR.items() if bio in CUR and (y['via_sponsor'] or y['via_cosponsor'])),gz=True)
reach=collections.Counter(c for (c,bio) in CMR if bio in CUR); spons=collections.Counter(c for (c,bio),y in CMR.items() if bio in CUR and (y['via_sponsor'] or y['via_cosponsor']))
sp1=collections.Counter(c for (c,bio),y in CMR.items() if bio in CUR and y['via_sponsor'])
nb=collections.Counter(c for (c,b) in CB); nc=collections.Counter(c for (c,t) in CC)
cusd=collections.Counter()
for f in FI: cusd[f[7]]+=f[11]
cnt['clients_summary']=W('clients_summary.csv',['client_key','client','lobbying_usd_2023_26','n_bills_lobbied','n_committees_via_bills','n_current_members_reached','n_current_members_sponsor_or_cosponsor','n_current_members_sponsor','computed_at'],
  sorted(([c,CL[c][0],cusd[c],nb[c],nc[c],reach[c],spons[c],sp1[c],NOW] for c in CL),key=lambda r:(-r[7],-r[2])))
json.dump(dict(stats=stats,counts=cnt,outlier_filings_excluded=outl,raw_pull_dates=sorted(pulled),computed_at=NOW),open('build_stats_ld2.json','w'),indent=1)
print(stats,file=sys.stderr)
