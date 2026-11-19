# OpenFEC committee detail (Form 1: treasurer, custodian of records, JFC participants) for (a) every JFC that received universe-lobbyist money and
# (b) every PAC whose FEC connected organisation is an LDA registrant in the universe. Also /committees/ list (designated agent) for every committee
# receiving universe-lobbyist money. Append-only cache; key read from file and redacted in api_calls.log.
import fecapi,json,os,csv,re,datetime
NOW=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
C={r['committee_id']:r for r in csv.DictReader(open('committees_classified.csv'))}
R=[r for r in csv.DictReader(open('lobbyist_to_pac_fec_rows.csv')) if not r['match_confidence'].startswith('low') and r['memo_cd']!='X']
ids=sorted({r['fec_committee_id'] for r in R})
P=list(csv.DictReader(open('../people_all.csv')))
nz=lambda s:re.sub(r'[^A-Z ]','',(s or '').upper()).strip()
regs={nz(x) for p in P for x in p['registrants'].split('; ')}
jfc=[i for i in ids if i in C and C[i]['committee_class']=='joint_fundraising_committee']
con=sorted(c for c,r in C.items() if r['connected_org'] and nz(r['connected_org']) in regs)
todo=list(dict.fromkeys(jfc+con))
cache='committee_detail_raw.jsonl'
have=set()
if os.path.exists(cache):
  for l in open(cache): have.add(json.loads(l)['_cid'])
with open(cache,'a') as f:
  for i,c in enumerate(todo):
    if c in have: continue
    try: d=fecapi.get(f'/committee/{c}/',{})
    except RuntimeError as e: f.write(json.dumps({'_cid':c,'_error':str(e)[:80],'_fetched':NOW})+'\n'); continue
    r=(d.get('results') or [{}])[0]; r['_cid']=c; r['_fetched']=NOW; f.write(json.dumps(r)+'\n'); f.flush()
    if i%50==0: print(i,len(todo),fecapi.STATE['remaining'],flush=True)
lc='committee_list_raw.jsonl'
if not os.path.exists(lc):
  with open(lc,'w') as f:
    for i in range(0,len(ids),100):
      d=fecapi.get('/committees/',{'committee_id':ids[i:i+100],'per_page':100})
      for r in d['results']: r['_fetched']=NOW; f.write(json.dumps(r)+'\n')
print('done detail',len(todo),'list',len(ids))
