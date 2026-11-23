# FEC independent expenditures (Schedule E + 24/48-hour reports, FEC bulk independent_expenditure_{2024,2026}.csv) -> spender->candidate support/oppose edges.
# Dedup: the bulk file contains originals, amendments and both 24/48-hour notices and the later Schedule E for the same expenditure.
# Rule: key=(spe_id, tran_id); keep the row from the highest file_num (latest filing). Rows with blank tran_id are kept as-is keyed by (spe_id,file_num,image_num).
import csv,json,sys,datetime,collections
sys.path.insert(0,'/workspace/gop-lobby-graph/full'); import gopnames as G
NOW=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
F2B={f:m for m in G.MEM for f in m['fec']}
B='/workspace/gop-lobby-graph/full/money_all/raw/fec_bulk'
CM={}
for c in ('24','26'):
  for l in open(f'{B}/cm{c}.txt',encoding='latin-1'):
    f=l.rstrip('\n').split('|'); CM[f[0]]=dict(name=f[1],tp=f[9],party=f[10],connected=f[13])
TPN={'O':'super_pac_ie_only','U':'single_candidate_ie','V':'hybrid_pac_nonqualified','W':'hybrid_pac_qualified','N':'pac_nonqualified','Q':'pac_qualified','X':'party_nonqualified','Y':'party_qualified','I':'ie_filer_not_committee','C':'communication_cost','E':'electioneering','H':'house_cand','S':'senate_cand','P':'pres_cand','D':'delegate'}
rows={}; raw=0
for y in ('2024','2026'):
  for r in csv.DictReader(open(f'raw/independent_expenditure_{y}.csv',encoding='latin-1')):
    raw+=1
    k=(r['spe_id'],r['tran_id']) if r['tran_id'] else (r['spe_id'],r['file_num'],r['image_num'],r['exp_amo'])
    fn=int(r['file_num'] or 0)
    if k not in rows or fn>=int(rows[k]['file_num'] or 0): r['_y']=y; rows[k]=r
def iso(d):
  try: return datetime.datetime.strptime(d,'%d-%b-%y').date().isoformat()
  except: return ''
out=[]
for r in rows.values():
  try: amt=float(r['exp_amo'] or 0)
  except: amt=0
  m=F2B.get(r['cand_id']); cm=CM.get(r['spe_id'],{})
  out.append(dict(spender_id=r['spe_id'],spender_name=r['spe_nam'].strip(),spender_type=TPN.get(cm.get('tp',''),cm.get('tp','') or 'not_in_committee_master'),
    spender_connected_org=cm.get('connected',''),cand_id=r['cand_id'],cand_name=r['cand_name'],bioguide=m['bio'] if m else '',member=m['name'] if m else '',member_party=m['party'] if m else '',
    office=r['can_office'],state=r['can_office_state'],district=r['can_office_dis'],cand_party=r['cand_pty_aff'],support_oppose=r['sup_opp'],amount=amt,
    exp_date=iso(r['exp_date']) or iso(r['dissem_dt']),dissem_date=iso(r['dissem_dt']),purpose=r['pur'],payee=r['pay'],election_type=r['ele_type'],
    fec_file_num=r['file_num'],amndt_ind=r['amndt_ind'],tran_id=r['tran_id'],image_num=r['image_num'],fec_url=f"https://docquery.fec.gov/cgi-bin/fecimg/?{r['image_num']}" if r['image_num'] else '',
    fec_election_yr=r['fec_election_yr'],bulk_file_year=r['_y'],
    quality_flag=('excluded_implausible_webform' if r['tran_id'].startswith('WFT') and amt>=1e6 else ('webform_filer' if r['tran_id'].startswith('WFT') else 'ok')),computed_at=NOW))
w=csv.DictWriter(open('ie_expenditures_dedup.csv','w'),fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
agg=collections.defaultdict(lambda: dict(amount=0.0,n=0,first='9999',last=''))
for o in out:
  if not o['bioguide'] or o['quality_flag'].startswith('excluded'): continue
  a=agg[(o['spender_id'],o['bioguide'],o['support_oppose'],o['fec_election_yr'])]
  a.update(spender_name=o['spender_name'],spender_type=o['spender_type'],spender_connected_org=o['spender_connected_org'],member=o['member'],member_party=o['member_party'])
  a['amount']+=o['amount']; a['n']+=1
  if o['exp_date']: a['first']=min(a['first'],o['exp_date']); a['last']=max(a['last'],o['exp_date'])
E=[dict(spender_id=k[0],spender_name=a['spender_name'],spender_type=a['spender_type'],spender_connected_org=a['spender_connected_org'],bioguide=k[1],member=a['member'],member_party=a['member_party'],
  support_oppose={'S':'support','O':'oppose'}.get(k[2],k[2] or 'unspecified'),cycle=k[3],usd=round(a['amount'],2),n_expenditures=a['n'],first_date=a['first'] if a['first']!='9999' else '',last_date=a['last'],
  source='FEC bulk independent_expenditure (Sched E + 24/48h), deduped',computed_at=NOW) for k,a in agg.items()]
E.sort(key=lambda e:-e['usd'])
w=csv.DictWriter(open('edges_ie_spender_to_member.csv','w'),fieldnames=list(E[0])); w.writeheader(); w.writerows(E)
st=dict(computed_at=NOW,raw_rows=raw,dedup_rows=len(out),rows_to_current_members=sum(1 for o in out if o['bioguide']),usd_all_ok=round(sum(o['amount'] for o in out if not o['quality_flag'].startswith('excluded'))),excluded_rows=sum(1 for o in out if o['quality_flag'].startswith('excluded')),excluded_usd=round(sum(o['amount'] for o in out if o['quality_flag'].startswith('excluded'))),
  usd_to_current_members=round(sum(o['amount'] for o in out if o['bioguide'] and not o['quality_flag'].startswith('excluded'))),by_cycle_member_usd={c:round(sum(o['amount'] for o in out if o['bioguide'] and o['fec_election_yr']==c and not o['quality_flag'].startswith('excluded'))) for c in ('2024','2026')},edges=len(E),members=len({e['bioguide'] for e in E}),spenders=len({e['spender_id'] for e in E}))
json.dump(st,open('ie_stats.json','w'),indent=1); print(st)
