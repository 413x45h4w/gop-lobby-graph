# Find Senate foreign-travel expenditure granules in the Congressional Record (GovInfo CREC MODS, 2023-2026; public, no key).
import re,json,os,urllib.request,concurrent.futures as cf
OUT='raw/crec_foreign_travel_granules.jsonl'; done=set()
if os.path.exists(OUT):
  for l in open(OUT): done.add(json.loads(l)['package'])
pk=[]
for y in (2023,2024,2025,2026):
  t=urllib.request.urlopen(f'https://www.govinfo.gov/sitemap/CREC_{y}_sitemap.xml',timeout=60).read().decode()
  pk+=sorted(set(re.findall(r'(CREC-\d{4}-\d\d-\d\d)',t)))
def scan(p):
  for a in range(3):
    try: x=urllib.request.urlopen(f'https://www.govinfo.gov/metadata/pkg/{p}/mods.xml',timeout=120).read().decode('utf-8','ignore'); break
    except Exception: x=None
  if x is None: return {'package':p,'status':'error','hits':[]}
  hits=[]
  for m in re.finditer(r'<relatedItem[^>]*ID="id-(CREC-[^"]+)"[^>]*>(.*?)</relatedItem>',x,re.S):
    t=re.search(r'<title>(.*?)</title>',m.group(2),re.S)
    if t and re.search(r'FOREIGN CURRENC|OFFICIAL FOREIGN TRAVEL|FOREIGN TRAVEL',t.group(1),re.I):
      ch=re.search(r'<chamber>(.*?)</chamber>',m.group(2)); hits.append({'granule':m.group(1),'title':t.group(1),'chamber':ch.group(1) if ch else ''})
  return {'package':p,'status':'ok','hits':hits}
with open(OUT,'a') as f, cf.ThreadPoolExecutor(4) as ex:
  for r in ex.map(scan,[p for p in pk if p not in done]): f.write(json.dumps(r)+'\n'); f.flush()
print('DONE')
