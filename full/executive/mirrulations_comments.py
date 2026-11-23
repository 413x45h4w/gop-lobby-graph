# regulations.gov public comments via the public Mirrulations S3 mirror (s3://mirrulations, AWS Open Data; Moravian University),
# scoped to rulemaking dockets opened 2025-2026 whose RIN also appears in an OIRA EO 12866 meeting (2025-2026). Per-docket cap on comments fetched.
# Writes raw/regs_dockets.jsonl and raw/regs_comments.jsonl (organization, name fields, category, posted date). Resumable.
import json,os,re,urllib.request,urllib.parse,concurrent.futures as cf,datetime,collections,sys
B='https://mirrulations.s3.amazonaws.com/'; CAP=int(sys.argv[1]) if len(sys.argv)>1 else 1500
def get(u,tries=3):
  for a in range(tries):
    try: return urllib.request.urlopen(u,timeout=60).read()
    except Exception as e: err=e
  return None
def ls(prefix,delim=True):
  out=[];tok=None
  while True:
    q={'list-type':'2','prefix':prefix,'max-keys':'1000'}
    if delim: q['delimiter']='/'
    if tok: q['continuation-token']=tok
    t=get(B+'?'+urllib.parse.urlencode(q)).decode()
    out+=re.findall(r'<Prefix>([^<]+)</Prefix>',t)[1:] if delim else re.findall(r'<Key>([^<]+)</Key>',t)
    m=re.search(r'<NextContinuationToken>([^<]+)</NextContinuationToken>',t)
    if not m: return out
    tok=m.group(1)
O=[json.loads(l) for l in open('raw/oira_meetings.jsonl')]
rins={o['rin'] for o in O if o.get('list_date','')>='2025-01-01' and o.get('rin')}
ags=collections.Counter()
for o in O:
  if o.get('list_date','')>='2025-01-01':
    a=(o.get('agency') or '').split('-',1)[-1]
    for x in a.split('/'): ags[x]+=1
top=set(ags)
existing={p.split('/')[1] for p in ls('raw-data/')}
agencies=sorted(a for a in top if a in existing)
print('rins',len(rins),'agencies',agencies,flush=True)
DK='raw/regs_dockets.jsonl'; CM='raw/regs_comments.jsonl'
seen_d={json.loads(l)['docket'] for l in open(DK)} if os.path.exists(DK) else set()
seen_c={json.loads(l)['id'] for l in open(CM)} if os.path.exists(CM) else set()
def dk(p):
  d=p.rstrip('/').split('/')[-1]
  j=get(f'{B}{p}text-{d}/docket/{d}.json')
  if not j: return {'docket':d,'status':'no_docket_json'}
  a=json.loads(j)['data']['attributes']
  return {'docket':d,'status':'ok','rin':a.get('rin'),'title':(a.get('title') or '')[:300],'type':a.get('docketType'),'agency':a.get('agencyId'),'modified':a.get('modifyDate'),'prefix':p}
with open(DK,'a') as f, cf.ThreadPoolExecutor(16) as ex:
  for ag in agencies:
    ps=[p for p in ls(f'raw-data/{ag}/') if re.search(r'-(2025|2026)-',p) and p.rstrip('/').split('/')[-1] not in seen_d]
    for r in ex.map(dk,ps): f.write(json.dumps(r)+'\n'); seen_d.add(r['docket'])
    print(ag,len(ps),'dockets scanned',flush=True)
D=[json.loads(l) for l in open(DK)]
tgt=[d for d in D if d.get('status')=='ok' and d.get('rin') in rins]
print('target dockets',len(tgt),flush=True)
def cm(k):
  j=get(B+k)
  if not j: return None
  a=json.loads(j)['data']; at=a['attributes']
  return {'id':a['id'],'docket':at.get('docketId'),'organization':at.get('organization'),'first':at.get('firstName'),'last':at.get('lastName'),'category':at.get('category'),'gov_agency':at.get('govAgency'),'posted':at.get('postedDate'),'title':(at.get('title') or '')[:200],'comment_on':at.get('commentOnDocumentId')}
with open(CM,'a') as f, cf.ThreadPoolExecutor(24) as ex:
  for d in tgt:
    keys=[k for k in ls(f"{d['prefix']}text-{d['docket']}/comments/",delim=False) if k.endswith('.json')]
    todo=[k for k in keys[:CAP] if k.rsplit('/',1)[1][:-5] not in seen_c]
    n=0
    for r in ex.map(cm,todo):
      if r: r['docket_n_comments_in_mirror']=len(keys); f.write(json.dumps(r)+'\n'); n+=1
    print(d['docket'],d['rin'],len(keys),'fetched',n,flush=True)
print('DONE')
