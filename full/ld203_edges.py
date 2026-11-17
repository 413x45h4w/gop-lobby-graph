# LD-203 contribution items by selected lobbyists -> current GOP members. one row per item, traceable to filing uuid.
import json,glob,csv,datetime,sys
sys.path.insert(0,'.'); from gopnames import match
sel={i:r for r in csv.DictReader(open('selected_top300.csv')) for i in r['person_key'].split('|')}
now=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
import re
PARTY=re.compile(r'NATIONAL REPUBLICAN|NRSC|NRCC|REPUBLICAN NATIONAL|RNC\b|REPUBLICAN PARTY|GOP\b|SENATE LEADERSHIP FUND|CONGRESSIONAL LEADERSHIP FUND|PROTECT THE HOUSE|MAJORITY COMMITTEE|SENATE REPUBLICAN',re.I)
def pkind(p):
  if PARTY.search(p or ''): return 'party_or_party_jfc'
  if re.search(r'VICTORY|JOINT|TEAM ',p or '',re.I): return 'jfc_or_victory'
  if re.search(r'PAC\b|LEADERSHIP|FUND\b|MAJORITY|POLITICAL ACTION',p or '',re.I) and not re.search(r'FOR (CONGRESS|SENATE)',p or '',re.I): return 'leadership_pac_or_other_pac'
  return 'candidate_committee'
rows=[];seen=set()
for fn in sorted(glob.glob('../lda/ld203_universe/ld203_*.jsonl.gz')):
  for line in __import__('gzip').open(fn,'rt'):
    d=json.loads(line)
    if str(d.get('lid')) not in sel: continue
    for i,(tp,contrib,payee,hon,amt,dt) in enumerate(d['items']):
      k=(d['uuid'],i)
      if k in seen: continue
      seen.add(k)
      m=match(hon,payee)
      if not m or m[1]!='Republican': continue
      rows.append(dict(person_id=sel[str(d['lid'])]['lda_lobbyist_id'],lda_lobbyist_id=d['lid'],lobbyist=sel[str(d['lid'])]['name'],bioguide=m[0],match_method=m[2],contribution_type=tp,
        contributor=contrib,contributor_kind='self' if (contrib or '').strip().upper() in ('SELF','','SELF.') else 'pac_or_other',payee_kind=pkind(payee),payee=payee,honoree=hon,amount=amt,date=dt,period=f"{d['y']}_{d['p']}",filing_uuid=d['uuid'],
        filing_url=f"https://lda.gov/filings/public/contribution/{d['uuid']}/print/",computed_at=now))
dk=set();dd=[]
for r in rows:
  k=(r['person_id'],r['payee'].upper().strip(),r['amount'],r['date'])
  if k in dk: continue
  dk.add(k); dd.append(r)
print('dropped amended/duplicate items',len(rows)-len(dd)); rows=dd
w=csv.DictWriter(open('edges_money_ld203.csv','w'),fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print(len(rows),'ld203 GOP-member items',len({r['person_id'] for r in rows}),'lobbyists')
