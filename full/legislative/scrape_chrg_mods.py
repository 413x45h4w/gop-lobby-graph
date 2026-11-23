# GovInfo CHRG (published hearing transcripts) MODS metadata for 118th/119th -> raw/chrg_mods.jsonl (resumable).
# Package list from public sitemaps https://www.govinfo.gov/sitemap/CHRG_<year>_sitemap.xml ; no API key needed.
import re,json,os,time,urllib.request,concurrent.futures as cf,datetime
import xml.etree.ElementTree as ET
OUT='raw/chrg_mods.jsonl'; NS='{http://www.loc.gov/mods/v3}'
pk=set()
for y in (2023,2024,2025,2026):
  t=urllib.request.urlopen(f'https://www.govinfo.gov/sitemap/CHRG_{y}_sitemap.xml',timeout=60).read().decode()
  pk|=set(re.findall(r'(CHRG-11[89][a-z]+\d+)',t))
done=set()
if os.path.exists(OUT):
  for l in open(OUT): done.add(json.loads(l)['package'])
def get(p):
  for a in range(3):
    try: x=urllib.request.urlopen(f'https://www.govinfo.gov/metadata/pkg/{p}/mods.xml',timeout=60).read(); break
    except Exception: time.sleep(5*(a+1)); x=None
  if x is None: return {'package':p,'status':'error'}
  r=ET.fromstring(x); ext=[e for e in r.iter(NS+'extension')]
  def all_(tag): return [ (e.text or '').strip() for e in r.iter(NS+tag) if e.text]
  coms=[{'id':c.get('authorityId'),'chamber':c.get('chamber'),'name':(c.find(NS+'name').text if c.find(NS+'name') is not None else '')} for c in r.iter(NS+'congCommittee')]
  mems=[{'bioguide':m.get('bioGuideId'),'role':m.get('role'),'party':m.get('party'),'state':m.get('state')} for m in r.iter(NS+'congMember')]
  wnames=[]
  for n in r.iter(NS+'name'):
    rt=[x.text for x in n.iter(NS+'roleTerm')]
    if 'witness' in rt:
      wnames.append({'namePart':' '.join((x.text or '').strip() for x in n.findall(NS+'namePart')),'affiliation':' '.join((x.text or '') for x in n.findall(NS+'affiliation'))})
  title=r.find(f'{NS}titleInfo/{NS}title')
  return {'package':p,'status':'ok','title':title.text if title is not None else '','chamber':(all_('chamber') or [''])[0],'congress':(all_('congress') or [''])[0],
    'held':sorted(set(all_('heldDate'))),'witness_text':all_('witness'),'witness_names':wnames,'committees':coms,'members':mems,
    'fetched_at':datetime.datetime.now().astimezone().isoformat(timespec='seconds')}
todo=sorted(pk-done); print('todo',len(todo),flush=True)
with open(OUT,'a') as f, cf.ThreadPoolExecutor(3) as ex:
  for k,r in enumerate(ex.map(get,todo)):
    f.write(json.dumps(r)+'\n'); f.flush()
    if k%200==0: print(k,r['package'],r['status'],flush=True)
print('DONE')
