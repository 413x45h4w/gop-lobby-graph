# ALL-PARTY money layer: pairs (person x current member), former-employer edges, bundling credit, ranking, per-member totals.
# Same scoring rules as full/build_money.py + full/rank_money.py (v2), applied to every lobbyist and every current member.
import csv,collections,datetime,yaml,json,re,sys
sys.path.insert(0,'..'); import partylex as PL
from safeio import keep_prev
NOW=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
P={r['person_id']:r for r in csv.DictReader(open('people_all.csv'))}
LC=json.load(open('../../raw/legislators-current.json'))
M={l['id']['bioguide']:dict(name=l['name'].get('official_full') or l['name']['first']+' '+l['name']['last'],party=l['terms'][-1]['party'],chamber='Senate' if l['terms'][-1]['type']=='sen' else 'House',state=l['terms'][-1]['state'],district=l['terms'][-1].get('district','')) for l in LC}
PA=lambda b:{'Republican':'R','Democrat':'D','Independent':'I'}.get(M[b]['party'],'?')
L=[r for r in csv.DictReader(open('edges_ld203_all.csv')) if r['bioguide'] in M]
F=[r for r in csv.DictReader(open('edges_fec_all.csv')) if r['bioguide'] in M]
CMT={}
for yy in ('24','26'):
  for line in open(f'raw/fec_bulk/cm{yy}.txt',encoding='latin-1'):
    f_=line.split('|'); CMT[f_[0]]=f_[9]
Fp=[r for r in F if CMT.get(r['fec_committee_id']) in ('X','Y','Z')]
F=[r for r in F if CMT.get(r['fec_committee_id']) not in ('X','Y','Z')]
stats=dict(computed_at=NOW,fec_rows_party_committee_excluded=len(Fp),fec_party_committee_raw_usd=round(sum(float(r['amount']) for r in Fp)),fec_party_committees_excluded=sorted({r['fec_committee_id'] for r in Fp}))
d=lambda s:datetime.date.fromisoformat(s[:10])
fidx=collections.defaultdict(list)
for f in F:
  if f['memo_cd']!='X': fidx[(f['person_id'],f['bioguide'],round(float(f['amount'])))].append(f)
for l in L:
  l['dup_of_fec_sub_id']=''
  try: a=round(float(l['amount'])); dl=d(l['date'])
  except: continue
  for f in fidx.get((l['person_id'],l['bioguide'],a),[]):
    if abs((d(f['date'])-dl).days)<=3: l['dup_of_fec_sub_id']=f['fec_sub_id']; break
w=csv.DictWriter(open(keep_prev('edges_ld203_all_dedup.csv'),'w'),fieldnames=list(L[0]));w.writeheader();w.writerows(L)
# former employer (covered position names a current member)
# Extra safeguards (all-party build), applied per covered-position segment (split on ';' and '||'):
#  - segment with an explicit negation of employment ('not employed by') -> rejected
#  - surname-only/ambiguous legislator matches (partylex ambiguous=True, e.g. two current Mike Rogers, 'Bob Matsui' vs Doris Matsui) -> kept out of scoring, listed in former_employer_rejected_all.csv
#  - segment naming >=3 legislators and containing no staff-role word (a contact list, not a job) -> rejected
NEG=re.compile(r"\bNOT (EMPLOYED|WORKED)|\bNEVER (EMPLOYED|WORKED)",re.I)  # note: '*No lobby activity or contact made to Senator X' is a cooling-off notice by a FORMER staffer, so it is kept
ROLE=re.compile(r"(19|20)\d\d|ASST|\bLEG\b|\bSA\b|\bCOS\b|POLICY|ASSIST|AIDE|DIRECTOR|\bDIR\b|COUNSEL|STAFF|CHIEF|ADVIS|\bL\.?A\.?\b|\bL\.?D\.?\b|\bL\.?C\.?\b|SCHEDUL|INTERN|FELLOW|SECRETARY|MANAGER|COORDINAT|CORRESPOND|SPECIALIST|DEPUTY|PRESS|COMMUNICATION|CLERK|ANALYST|AIDE|REPRESENTATIVE FOR|CASEWORK|OFFICER|LIAISON|CONSULTANT|WRITER|ASSOCIATE|EMPLOYEE|WORKED|INTERN|PAGE\b|ADVOCATE",re.I)
FE=[];FEREJ=[]
for pid,r in P.items():
  if not r['covered_positions']: continue
  for seg in re.split(r'\s*(?:;|\|\|)\s*',r['covered_positions']):
    if not seg.strip(): continue
    ppl=[p for p in PL.people_in(seg) if p['bio'] in M]
    if not ppl: continue
    why=''
    if NEG.search(seg): why='negation in covered-position text'
    elif len(PL.people_in(seg))>=3 and not ROLE.search(seg): why='list of >=3 legislators with no staff-role word (contact list, not employment)'
    for p in ppl:
      e=dict(person_id=pid,lobbyist=r['name'],firm=r['main_registrant'],bioguide=p['bio'],member=M[p['bio']]['name'],member_party=M[p['bio']]['party'],ambiguous=p.get('ambiguous',False),
        covered_position_text=seg[:300],evidence_filing_ids=r['sample_filing_ids'][:200],computed_at=NOW)
      if not why and e['ambiguous']: why='ambiguous legislator name (not scored)'
      (FEREJ.append(dict(e,reject_reason=why)) if why else FE.append(e))
