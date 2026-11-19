# Fresh (2026-11-18) pull of every Form 3L filing, cycles 2024+2026, all committees; plus efile F3LN/F3LA since 2026-07-01 as a recency cross-check; plus all-time F3L for every current member committee.
import fecapi,json,os,datetime,csv
NOW=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
out='f3l_filings_raw_all.jsonl'
if not os.path.exists(out):
  with open(out,'w') as f:
    for cyc in (2024,2026):
      page=1
      while True:
        d=fecapi.get('/filings/',{'form_type':'F3L','cycle':cyc,'per_page':100,'page':page,'sort':'receipt_date'})
        for r in d['results']: r['_cycle_q']=cyc; r['_page']=page; r['_fetched']=NOW; f.write(json.dumps(r)+'\n')
        print(cyc,page,d['pagination']['pages'],d['pagination']['count'],fecapi.STATE['remaining'],flush=True)
        if page>=d['pagination']['pages']: break
        page+=1
eo='f3l_efile_raw_all.jsonl'
if not os.path.exists(eo):
  with open(eo,'w') as f:
    for ft in ('F3LN','F3LA'):
      page=1
      while True:
        d=fecapi.get('/efile/filings/',{'form_type':ft,'min_receipt_date':'2026-07-01','per_page':100,'page':page,'sort':'-receipt_date'})
        for r in d['results']: r['_fetched']=NOW; f.write(json.dumps(r)+'\n')
        print(ft,page,d['pagination']['pages'],fecapi.STATE['remaining'],flush=True)
        if page>=d['pagination']['pages']: break
        page+=1
ao='member_f3l_alltime.jsonl'
if not os.path.exists(ao):
  ids=[r['committee_id'] for r in csv.DictReader(open('member_committees_all.csv'))]
  with open(ao,'w') as f:
    for i in range(0,len(ids),50):
      page=1
      while True:
        d=fecapi.get('/filings/',{'committee_id':ids[i:i+50],'form_type':'F3L','per_page':100,'page':page})
        for r in d['results']: r['_fetched']=NOW; f.write(json.dumps(r)+'\n')
        if page>=d['pagination']['pages']: break
        page+=1
      print('alltime',i,fecapi.STATE['remaining'],flush=True)
