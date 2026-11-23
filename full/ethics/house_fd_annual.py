# House annual financial disclosure (FilingType O = member original annual) electronic PDFs, filing years 2024+2025 (calendar 2023, 2024):
# Schedule A assets (value range), Schedule G gifts, Schedule H travel reimbursements, located by their column headers in pdftotext -layout output.
import re,os,json,subprocess,urllib.request,time,concurrent.futures as cf,datetime
T='/workspace/tmp_dcgraph/hfd'; OUT='raw/house_fd_annual_items.jsonl'; DOCS='raw/house_fd_annual_docs.jsonl'
done={json.loads(l)['doc_id'] for l in open(DOCS)} if os.path.exists(DOCS) else set()
idx=[]
for y in (2024,2025):
  t=open(f'{T}/{y}FD.xml').read()
  for m in re.finditer(r'<Member>(.*?)</Member>',t,re.S):
    g=lambda k: (re.search(f'<{k}>(.*?)</{k}>',m.group(1),re.S).group(1) if re.search(f'<{k}>(.*?)</{k}>',m.group(1),re.S) else '')
    if g('FilingType')=='O': idx.append({'doc_id':g('DocID'),'year':g('Year'),'last':g('Last'),'first':g('First'),'state_dst':g('StateDst'),'filing_date':g('FilingDate')})
VAL=re.compile(r'(\$[\d,]+\s*-\s*\$[\d,]+|Over \$[\d,]+|Spouse/DC Over \$1,000,000|None|Undetermined)')
def parse(txt):
  L=txt.split('\n'); sec=None; out=[]
  for i,l in enumerate(L):
    s=l.strip()
    if re.match(r'^Asset\s+Owner\s+Value of Asset',s): sec='A'; continue
    if re.match(r'^Asset\s+Owner\s+Date\s+Tx',s) or re.match(r'^Source\s+Type\s+Amount',s) or re.match(r'^Creditor',s) or re.match(r'^Position\s+Name',s) or re.match(r'^Date\s+Parties',s): sec=None; continue
    if re.match(r'^Source\s+Description\s+Value',s): sec='G'; continue
    if re.match(r'^Source\s+Start Date\s+End Date',s): sec='H'; continue
    if sec=='A':
      m=re.search(r'\[([A-Z]{2})\]',l)
      if not m: continue
      asset=l[:m.start()].strip(); v=VAL.search(l[m.end():])
      if not v:
        for j in (i-1,i-2):
          if j>=0 and VAL.search(L[j]): v=VAL.search(L[j]); break
      if len(asset)<3 and i>0: asset=(L[i-1].split('⇒')[-1].strip()+' '+asset).strip()
      out.append({'sched':'A','asset':asset,'asset_code':m.group(1),'value':v.group(1) if v else ''})
    elif sec in ('G','H'):
      if not s or s.startswith('Source') or s.startswith('Comments') or s.startswith('*'): continue
      parts=re.split(r'\s{2,}',s)
      if len(parts)>=3: out.append({'sched':sec,'cols':parts})
  return out
def work(d):
  if not d['doc_id'].startswith('1'): return d,[],'not_electronic'
  u=f"https://disclosures-clerk.house.gov/public_disc/financial-pdfs/{d['year']}/{d['doc_id']}.pdf"
  b=None
  for a in range(3):
    try: b=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0 research'}),timeout=90).read(); break
    except Exception: time.sleep(4)
  if not b or not b.startswith(b'%PDF'): return d,[],'fetch_failed'
  txt=subprocess.run(['pdftotext','-layout','-','-'],input=b,capture_output=True).stdout.decode('utf-8','ignore')
  it=parse(txt); return d,it,('ok' if it else 'no_items_parsed')
todo=[d for d in idx if d['doc_id'] not in done]; print('todo',len(todo),flush=True)
with open(OUT,'a') as fo, open(DOCS,'a') as fd, cf.ThreadPoolExecutor(3) as ex:
  for k,(d,it,st) in enumerate(ex.map(work,todo)):
    for x in it: x.update({'doc_id':d['doc_id'],'filer_last':d['last'],'filer_first':d['first'],'state_dst':d['state_dst'],'filing_year':d['year']}); fo.write(json.dumps(x)+'\n')
    d.update({'status':st,'n_items':len(it),'fetched_at':datetime.datetime.now().astimezone().isoformat(timespec='seconds')}); fd.write(json.dumps(d)+'\n'); fo.flush(); fd.flush()
    if k%100==0: print(k,d['doc_id'],st,len(it),flush=True)
print('DONE')
