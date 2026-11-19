import os
# PAC layer, final step: lobbyist->committee edges, indirect lobbyist->PAC->member attribution, registrant LD-203 credit, PAC officer roles,
# PAC score and the combined 'direct + PAC' ranking. Direct-layer files are read, never modified.
import csv,json,collections,datetime,re,sys,bisect
sys.path.insert(0,'..'); from safeio import keep_prev
NOW=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
P={r['person_id']:r for r in csv.DictReader(open('../people_all.csv'))}
C={r['committee_id']:r for r in csv.DictReader(open('committees_classified.csv'))}
LC=json.load(open('../../../raw/legislators-current.json'))
MP={l['id']['bioguide']:{'Republican':'R','Democrat':'D','Independent':'I'}.get(l['terms'][-1]['party'],'?') for l in LC}
MN={l['id']['bioguide']:l['name'].get('official_full') or l['name']['first']+' '+l['name']['last'] for l in LC}
MEMC=collections.defaultdict(set)
for r in csv.DictReader(open('../bundling/member_committees_all.csv')): MEMC[r['committee_id']].add(r['bioguide'])
# JFC party lean from where the JFC's money went (OpenFEC by_recipient_id): recipient = member committee (member party) or a committee with R/D lean.
# Applied only where the classifier left the JFC unknown/mixed; >=0.67 of lean-known transfers -> R or D. lean_source records this.
JFCLEAN={}
if os.path.exists('jfc_transfers_raw.jsonl'):
  for l in open('jfc_transfers_raw.jsonl'):
    d=json.loads(l); t=collections.Counter()
    for r in d.get('results') or []:
      rid=r.get('recipient_id'); u=float(r.get('total') or 0)
      ps={MP.get(b) for b in MEMC.get(rid,())} or {C.get(rid,{}).get('party_lean')}
      if len(ps)==1 and list(ps)[0] in ('R','D'): t[list(ps)[0]]+=u
    tot=t['R']+t['D']; cm=d['_jfc']
    if tot>=5000 and cm in C and C[cm].get('party_lean') in ('unknown','mixed',''):
      sh=t['R']/tot; lean='R' if sh>=0.67 else ('D' if sh<=0.33 else 'mixed')
      C[cm]['party_lean']=lean; C[cm]['lean_source']='jfc_transfer_recipients'; JFCLEAN[cm]=lean
cyc=lambda d:'2024' if d[:4] in ('2023','2024') else ('2026' if d[:4] in ('2025','2026') else '')
day=lambda s:datetime.date.fromisoformat(s[:10])
ST={'jfc_lean_from_transfers':dict(collections.Counter(JFCLEAN.values()))}
with open(keep_prev('jfc_lean_from_transfers.csv'),'w') as f:
  f.write('fec_committee_id,name,party_lean,lean_source,computed_at\n')
  for k,v in sorted(JFCLEAN.items()): f.write(f'{k},"{C[k]["name"]}",{v},jfc_transfer_recipients,{NOW}\n')
# ---- 1. lobbyist -> committee edges ----
F=[r for r in csv.DictReader(open('lobbyist_to_pac_fec_rows.csv')) if not r['match_confidence'].startswith('low') and r['memo_cd']!='X']
for r in F:
  a=float(r['amount']); r['_usd']=-abs(a) if r['transaction_tp'] in ('22Y','22Z') else a
LD=list(csv.DictReader(open('lobbyist_to_pac_ld203_resolved.csv')))
fidx=collections.defaultdict(list)
for r in F: fidx[(r['person_id'],r['fec_committee_id'],round(r['_usd']))].append(r)
ldk=[]
for l in LD:
  l['dup_of_fec_sub_id']=''
  try: a=round(float(l['amount'])); dl=day(l['date'])
  except: continue
  for f in fidx.get((l['person_id'],l['fec_committee_id'],a),[]):
    if abs((day(f['date'])-dl).days)<=3: l['dup_of_fec_sub_id']=f['fec_sub_id']; break
  if not l['dup_of_fec_sub_id']: ldk.append(l)
