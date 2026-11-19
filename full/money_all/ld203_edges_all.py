# LD-203 contribution items by EVERY lobbyist in people_all.csv -> any current member (all parties). One row per item, traceable to filing uuid.
import json,glob,csv,datetime,sys,re,gzip,collections
sys.path.insert(0,".")
sys.path.insert(0,'..'); from names_all import match
NOW=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
sel={}
for r in csv.DictReader(open('people_all.csv')):
  for i in r['person_key'].split('|'): sel[i]=r
PARTY=re.compile(r'NATIONAL REPUBLICAN|NRSC|NRCC|REPUBLICAN NATIONAL|RNC\b|REPUBLICAN PARTY|GOP\b|SENATE LEADERSHIP FUND|CONGRESSIONAL LEADERSHIP FUND|PROTECT THE HOUSE|MAJORITY COMMITTEE|SENATE REPUBLICAN'
  r'|DCCC|DSCC|\bDNC\b|DEMOCRATIC CONGRESSIONAL|DEMOCRATIC SENATORIAL|DEMOCRATIC NATIONAL|DEMOCRATIC PARTY|DEMOCRATIC STATE|HOUSE MAJORITY PAC|SENATE MAJORITY PAC|HOUSE DEMOCRAT|SENATE DEMOCRAT',re.I)
def pkind(p):
  if PARTY.search(p or ''): return 'party_or_party_jfc'
  if re.search(r'VICTORY|JOINT|TEAM ',p or '',re.I): return 'jfc_or_victory'
  if re.search(r'PAC\b|LEADERSHIP|FUND\b|MAJORITY|POLITICAL ACTION',p or '',re.I) and not re.search(r'FOR (CONGRESS|SENATE)',p or '',re.I): return 'leadership_pac_or_other_pac'
  return 'candidate_committee'
rows=[];REJ=[];seen=set();nomatch=collections.Counter();nitems=0
for fn in sorted(glob.glob('../../lda/ld203_universe/ld203_*.jsonl.gz')):
  for line in gzip.open(fn,'rt'):
    d=json.loads(line)
    if d['ft']!='lobbyist' or str(d.get('lid')) not in sel: continue
    p=sel[str(d['lid'])]
    for i,(tp,contrib,payee,hon,amt,dt) in enumerate(d['items']):
      k=(d['uuid'],i)
      if k in seen: continue
      seen.add(k); nitems+=1
      m,why=match(hon,payee)
      if why: REJ.append(dict(person_id=p['person_id'],lda_lobbyist_id=d['lid'],lobbyist=p['name'],payee=payee,honoree=hon,amount=amt,date=dt,filing_uuid=d['uuid'],reason=why,computed_at=NOW))
      if not m: continue
      rows.append(dict(person_id=p['person_id'],lda_lobbyist_id=d['lid'],lobbyist=p['name'],bioguide=m[0],member_party=m[1],match_method=m[2],contribution_type=tp,
        contributor=contrib,contributor_kind='self' if (contrib or '').strip().upper() in ('SELF','','SELF.') else 'pac_or_other',payee_kind=pkind(payee),payee=payee,honoree=hon,amount=amt,date=dt,period=f"{d['y']}_{d['p']}",filing_uuid=d['uuid'],
        filing_url=f"https://lda.gov/filings/public/contribution/{d['uuid']}/print/",computed_at=NOW))
dk=set();dd=[]
for r in rows:
  k=(r['person_id'],(r['payee'] or '').upper().strip(),r['amount'],r['date'])
  if k in dk: continue
  dk.add(k); dd.append(r)
print('LD-203 items scanned',nitems,'member-matched',len(rows),'dropped amended/duplicate',len(rows)-len(dd)); rows=dd
w=csv.DictWriter(open('ld203_rejected_name_matches.csv','w'),fieldnames=list(REJ[0]));w.writeheader();w.writerows(REJ)
print('rejected conflicting-given-name matches',len(REJ))
w=csv.DictWriter(open('edges_ld203_all.csv','w'),fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print(len(rows),'items',len({r['person_id'] for r in rows}),'lobbyists',len({r['bioguide'] for r in rows}),'members',collections.Counter(r['member_party'] for r in rows),collections.Counter(r['match_method'] for r in rows))
