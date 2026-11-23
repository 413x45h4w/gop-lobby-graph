# IRS Political Organization (527) filings: Form 8871 (notice; officers 'D' records) and Form 8872 (periodic reports: Sched A contributions, Sched B expenditures)
# from the IRS POFD full data file (raw/irs527_fulldata_20261122.zip, transmission 2026-11-21). Streamed, never unzipped to disk.
# Amendments: for each (EIN, period_begin, period_end) keep only the 8872 with the latest INSERT_DATETIME (then highest form id); A/B rows of superseded forms dropped.
# Scope: 8872 periods ending >= 2023-01-01; Sched A/B rows dated >= 2023-01-01 (undated rows kept if their form qualifies).
import zipfile,io,csv,sys,collections,datetime,json
sys.path.insert(0,'scripts'); import personmatch as M
sys.path.insert(0,'/workspace/gop-lobby-graph/full/boards/scripts'); from orgnorm import key as okey
NOW=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
Z='raw/irs527_fulldata_20261122.zip'
def lines():
  with zipfile.ZipFile(Z) as z, z.open(z.namelist()[0]) as fh:
    for l in io.TextIOWrapper(fh,encoding='latin-1',errors='replace'): yield l.rstrip('\r\n').split('|')
F={}; best={}; L8871={}
for f in lines():
  if f[0]=='2' and len(f)>45:
    fid=f[2]; per=(f[10],f[3],f[4]); ins=f[-2] if f[-1]=='' else f[-1]
    if f[4]<'20230101': continue
    F[fid]=dict(ein=f[10],org=f[9],pb=f[3],pe=f[4],amended=f[6],ins=ins,state=f[14])
    cur=best.get(per)
    if cur is None or (ins,int(fid))>(F[cur]['ins'],int(cur)): best[per]=fid
  elif f[0]=='1' and len(f)>8:
    ins=f[-3] if len(f)>3 else ''
    L8871[f[2]]=dict(ein=f[6],org=f[7],ins=ins)
keep=set(best.values())
print('8872 forms 2023+',len(F),'kept after amendment dedup',len(keep),flush=True)
latest8871={}
for fid,d in L8871.items():
  c=latest8871.get(d['ein'])
  if c is None or (d['ins'],int(fid))>(L8871[c]['ins'],int(c)): latest8871[d['ein']]=fid
k8871=set(latest8871.values())
ACTIVE={F[x]['ein'] for x in keep}  # 8871 officers kept only for 527s with an 8872 period ending 2023+ or an 8871 filed 2023+
k8871={x for x in k8871 if L8871[x]['ein'] in ACTIVE or L8871[x]['ins']>='2023'}
CM={}
for c in ('24','26'):
  for l in open(f'/workspace/gop-lobby-graph/full/money_all/raw/fec_bulk/cm{c}.txt',encoding='latin-1'):
    x=l.rstrip('\n').split('|'); k=okey(x[1])
    if k: CM.setdefault(k,(x[0],x[1],x[9]))
CL={r['client_key']:r for r in csv.DictReader(open('/workspace/gop-lobby-graph/full/boards/lda_clients_spend_2023_26.csv'))}
TG={}
for fn in ('targets_990.csv','targets_990_pass2.csv'):
  try:
    for r in csv.DictReader(open(fn)): TG.setdefault(okey(r['bmf_name']),r)
  except FileNotFoundError: pass