UN=[u for u in csv.DictReader(open('lobbyist_to_pac_ld203_unresolved.csv')) if u['person_id']]
E=[]
for r in F: E.append(dict(person_id=r['person_id'],lobbyist=r['lobbyist'],source='fec_indiv',fec_committee_id=r['fec_committee_id'],date=r['date'],usd=r['_usd'],evidence=r['fec_sub_id'],evidence_url=r['fec_url'],match_confidence=r['match_confidence']))
for l in ldk: E.append(dict(person_id=l['person_id'],lobbyist=l['lobbyist'],source='ld203_self',fec_committee_id=l['fec_committee_id'],date=l['date'],usd=float(l['amount'] or 0),evidence=l['filing_uuid'],evidence_url=l['filing_url'],match_confidence='ld203_'+l['resolution']))
for e in E:
  c=C.get(e['fec_committee_id'],{}); e.update(committee_name=c.get('name',''),committee_class=c.get('committee_class',''),committee_party_lean=c.get('party_lean','unknown'),cycle=cyc(e['date']),computed_at=NOW)
w=csv.DictWriter(open(keep_prev('../edges_lobbyist_to_pac_all.csv'),'w'),fieldnames=list(E[0]));w.writeheader();w.writerows(E)
ST['lobbyist_to_pac']=dict(rows=len(E),fec_rows=len(F),ld203_rows_after_fec_dedup=len(ldk),ld203_dup_of_fec=len(LD)-len(ldk),lobbyists=len({e['person_id'] for e in E}),committees=len({e['fec_committee_id'] for e in E}),
  pairs=len({(e['person_id'],e['fec_committee_id']) for e in E}),usd=round(sum(e['usd'] for e in E)),
  usd_by_committee_lean={k:round(v) for k,v in collections.Counter({}).items()},
  ld203_unresolved_rows=len(UN),ld203_unresolved_usd=round(sum(float(u['amount'] or 0) for u in UN)))
bl=collections.Counter(); bc=collections.Counter()
for e in E: bl[e['committee_party_lean']]+=e['usd']; bc[e['committee_class']]+=e['usd']
ST['lobbyist_to_pac']['usd_by_committee_lean']={k:round(v) for k,v in bl.items()}; ST['lobbyist_to_pac']['usd_by_committee_class']={k:round(v) for k,v in bc.most_common()}
# top committees
tc=collections.defaultdict(lambda:dict(usd=0.0,ppl=set()))
for e in E: tc[e['fec_committee_id']]['usd']+=e['usd']; tc[e['fec_committee_id']]['ppl'].add(e['person_id'])
TOP=[dict(fec_committee_id=k,name=C.get(k,{}).get('name',''),committee_class=C.get(k,{}).get('committee_class',''),party_lean=C.get(k,{}).get('party_lean',''),usd_from_universe_lobbyists=round(v['usd']),n_lobbyists=len(v['ppl']),computed_at=NOW) for k,v in tc.items()]
TOP.sort(key=lambda x:-x['usd_from_universe_lobbyists'])
w=csv.DictWriter(open(keep_prev('top_pacs_by_lobbyist_money.csv'),'w'),fieldnames=list(TOP[0]));w.writeheader();w.writerows(TOP)
# ---- 2. PAC -> member (from pas2 aggregate) ----
PM=list(csv.DictReader(open('../edges_pac_to_member_all.csv')))
give=collections.defaultdict(lambda:collections.defaultdict(lambda:collections.Counter()))  # give[cm][cyc][(bio,cat)]
for r in PM: give[r['committee_id']][r['cycle']][(r['bioguide'],r['category'])]+=float(r['usd'])
pm_party=collections.defaultdict(lambda:collections.Counter())
for r in PM: pm_party[r['category']][r['member_party']]+=float(r['usd'])
ST['pac_to_member']={k:{p:round(v) for p,v in c.items()} for k,c in pm_party.items()}
ST['pac_to_member_edges']=dict(collections.Counter(r['category'] for r in PM))
ST['pac_to_member_pacs']=len({r['committee_id'] for r in PM})
# ---- 3. indirect pro-rata ----
REC={c:{'2024':float(r['receipts_2024'] or 0),'2026':float(r['receipts_2026'] or 0)} for c,r in C.items()}
contrib=collections.Counter()
for e in E:
  if e['cycle']: contrib[(e['person_id'],e['fec_committee_id'],e['cycle'])]+=e['usd']
# lobbyist money to member committees (direct layer FEC rows) also flows on when that committee gives to OTHER members (leadership PACs, campaign transfers)
DF=[r for r in csv.DictReader(open('../edges_fec_all.csv')) if not r['match_confidence'].startswith('low') and r['memo_cd']!='X']
for r in DF:
  c_=cyc(r['date'])
  if c_: contrib[(r['person_id'],r['fec_committee_id'],c_)]+=float(r['amount'])
