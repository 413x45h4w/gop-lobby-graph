# Download each FARA Supplemental Statement (date stamped 2023-01-01+), extract text with pdftotext -layout,
# keep only gzipped text (raw/ss_text/<docname>.txt.gz); the temporary PDF is removed after extraction.
import zipfile,csv,io,os,sys,subprocess,urllib.request,json,datetime,gzip,tempfile,time
from concurrent.futures import ThreadPoolExecutor
zf=zipfile.ZipFile('raw/FARA_All_RegistrantDocs.csv.zip'); rows=list(csv.DictReader(io.TextIOWrapper(zf.open(zf.namelist()[0]),encoding='latin-1')))
todo=[]
for x in rows:
  if x['Document Type']!='Supplemental Statement': continue
  m,d,y=x['Date Stamped'].split('/')
  if not y.isdigit() or int(y)<2023: continue
  todo.append(x)
print('docs',len(todo),file=sys.stderr,flush=True)
LOG='raw/ss_fetch_log.jsonl'
done=set()
if os.path.exists(LOG):
  for l in open(LOG):
    j=json.loads(l)
    if j.get('ok'): done.add(j['url'])
def work(x):
  u=x['URL']
  if u in done: return
  name=u.split('/')[-1][:-4]; out=f'raw/ss_text/{name}.txt.gz'
  t0=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
  rec={'url':u,'reg':x['Registration Number'],'registrant':x['Registrant Name'],'date_stamped':x['Date Stamped'],'pulled_at':t0}
  for i in range(4):
    try:
      fd,tmp=tempfile.mkstemp(suffix='.pdf',dir='/tmp'); os.close(fd)
      with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0 research'}),timeout=180) as r, open(tmp,'wb') as f:
        while True:
          b=r.read(1<<20)
          if not b: break
          f.write(b)
      rec['pdf_bytes']=os.path.getsize(tmp)
      txt=subprocess.run(['pdftotext','-layout',tmp,'-'],capture_output=True,timeout=300).stdout.decode('utf-8','replace')
      os.remove(tmp)
      with gzip.open(out,'wt') as g: g.write(txt)
      rec.update(ok=True,text_chars=len(txt)); break
    except Exception as e:
      rec.update(ok=False,err=str(e)[:200])
      try: os.remove(tmp)
      except: pass
      time.sleep(10*(i+1))
  with open(LOG,'a') as f: f.write(json.dumps(rec)+'\n')
with ThreadPoolExecutor(4) as ex: list(ex.map(work,todo))
print('done',file=sys.stderr)
