from common import *
import time; t0=time.time()
MEM={r['bioguide']:r for r in rd('money_all/member_totals_all_with_pac.csv')}
MM=collections.defaultdict(lambda: collections.defaultdict(float))
OM=collections.defaultdict(lambda: collections.defaultdict(float))  # org key -> metrics
ON={}  # org key -> display name
def oname(k,n):
    if k not in ON or len(n)<len(ON[k]): ON[k]=n
JUST=('J000312','BLACKSTONE')
E2=collections.defaultdict(list)  # edge candidates by family: list of tuples
# IE
for r in rd('outside_money/edges_ie_spender_to_member.csv'):
    v=f(r['usd']); b=r['bioguide']; so=r['support_oppose']
    MM[b]['ie_'+so]+=v
    E2['ie'].append((r['spender_id'],r['spender_name'],r['spender_type'],b,so,v,r['cycle']))
# revolving pairs (current members)
for r in rd('revolving/former_staffer_member_pairs.csv'):
    c=r['best_confidence']
    if c in('high','medium') and r['member_current']=='True': MM[r['bioguide']]['staff_'+c]+=1
# clients via sponsorship
spons=collections.defaultdict(set); cospons=collections.defaultdict(set)
for r in rd('ld2/edges_client_member_reach.csv.gz'):
    k=okey(r['client']); oname(k,r['client'])
    if int(r['n_sponsored_bills_lobbied'] or 0)>0:
        spons[r['bioguide']].add(k); E2['sponsreach'].append((k,r['bioguide'],int(r['n_sponsored_bills_lobbied']),int(r['n_cosponsored_bills_lobbied'] or 0)))
    elif int(r['n_cosponsored_bills_lobbied'] or 0)>0: cospons[r['bioguide']].add(k)
for b,s in spons.items(): MM[b]['clients_spons']=len(s)
for b,s in cospons.items(): MM[b]['clients_cospons']=len(s|spons.get(b,set()))
print('reach',time.time()-t0)
# FARA contacts
fr=collections.defaultdict(lambda: collections.defaultdict(set))
for r in rd('fara/edges_fara_contact_member.csv'):
    if r['member_current']!='True': continue
    c=r['confidence']; fr[r['bioguide']][c].add(r['registration_number'])
    E2['faracontact'].append((r['registration_number'],r['registrant'],r['bioguide'],c,r['foreign_principal_attributed'],r['principal_attribution'],r['date_stamped']))
for b,d in fr.items():
    for c,s in d.items(): MM[b]['fara_'+c]=len(s)
for r in rd('fara/edges_fara_contribution_member.csv'):
    if not r['bioguide'] or r['member_current']!='True': continue
    c=r['confidence']; MM[r['bioguide']]['faracontrib_'+c]+=f(r['amount_usd'])
    E2['faracontrib'].append((r['registration_number'],r['registrant'],r['bioguide'],c,f(r['amount_usd'])))
for r in rd('fara/edges_principal_registrant_member.csv'):
    if r['member_current']=='True': E2['fprm'].append((r['foreign_principal'],r['country'],r['registration_number'],r['registrant'],r['bioguide'],r['principal_attribution'],int(r['n_docs'])))
# travel
for r in rd('ethics/edges_travel_sponsor_to_member.csv'):
    b=r['bioguide']
    if not b: continue
    n=int(r['n_trips']); MM[b]['trips']+=n; MM[b]['trip_sponsors']+=1
    k=okey(r['lda_org_key'] or r['sponsor']); oname(k,r['sponsor'])
    if r['lda_org_key']: OM[k]['travel']+=n
    E2['travel'].append((k,r['sponsor'],b,n,int(r['n_member_trips']),int(r['n_staff_trips']),bool(r['lda_org_key'])))
# trades/holdings in lobbying companies
th=collections.defaultdict(set); excl=[]
for r in rd('ethics/edges_member_company_trades.csv'):
    if not r['lda_org_key']: continue
    k=okey(r['lda_org_name'] or r['lda_org_key']); oname(k,r['lda_org_name'])
    if (r['bioguide'],r['lda_org_key'])==JUST or (r['bioguide']=='J000312' and 'BLACKSTONE' in k): excl.append(('trade',r['asset_example'])); continue
    th[r['bioguide']].add(k); MM[r['bioguide']]['trade_tx']+=int(r['n_tx']); OM[k]['members_trade']+=1
    E2['trade'].append((r['bioguide'],k,int(r['n_tx']),f(r['sum_amount_min']),f(r['sum_amount_max']),r['asset_key']))
for r in rd('ethics/edges_member_company_holdings.csv'):
    k=okey(r['lda_org_name'] or r['lda_org_key']); oname(k,r['lda_org_name'])
    if r['bioguide']=='J000312' and 'BLACKSTONE' in k: excl.append(('holding',r['asset_example'],r['sum_value_min'],r['sum_value_max'])); continue
    th[r['bioguide']].add(k); MM[r['bioguide']]['hold_n']+=1; OM[k]['members_hold']+=1
    E2['hold'].append((r['bioguide'],k,f(r['sum_value_min']),f(r['sum_value_max'])))
