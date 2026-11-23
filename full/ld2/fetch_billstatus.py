# GovInfo BILLSTATUS bulk (keyless) for the 118th & 119th Congress -> compact bill tables keyed like Congress.gov ids (hr1234-119).
# Temp zip deleted after parsing; per-zip pull log kept in bills/billstatus_pull_log.jsonl.
import zipfile,urllib.request,tempfile,os,json,csv,datetime,xml.etree.ElementTree as ET,sys
TYPES=['hr','s','hres','sres','hjres','sjres','hconres','sconres']
LOG='bills/billstatus_pull_log.jsonl'
done={(j['congress'],j['type']) for j in map(json.loads,open(LOG))} if os.path.exists(LOG) else set()
fb=open('bills/bills.csv','a',newline=''); wb=csv.writer(fb)
fc=open('bills/bill_committees.csv','a',newline=''); wc=csv.writer(fc)
fs=open('bills/bill_sponsors.csv','a',newline=''); ws=csv.writer(fs)
if os.path.getsize('bills/bills.csv')==0:
  wb.writerow(['bill_id','congress','bill_type','number','title','policy_area','introduced','latest_action_date','latest_action','origin_chamber','pulled_at'])
  wc.writerow(['bill_id','committee_code','committee_name','chamber','committee_type','activity','pulled_at'])
  ws.writerow(['bill_id','bioguide','role','name','party','state','pulled_at'])
def t(e,p):
  x=e.find(p); return (x.text or '').strip() if x is not None and x.text else ''
for cg in (118,119):
  for ty in TYPES:
    if (cg,ty) in done: continue
    u=f'https://www.govinfo.gov/bulkdata/BILLSTATUS/{cg}/{ty}/BILLSTATUS-{cg}-{ty}.zip'
    now=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
    fd,tmp=tempfile.mkstemp(suffix='.zip',dir='/tmp'); os.close(fd)
    with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0 research'}),timeout=600) as r, open(tmp,'wb') as f:
      while True:
        b=r.read(1<<20)
        if not b: break
        f.write(b)
    z=zipfile.ZipFile(tmp); n=0
    for nm in z.namelist():
      if not nm.endswith('.xml'): continue
      root=ET.fromstring(z.read(nm)); b=root.find('bill')
      if b is None: continue
      num=t(b,'number'); typ=(t(b,'type') or t(b,'billType')).lower(); bid=f'{typ}{num}-{cg}'
      la=b.find('latestAction')
      wb.writerow([bid,cg,typ,num,t(b,'title')[:300],t(b,'policyArea/name'),t(b,'introducedDate'),t(la,'actionDate') if la is not None else '',(t(la,'text') if la is not None else '')[:200],t(b,'originChamber'),now])
      for c in b.findall('committees/item'):
        acts='|'.join(sorted({t(a,'name') for a in c.findall('activities/item') if t(a,'name')}))
        wc.writerow([bid,t(c,'systemCode'),t(c,'name'),t(c,'chamber'),t(c,'type'),acts,now])
        for sc in c.findall('subcommittees/item'):
          wc.writerow([bid,t(sc,'systemCode'),t(c,'name')+' :: '+t(sc,'name'),t(c,'chamber'),'Subcommittee','|'.join(sorted({t(a,'name') for a in sc.findall('activities/item') if t(a,'name')})),now])
      for s in b.findall('sponsors/item'): ws.writerow([bid,t(s,'bioguideId'),'sponsor',t(s,'fullName'),t(s,'party'),t(s,'state'),now])
      for s in b.findall('cosponsors/item'): ws.writerow([bid,t(s,'bioguideId'),'cosponsor',t(s,'fullName'),t(s,'party'),t(s,'state'),now])
      n+=1
    os.remove(tmp); fb.flush(); fc.flush(); fs.flush()
    open(LOG,'a').write(json.dumps({'congress':cg,'type':ty,'url':u,'pulled_at':now,'bills':n})+'\n'); print(cg,ty,n,flush=True)
