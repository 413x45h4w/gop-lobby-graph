# Stream Report of the Secretary of the Senate (GovInfo CDOC PDFs, parts 1 & 2); extract payroll lines
# (office header + staff 'LAST, FIRST' + title + amount). Temp PDF/text deleted after parsing; only extracted rows kept.
import re,sys,os,json,gzip,csv,subprocess,urllib.request,datetime,tempfile
urls=[l.strip() for l in open('raw/senate_secsen_urls.txt') if l.strip()]
LOG='raw/senate_pull_log.jsonl'
done=set(json.loads(l)['url'] for l in open(LOG) if json.loads(l).get('ok')) if os.path.exists(LOG) else set()
HDR=re.compile(r'^(\S.*?)\s{3,}DESCRIPTION\s{3,}NET FUNDS')
STAFF=re.compile(r"^\s{8,}([A-Z][A-Z'\-\.]*(?: [A-Z'\-\.]+)*, [A-Z][A-Z'\-\. ]*?)\s{3,}(\S.*?)\s{2,}\$?(-?[\d,]+\.\d\d)\s*$")
PER=re.compile(r'(\d\d/\d\d/\d{4}) THRU')
for u in urls:
  if u in done: continue
  t0=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
  fd,tmp=tempfile.mkstemp(suffix='.pdf',dir='/tmp'); os.close(fd)
  try:
    with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0 research'}),timeout=600) as r, open(tmp,'wb') as f:
      while True:
        b=r.read(1<<20)
        if not b: break
        f.write(b)
    p=subprocess.Popen(['pdftotext','-layout',tmp,'-'],stdout=subprocess.PIPE,text=True,errors='replace')
    office=None; period_end=None; n=0; rows=[]
    for line in p.stdout:
      m=HDR.match(line)
      if m: office=m.group(1).strip(); continue
      if period_end is None:
        mp=PER.search(line)
        if mp: pass
      if 'THRU' in line and period_end is None:
        mm=re.search(r'(\d\d/\d\d/\d{4})',line)
      ms=STAFF.match(line)
      if ms and office:
        rows.append([u.split('/')[-1],office,ms.group(1).strip(),re.sub(r'\s+',' ',ms.group(2).strip()),ms.group(3).replace(',','')]); n+=1
    p.wait(); os.remove(tmp)
    with gzip.open('raw/senate_payroll_rows.csv.gz','at',newline='') as g: csv.writer(g).writerows(rows)
    open(LOG,'a').write(json.dumps({'url':u,'pulled_at':t0,'ok':True,'staff_rows':n})+'\n'); print('ok',u,n,flush=True)
  except Exception as e:
    try: os.remove(tmp)
    except: pass
    open(LOG,'a').write(json.dumps({'url':u,'pulled_at':t0,'ok':False,'err':str(e)[:200]})+'\n'); print('ERR',u,e,flush=True)
