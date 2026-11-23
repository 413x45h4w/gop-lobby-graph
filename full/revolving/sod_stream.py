# Stream House Statement of Disbursements DETAIL CSVs (2016Q1..latest); keep only PERSONNEL COMPENSATION (BOC 11) rows,
# aggregated per (office, staff name, title). Raw CSVs are NOT kept (each ~30MB); a per-file pull log records URL, pull time, rows.
import csv,sys,io,urllib.request,json,datetime,gzip,re,os,collections
urls=[l.strip() for l in open('raw/sod_urls.txt') if l.strip()]
done=set(json.loads(l)['url'] for l in open('raw/sod_pull_log.jsonl')) if os.path.exists('raw/sod_pull_log.jsonl') else set()
def col(h,*keys):
  for k in keys:
    for i,x in enumerate(h):
      if x.strip().upper()==k: return i
  for k in keys:
    for i,x in enumerate(h):
      if k in x.strip().upper(): return i
  return None
for u in urls:
  if u in done: continue
  t0=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
  try:
    resp=urllib.request.urlopen(urllib.request.Request('https://www.house.gov'+u,headers={'User-Agent':'Mozilla/5.0 research'}),timeout=300)
    txt=io.TextIOWrapper(resp,encoding='latin-1',newline='')
    r=csv.reader(txt); h=next(r)
    iO=col(h,'ORGANIZATION','OFFICE'); iC=col(h,'BUDGET OBJECT CLASS','CATEGORY'); iS=col(h,'SORT SUBTOTAL DESCRIPTION','CATEGORY')
    iV=col(h,'VENDOR NAME','PAYEE'); iD=col(h,'DESCRIPTION','PURPOSE'); iA=col(h,'AMOUNT'); iPS=col(h,'PERFORM START DT','START DATE'); iPE=col(h,'PERFORM END DT','END DATE')
    agg=collections.defaultdict(lambda:[None,None,0.0,0]); n=0
    for x in r:
      n+=1
      if len(x)<=max(i for i in (iO,iV,iA) if i is not None): continue
      sub=(x[iS] if iS is not None else '').upper(); boc=(x[iC] if iC is not None else '').strip()
      if not (boc=='11' or 'PERSONNEL COMP' in sub): continue
      k=(x[iO].strip(),x[iV].strip(),x[iD].strip() if iD is not None else '')
      a=agg[k]; s=x[iPS].strip() if iPS is not None else ''; e=x[iPE].strip() if iPE is not None else ''
      a[0]=s if a[0] is None else a[0]; a[1]=e or a[1]
      try: a[2]+=float(re.sub(r'[^0-9.\-]','',x[iA]) or 0)
      except: pass
      a[3]+=1
    with gzip.open('raw/sod_personnel_rows.csv.gz','at',newline='') as f:
      w=csv.writer(f)
      for (o,v,d),(s,e,amt,c) in agg.items(): w.writerow([u.split('/')[-1],o,v,d,s,e,round(amt,2),c])
    open('raw/sod_pull_log.jsonl','a').write(json.dumps({'url':u,'pulled_at':t0,'rows_total':n,'personnel_aggregates':len(agg),'header':h})+'\n')
    print('ok',u,n,len(agg),flush=True)
  except Exception as ex:
    print('ERR',u,ex,flush=True)
