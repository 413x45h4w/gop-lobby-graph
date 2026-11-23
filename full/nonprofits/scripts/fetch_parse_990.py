# Fetch selected IRS e-file 990 XMLs by HTTP range reads from IRS TEOS zip batches (no full zip download) and parse:
# officers/directors/key employees (990 Part VII-A, 990EZ Part IV, 990PF Part VIII), Schedule I grants, 990PF paid grants,
# Schedule C (all numeric leaves + any named org/EIN groups e.g. payments to 527s), Schedule R related orgs and transactions, Part IV political/lobbying flags.
# Append-only checkpoint: raw/parsed_990.jsonl (one record per object_id); rerun skips done ids. XML is not stored (disk).
import csv,json,sys,os,time,collections,datetime,traceback
import remotezip,struct,inflate64
def zread(z,name):
  # some 2025/2026 IRS TEOS batches use Deflate64 (method 9), unsupported by zipfile: read the raw member via range request and inflate with inflate64
  zi=z.getinfo(name)
  if zi.compress_type!=9: return z.read(name)
  z.fp.seek(zi.header_offset); h=z.fp.read(30); n,m=struct.unpack('<HH',h[26:30])
  z.fp.seek(zi.header_offset+30+n+m); data=z.fp.read(zi.compress_size)
  return inflate64.Inflater().inflate(data)
from lxml import etree
tf=sys.argv[1] if len(sys.argv)>1 else 'targets_990.csv'
OUT='raw/parsed_990.jsonl'
done=set()
if os.path.exists(OUT):
  for l in open(OUT):
    try:
      d=json.loads(l)
      if 'error' not in d: done.add(d['object_id'])  # retry errors on rerun; loaders keep the last record per object_id
    except: pass
T=[r for r in csv.DictReader(open(tf)) if r['object_id'] and r['object_id'] not in done]
by=collections.defaultdict(list)
for r in T: by[(r['index_year'],r['xml_batch'])].append(r)
print(len(T),'to fetch in',len(by),'batches',flush=True)
def L(e): return etree.QName(e).localname
def txt(e,*names):
  for n in names:
    x=e.find('.//{*}'+n)
    if x is not None:
      s=' '.join(t.strip() for t in x.itertext() if t.strip())
      if s: return s
  return ''
def flat(e,prefix=''):
  out={}
  for c in e:
    if not isinstance(c.tag,str): continue
    p=prefix+'/'+L(c) if prefix else L(c)
    if len(c): out.update(flat(c,p))
    else: out[p]=(c.text or '').strip()
  return out
