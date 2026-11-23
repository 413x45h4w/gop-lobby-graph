# Pass 2 targets: (a) Schedule I / 990PF grantees of pass-1 orgs that are 501(c)(4)/(5)/(6) per IRS BMF with grants >= $100k;
# (b) organizations among the top super PAC donors (outside_money/superpac_top_donors.csv, itemized >= $1k rows) whose normalized name exactly equals a BMF 501(c)(3)-(6) org.
import csv,json,sys,collections,datetime,glob
sys.path.insert(0,'/workspace/gop-lobby-graph/full/boards/scripts'); from orgnorm import key
NOW=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
E={}; BMF=collections.defaultdict(list)
for fn in sorted(glob.glob('raw/eo[1-4].csv')):
  for r in csv.DictReader(open(fn,encoding='latin-1')):
    rr=dict(ein=r['EIN'],name=r['NAME'],sub=r['SUBSECTION'],state=r['STATE'],ntee=r['NTEE_CD'],rev=float(r['REVENUE_AMT'] or 0)); E[r['EIN']]=rr
    k=key(r['NAME'])
    if k: BMF[k].append(rr)
IDX=json.load(open('raw/latest_filing_by_ein.json'))
have={r['ein'] for r in csv.DictReader(open('targets_990.csv'))}
D={}
for l in open('raw/parsed_990.jsonl'):
  d=json.loads(l); D[d['object_id']]=d
T={}
def add(x,src,det):
  if x['ein'] in have or x['ein'] in T: 
    if x['ein'] in T: T[x['ein']]['selection_detail']+=' ; '+det
    return
  f=IDX.get(x['ein'])
  T[x['ein']]=dict(ein=x['ein'],bmf_name=x['name'],subsection='501(c)('+str(int(x['sub']))+')',state=x['state'],ntee=x['ntee'],bmf_revenue=int(x['rev']),selection_source=src,selection_detail=det,name_match_note='',
    object_id=f['OBJECT_ID'] if f else '',return_type=f['RETURN_TYPE'] if f else '',tax_period=f['TAX_PERIOD'] if f else '',xml_batch=f['XML_BATCH_ID'] if f else '',index_year=f['_y'] if f else '',computed_at=NOW)
for d in D.values():
  for g in d.get('grants',[]):
    e=(g.get('ein') or '').zfill(9) if g.get('ein') else ''
    try: a=float(g.get('cash') or 0)+float(g.get('noncash') or 0)
    except: a=0
    if e in E and E[e]['sub'] in ('04','05','06') and a>=100000: add(E[e],'pass2_grantee_c4c5c6',f"${int(a)} from {d['target_name']}")
for r in csv.DictReader(open('/workspace/gop-lobby-graph/full/outside_money/superpac_top_donors.csv')):
  c=[x for x in BMF.get(key(r['fec_contributor_name']),[]) if x['sub'] in ('03','04','05','06')]
  if c:
    c.sort(key=lambda x:-x['rev'])
    add(c[0],'pass2_superpac_org_donor',f"{r['fec_contributor_name']} -> {r['committee_name']} ${r['usd']} ({r['cycle']})"+('' if len(c)==1 else f' [{len(c)} BMF name matches; largest revenue picked]'))
R=list(T.values())
w=csv.DictWriter(open('targets_990_pass2.csv','w'),fieldnames=list(R[0])); w.writeheader(); w.writerows(R)
print(len(R),collections.Counter(r['selection_source'] for r in R),sum(1 for r in R if r['object_id']))