FA='form_id,sched_a_id,org_527,org_527_ein,contributor_name,city,state,employer,occupation,amount,agg_ytd,date,contributor_kind,lobbyist_person_id,lobbyist,lobbyist_confidence,lobbyist_basis,lda_client_key,lda_client_name,nonprofit_ein,nonprofit_name,url,computed_at'.split(',')
wa=csv.DictWriter(open('irs527_contributions_2023_26.csv','w'),fieldnames=FA); wa.writeheader()
FB='form_id,sched_b_id,org_527,org_527_ein,recipient_name,city,state,recipient_employer,recipient_occupation,amount,date,purpose,fec_committee_id,fec_committee_name,fec_committee_type,member_bioguide,member_name,member_confidence,url,computed_at'.split(',')
wb=csv.DictWriter(open('irs527_expenditures_2023_26.csv','w'),fieldnames=FB); wb.writeheader()
FD='form_8871_id,org_527,org_527_ein,person_name,title,lobbyist_person_id,lobbyist,lobbyist_confidence,member_bioguide,member_name,member_confidence,computed_at'.split(',')
wd=csv.DictWriter(open('irs527_officers_8871.csv','w'),fieldnames=FD); wd.writeheader()
st=collections.Counter(); ORG=collections.defaultdict(lambda: dict(a=0.0,b=0.0,na=0,nb=0,name=''))
for f in lines():
  t=f[0]
  if t=='A' and len(f)>=17 and f[1] in keep:
    dt=f[16]
    if dt and dt<'20230101': continue
    try: a=float(f[13] or 0)
    except: a=0
    o=ORG[f[4]]; o['a']+=a; o['na']+=1; o['name']=f[3]; st['A']+=1
    name=f[5]; emp=f[12]; ck=okey(name); ek=okey(emp)
    row=dict(form_id=f[1],sched_a_id=f[2],org_527=f[3],org_527_ein=f[4],contributor_name=name,city=f[8],state=f[9],employer=emp,occupation=f[14],amount=a,agg_ytd=f[15],date=f'{dt[:4]}-{dt[4:6]}-{dt[6:8]}' if dt else '',
      url=f"https://forms.irs.gov/app/pod/basicSearch/search?formType=8872&ein={f[4]}",computed_at=NOW,contributor_kind='')
    hit=False
    if ck in CL: row.update(contributor_kind='org_lda_client',lda_client_key=ck,lda_client_name=CL[ck]['client_name']); hit=True
    if ck in TG: row.update(contributor_kind=(row['contributor_kind']+'|' if row['contributor_kind'] else '')+'org_nonprofit_target',nonprofit_ein=TG[ck]['ein'],nonprofit_name=TG[ck]['bmf_name']); hit=True
    if not hit:
      m=M.match_lobbyist(name,emp)
      if m and m['confidence']!='low_name_only':
        row.update(contributor_kind='person_lobbyist',lobbyist_person_id=m['person_id'],lobbyist=m['name'],lobbyist_confidence=m['confidence'],lobbyist_basis=m['basis']); hit=True; st['A_lobbyist']+=1
      elif ek in CL: row.update(contributor_kind='person_employee_of_lda_client',lda_client_key=ek,lda_client_name=CL[ek]['client_name']); hit=True
    if hit or a>=5000: wa.writerow(row)
  elif t=='B' and len(f)>=17 and f[1] in keep:
    dt=f[15]
    if dt and dt<'20230101': continue
    try: a=float(f[13] or 0)
    except: a=0
    o=ORG[f[4]]; o['b']+=a; o['nb']+=1; o['name']=f[3]; st['B']+=1
    if a<1000: continue
    rk=okey(f[5]); c=CM.get(rk)
    row=dict(form_id=f[1],sched_b_id=f[2],org_527=f[3],org_527_ein=f[4],recipient_name=f[5],city=f[8],state=f[9],recipient_employer=f[12],recipient_occupation=f[14],amount=a,date=f'{dt[:4]}-{dt[4:6]}-{dt[6:8]}' if dt else '',purpose=f[16],
      url=f"https://forms.irs.gov/app/pod/basicSearch/search?formType=8872&ein={f[4]}",computed_at=NOW)
    if c: row.update(fec_committee_id=c[0],fec_committee_name=c[1],fec_committee_type=c[2]); st['B_to_fec_committee']+=1
    wb.writerow(row)
  elif t=='D' and len(f)>=7 and f[1] in k8871:
    row=dict(form_8871_id=f[1],org_527=f[3],org_527_ein=f[4],person_name=f[5],title=f[6],computed_at=NOW)
    m=M.match_lobbyist(f[5],f[3])
    if m and m['confidence']!='low_name_only': row.update(lobbyist_person_id=m['person_id'],lobbyist=m['name'],lobbyist_confidence=m['confidence'])
    mm=M.match_member(f[5],f[6]+' '+f[3])
    if mm and mm['confidence']!='low_name_only': row.update(member_bioguide=mm['bioguide'],member_name=mm['name'],member_confidence=mm['confidence'])
    wd.writerow(row); st['D']+=1
O=[dict(org_527_ein=e,org_527=o['name'],sched_a_usd_2023_26=round(o['a']),n_sched_a=o['na'],sched_b_usd_2023_26=round(o['b']),n_sched_b=o['nb'],computed_at=NOW) for e,o in ORG.items()]
O.sort(key=lambda x:-x['sched_a_usd_2023_26'])
w=csv.DictWriter(open('irs527_orgs_totals_2023_26.csv','w'),fieldnames=list(O[0])); w.writeheader(); w.writerows(O)
json.dump(dict(computed_at=NOW,forms_2023=len(F),forms_kept=len(keep),stats=st),open('irs527_stats.json','w'),indent=1)
print('DONE',dict(st))