for b,s in th.items(): MM[b]['th_orgs']=len(s)
print('excluded Justice/Blackstone',excl)
# legislative
for r in rd('legislative/member_committee_edges.csv'):
    MM[r['bioguide']]['n_comm' if r['level']=='committee' else 'n_subcomm']+=1
    E2['roster'].append((r['bioguide'],r['committee_code'],r['committee_name'],r['level'],r['side'],r['rank'],r['title']))
for r in rd('legislative/member_cosponsor_edges.csv'):
    E2['cospon'].append((r['sponsor_bioguide'],r['cosponsor_bioguide'],int(r['n_bills']),r['cross_party']=='1'))
    MM[r['sponsor_bioguide']]['cospon_recv']+=int(r['n_bills'])
for r in rd('state_events/member_caucus_edges.csv'):
    MM[r['bioguide']]['caucus']+=1; E2['caucus'].append((r['bioguide'],r['caucus'],r['confidence']))
for r in rd('state_events/edges_member_codel_cotravel.csv'):
    E2['codel'].append((r['bioguide_a'],r['bioguide_b'],int(r['n_shared_legs']),r['cross_party']=='1','high'))
    MM[r['bioguide_a']]['codel']+=1; MM[r['bioguide_b']]['codel']+=1
for r in rd('state_events/edges_senator_codel_cotravel.csv'):
    E2['codel'].append((r['bioguide_a'],r['bioguide_b'],int(r['n_shared_report_sections']),r['cross_party']=='1','medium'))
    MM[r['bioguide_a']]['codel']+=1; MM[r['bioguide_b']]['codel']+=1
# 990 officers who are (former) members
for r in rd('nonprofits/edges_person_org_officer.csv'):
    if r['member_bioguide']:
        E2['off990m'].append((r['member_bioguide'],r['member_name'],r['ein'],r['org'],r['title'],r['member_confidence'].split('_')[0],r['member_current']=='True',r['member_party']))
for r in rd('boards/edges_person_company_board.csv'):
    if r['member_bioguide']:
        k=okey(r['lda_client_names'].split(' | ')[0]) if r['lda_client_names'] else okey(r['company'])
        E2['boardm'].append((r['member_bioguide'],r['member_name'],k,r['company'],r['member_confidence'],r['member_party']))
# ===== orgs (clients) =====
for r in rd('ld2/clients_summary.csv'):
    k=okey(r['client']); oname(k,r['client'])
    o=OM[k]; o['ld2_usd']+=f(r['lobbying_usd_2023_26']); o['n_bills']=max(o['n_bills'],f(r['n_bills_lobbied'])); o['spons_members']=max(o['spons_members'],f(r['n_current_members_sponsor']))
for r in rd('ld2/clients.csv'):
    k=okey(r['client']); 
    if k in OM and r['general_description'] and 'desc' not in ON: pass
for r in rd('outside_money/edges_client_org_to_superpac_agg.csv'):
    k=okey(r['client_name']); oname(k,r['client_name']); v=f(r['usd']); OM[k]['spac']+=v
    E2['clientspac'].append((k,r['fec_committee_id'],r['committee_name'],v,r['committee_ie_lean'],r['cycle']))
for r in rd('outside_money/edges_client_employees_to_superpac.csv'):
    k=okey(r.get('client_name') or r.get('client_key')); OM[k]['spac_emp']+=f(r.get('usd'))
for r in rd('executive/edges_org_to_agency_oira.csv'):
    k=okey(r['lda_org_name']); oname(k,r['lda_org_name']); n=int(r['n_meetings']); OM[k]['oira']+=n
    E2['orgoira'].append((k,r['agency'],n,r['confidence']))
for r in rd('executive/edges_org_to_docket_comments.csv'):
    k=okey(r['lda_org_name']); OM[k]['dockets']+=1; OM[k]['comments']+=int(r['n_comments'])
    E2['docket'].append((k,r['agency'],r['docket'],int(r['n_comments']),r['confidence']))
for r in rd('legislative/edges_witness_org_to_committee.csv'):
    k=okey(r['lda_org_name']); oname(k,r['lda_org_name']); n=int(r['n_witness_appearances_dedup']); OM[k]['witness']+=n
    E2['orgwit'].append((k,r['committee_code'],n,int(r['n_hearing_days']),r['confidence']))
for r in rd('ld2/edges_client_committee.csv.gz'):
    k=okey(r['client']); E2['clientcomm'].append((k,r['committee_id'],int(r['n_bills']),f(r['sum_filing_usd_mentioning_bills'])))
for r in rd('ld2/edges_client_agency.csv.gz'):
    g=r['government_entity']
    if g in ('HOUSE OF REPRESENTATIVES','SENATE'): continue
    k=okey(r['client']); OM[k]['n_agencies']+=1; E2['clientagency'].append((k,g,int(r['n_filings']),f(r['sum_filing_usd'])))
print('client agency',time.time()-t0)
save('s2',{'MM':{k:dict(v) for k,v in MM.items()},'OM':{k:dict(v) for k,v in OM.items()},'ON':ON,'E2':dict(E2),'excl':excl})
print('done',time.time()-t0, {k:len(v) for k,v in E2.items()})