SH=[];SKIP=collections.Counter()
ind=collections.defaultdict(lambda:dict(direct=0.0,ies=0.0,ieo=0.0,coord=0.0,pacs=collections.Counter()))
for (pid,cm,cy),usd in contrib.items():
  if usd<=0: continue
  rec=REC.get(cm,{}).get(cy,0)
  if rec<=0: SKIP['no_receipts_in_webk']+=1; continue
  sh=min(1.0,usd/rec)
  g=give.get(cm,{}).get(cy,{})
  att=0.0
  for (b,cat),u in g.items():
    if b in MEMC.get(cm,()): continue
    x=ind[(pid,b)]
    if cat in ('direct_contribution','direct_inkind'): x['direct']+=sh*u; att+=sh*u; x['pacs'][cm]+=sh*u
    elif cat=='ie_support': x['ies']+=sh*u
    elif cat=='ie_oppose': x['ieo']+=sh*u
    else: x['coord']+=sh*u
  SH.append(dict(person_id=pid,lobbyist=P[pid]['name'],fec_committee_id=cm,committee_name=C.get(cm,{}).get('name',''),committee_class=C.get(cm,{}).get('committee_class',''),cycle=cy,lobbyist_usd=round(usd,2),committee_receipts=rec,share=round(sh,8),attributed_direct_to_members_usd=round(att,2),computed_at=NOW))
w=csv.DictWriter(open(keep_prev('indirect_shares_by_lobbyist_pac_cycle.csv'),'w'),fieldnames=list(SH[0]));w.writeheader();w.writerows(SH)
# JFC pro-rata (separate sub-component): share = lobbyist $ to JFC in cycle / JFC receipts (webk); credited = share x JFC transfers to the member's
# committees in that cycle (OpenFEC schedule_b by_recipient_id). If webk receipts missing, denominator = JFC total transfers out (documented fallback).
JT=collections.defaultdict(lambda:collections.defaultdict(collections.Counter))
for l in (open('jfc_transfers_raw.jsonl') if os.path.exists('jfc_transfers_raw.jsonl') else []):
  d=json.loads(l)
  for r in d.get('results') or []:
    if r.get('recipient_id') and r.get('total'): JT[d['_jfc']][str(r['cycle'])][r['recipient_id']]+=float(r['total'])
JP={k:1 for k in JT}
jfc=collections.Counter(); JR=[]
for (pid,cm,cy),usd in contrib.items():
  t=JT.get(cm,{}).get(cy)
  if not t or usd<=0: continue
  rec=REC.get(cm,{}).get(cy,0); den=rec if rec>0 else sum(t.values()); sh=min(1.0,usd/den)
  for pc,u in t.items():
    for b in MEMC.get(pc,()):
      jfc[(pid,b)]+=sh*u; JR.append(dict(person_id=pid,jfc_id=cm,jfc_name=C.get(cm,{}).get('name',''),cycle=cy,participant_committee=pc,bioguide=b,member=MN.get(b,''),lobbyist_usd=round(usd,2),jfc_receipts=rec,denominator='webk_receipts' if rec>0 else 'jfc_transfers_out',share=round(sh,8),jfc_transfer_to_participant_usd=u,credited_usd=round(sh*u,2),computed_at=NOW))
if JR:
  w=csv.DictWriter(open(keep_prev('../edges_lobbyist_jfc_split_to_member.csv'),'w'),fieldnames=list(JR[0]));w.writeheader();w.writerows(JR)
IR=[]
for (pid,b),x in ind.items():
  IR.append(dict(person_id=pid,lobbyist=P[pid]['name'],bioguide=b,member=MN[b],member_party=MP[b],indirect_pac_direct_usd=round(x['direct'],2),indirect_ie_support_usd=round(x['ies'],2),indirect_ie_oppose_usd=round(x['ieo'],2),indirect_party_coordinated_usd=round(x['coord'],2),
    jfc_split_usd=round(jfc.get((pid,b),0),2),top_pacs='|'.join(f"{C.get(k,{}).get('name','')[:40]} ${v:.0f}" for k,v in x['pacs'].most_common(3)),method='share = lobbyist $ to committee in cycle / committee total receipts (webk); attributed = share x committee direct contributions to member (pas2 24K+24Z)',computed_at=NOW))
