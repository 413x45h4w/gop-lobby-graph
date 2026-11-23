# Scrape House Committee Repository event pages (docs.house.gov) -> raw/house_events.jsonl (resumable, append-only).
import re,html,json,os,sys,time,urllib.request,concurrent.futures as cf,datetime
OUT='raw/house_events.jsonl'; lo,hi=int(sys.argv[1]),int(sys.argv[2])
done=set()
if os.path.exists(OUT):
  for l in open(OUT): done.add(json.loads(l)['event_id'])
def clean(s): return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',s or ''))).strip()
def get(eid):
  u=f'https://docs.house.gov/Committee/Calendar/ByEvent.aspx?EventID={eid}'
  for a in range(3):
    try:
      t=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'research (gop-lobby-graph)'}),timeout=30).read().decode('utf-8','ignore'); break
    except Exception as e: time.sleep(3*(a+1)); t=None
  if t is None: return {'event_id':eid,'status':'error'}
  i=t.find('<div id="previewPanel"')
  if i<0: return {'event_id':eid,'status':'no_event'}
  p=t[i:]
  h1=re.search(r'<h1>(.*?)<small',p,re.S); kind_title=clean(h1.group(1)) if h1 else ''
  m=re.match(r'([A-Za-z \-]+):\s*(.*)',kind_title); kind,title=(m.group(1),m.group(2)) if m else ('',kind_title)
  com=re.search(r'<blockquote>\s*<p>(.*?)</p>',p,re.S); com=clean(com.group(1)) if com else ''
  dt=re.search(r'<p class="meetingTime">(.*?)</p>',p,re.S) or re.search(r'(\w+day, \w+ \d+, \d{4})',p)
  dts=clean(dt.group(1)) if dt else ''
  codes=sorted(set(re.findall(r'/meetings/([A-Z]{2})/([A-Z]{2}\d{2})/',p)))
  wits=[]
  for w in re.findall(r'<div class="witnessPanel">(.*?)</div>',p,re.S):
    n=re.search(r'<strong>(.*?)</strong>',w,re.S); s=re.search(r'<small[^>]*>(.*?)</small>',w,re.S)
    docs=re.findall(r'href="([^"]+\.pdf)"',w)
    wits.append({'name':clean(n.group(1)) if n else '','title_org':clean(s.group(1)) if s else '','n_docs':len(docs)})
  return {'event_id':eid,'status':'ok','kind':kind,'title':title,'committee_text':com,'date_text':dts,'repo_codes':[b for a,b in codes],'witnesses':wits,'fetched_at':datetime.datetime.now().astimezone().isoformat(timespec='seconds')}
todo=[e for e in range(lo,hi+1) if e not in done]
with open(OUT,'a') as f, cf.ThreadPoolExecutor(3) as ex:
  for k,r in enumerate(ex.map(get,todo)):
    f.write(json.dumps(r)+'\n'); f.flush()
    if k%200==0: print(k,len(todo),r['event_id'],r['status'],flush=True)
    time.sleep(0.1)
print('DONE')
