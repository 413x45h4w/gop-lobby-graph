# Match super PAC / hybrid PAC / IE-only receipts (FEC indiv bulk, streamed to raw/superpac_receipts{24,26}.txt.gz) to:
#  (a) people in money_all/people_all.csv (lobbyist universe) using EXACTLY the index + confidence rules of money_all/fec_match_all.py (exec'd from its source);
#  (b) LDA clients/registrants: ORG-entity contributors whose normalized name == normalized LDA client/registrant name (exact key match) -> client_org_donor;
#      individual contributors whose EMPLOYER normalized == LDA client key -> aggregated client_employee_donor (signal only, NOT attributable to the company).
# Memo rows (memo_cd X) are skipped to avoid double counting earmark detail. Rows dated before 2023-01-01 are skipped.
import os,sys,gzip,csv,json,collections,datetime,re
OUT=os.path.abspath('.'); os.chdir('/workspace/gop-lobby-graph/full/money_all')
src=open('fec_match_all.py').read(); src=src[:src.index('out=[];amb=[]')]
g={'__name__':'fm'}; exec(compile(src,'fec_match_all.py(index part)','exec'),g)
idx,P,W,normorg,regnorm,LOBW,PROW,RANK,cl=(g[k] for k in ('idx','P','W','normorg','regnorm','LOBW','PROW','RANK','cl'))
sys.path.insert(0,'/workspace/gop-lobby-graph/full/boards/scripts'); from orgnorm import key as okey
NOW=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
B='/workspace/gop-lobby-graph/full/money_all/raw/fec_bulk'
CM={}
for c in ('24','26'):
  for l in open(f'{B}/cm{c}.txt',encoding='latin-1'):
    f=l.rstrip('\n').split('|'); CM[f[0]]=dict(name=f[1],tp=f[9],party=f[10],connected=f[13])
CL={}
for r in csv.DictReader(open('/workspace/gop-lobby-graph/full/boards/lda_clients_spend_2023_26.csv')): CL[r['client_key']]=r
REGK={}
for rg in {r for s in g['regs'].values() for r in s}:
  k=okey(rg)
  if k and k not in CL: REGK[k]=rg
