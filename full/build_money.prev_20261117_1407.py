# Money layer: aggregate per (person, current GOP member) pair. Every number traceable to LD-203 filing uuids / FEC sub_ids.
import csv,collections,datetime,yaml,json,re
import partylex as P
NOW=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
S={r['lda_lobbyist_id']:r for r in csv.DictReader(open('selected_top300.csv'))}
M={r['bioguide']:r for r in csv.DictReader(open('../nodes_gop_members.csv'))}
L=[r for r in csv.DictReader(open('edges_money_ld203.csv')) if r['bioguide'] in M]
F=[r for r in csv.DictReader(open('edges_money_fec_raw.csv')) if r['bioguide'] in M]
d=lambda s:datetime.date.fromisoformat(s[:10])
# dedupe LD-203 FECA vs FEC: same person, member, amount, date +-3 days -> prefer FEC
fidx=collections.defaultdict(list)
for f in F:
  if f['memo_cd']!='X': fidx[(f['person_id'],f['bioguide'],round(float(f['amount'])))].append(f)
for l in L:
  l['dup_of_fec_sub_id']=''
  try: a=round(float(l['amount'])); dl=d(l['date'])
  except: continue
  for f in fidx.get((l['person_id'],l['bioguide'],a),[]):
    if abs((d(f['date'])-dl).days)<=3: l['dup_of_fec_sub_id']=f['fec_sub_id']; break
w=csv.DictWriter(open('edges_money_ld203.csv','w'),fieldnames=list(L[0]));w.writeheader();w.writerows(L)
# former employer ties
FE=[]
for pid,r in S.items():
  for p in P.people_in(r['covered_positions']):
    if p['bio'] in M:
      FE.append(dict(person_id=pid,lobbyist=r['name'],bioguide=p['bio'],member=M[p['bio']]['name'],ambiguous=p.get('ambiguous',False),
        covered_position_text=r['covered_positions'][:300],evidence_filing_ids=r['sample_filing_ids'][:200],computed_at=NOW))
w=csv.DictWriter(open('edges_money_former_employer.csv','w'),fieldnames=list(FE[0]));w.writeheader();w.writerows(FE)
# jurisdiction (rough issue-code -> committee thomas_id prefixes); zero weight in scores
ISS={'TAX':['HSWM','SSFI'],'HCR':['HSIF','HSWM','SSFI','SSHR'],'MMM':['HSWM','HSIF','SSFI'],'ENG':['HSIF','SSEG'],'FUE':['HSIF','SSEG'],'DEF':['HSAS','SSAS'],
 'BUD':['HSAP','SSAP','HSBU','SSBU'],'TRA':['HSPW','SSCM'],'AVI':['HSPW','SSCM'],'TEC':['HSIF','SSCM'],'TEL':['HSIF','SSCM'],'BAN':['HSBA','SSBK'],'FIN':['HSBA','SSBK'],
 'AGR':['HSAG','SSAF'],'ENV':['HSIF','SSEV'],'TRD':['HSWM','SSFI'],'IMM':['HSJU','SSJU'],'LAW':['HSJU','SSJU'],'HOM':['HSHM','SSGA'],'EDU':['HSED','SSHR'],
 'LBR':['HSED','SSHR'],'VET':['HSVR','SSVA'],'NAT':['HSII','SSEG'],'GOV':['HSGO','SSGA'],'CPT':['HSJU','SSJU'],'FOR':['HSFA','SSFR'],'INT':['HSIF','SSCM']}
CM=yaml.safe_load(open('../raw/committee-membership-current.yaml'))
mcom=collections.defaultdict(set)
for cid,mems in CM.items():
  if len(cid)==4:
    for m in mems: mcom[m['bioguide']].add(cid)
def juris(pid,bio):
  iss=S[pid]['top_issues'].split('|')
  return sorted({c for i in iss for c in ISS.get(i,[]) if c in mcom[bio]})
pairs=collections.defaultdict(lambda:dict(ld203_usd=0.0,ld203_n=0,ld203_pac_usd=0.0,fec_usd=0.0,fec_n=0,ld203_ids=[],fec_ids=[],fe=False,first='',last=''))
for l in L:
  if l['dup_of_fec_sub_id']: continue
  p=pairs[(l['person_id'],l['bioguide'])]; raw=float(l['amount'] or 0); a=min(raw,7000.0); p['raw']=p.get('raw',0)+raw
  w=1.0 if l['payee_kind']!='party_or_party_jfc' else 0.5
  if l['contributor_kind']=='self': p['ld203_usd']+=a*w
  else: p['ld203_pac_usd']+=a*w
  p['ld203_n']+=1; p['ld203_ids'].append(l['filing_uuid'])
for f in F:
  if f['memo_cd']=='X' or f['match_confidence'].startswith('low'): continue
  p=pairs[(f['person_id'],f['bioguide'])]; p['fec_usd']+=min(float(f['amount']),7000.0); p['raw']=p.get('raw',0)+float(f['amount']); p['fec_n']+=1; p['fec_ids'].append(f['fec_sub_id'])
for e in FE: pairs[(e['person_id'],e['bioguide'])]['fe']=True
rows=[]
for (pid,bio),p in pairs.items():
  rows.append(dict(person_id=pid,lobbyist=S[pid]['name'],firm=S[pid]['main_registrant'],bioguide=bio,member=M[bio]['name'],chamber=M[bio]['chamber'],
    ld203_self_usd=round(p['ld203_usd']),ld203_pac_usd=round(p['ld203_pac_usd']),ld203_items=p['ld203_n'],fec_indiv_usd=round(p['fec_usd']),fec_rows=p['fec_n'],
    raw_reported_usd=round(p.get('raw',0)),total_usd=round(p['ld203_usd']+p['fec_usd']+0.5*p['ld203_pac_usd']),former_employer_tie=p['fe'],jurisdiction_overlap='|'.join(juris(pid,bio)),
    ld203_filing_uuids='|'.join(dict.fromkeys(p['ld203_ids']))[:400],fec_sub_ids='|'.join(p['fec_ids'][:10]),computed_at=NOW))
rows.sort(key=lambda r:-r['total_usd'])
w=csv.DictWriter(open('edges_money_pairs.csv','w'),fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print('pairs',len(rows),'former-employer ties',len(FE),'ld203 dup of fec',sum(1 for l in L if l['dup_of_fec_sub_id']),'total $',sum(r['total_usd'] for r in rows))
