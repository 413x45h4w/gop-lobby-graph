# OpenFEC helper: key read from file, never printed; redacts key from any URL saved.
import json,time,urllib.request,urllib.parse,os,sys
KEY=open('/home/box/secrets/fec_api_key').read().strip()
BASE='https://api.open.fec.gov/v1'
STATE={'remaining':None,'limit':None,'calls':0}
LOG=os.path.join(os.path.dirname(__file__),'api_calls.log')
def redact(u): return u.replace(KEY,'REDACTED')
def get(path,params=None,tries=8):
  p=dict(params or {}); p['api_key']=KEY
  url=BASE+path+'?'+urllib.parse.urlencode(p,doseq=True)
  back=5
  for t in range(tries):
    try:
      req=urllib.request.Request(url,headers={'User-Agent':'research'})
      with urllib.request.urlopen(req,timeout=90) as r:
        h=r.headers; STATE['remaining']=h.get('x-ratelimit-remaining'); STATE['limit']=h.get('x-ratelimit-limit'); STATE['calls']+=1
        d=json.load(r)
      with open(LOG,'a') as f: f.write(f"{__import__('datetime').datetime.now().astimezone().isoformat(timespec='seconds')}\t200\t{STATE['remaining']}\t{redact(url)}\n")
      try:
        if STATE['remaining'] is not None and int(STATE['remaining'])<3: time.sleep(30)
      except: pass
      return d
    except urllib.error.HTTPError as e:
      with open(LOG,'a') as f: f.write(f"{__import__('datetime').datetime.now().astimezone().isoformat(timespec='seconds')}\t{e.code}\t-\t{redact(url)}\n")
      if e.code in (429,500,502,503,504): time.sleep(back); back=min(back*2,300); continue
      raise RuntimeError(f'HTTP {e.code} {redact(url)}')
    except Exception as e:
      time.sleep(back); back=min(back*2,300)
  raise RuntimeError('failed '+redact(url))
