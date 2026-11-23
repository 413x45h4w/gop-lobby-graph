# Build nonprofit layer CSVs from raw/parsed_990.jsonl (last record per object_id wins).
import json,csv,sys,collections,datetime,glob
sys.path.insert(0,'scripts'); import personmatch as M
sys.path.insert(0,'/workspace/gop-lobby-graph/full/boards/scripts'); from orgnorm import key as okey
NOW=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
D={}
for l in open('raw/parsed_990.jsonl'):
  d=json.loads(l); D[d['object_id']]=d
TG={}
for fn in ('targets_990.csv','targets_990_pass2.csv'):
  for r in csv.DictReader(open(fn)): TG[r['ein']]=r
E={}
for fn in sorted(glob.glob('raw/eo[1-4].csv')):
  for r in csv.DictReader(open(fn,encoding='latin-1')): E[r['EIN']]=(r['NAME'],r['SUBSECTION'],r['STATE'])
CL={r['client_key']:r for r in csv.DictReader(open('/workspace/gop-lobby-graph/full/boards/lda_clients_spend_2023_26.csv'))}
CM={}; CMID={}
for c in ('24','26'):
  for l in open(f'/workspace/gop-lobby-graph/full/money_all/raw/fec_bulk/cm{c}.txt',encoding='latin-1'):
    x=l.rstrip('\n').split('|'); k=okey(x[1]); CMID[x[0]]=x
    if k: CM.setdefault(k,(x[0],x[1],x[9],x[10]))
def num(x):
  try: return float(x)
  except: return 0.0
ok=[d for d in D.values() if 'error' not in d]
# orgs
O=[]
for d in ok:
  t=TG.get(d['ein'],{}); c=d.get('schedC',{}); f=d.get('flags',{})
  ck=okey(d['filer_name'] or t.get('bmf_name',''))
  O.append(dict(ein=d['ein'],name=d['filer_name'] or t.get('bmf_name',''),subsection=t.get('subsection',''),state=t.get('state',''),ntee=t.get('ntee',''),return_type=d['return_type'],tax_period_end=d['tax_period_end'],
    total_revenue=d.get('total_revenue',''),political_campaign_activity=f.get('PoliticalCampaignActyInd',''),lobbying_activity=f.get('LobbyingActivitiesInd',''),
    schedC_political_expenditures=c.get('PoliticalExpendituresAmt',''),schedC_527_exempt_function_expend=c.get('TotalExemptFunctionExpendAmt',''),schedC_internal_funds_to_527=c.get('InternalFundsContributedAmt',''),
    schedC_total_lobbying=c.get('TotalLobbyingExpendituresAmt','') or c.get('TotalLobbyingExpendGrp/FilingOrganizationsTotalAmt',''),schedC_nondeductible_lobby_political=c.get('NonDeductibleLbbyngPltclTotAmt',''),
    schedC_dues=c.get('DuesAssessmentsAmt',''),lda_client_key=ck if ck in CL else '',lda_spend_2023_26=CL[ck]['lda_spend_2023_26'] if ck in CL else '',
    n_people=len(d.get('people',[])),n_grants=len(d.get('grants',[])),n_related=len(d.get('related',[])),mission=(f.get('MissionDesc') or f.get('ActivitiesOrMissionDesc') or '')[:300],website=f.get('WebsiteAddressTxt',''),
    selection_source=t.get('selection_source',''),selection_detail=t.get('selection_detail','')[:300],object_id=d['object_id'],source_url=d['url'],computed_at=NOW))
