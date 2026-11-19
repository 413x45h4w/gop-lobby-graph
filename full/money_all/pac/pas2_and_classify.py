# PAC layer, step 2: PAC -> member edges from FEC bulk pas2 (committee-to-candidate contributions and independent expenditures, 2024+2026 files dated 2026-11-15),
# and classification of every FEC committee by type and party lean.
import csv,json,collections,datetime,gzip,sys,re
sys.path.insert(0,'..'); from safeio import keep_prev
NOW=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
LC=json.load(open('../../../raw/legislators-current.json'))
C2B={}
for l in LC:
  for c in l['id'].get('fec',[]): C2B[c]=l['id']['bioguide']
C2B['S6SC04437']='G000608'  # manual cn26 match, see bundling/member_committees_all.py
MP={l['id']['bioguide']:{'Republican':'R','Democrat':'D','Independent':'I'}.get(l['terms'][-1]['party'],'?') for l in LC}
MN={l['id']['bioguide']:l['name'].get('official_full') or l['name']['first']+' '+l['name']['last'] for l in LC}
CNP={}
for yy in ('24','26'):
  for line in open(f'../raw/fec_bulk/cn{yy}.txt',encoding='latin-1'):
    q=line.split('|'); CNP[q[0]]=q[2]
CM={}
for yy in ('24','26'):
  for line in open(f'../raw/fec_bulk/cm{yy}.txt',encoding='latin-1'):
    q=line.rstrip('\n').split('|'); CM[q[0]]=dict(name=q[1],treasurer=q[2],city=q[5],state=q[6],dsgn=q[8],tp=q[9],party=q[10],org_tp=q[12],connected_org=q[13],cand_id=q[14] if len(q)>14 else '')
OWN=collections.defaultdict(set)
for r in csv.DictReader(open('../bundling/member_committees_all.csv')): OWN[r['committee_id']].add(r['bioguide'])
CAT={'24K':'direct_contribution','24Z':'direct_inkind','24E':'ie_support','24A':'ie_oppose','24C':'party_coordinated','24F':'communication_cost_support','24N':'communication_cost_oppose'}
SUPPORT={'24K','24Z','24E','24C','24F'}
lean=collections.defaultdict(lambda:collections.Counter())
agg=collections.defaultdict(lambda:dict(usd=0.0,n=0,subs=[],first='',last=''))
rows_out=gzip.open('../raw/pas2_member_rows_2023_2026.csv.gz','wt'); w=csv.writer(rows_out)
w.writerow(['cycle','committee_id','transaction_tp','category','cand_id','bioguide','date','amount','memo_cd','sub_id','image_num','fec_url','computed_at'])
st=collections.Counter()
for yy in ('24','26'):
  import zipfile
  with zipfile.ZipFile(f'../raw/fec_bulk/pas2{yy}.zip') as z:
    for line in z.open('itpas2.txt'):
      q=line.decode('latin-1').rstrip('\n').split('|')
      cm,tp,dt,amt,cand,memo,sub,img=q[0],q[5],q[13],q[14],q[16],q[19],q[21],q[4]
      iso=f"{dt[4:8]}-{dt[0:2]}-{dt[2:4]}" if len(dt)==8 else ''
      if iso<'2023-01-01' or tp not in CAT: st['skip_date_or_type']+=1; continue
      try: a=float(amt)
      except: continue
      p=CNP.get(cand,'')
      if memo!='X':
        sign=1 if tp in SUPPORT else -1
        if p in ('REP','DEM'): lean[cm][('R' if p=='REP' else 'D') if sign>0 else ('D' if p=='REP' else 'R')]+=a
      b=C2B.get(cand)
      if not b: continue
      if b in OWN.get(cm,()): st['own_committee_transfer_skipped']+=1; continue
      if memo=='X': st['memo_skipped']+=1; continue
      w.writerow(['20'+yy,cm,tp,CAT[tp],cand,b,iso,a,memo,sub,img,f'https://docquery.fec.gov/cgi-bin/fecimg/?{img}',NOW])
      g=agg[(cm,b,'20'+yy,CAT[tp])]; g['usd']+=a; g['n']+=1
      if len(g['subs'])<5: g['subs'].append(sub)
      st['member_rows']+=1