w=csv.DictWriter(open(keep_prev('former_employer_rejected_all.csv'),'w'),fieldnames=list(FEREJ[0]));w.writeheader();w.writerows(FEREJ)
stats['former_employer_rejected']=dict(edges=len(FEREJ),by_reason=dict(collections.Counter(e['reject_reason'] for e in FEREJ)))
fe_seen=set(); FE=[e for e in FE if not ((e['person_id'],e['bioguide']) in fe_seen or fe_seen.add((e['person_id'],e['bioguide'])))]
w=csv.DictWriter(open(keep_prev('edges_former_employer_all.csv'),'w'),fieldnames=list(FE[0]));w.writeheader();w.writerows(FE)
# jurisdiction (weight 0)
ISS={'TAX':['HSWM','SSFI'],'HCR':['HSIF','HSWM','SSFI','SSHR'],'MMM':['HSWM','HSIF','SSFI'],'ENG':['HSIF','SSEG'],'FUE':['HSIF','SSEG'],'DEF':['HSAS','SSAS'],
 'BUD':['HSAP','SSAP','HSBU','SSBU'],'TRA':['HSPW','SSCM'],'AVI':['HSPW','SSCM'],'TEC':['HSIF','SSCM'],'TEL':['HSIF','SSCM'],'BAN':['HSBA','SSBK'],'FIN':['HSBA','SSBK'],
 'AGR':['HSAG','SSAF'],'ENV':['HSIF','SSEV'],'TRD':['HSWM','SSFI'],'IMM':['HSJU','SSJU'],'LAW':['HSJU','SSJU'],'HOM':['HSHM','SSGA'],'EDU':['HSED','SSHR'],
 'LBR':['HSED','SSHR'],'VET':['HSVR','SSVA'],'NAT':['HSII','SSEG'],'GOV':['HSGO','SSGA'],'CPT':['HSJU','SSJU'],'FOR':['HSFA','SSFR'],'INT':['HSIF','SSCM']}
CM=yaml.safe_load(open('../../raw/committee-membership-current.yaml'))
mcom=collections.defaultdict(set)
for cid,mems in CM.items():
  if len(cid)==4:
    for m in mems: mcom[m['bioguide']].add(cid)
def juris(pid,bio): return sorted({c for i in P[pid]['top_issues'].split('|') for c in ISS.get(i,[]) if c in mcom[bio]})
pairs=collections.defaultdict(lambda:dict(ld203_usd=0.0,ld203_n=0,ld203_pac_usd=0.0,fec_usd=0.0,fec_n=0,ld203_ids=[],fec_ids=[],fe=False,raw=0.0))
for l in L:
  if l['dup_of_fec_sub_id']: continue
  p=pairs[(l['person_id'],l['bioguide'])]
  try: raw=float(l['amount'] or 0)
  except: raw=0.0
  a=min(raw,7000.0); p['raw']+=raw
  wt=1.0 if l['payee_kind']!='party_or_party_jfc' else 0.5
  if l['contributor_kind']=='self': p['ld203_usd']+=a*wt
  else: p['ld203_pac_usd']+=a*wt
  p['ld203_n']+=1; p['ld203_ids'].append(l['filing_uuid'])
