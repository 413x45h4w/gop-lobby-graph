# Select 990 filers to parse. Sources: (1) curated list (scripts/curated_orgs.txt), (2) LDA clients+registrants (top 3000 clients by 2023-26 LDA spend)
# whose normalized name exactly equals an IRS EO BMF organization with subsection 03/04/05/06 (c3 charities, c4 social welfare, c5 labor, c6 trade assns),
# (3) (later passes) org donors to super PACs and Schedule I grantees. Latest e-filed 990/990EZ/990PF from IRS TEOS indexes 2024-2026.
import csv,sys,collections,json,datetime,glob
sys.path.insert(0,'/workspace/gop-lobby-graph/full/boards/scripts'); from orgnorm import key
NOW=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
BMF=collections.defaultdict(list); E={}
for fn in sorted(glob.glob('raw/eo[1-4].csv')):
  for r in csv.DictReader(open(fn,encoding='latin-1')):
    rr=dict(ein=r['EIN'],name=r['NAME'],sub=r['SUBSECTION'],state=r['STATE'],ntee=r['NTEE_CD'],rev=float(r['REVENUE_AMT'] or 0),assets=float(r['ASSET_AMT'] or 0))
    E[r['EIN']]=rr; k=key(r['NAME'])
    if k: BMF[k].append(rr)
IDX={}
for y in ('2024','2025','2026'):
  for r in csv.DictReader(open(f'raw/index_{y}.csv',encoding='latin-1')):
    if r['RETURN_TYPE'] not in ('990','990EZ','990PF') or not r.get('XML_BATCH_ID'): continue
    e=r['EIN'].zfill(9); cur=IDX.get(e)
    if cur is None or (r['TAX_PERIOD'],r['OBJECT_ID'])>(cur['TAX_PERIOD'],cur['OBJECT_ID']): r['_y']=y; IDX[e]=r
json.dump({e:{k:r[k] for k in ('TAX_PERIOD','RETURN_TYPE','OBJECT_ID','XML_BATCH_ID','TAXPAYER_NAME','_y')} for e,r in IDX.items()},open('raw/latest_filing_by_ein.json','w'))
T={}
def pick(k,hint,src,extra):
  c=[x for x in BMF.get(k,[]) if x['sub'] in ('03','04','05','06')]
  if not c: return None
  c.sort(key=lambda x:(-(x['state']==hint), -x['rev']))
  amb='' if len(c)==1 else f'{len(c)} BMF orgs share normalized name; picked state-hint/largest revenue'
  x=c[0]
  if x['ein'] not in T: T[x['ein']]=dict(ein=x['ein'],bmf_name=x['name'],subsection='501(c)('+str(int(x['sub']))+')',state=x['state'],ntee=x['ntee'],bmf_revenue=int(x['rev']),selection_source=src,selection_detail=extra,name_match_note=amb)
  else: T[x['ein']]['selection_source']+='|'+src
  return x
miss=[]
for l in open('scripts/curated_orgs.txt'):
  if l.startswith('#') or not l.strip(): continue
  n,h=(l.strip().split('|')+[''])[:2]
  if not pick(key(n),h,'curated',n): miss.append(n)
for r in csv.DictReader(open('/workspace/gop-lobby-graph/full/boards/lda_clients_spend_2023_26.csv')):
  if int(r['rank'])>3000: break
  pick(r['client_key'],'DC','lda_top3000_client',f"rank {r['rank']} {r['client_name']} ${r['lda_spend_2023_26']}")
for e,t in T.items():
  f=IDX.get(e); t.update(object_id=f['OBJECT_ID'] if f else '',return_type=f['RETURN_TYPE'] if f else '',tax_period=f['TAX_PERIOD'] if f else '',xml_batch=f['XML_BATCH_ID'] if f else '',index_year=f['_y'] if f else '',computed_at=NOW)
R=list(T.values())
w=csv.DictWriter(open('targets_990.csv','w'),fieldnames=list(R[0])); w.writeheader(); w.writerows(R)
open('targets_curated_unresolved.txt','w').write('\n'.join(miss)+'\n')
print(len(R),'targets;',sum(1 for r in R if r['object_id']),'with e-file;',collections.Counter(r['subsection'] for r in R),'curated unresolved',len(miss),miss)