os.chdir(OUT)
FN='person_id,lobbyist,lobbyist_firm,match_confidence,fec_committee_id,committee_name,committee_type,fec_contributor_name,entity_tp,city,state,employer,occupation,date,amount,transaction_tp,memo_text,fec_sub_id,fec_image_num,fec_url,cycle,computed_at'.split(',')
wo=csv.DictWriter(open('edges_lobbyist_to_superpac.csv','w'),fieldnames=FN); wo.writeheader()
wa=csv.DictWriter(open('superpac_lobbyist_ambiguous.csv','w'),fieldnames=['candidate_person_ids','candidate_names','candidate_firms','reason']+FN[4:]); wa.writeheader()
FO='client_key,client_name,lda_spend_2023_26,match_kind,fec_committee_id,committee_name,committee_type,fec_contributor_name,city,state,date,amount,fec_sub_id,fec_image_num,fec_url,cycle,computed_at'.split(',')
wc=csv.DictWriter(open('edges_client_org_to_superpac_rows.csv','w'),fieldnames=FO); wc.writeheader()
EMP=collections.defaultdict(lambda:[0.0,set(),0])   # (client_key,cmte,cycle)->[usd,donor names,rows]
CMT=collections.defaultdict(lambda:[0.0,0]); DON=collections.defaultdict(lambda:[0.0,0,collections.Counter()])
st=collections.Counter()
# Conduits registered as hybrid PACs: their receipts are earmarked pass-throughs to candidates, not super-PAC money (excluded; added 2026-11-22 after first run)
CONDUITS={'C00401224','C00694323'}
for cyc in ('24','26'):
  fn=f'raw/superpac_receipts{cyc}.txt.gz'
  for line in gzip.open(fn,'rt',encoding='latin-1'):
    f=line.rstrip('\n').split('|')
    if len(f)<21: st['bad']+=1; continue
    cmte,_,_,_,image,tp,ent,name,city,stt,_,emp,occ,dt,amt,_,_,_,memo,memo_text,sub=f[:21]
    st['rows']+=1
    if cmte in CONDUITS: st['conduit_skipped']+=1; continue
    if memo=='X': st['memo_skipped']+=1; continue
    iso=f"{dt[4:8]}-{dt[0:2]}-{dt[2:4]}" if len(dt)==8 else dt
    if iso<'2023-01-01': st['pre2023']+=1; continue
    try: a=float(amt)
    except: continue
    cm=CM.get(cmte,{}); CMT[(cmte,'20'+cyc)][0]+=a; CMT[(cmte,'20'+cyc)][1]+=1
    if a>=1000: d=DON[(name,cmte,"20"+cyc)]; d[0]+=a; d[1]+=1; d[2][emp]+=1
    base=dict(fec_committee_id=cmte,committee_name=cm.get('name',''),committee_type=cm.get('tp',''),fec_contributor_name=name,city=city,state=stt,date=iso,amount=a,fec_sub_id=sub,fec_image_num=image,
      fec_url=f"https://docquery.fec.gov/cgi-bin/fecimg/?{image}",cycle='20'+cyc,computed_at=NOW)
    if ent in ('ORG','CORP','COM','PAC'):
      k=okey(name)
      if k in CL: wc.writerow(dict(client_key=k,client_name=CL[k]['client_name'],lda_spend_2023_26=CL[k]['lda_spend_2023_26'],match_kind='org_name_eq_lda_client',**base)); st['client_org_rows']+=1
      elif k in REGK: wc.writerow(dict(client_key=k,client_name=REGK[k],lda_spend_2023_26='',match_kind='org_name_eq_lda_registrant',**base)); st['registrant_org_rows']+=1
      continue
    if ent!='IND' and ent!='': continue
    k=okey(emp)
    if k in CL: e=EMP[(k,cmte,'20'+cyc)]; e[0]+=a; e[1].add(name); e[2]+=1; st['client_employee_rows']+=1
    if ',' not in name: continue
    last,rest=name.split(',',1); last=cl(last)
    toks=[t for t in re.split(r'[\s\.]+',rest) if t and t not in ('MR','MS','MRS','DR','HON')]
    if not toks: continue
    cands=idx.get((last,toks[0]),[])
    if not cands: continue
    st['name_hit']+=1
    ew=set(W(emp+' '+occ)); empn=' '.join(re.findall(r"[A-Z0-9']+",emp.upper())); en=normorg(emp)
    scored=[]
    for pid,rw,phr,rn in cands:
      if (rw & ew) or any(p in empn for p in phr): c='high_employer_matches_registrant'
      elif LOBW.search(emp+' '+occ): c='medium_lobbying_occupation'
      elif PROW.search(occ) and stt in ('DC','VA','MD'): c='low_dc_area_professional'
      else: c=None
      if c: scored.append((RANK[c],c,pid,rn))
    row=dict(entity_tp=ent,employer=emp,occupation=occ,transaction_tp=tp,memo_text=memo_text,**base)
    if not scored: st['rej_no_evidence']+=1; continue
    best=min(s[0] for s in scored); top=[s for s in scored if s[0]==best]; reason=''
    if len(top)>1: reason=f'{len(top)} same-name LDA people tie at {top[0][1]}'
    elif len(cands)>1 and best>0: reason=f'{len(cands)} same-name LDA people and best evidence only {top[0][1]}'
    elif best==1 and en and en in regnorm and en not in top[0][3]: reason=f'lobbying occupation but employer is a different LDA registrant ({regnorm[en]})'
    if reason: wa.writerow(dict(candidate_person_ids='|'.join(s[2] for s in top),candidate_names='|'.join(P[s[2]]['name'] for s in top),candidate_firms='|'.join(P[s[2]]['main_registrant'] for s in top),reason=reason,**row)); st['ambiguous']+=1; continue
    s=top[0]; st[s[1]]+=1
    wo.writerow(dict(person_id=s[2],lobbyist=P[s[2]]['name'],lobbyist_firm=P[s[2]]['main_registrant'],match_confidence=s[1],**row))
  print(cyc,dict(st),flush=True)
E=[dict(client_key=k[0],client_name=CL[k[0]]['client_name'],lda_spend_2023_26=CL[k[0]]['lda_spend_2023_26'],fec_committee_id=k[1],committee_name=CM.get(k[1],{}).get('name',''),committee_type=CM.get(k[1],{}).get('tp',''),
  cycle=k[2],usd_from_employees=round(v[0],2),n_employee_donors=len(v[1]),n_rows=v[2],caveat='employer self-reported by individual donors; personal money, not company money',computed_at=NOW) for k,v in EMP.items()]
E.sort(key=lambda e:-e['usd_from_employees'])
w=csv.DictWriter(open('edges_client_employees_to_superpac.csv','w'),fieldnames=list(E[0])); w.writeheader(); w.writerows(E)
C=[dict(fec_committee_id=k[0],committee_name=CM.get(k[0],{}).get('name',''),committee_type=CM.get(k[0],{}).get('tp',''),connected_org=CM.get(k[0],{}).get('connected',''),cycle=k[1],itemized_receipts_usd_nonmemo=round(v[0],2),n_rows=v[1],computed_at=NOW) for k,v in CMT.items()]
C.sort(key=lambda e:-e['itemized_receipts_usd_nonmemo'])
w=csv.DictWriter(open('superpac_committees_receipts.csv','w'),fieldnames=list(C[0])); w.writeheader(); w.writerows(C)
D=sorted(DON.items(),key=lambda kv:-kv[1][0])[:5000]
w=csv.writer(open('superpac_top_donors.csv','w')); w.writerow(['rank','fec_contributor_name','fec_committee_id','committee_name','cycle','usd','n_rows','top_employer','computed_at','note'])
for i,(k,v) in enumerate(D,1): w.writerow([i,k[0],k[1],CM.get(k[1],{}).get('name',''),k[2],round(v[0],2),v[1],v[2].most_common(1)[0][0],NOW,'sum of itemized non-memo rows >= $1000 only']) 
json.dump(dict(computed_at=NOW,stats=st),open('superpac_match_stats.json','w'),indent=1)
print('DONE',dict(st))
