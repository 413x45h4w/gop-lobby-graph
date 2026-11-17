import csv,collections,datetime
NOW=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
S=list(csv.DictReader(open('selected_top300.csv')))
P=list(csv.DictReader(open('edges_money_pairs.csv')))
# Bundling layer (FEC Form 3L, in scope = GOP members' principal/authorized committees + leadership PACs, 2023-26)
B=collections.defaultdict(lambda:dict(usd=0.0,members=set()))
for b in csv.DictReader(open('edges_money_bundling.csv')):
  if b['scope']!='gop_member_pcc_or_lpac' or not b['matched_person_ids'] or b['match_confidence'].startswith('low'): continue
  for pid in b['matched_person_ids'].split('|'):
    B[pid]['usd']+=float(b['bundled_usd'])/len(b['matched_person_ids'].split('|')); B[pid]['members'].add(b['gop_member_bioguide'])
agg=collections.defaultdict(lambda:dict(usd=0,members=set(),fe=set(),ld203=0,fec=0,top=[]))
for p in P:
  a=agg[p['person_id']]; a['usd']+=int(p['total_usd']); a['ld203']+=int(p['ld203_self_usd']); a['fec']+=int(p['fec_indiv_usd'])
  if int(p['total_usd'])>0: a['members'].add(p['bioguide'])
  if p['former_employer_tie']=='True': a['fe'].add(p['member'])
  a['top'].append((int(p['total_usd']),p['member']))
def pct(vals):
  s=sorted(vals); n=len(s)
  return lambda v:(sum(1 for x in s if x<v)+0.5*sum(1 for x in s if x==v))/n
rows=[]
for r in S:
  a=agg[r['lda_lobbyist_id']]
  rows.append(dict(person_id=r['lda_lobbyist_id'],lobbyist=r['name'],firm=r['main_registrant'],income_rank=r['rank_income_eligible'],attrib_income_2023_26=int(r['attrib_income_2023_26']),
    usd_to_gop_members=a['usd'],ld203_self_usd=a['ld203'],fec_indiv_usd=a['fec'],n_members_funded=len(a['members']),former_employer_members='|'.join(sorted(a['fe'])),n_former_employer=len(a['fe']),
    top_recipients='|'.join(f"{m} ${u}" for u,m in sorted(a['top'],reverse=True)[:5]),bundled_usd_to_gop_members=round(B[r['lda_lobbyist_id']]['usd'],2),n_members_bundled_for=len(B[r['lda_lobbyist_id']]['members']),gop_signals=r['gop_signals'],covered_positions=r['covered_positions'][:200]))
pi=pct([x['attrib_income_2023_26'] for x in rows]); pu=pct([x['usd_to_gop_members'] for x in rows]); pm=pct([x['n_members_funded'] for x in rows]); pf=pct([x['n_former_employer'] for x in rows]); pb=pct([x['bundled_usd_to_gop_members'] for x in rows])
for x in rows:
  # v2 weights (2026-11-17): income 0.315, $ 0.315, members 0.18, former employer 0.09, Form 3L bundling 0.10. If nobody has bundling, the term is constant (0.5*0.10) and scores are rescaled by /0.9 back to the old 0-100 basis.
  base=0.315*pi(x['attrib_income_2023_26'])+0.315*pu(x['usd_to_gop_members'])+0.18*pm(x['n_members_funded'])+0.09*pf(x['n_former_employer'])
  anyb=any(y['bundled_usd_to_gop_members']>0 for y in rows)
  x['money_score']=round(100*((base+0.10*pb(x['bundled_usd_to_gop_members'])) if anyb else base/0.9),2)
  x['computed_at']=NOW
rows.sort(key=lambda x:-x['money_score'])
for i,x in enumerate(rows,1): x['money_rank']=i
w=csv.DictWriter(open('ranking_money.csv','w'),fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
for x in rows[:30]: print(x['money_rank'],x['lobbyist'],x['firm'][:25],x['attrib_income_2023_26'],x['usd_to_gop_members'],x['n_members_funded'],x['n_former_employer'],x['money_score'])
