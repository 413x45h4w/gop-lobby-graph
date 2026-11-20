# Shared helpers: parse a write_to_file X result, append-only call log + raw store.
import json,re,csv,os,datetime,hashlib
BASE='/workspace/gop-lobby-graph/full/x_all/'
CALLS=BASE+'x_calls_all.csv'
HDR=['call_seq','logged_at_ET','tool','request_id','request_summary','result_count','next_token','errors_n','reads_left_minute','reads_left_today','minute_reset_utc','raw_file','note']
def now(): return datetime.datetime.now().astimezone().isoformat(timespec='seconds')
def parse(path):
  t=open(path).read()
  m0=re.search(r'Full text: (/\S+?\.txt)',t)
  if m0 and os.path.exists(m0.group(1)): t=open(m0.group(1)).read()
  m=re.search(r'X reads left for this user: (\d+) of \d+ this minute \(resets at ([^)]+)\), (\d+) of \d+ today',t)
  try: j=json.JSONDecoder().raw_decode(t[t.find('{'):])[0]
  except Exception: j={'_unparsed':t[:3000]}
  return j,(int(m.group(1)) if m else None),(m.group(2) if m else ''),(int(m.group(3)) if m else None),t
def log_call(tool,req_id,summary,j,rlm,reset,rlt,note=''):
  new=not os.path.exists(CALLS)
  n=0 if new else sum(1 for _ in open(CALLS))-1
  day=datetime.datetime.now().strftime('%Y%m%d')
  raw=f'raw/x_raw_{day}.jsonl'
  with open(BASE+raw,'a') as f: f.write(json.dumps({'logged_at':now(),'tool':tool,'request_id':req_id,'request':summary,'response':j})+'\n')
  with open(CALLS,'a',newline='') as f:
    w=csv.writer(f)
    if new: w.writerow(HDR)
    w.writerow([n+1,now(),tool,req_id,summary[:1100],len(j.get('data',[]) or []),(j.get('meta') or {}).get('next_token',''),len(j.get('errors',[]) or []),rlm,rlt,reset,raw,note])
  return n+1