for f in F:
  if f['memo_cd']=='X' or f['match_confidence'].startswith('low'): continue
  p=pairs[(f['person_id'],f['bioguide'])]; p['fec_usd']+=min(float(f['amount']),7000.0); p['raw']+=float(f['amount']); p['fec_n']+=1; p['fec_ids'].append(f['fec_sub_id'])
for e in FE: pairs[(e['person_id'],e['bioguide'])]['fe']=True
rows=[]
for (pid,bio),p in pairs.items():
  rows.append(dict(person_id=pid,lobbyist=P[pid]['name'],firm=P[pid]['main_registrant'],lobbyist_kind=P[pid]['lobbyist_kind'],bioguide=bio,member=M[bio]['name'],member_party=PA(bio),chamber=M[bio]['chamber'],state=M[bio]['state'],
    ld203_self_usd=round(p['ld203_usd']),ld203_pac_usd=round(p['ld203_pac_usd']),ld203_items=p['ld203_n'],fec_indiv_usd=round(p['fec_usd']),fec_rows=p['fec_n'],
    raw_reported_usd=round(p['raw']),total_usd=round(p['ld203_usd']+p['fec_usd']+0.5*p['ld203_pac_usd']),former_employer_tie=p['fe'],jurisdiction_overlap='|'.join(juris(pid,bio)),
    ld203_filing_uuids='|'.join(dict.fromkeys(p['ld203_ids']))[:400],fec_sub_ids='|'.join(p['fec_ids'][:10]),computed_at=NOW))
