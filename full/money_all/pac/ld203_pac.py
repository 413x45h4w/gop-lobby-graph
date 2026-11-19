# PAC layer step 4: LD-203 items that are NOT to a current member.
#  (a) lobbyist-filed items with contributor SELF -> lobbyist -> committee edges (payee resolved to an FEC committee when the name is unique)
#  (b) registrant-filed (organization) LD-203 items -> registrant -> member edges (honoree/payee matched with names_all) and registrant -> committee edges,
#      credited to the registrant's universe lobbyists split equally (same as Form 3L org bundling).
import json,glob,csv,datetime,sys,re,gzip,collections
sys.path.insert(0,'..'); sys.path.insert(0,'../..')
from names_all import match
from safeio import keep_prev
NOW=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
P={r['person_id']:r for r in csv.DictReader(open('../people_all.csv'))}
lid2p={i:pid for pid,r in P.items() for i in r['person_key'].split('|')}
CM={}
for yy in ('24','26'):
  for line in open(f'../raw/fec_bulk/cm{yy}.txt',encoding='latin-1'):
    q=line.rstrip('\n').split('|'); CM[q[0]]=(q[1],q[9])
def nn(s): return ' '.join(re.findall(r'[A-Z0-9&]+',(s or '').upper().replace(' AND ',' & ')))
NAMEIDX=collections.defaultdict(set)
for c,(n,t) in CM.items():
  NAMEIDX[nn(n)].add(c)
  for par in re.findall(r'\(([^)]+)\)',n):
    if len(nn(par))>=4: NAMEIDX[nn(par)].add(c)
ALIAS=[(r'^(NRSC|NATIONAL REPUBLICAN SENATORIAL COMMITTEE)\b','C00027466'),(r'^(NRCC|NATIONAL REPUBLICAN CONGRESSIONAL COMMITTEE)\b','C00075820'),
 (r'^(RNC|REPUBLICAN NATIONAL COMMITTEE)\b','C00003418'),(r'^(DSCC|DEMOCRATIC SENATORIAL CAMPAIGN COMMITTEE)\b','C00042366'),
 (r'^(DCCC|DEMOCRATIC CONGRESSIONAL CAMPAIGN COMMITTEE)\b','C00000935'),(r'^(DNC|DEMOCRATIC NATIONAL COMMITTEE)\b','C00010603')]
CANDLIKE=re.compile(r'\bFOR (CONGRESS|SENATE|PRESIDENT|AMERICA|GOVERNOR)\b|\bFRIENDS OF\b|\bVICTORY\b|\bCAMPAIGN\b|\bELECT\b',re.I)
PR=re.compile(r"\b(NRCC|NRSC|RNC|REPUBLICAN|GOP)\b",re.I); PD=re.compile(r"\b(DCCC|DSCC|DNC|DEMOCRAT\w*)\b",re.I)
def resolve(payee):
  N=nn(payee)
  for rx,c in ALIAS:
    if re.search(rx,N): return c,'alias_national_party'
  ids=NAMEIDX.get(N,set())
  if len(ids)==1: return next(iter(ids)),'exact_fec_name'
  if len(ids)>1: return '',f'{len(ids)} FEC committees share this exact name'
  return '','no FEC committee with this exact name'
# registrant id -> people (LD-2 2023+)
rid2p=collections.defaultdict(set)
for fn in glob.glob('../../../lda/ld2_universe/*.jsonl.gz'):
  for line in gzip.open(fn,'rt'):
    d=json.loads(line)
    if d['y']<2023: continue
    for a in d['acts']:
      for x in a['lob']:
        if str(x[0]) in lid2p: rid2p[d['rid']].add(lid2p[str(x[0])])
LOBC=[];REGM=[];REGC=[];UNRES=[];st=collections.Counter();seen=set()
for fn in sorted(glob.glob('../../../lda/ld203_universe/ld203_*.jsonl.gz')):
  for line in gzip.open(fn,'rt'):
    d=json.loads(line)
    for i,(tp,contrib,payee,hon,amt,dt) in enumerate(d['items']):
      if tp!='feca': st['non_feca_item']+=1; continue
      try: a=float(amt or 0)
      except: a=0.0
      base=dict(payee=payee,honoree=hon,contributor=contrib,amount=a,date=dt,period=f"{d['y']}_{d['p']}",filing_uuid=d['uuid'],filing_url=f"https://lda.gov/filings/public/contribution/{d['uuid']}/print/",computed_at=NOW)
      if d['ft']=='lobbyist':
        pid=lid2p.get(str(d.get('lid')))
        if not pid: continue
        if (contrib or '').strip().upper() not in ('SELF','','SELF.'): st['lobbyist_item_pac_sourced_skip']+=1; continue
        m,why=match(hon,payee)
        if m or why: continue  # member items are the direct layer (or rejected there)
        k=(pid,nn(payee),a,dt)
        if k in seen: continue
        seen.add(k)
        c,how=resolve(payee)
        if c and CM[c][1] in ('H','S','P'): st['lobbyist_item_to_candidate_committee']+=1; continue
        if not c and CANDLIKE.search(payee or ''): st['lobbyist_item_candidatelike_unresolved_skip']+=1; continue
        row=dict(person_id=pid,lobbyist=P[pid]['name'],fec_committee_id=c,committee_name=CM[c][0] if c else '',resolution=how,
          text_party=('R' if PR.search(payee or '') and not PD.search(payee or '') else ('D' if PD.search(payee or '') and not PR.search(payee or '') else '')),**base)
        (LOBC if c else UNRES).append(row)
      elif d['ft']=='organization':
        rid=d['rid']; ppl=sorted(rid2p.get(rid,()))
        k=(rid,nn(payee),a,dt)
        if k in seen: st['org_dup']+=1; continue
        seen.add(k)
        m,why=match(hon,payee)
        rb=dict(registrant_id=rid,registrant=d['rn'],n_universe_lobbyists=len(ppl),person_ids='|'.join(ppl),**base)
        if m: REGM.append(dict(bioguide=m[0],member_party=m[1],match_method=m[2],**rb)); continue
        if why: UNRES.append(dict(person_id='',lobbyist='',fec_committee_id='',committee_name='',resolution='registrant item: '+why,text_party='',**{k_:v for k_,v in rb.items() if k_ in base})); continue
        c,how=resolve(payee)
        if c and CM[c][1] in ('H','S','P'): st['org_item_to_candidate_committee']+=1; continue
        REGC.append(dict(fec_committee_id=c,committee_name=CM[c][0] if c else '',resolution=how,**rb))
def wr(fn,rows):
  if not rows: return
  w=csv.DictWriter(open(keep_prev(fn),'w'),fieldnames=list(rows[0]),extrasaction='ignore');w.writeheader();w.writerows(rows)
wr('lobbyist_to_pac_ld203_resolved.csv',LOBC); wr('lobbyist_to_pac_ld203_unresolved.csv',UNRES)
wr('../edges_registrant_ld203_to_member.csv',REGM); wr('registrant_ld203_to_committee.csv',REGC)
print(dict(st),'lobbyist->committee resolved',len(LOBC),'unresolved',len(UNRES),'registrant->member',len(REGM),'registrant->committee',len(REGC))
print('registrant->member $',round(sum(r['amount'] for r in REGM)),collections.Counter(r['member_party'] for r in REGM),'with universe lobbyists',sum(1 for r in REGM if r['n_universe_lobbyists']))
