# Derived summaries for the map: super PAC party lean from IE support/oppose, lobbyist->super PAC aggregates, and client->super PAC aggregates.
import csv,collections,json,datetime
NOW=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
lean=collections.defaultdict(lambda: collections.Counter())
for r in csv.DictReader(open('ie_expenditures_dedup.csv')):
  if r['quality_flag'].startswith('excluded'): continue
  p=r['cand_party'].upper(); a=float(r['amount'] or 0)
  side='R' if 'REPUBLICAN' in p else ('D' if 'DEMOCRAT' in p else None)
  if not side: continue
  if r['support_oppose']=='O': side={'R':'D','D':'R'}[side]
  lean[r['spender_id']][side]+=a
def L(c):
  x=lean.get(c)
  if not x or sum(x.values())==0: return '',''
  s=x['R']/(x['R']+x['D']); return ('R' if s>=0.8 else 'D' if s<=0.2 else 'mixed'),round(s,3)
rec=collections.defaultdict(float)
for r in csv.DictReader(open('superpac_committees_receipts.csv')): rec[r['fec_committee_id']]+=float(r['itemized_receipts_usd_nonmemo'])
A=collections.defaultdict(lambda: dict(usd=0.0,n=0,first='9999',last='',conf=collections.Counter()))
for r in csv.DictReader(open('edges_lobbyist_to_superpac.csv')):
  a=A[(r['person_id'],r['fec_committee_id'],r['cycle'])]; a.update(lobbyist=r['lobbyist'],firm=r['lobbyist_firm'],cname=r['committee_name'],ctype=r['committee_type'])
  a['usd']+=float(r['amount']); a['n']+=1; a['first']=min(a['first'],r['date']); a['last']=max(a['last'],r['date']); a['conf'][r['match_confidence']]+=1
TP={'O':'super_pac_ie_only','U':'single_candidate_ie','V':'hybrid_pac_nonqualified','W':'hybrid_pac_qualified','I':'ie_filer_not_committee'}
out=[]
for (p,c,cy),a in A.items():
  l,s=L(c)
  out.append(dict(person_id=p,lobbyist=a['lobbyist'],lobbyist_firm=a['firm'],fec_committee_id=c,committee_name=a['cname'],committee_type=TP.get(a['ctype'],a['ctype'] or 'ie_spender'),committee_ie_lean=l,committee_ie_R_share=s,
    cycle=cy,usd=round(a['usd'],2),n_contributions=a['n'],first_date=a['first'],last_date=a['last'],best_confidence=min(a['conf'],key=lambda k:{'high_employer_matches_registrant':0,'medium_lobbying_occupation':1,'low_dc_area_professional':2}[k]),
    share_of_committee_itemized=round(a['usd']/rec[c],6) if rec.get(c) else '',computed_at=NOW))
out.sort(key=lambda x:-x['usd'])
w=csv.DictWriter(open('edges_lobbyist_to_superpac_agg.csv','w'),fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
C=collections.defaultdict(lambda: dict(usd=0.0,n=0))
for r in csv.DictReader(open('edges_client_org_to_superpac_rows.csv')):
  c=C[(r['client_key'],r['client_name'],r['match_kind'],r['fec_committee_id'],r['committee_name'],r['committee_type'],r['cycle'])]; c['usd']+=float(r['amount']); c['n']+=1
co=[dict(client_key=k[0],client_name=k[1],match_kind=k[2],fec_committee_id=k[3],committee_name=k[4],committee_type=TP.get(k[5],k[5]),committee_ie_lean=L(k[3])[0],cycle=k[6],usd=round(v['usd'],2),n_rows=v['n'],computed_at=NOW) for k,v in C.items()]
co.sort(key=lambda x:-x['usd'])
w=csv.DictWriter(open('edges_client_org_to_superpac_agg.csv','w'),fieldnames=list(co[0])); w.writeheader(); w.writerows(co)
S=[]
ids=set(lean)|set(rec)
CMn={}
for r in csv.DictReader(open('superpac_committees_receipts.csv')): CMn[r['fec_committee_id']]=(r['committee_name'],r['committee_type'],r['connected_org'])
IEt=collections.defaultdict(float)
for r in csv.DictReader(open('edges_ie_spender_to_member.csv')): IEt[r['spender_id']]+=float(r['usd'])
for c in ids:
  l,s=L(c); n=CMn.get(c,('','',''))
  S.append(dict(fec_committee_id=c,committee_name=n[0],committee_type=TP.get(n[1],n[1]),connected_org=n[2],ie_lean=l,ie_R_share=s,ie_usd_all_candidates_D_R=round(sum(lean[c].values())) if c in lean else 0,
    ie_usd_current_members=round(IEt.get(c,0)),itemized_receipts_2023_26_nonmemo=round(rec.get(c,0)),computed_at=NOW))
S.sort(key=lambda x:-(x['ie_usd_all_candidates_D_R']+x['itemized_receipts_2023_26_nonmemo']))
w=csv.DictWriter(open('outside_spenders_summary.csv','w'),fieldnames=list(S[0])); w.writeheader(); w.writerows(S)
st=dict(computed_at=NOW,lobbyist_superpac_agg_edges=len(out),lobbyists=len({o['person_id'] for o in out}),usd=round(sum(o['usd'] for o in out)),
  usd_high=round(sum(o['usd'] for o in out if o['best_confidence'].startswith('high'))),client_org_agg_edges=len(co),client_org_usd=round(sum(c['usd'] for c in co)),spenders=len(S))
json.dump(st,open('summary_stats.json','w'),indent=1); print(st)
