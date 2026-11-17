import csv,collections,datetime
NOW=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
S=list(csv.DictReader(open('selected_top300.csv')))
P=list(csv.DictReader(open('edges_money_pairs.csv')))
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
    top_recipients='|'.join(f"{m} ${u}" for u,m in sorted(a['top'],reverse=True)[:5]),gop_signals=r['gop_signals'],covered_positions=r['covered_positions'][:200]))
pi=pct([x['attrib_income_2023_26'] for x in rows]); pu=pct([x['usd_to_gop_members'] for x in rows]); pm=pct([x['n_members_funded'] for x in rows]); pf=pct([x['n_former_employer'] for x in rows])
for x in rows:
  x['money_score']=round(100*(0.35*pi(x['attrib_income_2023_26'])+0.35*pu(x['usd_to_gop_members'])+0.20*pm(x['n_members_funded'])+0.10*pf(x['n_former_employer'])),2)
  x['computed_at']=NOW
rows.sort(key=lambda x:-x['money_score'])
for i,x in enumerate(rows,1): x['money_rank']=i
w=csv.DictWriter(open('ranking_money.csv','w'),fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
for x in rows[:30]: print(x['money_rank'],x['lobbyist'],x['firm'][:25],x['attrib_income_2023_26'],x['usd_to_gop_members'],x['n_members_funded'],x['n_former_employer'],x['money_score'])