for (pid,b),v in jfc.items():
  if (pid,b) not in ind: IR.append(dict(person_id=pid,lobbyist=P[pid]['name'],bioguide=b,member=MN[b],member_party=MP[b],indirect_pac_direct_usd=0,indirect_ie_support_usd=0,indirect_ie_oppose_usd=0,indirect_party_coordinated_usd=0,jfc_split_usd=round(v,2),top_pacs='',method='JFC pro rata only',computed_at=NOW))
IR.sort(key=lambda r:-(r['indirect_pac_direct_usd']+r['jfc_split_usd']))
w=csv.DictWriter(open(keep_prev('../edges_indirect_lobbyist_pac_member.csv'),'w'),fieldnames=list(IR[0]));w.writeheader();w.writerows(IR)
ip=collections.defaultdict(collections.Counter)
for r in IR:
  for k in ('indirect_pac_direct_usd','indirect_ie_support_usd','indirect_ie_oppose_usd','jfc_split_usd'): ip[k][r['member_party']]+=r[k]
ST['indirect']=dict(pairs=len(IR),lobbyists=len({r['person_id'] for r in IR}),skipped=dict(SKIP),jfcs_with_participants=len(JP),**{k:{p:round(v) for p,v in c.items()} for k,c in ip.items()})
# ---- 4. registrant LD-203 -> member, split among registrant's lobbyists ----
RG=list(csv.DictReader(open('../edges_registrant_ld203_to_member.csv')))
regc=collections.defaultdict(collections.Counter); regm=collections.Counter(); rp=collections.Counter(); rraw=collections.Counter()
for r in RG:
  a=min(float(r['amount'] or 0),7000.0); rp[MP.get(r['bioguide'],'?')]+=a; rraw[MP.get(r['bioguide'],'?')]+=float(r['amount'] or 0); regm[r['bioguide']]+=a
  ids=[i for i in r['person_ids'].split('|') if i]
  for i in ids: regc[i][r['bioguide']]+=a/len(ids)
ST['registrant_ld203']=dict(items=len(RG),registrants=len({r['registrant_id'] for r in RG}),members=len({r['bioguide'] for r in RG}),raw_usd_by_party={k:round(v) for k,v in rraw.items()},capped_usd_by_party={k:round(v) for k,v in rp.items()},lobbyists_credited=len(regc))
# ---- 5. officers ----
SUF={'JR','SR','II','III','IV','MR','MRS','MS','DR','HON','ESQ','CPA'}
def nameparts(s):
  if ',' not in (s or ''): return None
  la,fi=s.upper().split(',',1); la=' '.join(x for x in re.split(r'[\s\.]+',la) if x and x not in SUF); f=[x for x in re.split(r'[\s\.]+',fi) if x and x not in SUF]
  return (la,f[0]) if f and la else None
sys.path.insert(0,'../..'); from nicks import NICK
idx=collections.defaultdict(set)
for pid,r in P.items():
  for nm in r['merged_names'].split('|'):
    t=[x for x in re.split(r'[\s\.,]+',nm.upper()) if x and x not in SUF]
    if len(t)>=2:
      for f in {t[0]}|set(NICK.get(t[0],[]))|{k for k,v in NICK.items() if t[0] in v}: idx[(t[-1],f)].add(pid)
W=lambda s:set(re.findall(r"[A-Z0-9&']{3,}",(s or '').upper()))
STOP={'THE','LLC','LLP','INC','AND','PAC','POLITICAL','ACTION','COMMITTEE','FUND','FEDERAL','GROUP','AMERICAN','NATIONAL','ASSOCIATION','COMPANY','CORPORATION','CORP','UNITED','STATES','FOR','OF','AMERICA','COUNCIL','INSTITUTE','INTERNATIONAL'}
roles=[]
for c,r in C.items(): roles.append((c,'treasurer(fec_cm_bulk)',r['treasurer']))
for l in open('committee_detail_raw.jsonl'):
  d=json.loads(l)
  if d.get('custodian_name_full'): roles.append((d['_cid'],'custodian_of_records(form1)',d['custodian_name_full']))
  if d.get('treasurer_name'): roles.append((d['_cid'],'treasurer(form1)',d['treasurer_name']))
import os
for l in (open('committee_list_raw.jsonl') if os.path.exists('committee_list_raw.jsonl') else []):
  d=json.loads(l)
  if d.get('designated_agent_name'): roles.append((d['committee_id'],'designated_agent(form1)',d['designated_agent_name']))