rows.sort(key=lambda r:-r['total_usd'])
w=csv.DictWriter(open(keep_prev('edges_money_pairs_all.csv'),'w'),fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
# layer totals by recipient party (scored = capped/weighted credit; raw = as reported)
def tot(it,key): 
  c=collections.Counter()
  for x in it: c[x[0]]+=x[1]
  return {k:round(v) for k,v in c.items()}
Ls=[l for l in L if not l['dup_of_fec_sub_id']]
stats['ld203']=dict(items_all=len(L),items_after_fec_dedup=len(Ls),lobbyists=len({l['person_id'] for l in Ls}),members=len({l['bioguide'] for l in Ls}),
  raw_usd_by_party=tot(((PA(l['bioguide']),float(l['amount'] or 0)) for l in Ls),0),
  scored_usd_by_party=tot(((PA(l['bioguide']),min(float(l['amount'] or 0),7000)*(1 if l['payee_kind']!='party_or_party_jfc' else .5)*(1 if l['contributor_kind']=='self' else .5)) for l in Ls),0))
Fs=[f for f in F if f['memo_cd']!='X' and not f['match_confidence'].startswith('low')]
stats['fec']=dict(rows_all_conf=len(F),rows_scored=len(Fs),rows_high=sum(1 for f in Fs if f['match_confidence'].startswith('high')),rows_medium=sum(1 for f in Fs if f['match_confidence'].startswith('medium')),
  lobbyists=len({f['person_id'] for f in Fs}),members=len({f['bioguide'] for f in Fs}),
  raw_usd_by_party=tot(((PA(f['bioguide']),float(f['amount'])) for f in Fs),0),scored_usd_by_party=tot(((PA(f['bioguide']),min(float(f['amount']),7000)) for f in Fs),0),
  leadership_pac_rows=sum(1 for f in Fs if f['committee_link'].startswith('lead')))
stats['former_employer']=dict(edges=len(FE),lobbyists=len({e['person_id'] for e in FE}),members=len({e['bioguide'] for e in FE}),by_party=dict(collections.Counter(PA(e['bioguide']) for e in FE)),ambiguous_surname_edges=sum(1 for e in FE if e['ambiguous']))
stats['pairs']=dict(pairs=len(rows),pairs_with_usd=sum(1 for r in rows if r['total_usd']>0),members_reached=len({r['bioguide'] for r in rows if r['total_usd']>0}),scored_total_usd=sum(r['total_usd'] for r in rows),
  scored_usd_by_party=tot(((r['member_party'],r['total_usd']) for r in rows),0))
# bundling credit per person (only scored rows: member committee, matched, not ambiguous/low). Org/PAC bundles split equally among the registrant's people (as in GOP build)
B=collections.defaultdict(lambda:dict(usd=0.0,members=set(),org=0.0,ind=0.0)); BM=collections.defaultdict(float)
for b in csv.DictReader(open('edges_bundling_all.csv')):
  if b['scored']!='True': continue
  BM[b['member_bioguide']]+=float(b['bundled_usd'])
  ids=b['matched_person_ids'].split('|')
  for pid in ids:
    s=float(b['bundled_usd'])/len(ids); B[pid]['usd']+=s; B[pid]['members'].add(b['member_bioguide'])
    B[pid]['org' if b['bundler_entity']!='IND' else 'ind']+=s
json.dump(stats,open(keep_prev('build_stats_all.json'),'w'),indent=1,default=str)
# ---- ranking ----
agg=collections.defaultdict(lambda:dict(usd=0,R=0,D=0,I=0,members=set(),fe=set(),ld203=0,fec=0,top=[]))
for p in rows:
  a=agg[p['person_id']]; a['usd']+=p['total_usd']; a['ld203']+=p['ld203_self_usd']; a['fec']+=p['fec_indiv_usd']; a[p['member_party']]+=p['total_usd']
  if p['total_usd']>0: a['members'].add(p['bioguide'])
  if p['former_employer_tie']: a['fe'].add((p['member'],p['member_party']))
  a['top'].append((p['total_usd'],p['member']+f" ({p['member_party']})"))
prev={}
try:
  for r in csv.DictReader(open('../ranking_money.csv')): prev[r['person_id']]=r['money_rank']
except FileNotFoundError: pass
lid2p={i:pid for pid,r in P.items() for i in r['person_key'].split('|')}
prev={lid2p.get(k):v for k,v in prev.items() if lid2p.get(k)}
def pct(vals):
  s=sorted(vals); n=len(s); import bisect
  return lambda v:(bisect.bisect_left(s,v)+0.5*(bisect.bisect_right(s,v)-bisect.bisect_left(s,v)))/n
def lean(r_,d_):
  t=r_+d_
  if t<2000: return ''
  sh=r_/t; return 'R' if sh>=0.67 else ('D' if sh<=0.33 else 'mixed')
R=[]
for pid,r in P.items():
  a=agg[pid]; t=a['R']+a['D']+a['I']
  gl=lean(a['R'],a['D']+a['I']); cl=r['covered_position_lean']
  ld=lean(int(r['ld203_R_usd']),int(r['ld203_D_usd']))
  if gl: pl,src=gl,'member_giving'
  elif ld: pl,src=ld,'ld203_all_feca_giving'
  elif cl!='none': pl,src=cl,'covered_position'
  else: pl,src='unknown',''
  R.append(dict(person_id=pid,person_key=r['person_key'],lobbyist=r['name'],firm=r['main_registrant'],lobbyist_kind=r['lobbyist_kind'],
    attrib_lobbying_usd_2023_26=int(r['attrib_lobbying_usd_2023_26']),attrib_income_2023_26=int(r['attrib_income_2023_26']),attrib_inhouse_expense_2023_26=int(r['attrib_inhouse_expense_2023_26']),
    usd_to_members=a['usd'],usd_to_R_members=a['R'],usd_to_D_members=a['D'],usd_to_I_members=a['I'],member_giving_R_share='' if not t else round(a['R']/t,3),
    ld203_all_feca_R_share=r['ld203_R_share'],covered_position_lean=cl,cov_R_hits=r['cov_R_hits'],cov_D_hits=r['cov_D_hits'],party_lean=pl,party_lean_source=src,former_member_party=r['former_member_party'],
    ld203_self_usd=a['ld203'],fec_indiv_usd=a['fec'],n_members_funded=len(a['members']),
    former_employer_members='|'.join(sorted(f"{m} ({q})" for m,q in a['fe'])),n_former_employer=len(a['fe']),
    top_recipients='|'.join(f"{m} ${u}" for u,m in sorted(a['top'],reverse=True)[:5]),
    bundled_usd_to_members=round(B[pid]['usd'],2),bundled_via_org_pac_usd=round(B[pid]['org'],2),bundled_individual_usd=round(B[pid]['ind'],2),n_members_bundled_for=len(B[pid]['members']),
    gop300_prev_money_rank=prev.get(pid,''),covered_positions=r['covered_positions'][:200]))
pi=pct([x['attrib_lobbying_usd_2023_26'] for x in R]); pu=pct([x['usd_to_members'] for x in R]); pm=pct([x['n_members_funded'] for x in R]); pf=pct([x['n_former_employer'] for x in R]); pb=pct([x['bundled_usd_to_members'] for x in R])
for x in R:
  x['money_score']=round(100*(0.315*pi(x['attrib_lobbying_usd_2023_26'])+0.315*pu(x['usd_to_members'])+0.18*pm(x['n_members_funded'])+0.09*pf(x['n_former_employer'])+0.10*pb(x['bundled_usd_to_members'])),2)
  x['computed_at']=NOW
R.sort(key=lambda x:(-x['money_score'],-x['usd_to_members']))
for i,x in enumerate(R,1): x['money_rank']=i
for lab in ('R','D'):
  k=0
  for x in R:
    if x['party_lean']==lab: k+=1; x[f'rank_within_{lab}_lean']=k
fields=['money_rank','money_score']+[k for k in R[0] if k not in ('money_rank','money_score')]+['rank_within_R_lean','rank_within_D_lean']
fields=list(dict.fromkeys(fields))
w=csv.DictWriter(open(keep_prev('ranking_money_all.csv'),'w'),fieldnames=fields);w.writeheader();w.writerows(R)
# per member totals
MT=collections.defaultdict(lambda:dict(usd=0,ld203=0,fec=0,lob=set(),fe=set(),top=[]))
for p in rows:
  m=MT[p['bioguide']]; m['usd']+=p['total_usd']; m['ld203']+=p['ld203_self_usd']+0.5*p['ld203_pac_usd']; m['fec']+=p['fec_indiv_usd']
  if p['total_usd']>0: m['lob'].add(p['person_id']); m['top'].append((p['total_usd'],p['lobbyist']))
  if p['former_employer_tie']: m['fe'].add(p['lobbyist'])
MR=[]
for b,mm in M.items():
  m=MT[b]
  MR.append(dict(bioguide=b,member=mm['name'],party=PA(b),chamber=mm['chamber'],state=mm['state'],district=mm['district'],lobbyist_usd_scored=m['usd'],ld203_usd_scored=round(m['ld203']),fec_usd_scored=m['fec'],
    n_lobbyists_giving=len(m['lob']),bundled_usd_form3l=round(BM.get(b,0),2),n_former_staff_now_lobbyists=len(m['fe']),former_staff_lobbyists='|'.join(sorted(m['fe']))[:400],
    top_lobbyist_donors='|'.join(f"{n} ${u}" for u,n in sorted(m['top'],reverse=True)[:5]),computed_at=NOW))
MR.sort(key=lambda r:-r['lobbyist_usd_scored'])
for i,r in enumerate(MR,1): r['rank_by_lobbyist_usd']=i
w=csv.DictWriter(open(keep_prev('member_totals_all.csv'),'w'),fieldnames=['rank_by_lobbyist_usd']+[k for k in MR[0] if k!='rank_by_lobbyist_usd']);w.writeheader();w.writerows(MR)
print(json.dumps({k:v for k,v in stats.items() if k!='fec_party_committees_excluded'},indent=1,default=str))
for x in R[:20]: print(x['money_rank'],x['lobbyist'],x['firm'][:28],x['lobbyist_kind'],x['attrib_lobbying_usd_2023_26'],x['usd_to_members'],x['n_members_funded'],x['n_former_employer'],x['bundled_usd_to_members'],x['party_lean'],x['money_score'])