O.sort(key=lambda o:-num(o['total_revenue']))
w=csv.DictWriter(open('orgs_990.csv','w'),fieldnames=list(O[0])); w.writeheader(); w.writerows(O)
# people
P=[]; amb=[]
for d in ok:
  ck=okey(d['filer_name'])
  for p in d.get('people',[]):
    name=p['person'] or p['business']
    if not name: continue
    lm=M.match_lobbyist(name,d['filer_name']) if p['person'] else None
    mm=M.match_member(name,p['title']+' '+d['filer_name']) if p['person'] else None
    row=dict(person_name=name,title=p['title'],is_director=p['director'],is_officer=p['officer'],is_key_employee=p['key_employee'],is_highest_comp=p['highest_comp'],is_former=p['former'],hours_per_week=p['hours'],
      comp_from_org=p['comp'],comp_from_related=p['comp_related'],ein=d['ein'],org=d['filer_name'],subsection=TG.get(d['ein'],{}).get('subsection',''),tax_period_end=d['tax_period_end'],
      lobbyist_person_id='',lobbyist='',lobbyist_firm='',lobbyist_confidence='',lobbyist_basis='',member_bioguide='',member_name='',member_party='',member_current='',member_confidence='',member_basis='',
      source_url=d['url'],computed_at=NOW)
    if lm:
      if lm['confidence']=='low_name_only': amb.append(dict(kind='lobbyist',candidates=lm['person_id'],basis=lm['basis'],**{k:row[k] for k in ('person_name','title','ein','org','source_url')}))
      else: row.update(lobbyist_person_id=lm['person_id'],lobbyist=lm['name'],lobbyist_firm=lm['firm'],lobbyist_confidence=lm['confidence'],lobbyist_basis=lm['basis'])
    if mm:
      if mm['confidence']=='low_name_only': amb.append(dict(kind='member',candidates=mm['bioguide'],basis=mm['basis'],**{k:row[k] for k in ('person_name','title','ein','org','source_url')}))
      else: row.update(member_bioguide=mm['bioguide'],member_name=mm['name'],member_party=mm['party'],member_current=mm['current'],member_confidence=mm['confidence'],member_basis=mm['basis'])
    P.append(row)
w=csv.DictWriter(open('edges_person_org_officer.csv','w'),fieldnames=list(P[0])); w.writeheader(); w.writerows(P)
w=csv.DictWriter(open('person_match_ambiguous.csv','w'),fieldnames=list(amb[0])); w.writeheader(); w.writerows(amb)
# grants
G=[]
for d in ok:
  rev=num(d.get('total_revenue'))
  for g in d.get('grants',[]):
    e=(g['ein'] or '').strip(); e9=e.zfill(9) if e else ''
    gk=okey(g['name']); b=E.get(e9)
    G.append(dict(grantor_ein=d['ein'],grantor=d['filer_name'],grantor_subsection=TG.get(d['ein'],{}).get('subsection',''),grantee_name=g['name'],grantee_ein=e9,grantee_state=g['state'],
      grantee_irc_as_reported=g['irc'],grantee_bmf_subsection=('501(c)('+str(int(b[1]))+')') if b and b[1].isdigit() else '',grantee_in_990_set='Y' if e9 in TG else '',
      grantee_lda_client_key=gk if gk in CL else '',cash=g['cash'],noncash=g['noncash'],usd=num(g['cash'])+num(g['noncash']),purpose=g['purpose'][:300],source=g['src'],
      quality_flag=('grant_exceeds_grantor_total_revenue_check_filing' if rev>0 and num(g['cash'])+num(g['noncash'])>rev else 'ok'),tax_period_end=d['tax_period_end'],source_url=d['url'],computed_at=NOW))
G.sort(key=lambda x:-x['usd'])
w=csv.DictWriter(open('edges_org_to_org_grants.csv','w'),fieldnames=list(G[0])); w.writeheader(); w.writerows(G)
# related orgs (Schedule R)
R=[]
for d in ok:
  for r in d.get('related',[]):
    if not r['name']: continue
    R.append(dict(org_ein=d['ein'],org=d['filer_name'],related_name=r['name'],related_ein=r['ein'],schedule_r_group=r['grp'],exempt_code=r['exempt'],controlled=r['controlled'],activity=r['activity'],
      txn_type=r['txn_type'],txn_amount=r['amount'],direct_controlling_entity=r['direct_controlling'],related_in_990_set='Y' if r['ein'] and r['ein'].zfill(9) in TG else '',tax_period_end=d['tax_period_end'],source_url=d['url'],computed_at=NOW))
