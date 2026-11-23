# Senate eFD (efdsearch.senate.gov) public reports: PTRs (type 11) and annual reports (type 7), filed 2023-01-01..now.
# Access: the site's public-records notice (statutory prohibition on commercial/credit/solicitation use) is acknowledged, as every visitor must;
# use here is non-commercial research. Electronic reports are HTML tables -> raw/senate_efd_reports.jsonl (resumable). Paper filings recorded only.
import requests,re,html,json,os,time,datetime
OUT='raw/senate_efd_reports.jsonl'; done=set()
if os.path.exists(OUT):
  for l in open(OUT): done.add(json.loads(l)['report_id'])
B='https://efdsearch.senate.gov'
s=requests.Session(); s.headers['User-Agent']='Mozilla/5.0 (research; gop-lobby-graph)'
def login():
  r=s.get(B+'/search/home/'); tok=re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"',r.text).group(1)
  s.post(B+'/search/home/',data={'csrfmiddlewaretoken':tok,'prohibition_agreement':'1'},headers={'Referer':B+'/search/home/'})
login()
def lst(rt):
  out=[];start=0
  while True:
    d={'start':str(start),'length':'100','report_types':f'[{rt}]','filer_types':'[1]','submitted_start_date':'01/01/2023 00:00:00','submitted_end_date':'','candidate_state':'','senator_state':'','office_id':'','first_name':'','last_name':''}
    j=s.post(B+'/search/report/data/',data=d,headers={'X-CSRFToken':s.cookies.get('csrftoken'),'Referer':B+'/search/'}).json()
    out+=j['data']; start+=100
    if start>=j['recordsTotal']: break
    time.sleep(0.5)
  return out
def clean(x): return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',x))).strip()
def tables(t):
  res=[]
  for m in re.finditer(r'<h3[^>]*>(.*?)</h3>|<table.*?</table>',t,re.S):
    if m.group(1) is not None: res.append({'section':clean(m.group(1)),'rows':[]}); continue
    rows=[[clean(c) for c in re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>',tr,re.S)] for tr in re.findall(r'<tr.*?</tr>',m.group(0),re.S)]
    if not res: res.append({'section':'','rows':[]})
    res[-1]['rows']+=rows
  return [x for x in res if x['rows']]
f=open(OUT,'a'); n=0
for rt,name in ((11,'ptr'),(7,'annual')):
  L=lst(rt); print(name,len(L),flush=True)
  for first,last,filer,link,date in L:
    href=re.search(r'href="([^"]+)"',link).group(1); rid=href.strip('/').split('/')[-1]
    if rid in done: continue
    rec={'report_id':rid,'kind':name,'first':first,'last':last,'filer':filer,'title':clean(link),'filed':date,'url':B+href}
    if '/paper/' in href: rec['status']='paper_not_parsed'
    else:
      for a in range(3):
        r=s.get(B+href)
        if 'prohibition_agreement' in r.text: login(); continue
        break
      rec['tables']=tables(r.text); rec['status']='ok' if rec['tables'] else 'no_tables'
      time.sleep(0.6)
    rec['fetched_at']=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
    f.write(json.dumps(rec)+'\n'); f.flush(); done.add(rid); n+=1
    if n%50==0: print(n,name,rec['status'],flush=True)
print('DONE',n)
