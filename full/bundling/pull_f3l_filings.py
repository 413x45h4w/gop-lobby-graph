import fecapi,json,gzip,os
out='f3l_filings_raw.jsonl'
done=set()
if os.path.exists(out):
  for l in open(out): done.add((json.loads(l)['_cycle_q'],json.loads(l)['_page']))
for cyc in (2024,2026):
  page=1
  while True:
    if (cyc,page) in done: page+=1; continue
    d=fecapi.get('/filings/',{'form_type':'F3L','cycle':cyc,'per_page':100,'page':page,'sort':'receipt_date'})
    with open(out,'a') as f:
      for r in d['results']: r['_cycle_q']=cyc; r['_page']=page; f.write(json.dumps(r)+'\n')
      if not d['results']: f.write(json.dumps({'_cycle_q':cyc,'_page':page,'_empty':True})+'\n')
    print(cyc,page,d['pagination']['pages'],fecapi.STATE['remaining'],flush=True)
    if page>=d['pagination']['pages']: break
    page+=1