w=csv.DictWriter(open('edges_org_related_schedR.csv','w'),fieldnames=list(R[0])); w.writeheader(); w.writerows(R)
# org -> 527 / committee (Schedule C Part I-C line 5)
C=[]
for d in ok:
  for o in d.get('schedC_orgs',[]):
    nm=o.get('OrganizationBusinessName/BusinessNameLine1Txt','') or next((v for k,v in o.items() if k.endswith('BusinessNameLine1Txt')),'')
    import re; nk=okey(re.sub(r'\(.*?\)','',nm)); c=CM.get(nk)
    C.append(dict(org_ein=d['ein'],org=d['filer_name'],org_subsection=TG.get(d['ein'],{}).get('subsection',''),recipient_527=nm,recipient_ein=o.get('EIN',''),paid_internal_funds=o.get('PaidInternalFundsAmt',''),
      contributions_received_delivered=o.get('ContributionsRcvdDlvrAmt',''),fec_committee_id=c[0] if c else '',fec_committee_name=c[1] if c else '',fec_committee_type=c[2] if c else '',
      fec_match='exact normalized name' if c else '',tax_period_end=d['tax_period_end'],source_url=d['url'],computed_at=NOW))
w=csv.DictWriter(open('edges_org_to_527_or_committee_schedC.csv','w'),fieldnames=list(C[0])); w.writeheader(); w.writerows(C)
# nonprofit -> FEC super PAC (from FEC itemized receipts; top-5000 donor/committee pairs >= $1k rows)
EIN_BY_KEY={okey(o['name']):o['ein'] for o in O}
for e,t in TG.items(): EIN_BY_KEY.setdefault(okey(t['bmf_name']),e)
S=[]
for r in csv.DictReader(open('/workspace/gop-lobby-graph/full/outside_money/superpac_top_donors.csv')):
  e=EIN_BY_KEY.get(okey(r['fec_contributor_name']))
  if e: S.append(dict(org_ein=e,org=TG.get(e,{}).get('bmf_name',r['fec_contributor_name']),org_subsection=TG.get(e,{}).get('subsection',''),fec_contributor_name=r['fec_contributor_name'],fec_committee_id=r['fec_committee_id'],
    committee_name=r['committee_name'],cycle=r['cycle'],usd=r['usd'],n_rows=r['n_rows'],match='exact normalized name (FEC contributor name = IRS name)',source='outside_money/superpac_top_donors.csv',computed_at=NOW))
w=csv.DictWriter(open('edges_nonprofit_to_superpac_fec.csv','w'),fieldnames=list(S[0]) if S else ['org_ein']); w.writeheader(); w.writerows(S)
st=dict(computed_at=NOW,filings_parsed=len(ok),filing_errors=len(D)-len(ok),orgs=len(O),people_rows=len(P),people_lobbyist_matched=sum(1 for p in P if p['lobbyist_person_id']),
  people_lobbyist_by_conf=collections.Counter(p['lobbyist_confidence'] for p in P if p['lobbyist_confidence']),people_member_matched=sum(1 for p in P if p['member_bioguide']),
  people_member_by_conf=collections.Counter(p['member_confidence'] for p in P if p['member_confidence']),ambiguous=len(amb),grant_rows=len(G),grant_usd=round(sum(g['usd'] for g in G)),grant_usd_ok=round(sum(g['usd'] for g in G if g['quality_flag']=='ok')),grants_flagged=sum(1 for g in G if g['quality_flag']!='ok'),
  grants_to_990_set=sum(1 for g in G if g['grantee_in_990_set']),related_rows=len(R),schedC_527_rows=len(C),schedC_527_fec_matched=sum(1 for c in C if c['fec_committee_id']),nonprofit_to_superpac_rows=len(S))
json.dump(st,open('nonprofits_stats.json','w'),indent=1,default=dict); print(st)