OFF=[];OAMB=[];seenr=set()
for c,role,nm in roles:
  np_=nameparts(nm)
  if not np_: continue
  cands=idx.get(np_,set())
  if not cands: continue
  cr=C.get(c,{}); cw=(W(cr.get('name',''))|W(cr.get('connected_org','')))-STOP
  ev=[pid for pid in cands if cw & ((W(P[pid]['registrants'])-STOP)-set(np_[0].split()))]
  rowb=dict(fec_committee_id=c,committee_name=cr.get('name',''),committee_class=cr.get('committee_class',''),connected_org=cr.get('connected_org',''),role=role,fec_name=nm,
    member_committee_of='|'.join(sorted(MEMC.get(c,()))),computed_at=NOW)
  if len(ev)==1:
    k=(ev[0],c,role.split('(')[0])
    if k in seenr: continue
    seenr.add(k); OFF.append(dict(person_id=ev[0],lobbyist=P[ev[0]]['name'],firm=P[ev[0]]['main_registrant'],evidence='committee name/connected org shares a distinctive word with the lobbyist\'s LDA registrant',**rowb))
  else:
    OAMB.append(dict(candidate_person_ids='|'.join(sorted(cands)),candidate_names='|'.join(P[i]['name'] for i in sorted(cands)),reason=('several same-name lobbyists match the committee' if len(ev)>1 else 'name match only; committee not linked to the lobbyist\'s registrant'),**rowb))
w=csv.DictWriter(open(keep_prev('../edges_lobbyist_pac_officer.csv'),'w'),fieldnames=list(OFF[0]));w.writeheader();w.writerows(OFF)
w=csv.DictWriter(open(keep_prev('pac_officer_ambiguous.csv'),'w'),fieldnames=list(OAMB[0]));w.writeheader();w.writerows(OAMB)
ST['officers']=dict(edges=len(OFF),lobbyists=len({o['person_id'] for o in OFF}),committees=len({o['fec_committee_id'] for o in OFF}),by_role=dict(collections.Counter(o['role'] for o in OFF)),
  of_member_committees=sum(1 for o in OFF if o['member_committee_of']),ambiguous_rows=len(OAMB),detail_calls=sum(1 for _ in open('committee_detail_raw.jsonl')))
# ---- per-person aggregates + scores ----
D=list(csv.DictReader(open('../ranking_money_all.csv')))
lp=collections.defaultdict(lambda:collections.Counter())
for e in E: lp[e['person_id']][e['committee_party_lean']]+=e['usd']; lp[e['person_id']]['_tot']+=e['usd']; lp[e['person_id']]['_party']+=e['usd'] if e['committee_class'].startswith('party') else 0
iu=collections.defaultdict(collections.Counter)
for r in IR: iu[r['person_id']]['pac']+=r['indirect_pac_direct_usd']; iu[r['person_id']]['jfc']+=r['jfc_split_usd']; iu[r['person_id']]['ies']+=r['indirect_ie_support_usd']; iu[r['person_id']]['ieo']+=r['indirect_ie_oppose_usd']
uu=collections.Counter(); 
for u in UN: uu[u['person_id']]+=float(u['amount'] or 0)
offc=collections.Counter(o['person_id'] for o in OFF)
offm=collections.defaultdict(set)
for o in OFF: offm[o['person_id']].add(o['committee_name'][:40]+' ('+o['role'].split('(')[0]+')')
for r in D:
  pid=r['person_id']; L=lp[pid]
  r.update(lobbyist_to_pac_usd=round(L['_tot']),lobbyist_to_party_committees_usd=round(L['_party']),lobbyist_to_R_lean_committees_usd=round(L['R']),lobbyist_to_D_lean_committees_usd=round(L['D']),
    lobbyist_to_mixed_unknown_committees_usd=round(L['mixed']+L['unknown']+L['']),ld203_unresolved_committee_usd=round(uu[pid]),
    indirect_via_pac_usd=round(iu[pid]['pac']),indirect_via_jfc_split_usd=round(iu[pid]['jfc']),indirect_ie_support_usd=round(iu[pid]['ies']),indirect_ie_oppose_usd=round(iu[pid]['ieo']),
    registrant_ld203_member_usd_split=round(sum(regc[pid].values()),2),n_pac_officer_roles=offc[pid],pac_officer_of='|'.join(sorted(offm[pid]))[:300])
  pl=L['R']+L['D']; r['pac_giving_R_share']='' if not pl else round(L['R']/pl,3)
