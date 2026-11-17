import fecapi,json,os
R=[json.loads(l) for l in open('f3l_filings_raw.jsonl') if '_empty' not in l]
ids=sorted({r['committee_id'] for r in R})
out='f3l_committees.jsonl'
have={json.loads(l)['committee_id'] for l in open(out)} if os.path.exists(out) else set()
todo=[i for i in ids if i not in have]
for i in range(0,len(todo),50):
  b=todo[i:i+50]
  d=fecapi.get('/committees/',{'committee_id':b,'per_page':100})
  with open(out,'a') as f:
    for r in d['results']: f.write(json.dumps(r)+'\n')
  print(i,len(d['results']),fecapi.STATE['remaining'],flush=True)
print('ids',len(ids))