rows_out.close()
# committee classification
NAT={'C00027466':'NRSC','C00075820':'NRCC','C00003418':'RNC','C00042366':'DSCC','C00000935':'DCCC','C00010603':'DNC'}
def cls(c,m):
  t,d,o=m['tp'],m['dsgn'],m['org_tp']
  if c in NAT: return 'party_national_committee'
  if c in OWN and t not in ('X','Y','Z') and d!='D': return 'member_campaign_or_jfc'
  if t in ('X','Y'): return 'party_committee_national' if t=='Y' and re.search(r'NATIONAL|SENATORIAL|CONGRESSIONAL',m['name']) else 'party_committee_state_local'
  if t=='Z': return 'party_nonfederal_account'
  if d=='J': return 'joint_fundraising_committee'
  if d=='D': return 'leadership_pac_of_member' if c in OWN else 'leadership_pac_nonmember'
  if t=='O': return 'super_pac_independent_expenditure_only'
  if t in ('V','W'): return 'hybrid_pac'
  if t in ('N','Q'):
    return {'C':'corporate_pac','L':'labor_pac','M':'membership_pac','T':'trade_association_pac','V':'cooperative_pac','W':'corp_without_stock_pac'}.get(o,'nonconnected_pac')
  if t=='I': return 'independent_expenditor_person_or_group'
  if t=='E': return 'electioneering_communication'
  if t=='C': return 'communication_cost_filer'
  if t in ('H','S','P'): return 'candidate_committee'
  return 'other_'+(t or 'unknown')
REC=collections.defaultdict(dict)
for yy in ('24','26'):
  for line in open(f'../raw/fec_bulk/webk{yy}.txt',encoding='latin-1'):
    q=line.rstrip('\n').split('|')
    try: REC[q[0]]['20'+yy]=float(q[5] or 0)
    except: pass
out=[]
for c,m in CM.items():
  L=lean[c]; R,D=L['R'],L['D']
  if m['party'] in ('REP','DEM') and cls(c,m).startswith('party'): pl,src='R' if m['party']=='REP' else 'D','fec_party_affiliation'
  elif c in NAT: pl,src=('R' if NAT[c] in ('NRSC','NRCC','RNC') else 'D'),'national_party_committee'
  elif R+D>=5000: sh=R/(R+D); pl,src=('R' if sh>=0.67 else ('D' if sh<=0.33 else 'mixed')),'pas2_support_oppose_dollars_2023_26'
  elif m['party'] in ('REP','DEM'): pl,src='R' if m['party']=='REP' else 'D','fec_party_affiliation'
  else: pl,src='unknown',''
  out.append(dict(committee_id=c,name=m['name'],committee_type=m['tp'],designation=m['dsgn'],org_type=m['org_tp'],connected_org=m['connected_org'],fec_party=m['party'],committee_class=cls(c,m),
    party_lean=pl,lean_source=src,pas2_pro_R_usd=round(R),pas2_pro_D_usd=round(D),pas2_R_share='' if not R+D else round(R/(R+D),3),
    receipts_2024=REC[c].get('2024',''),receipts_2026=REC[c].get('2026',''),treasurer=m['treasurer'],state=m['state'],computed_at=NOW))
w=csv.DictWriter(open(keep_prev('committees_classified.csv'),'w'),fieldnames=list(out[0]));w.writeheader();w.writerows(out)
A=[]
for (cm,b,cy,cat),g in agg.items():
  m=CM.get(cm,{}); A.append(dict(committee_id=cm,committee_name=m.get('name',''),committee_class=cls(cm,m) if m else '',bioguide=b,member=MN[b],member_party=MP[b],cycle=cy,category=cat,usd=round(g['usd'],2),n_rows=g['n'],sample_sub_ids='|'.join(g['subs']),computed_at=NOW))
A.sort(key=lambda a:-a['usd'])
w=csv.DictWriter(open(keep_prev('../edges_pac_to_member_all.csv'),'w'),fieldnames=list(A[0]));w.writeheader();w.writerows(A)
print(dict(st),'agg',len(A),collections.Counter(a['category'] for a in A))
print(collections.Counter(o['committee_class'] for o in out).most_common())
