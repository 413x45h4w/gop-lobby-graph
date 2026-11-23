from common import *
import time; t0=time.time()
R={}; key2pid={}
for r in rd('money_all/ranking_money_all_with_pac.csv'):
    R[r['person_id']]=r
    for k in r['person_key'].split('|'): key2pid[k]=r['person_id']
P=lambda p: key2pid.get(p,p)
LM=collections.defaultdict(lambda: collections.defaultdict(float))  # pid -> metric -> value
T=collections.defaultdict(lambda: collections.defaultdict(list))   # pid -> family -> [(target,label,value,conf)]
# LD-2 clients
for r in rd('ld2/edges_lobbyist_client.csv.gz'):
    p=P(r['person_id']); v=f(r['attributed_usd'])
    LM[p]['ld2_usd']+=v; LM[p]['n_clients']+=1
    T[p]['client'].append((okey(r['client']),r['client'],v,int(r['n_filings'])))
print('clients',time.time()-t0)
for r in rd('ld2/edges_lobbyist_bill.csv.gz'):
    p=P(r['person_id']);
    if r['bill_in_billstatus']!='True': continue
    LM[p]['n_bills']+=1; T[p]['bill'].append((r['bill_id'],int(r['n_filings'])))
print('bills',time.time()-t0)
for r in rd('ld2/edges_lobbyist_agency.csv.gz'):
    g=r['government_entity']
    if g in ('HOUSE OF REPRESENTATIVES','SENATE'): continue
    p=P(r['person_id']); LM[p]['n_agencies']+=1; T[p]['agency'].append((g,int(r['n_filings'])))
print('agency',time.time()-t0)
for r in rd('revolving/former_staffer_member_pairs.csv'):
    p=P(r['person_id']); c=r['best_confidence']
    if c not in('high','medium'): continue
    LM[p]['staff_'+c]+=1; T[p]['staff'].append((r['bioguide'],r['member'],r['member_current']=='True',c,r['sources']))
for r in rd('revolving/edges_former_staffer_committee.csv'):
    p=P(r['person_id']); LM[p]['staff_comm']+=1; T[p]['staffcomm'].append((r['committee_ids'],r['confidence']))
for r in rd('revolving/edges_lobbyist_former_agency.csv'):
    p=P(r['person_id']); LM[p]['former_agency']+=1; T[p]['formeragency'].append((r['agency'],))
FM={}
for r in rd('revolving/former_member_lobbyists.csv'):
    FM[P(r['person_id'])]=(r['confidence'],r['member'],r['member_party'],r['bioguide'])
for r in rd('executive/edges_lobbyist_to_agency_oira.csv'):
    for p0 in r['lobbyist_person_id'].split('|'):
        p=P(p0); c=r['confidence']; LM[p]['oira_'+c]+=1; T[p]['oira'].append((r['agency'],r['meeting_id'],c,r['date']))
for r in rd('executive/edges_lobbyist_to_wh_visitee.csv'):
    p=P(r['lobbyist_person_id']); LM[p]['wh_low']+=int(r['n_visits'] or 0)
for r in rd('outside_money/edges_lobbyist_to_superpac_agg.csv'):
    p=P(r['person_id']); c=r['best_confidence'].split('_')[0]; v=f(r['usd'])
    LM[p]['spac_'+c]+=v; T[p]['spac'].append((r['fec_committee_id'],r['committee_name'],v,c,r['committee_ie_lean']))
for r in rd('fara/edges_registrant_agent.csv'):
    c=r['lda_match_confidence']
    if c not in ('high','medium') or not r['lda_person_ids']: continue
    for p0 in r['lda_person_ids'].split('|'):
        p=P(p0); LM[p]['fara_'+c]+=1; T[p]['fara'].append((r['registration_number'],r['registrant'],c,r['active_2023_plus']=='True'))
for r in rd('legislative/edges_lobbyist_witness_to_committee.csv'):
    ids=r['lobbyist_person_ids'].split('|')
    if len(ids)!=1: continue
    p=P(ids[0]); c=r['confidence']; LM[p]['wit_'+c]+=1; T[p]['wit'].append((r['committee_code'],r['date'],c,r['hearing_id']))
for r in rd('nonprofits/edges_person_org_officer.csv'):
    if not r['lobbyist_person_id']: continue
    p=P(r['lobbyist_person_id']); c=r['lobbyist_confidence'].split('_')[0]; LM[p]['off990_'+c]+=1
    T[p]['off990'].append((r['ein'],r['org'],r['title'],c,r['subsection']))
for r in rd('boards/edges_person_company_board.csv'):
    if r['lobbyist_person_id']:
        p=P(r['lobbyist_person_id']); LM[p]['board']+=1; T[p]['board'].append((r['company'],r['lobbyist_confidence']))
for r in rd('nonprofits/irs527_officers_8871.csv'):
    if r['lobbyist_person_id']:
        p=P(r['lobbyist_person_id']); c=(r['lobbyist_confidence'] or '').split('_')[0]; LM[p]['off527_'+c]+=1; T[p]['off527'].append((r['org_527_ein'],r['org_527'],r['title'],c))
for r in rd('nonprofits/irs527_contributions_2023_26.csv'):
    if r['contributor_kind']=='person_lobbyist' and r['lobbyist_person_id']:
        p=P(r['lobbyist_person_id']); c=(r['lobbyist_confidence'] or '').split('_')[0]; LM[p]['c527_'+c]+=f(r['amount'])
XR={r['person_id']:r for r in rd('x_all/ranking_x_all_party.csv')}
xe=collections.defaultdict(float)
for x in rd('x_all/x_edges_all_party.csv'):
    w=f(x['weight_raw'])
    if w>0: xe[(P(x['person_id']),x['member_bioguide'])]+=w
for (p,b),w in xe.items(): LM[p]['x_w']+=w; LM[p]['x_n']+=1
print('missing pids',sum(1 for p in LM if p not in R), 'of', len(LM))
save('s1_lob',{'LM':{k:dict(v) for k,v in LM.items()},'T':{k:{a:b for a,b in v.items()} for k,v in T.items()},'FM':FM,'xe':dict(xe)})
print('done',time.time()-t0)