def parse(x,meta):
  r=etree.fromstring(x)
  rec=dict(object_id=meta['object_id'],ein=meta['ein'],target_name=meta['bmf_name'],subsection=meta['subsection'],return_type=txt(r,'ReturnTypeCd'),tax_period_end=txt(r,'TaxPeriodEndDt'),
    filer_name=txt(r.find('.//{*}Filer'),'BusinessNameLine1Txt') if r.find('.//{*}Filer') is not None else '',url=f"https://apps.irs.gov/pub/epostcard/990/xml/{meta['index_year']}/{meta['xml_batch']}.zip#{meta['object_id']}_public.xml")
  F=r.find('.//{*}ReturnData')
  rec['total_revenue']=txt(F,'CYTotalRevenueAmt','TotalRevenueAmt','TotalRevAndExpnssAmt')
  rec['flags']={k:txt(F,k) for k in ('PoliticalCampaignActyInd','LobbyingActivitiesInd','SubjectToProxyTaxInd','GrantsToOrganizationsInd','PoliticalActivitiesInd','LobbyingActivitiesInd','ActivitiesOrMissionDesc','MissionDesc','WebsiteAddressTxt')}
  P=[]
  for g in F.iter('{*}Form990PartVIISectionAGrp','{*}OfficerDirectorTrusteeEmplGrp','{*}OfficerDirTrstKeyEmplGrp','{*}CompensationHighestPaidEmplGrp'):
    P.append(dict(person=txt(g,'PersonNm'),business=txt(g,'BusinessNameLine1Txt'),title=txt(g,'TitleTxt'),hours=txt(g,'AverageHoursPerWeekRt','AverageHrsPerWkDevotedToPosRt'),
      director='X' if g.find('{*}IndividualTrusteeOrDirectorInd') is not None or g.find('{*}InstitutionalTrusteeInd') is not None else '',officer='X' if g.find('{*}OfficerInd') is not None else '',
      key_employee='X' if g.find('{*}KeyEmployeeInd') is not None else '',highest_comp='X' if g.find('{*}HighestCompensatedEmployeeInd') is not None or L(g)=='CompensationHighestPaidEmplGrp' else '',
      former='X' if g.find('{*}FormerOfcrDirectorTrusteeInd') is not None else '',comp=txt(g,'ReportableCompFromOrgAmt','CompensationAmt'),comp_related=txt(g,'ReportableCompFromRltdOrgAmt'),grp=L(g)))
  rec['people']=P
  G=[]
  for g in F.iter('{*}RecipientTable'):
    G.append(dict(name=' '.join(filter(None,[txt(g.find('{*}RecipientBusinessName'),'BusinessNameLine1Txt') if g.find('{*}RecipientBusinessName') is not None else '',txt(g.find('{*}RecipientBusinessName'),'BusinessNameLine2Txt') if g.find('{*}RecipientBusinessName') is not None else ''])),
      ein=txt(g,'RecipientEIN','EINOfRecipient'),state=txt(g,'StateAbbreviationCd'),irc=txt(g,'IRCSectionDesc'),cash=txt(g,'CashGrantAmt'),noncash=txt(g,'NonCashAssistanceAmt'),purpose=txt(g,'PurposeOfGrantTxt'),src='schedI'))
  for g in F.iter('{*}GrantOrContributionPdDurYrGrp'):
    G.append(dict(name=txt(g,'RecipientBusinessName') or txt(g,'RecipientPersonNm'),ein='',state=txt(g,'StateAbbreviationCd'),irc=txt(g,'RecipientFoundationStatusTxt'),cash=txt(g,'Amt'),noncash='',purpose=txt(g,'GrantOrContributionPurposeTxt'),src='990PF'))
  rec['grants']=G
  C=F.find('.//{*}IRS990ScheduleC'); rec['schedC']=flat(C) if C is not None else {}
  rec['schedC_orgs']=[]
  if C is not None:
    for g in C.iter():
      if not isinstance(g.tag,str) or not len(g): continue
      if g.find('{*}EIN') is not None or g.find('.//{*}BusinessNameLine1Txt') is not None and L(g).endswith('Grp'):
        if any(L(c) in ('EIN','OrganizationBusinessName','BusinessName') for c in g): rec['schedC_orgs'].append(dict(grp=L(g),**flat(g)))
  R=F.find('.//{*}IRS990ScheduleR'); rel=[]
  if R is not None:
    for g in R:
      if not isinstance(g.tag,str): continue
      d=flat(g); name=next((v for k,v in d.items() if k.endswith('BusinessNameLine1Txt')),'')
      rel.append(dict(grp=L(g),name=name,ein=d.get('EIN',''),exempt=d.get('ExemptCodeSectionTxt',''),controlled=d.get('ControlledOrganizationInd',''),activity=d.get('PrimaryActivitiesTxt',''),
        txn_type=d.get('TransactionTypeTxt',''),amount=d.get('InvolvedAmt',''),direct_controlling=next((v for k,v in d.items() if k.startswith('DirectControllingEntityName')),'')))
  rec['related']=rel
  return rec
n=0; SIB={}
with open(OUT,'a') as o:
  for (y,b),rows in by.items():
    for attempt in range(3):
      try:
        z=remotezip.RemoteZip(f'https://apps.irs.gov/pub/epostcard/990/xml/{y}/{b}.zip'); names={os.path.basename(x).split('_')[0]:x for x in z.namelist()}; break
      except Exception as e: print('zip fail',b,e,flush=True); time.sleep(5); z=None
    if z is None: continue
    for r in rows:
      try:
        nm=names.get(r['object_id']); zz=z
        if not nm:
          # IRS index sometimes names batch ..._05A while the file sits in sibling ..._05B (seen 2026-11-22); probe siblings B..D
          for sfx in 'BCD':
            kk=f'{y}/{b[:-1]}{sfx}'
            if kk not in SIB:
              try:
                z2=remotezip.RemoteZip(f'https://apps.irs.gov/pub/epostcard/990/xml/{kk}.zip'); SIB[kk]=(z2,{os.path.basename(x).split('_')[0]:x for x in z2.namelist()})
              except Exception: SIB[kk]=None
            if SIB[kk] is None: break
            if r['object_id'] in SIB[kk][1]: zz,nm=SIB[kk][0],SIB[kk][1][r['object_id']]; break
        if not nm: o.write(json.dumps(dict(object_id=r['object_id'],ein=r['ein'],error='not_in_zip'))+'\n'); continue
        rec=parse(zread(zz,nm),r); rec['fetched_at']=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
        o.write(json.dumps(rec)+'\n'); o.flush(); n+=1
      except Exception as e:
        o.write(json.dumps(dict(object_id=r['object_id'],ein=r['ein'],error=repr(e)[:300]))+'\n'); o.flush()
    print(datetime.datetime.now().isoformat(timespec='seconds'),b,'done',n,flush=True)
print('DONE',n)