def pct(vals):
  s=sorted(vals); n=len(s)
  return lambda v:(bisect.bisect_left(s,v)+0.5*(bisect.bisect_right(s,v)-bisect.bisect_left(s,v)))/n
a=pct([r['lobbyist_to_pac_usd'] for r in D]); b=pct([r['indirect_via_pac_usd']+r['indirect_via_jfc_split_usd'] for r in D]); c=pct([r['registrant_ld203_member_usd_split'] for r in D]); o=pct([r['n_pac_officer_roles'] for r in D])
for r in D:
  r['pac_score']=round(100*(0.35*a(r['lobbyist_to_pac_usd'])+0.35*b(r['indirect_via_pac_usd']+r['indirect_via_jfc_split_usd'])+0.15*c(r['registrant_ld203_member_usd_split'])+0.15*o(r['n_pac_officer_roles'])),2)
  r['direct_only_score']=r['money_score']; r['direct_only_rank']=r['money_rank']
  r['direct_plus_pac_score']=round(0.75*float(r['money_score'])+0.25*r['pac_score'],2)
D.sort(key=lambda r:(-r['direct_plus_pac_score'],-int(r['usd_to_members'])))
for i,r in enumerate(D,1): r['direct_plus_pac_rank']=i
for lab in ('R','D'):
  k=0
  for r in D:
    if r['party_lean']==lab: k+=1; r[f'direct_plus_pac_rank_within_{lab}_lean']=k
first=['direct_plus_pac_rank','direct_plus_pac_score','direct_only_rank','direct_only_score','pac_score']
fields=first+[k for k in D[0] if k not in first and k not in ('money_rank','money_score')]+['direct_plus_pac_rank_within_R_lean','direct_plus_pac_rank_within_D_lean']
fields=list(dict.fromkeys(fields))
w=csv.DictWriter(open(keep_prev('../ranking_money_all_with_pac.csv'),'w'),fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(D)
# ---- members ----
M=list(csv.DictReader(open('../member_totals_all.csv')))
pmm=collections.defaultdict(collections.Counter)
for r in PM: pmm[r['bioguide']][r['category']]+=float(r['usd'])
lpacs={e['fec_committee_id'] for e in E}
pml=collections.Counter()
for r in PM:
  if r['committee_id'] in lpacs and r['category'] in ('direct_contribution','direct_inkind'): pml[r['bioguide']]+=float(r['usd'])
im=collections.defaultdict(collections.Counter)
for r in IR: im[r['bioguide']]['pac']+=r['indirect_pac_direct_usd']; im[r['bioguide']]['jfc']+=r['jfc_split_usd']
om=collections.Counter()
for o in OFF:
  for b in o['member_committee_of'].split('|'):
    if b: om[b]+=1
for m in M:
  b=m['bioguide']; g=pmm[b]
  m.update(pac_direct_usd_all_pacs=round(g['direct_contribution']+g['direct_inkind']),pac_direct_usd_from_lobbyist_funded_pacs=round(pml[b]),ie_support_usd=round(g['ie_support']),ie_oppose_usd=round(g['ie_oppose']),
    party_coordinated_and_comm_cost_usd=round(g['party_coordinated']+g['communication_cost_support']),indirect_lobbyist_via_pac_usd=round(im[b]['pac']),indirect_lobbyist_via_jfc_split_usd=round(im[b]['jfc']),
    registrant_ld203_usd_capped=round(regm[b]),n_lobbyist_officers_of_member_committees=om[b])
  m['lobbyist_direct_plus_indirect_usd']=int(m['lobbyist_usd_scored'])+m['indirect_lobbyist_via_pac_usd']+m['indirect_lobbyist_via_jfc_split_usd']
M.sort(key=lambda m:-m['lobbyist_direct_plus_indirect_usd'])
for i,m in enumerate(M,1): m['rank_direct_plus_indirect']=i
w=csv.DictWriter(open(keep_prev('../member_totals_all_with_pac.csv'),'w'),fieldnames=['rank_direct_plus_indirect']+[k for k in M[0] if k!='rank_direct_plus_indirect']);w.writeheader();w.writerows(M)
json.dump(ST,open(keep_prev('pac_layer_stats.json'),'w'),indent=1,default=str)
print(json.dumps(ST,indent=1,default=str)[:6000])
