# House periodic transaction reports (STOCK Act) 2023-2026: index from disclosures-clerk.house.gov/public_disc/financial-pdfs/<yr>FD.zip,
# electronic PTR PDFs (DocID 2xxxxxxx) parsed with pdftotext -layout; scanned/paper PTRs recorded as not parsed. Resumable.
import re,os,json,subprocess,urllib.request,time,concurrent.futures as cf,datetime
T='/workspace/tmp_dcgraph/hfd'; OUT='raw/house_ptr_transactions.jsonl'; DOCS='raw/house_ptr_docs.jsonl'
done=set()
if os.path.exists(DOCS):
  for l in open(DOCS): done.add(json.loads(l)['doc_id'])
idx=[]
for y in (2023,2024,2025,2026):
  t=open(f'{T}/{y}FD.xml').read()
  for m in re.finditer(r'<Member>(.*?)</Member>',t,re.S):
    g=lambda k: (re.search(f'<{k}>(.*?)</{k}>',m.group(1),re.S) or [None,''])[1] if re.search(f'<{k}>(.*?)</{k}>',m.group(1),re.S) else ''
    if g('FilingType')!='P': continue
    idx.append({'doc_id':g('DocID'),'year':g('Year'),'last':g('Last'),'first':g('First'),'state_dst':g('StateDst'),'filing_date':g('FilingDate')})
TX=re.compile(r'^(?P<pre>.*?)\s{2,}(?P<type>P|S|S \(partial\)|E)\s+(?P<td>\d\d/\d\d/\d{4})\s+(?P<nd>\d\d/\d\d/\d{4})\s+(?P<amt>(?:\$[\d,]+(?:\s*-\s*(?:\$[\d,]+)?)?|Over \$[\d,]+|Spouse/DC Over \$1,000,000))(?P<rest>.*)$')
def parse(txt):
  L=txt.split('\n'); out=[]
  for i,l in enumerate(L):
    m=TX.match(l)
    if not m: continue
    pre=m.group('pre').strip(); owner=''
    mo=re.match(r'^(SP|JT|DC)\s+(.*)',pre)
    if mo: owner,pre=mo.group(1),mo.group(2)
    asset=pre; amt=m.group('amt').strip()
    for j in range(i+1,min(i+4,len(L))):
      nx=L[j].strip()
      if not nx or re.match(r'^(F\s+S|S\s+O|D\s+:|C\s*:|ID\s+Owner)',nx) or TX.match(L[j]): break
      parts=re.split(r'\s{3,}',nx)
      asset+=' '+parts[0]
      if amt.endswith('-') and re.search(r'\$[\d,]+\s*$',nx): amt+=' '+re.search(r'(\$[\d,]+)\s*$',nx).group(1)
    tk=re.findall(r'\(([A-Z][A-Z0-9.\-/]{0,7})\)',asset); at=re.findall(r'\[([A-Z]{2})\]',asset)
    out.append({'owner':owner,'asset':re.sub(r'\s+',' ',asset).strip(),'ticker':tk[-1] if tk else '','asset_type':at[-1] if at else '','tx_type':m.group('type'),'tx_date':m.group('td'),'notification_date':m.group('nd'),'amount':re.sub(r'\s+',' ',amt)})
  return out
def work(d):
  if not d['doc_id'].startswith('2'): return d,[], 'not_electronic'
  u=f"https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/{d['year']}/{d['doc_id']}.pdf"
  for a in range(3):
    try:
      b=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0 research'}),timeout=60).read(); break
    except Exception: time.sleep(4); b=None
  if not b or not b.startswith(b'%PDF'): return d,[],'fetch_failed'
  txt=subprocess.run(['pdftotext','-layout','-','-'],input=b,capture_output=True).stdout.decode('utf-8','ignore')
  tx=parse(txt); return d,tx,('ok' if tx else 'no_rows_parsed')
todo=[d for d in idx if d['doc_id'] not in done]; print('todo',len(todo),flush=True)
with open(OUT,'a') as fo, open(DOCS,'a') as fd, cf.ThreadPoolExecutor(3) as ex:
  for k,(d,tx,st) in enumerate(ex.map(work,todo)):
    now=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
    for t in tx: t.update({'doc_id':d['doc_id'],'filer_last':d['last'],'filer_first':d['first'],'state_dst':d['state_dst'],'filing_date':d['filing_date']}); fo.write(json.dumps(t)+'\n')
    d.update({'status':st,'n_tx':len(tx),'fetched_at':now}); fd.write(json.dumps(d)+'\n'); fo.flush(); fd.flush()
    if k%100==0: print(k,d['doc_id'],st,len(tx),flush=True)
print('DONE')
