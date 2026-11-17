import json,sys,time,urllib.request,urllib.parse,datetime,os
year,ftype=sys.argv[1],sys.argv[2]
fn=f'ld2_{year}_{ftype}.jsonl'; state=fn+'.next'
u=open(state).read().strip() if os.path.exists(state) else "https://lda.gov/api/v1/filings/?"+urllib.parse.urlencode({'filing_year':year,'filing_type':ftype,'page_size':25})
out=open(fn,'a')
while u:
  for i in range(8):
    try:
      d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'Accept':'application/json','User-Agent':'gop-lobby-graph research'}),timeout=60)); break
    except Exception as e:
      print('err',e,file=sys.stderr,flush=True); time.sleep(15*(i+1))
  else: sys.exit(1)
  now=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
  for r in d['results']:
    acts=[]
    for la in r['lobbying_activities']:
      acts.append({'issue':la['general_issue_code'],'ents':[g.get('name') for g in (la.get('government_entities') or [])],
                   'lob':[[l['lobbyist']['id'],l['lobbyist']['first_name'],l['lobbyist']['last_name'],l['covered_position']] for l in la['lobbyists']]})
    out.write(json.dumps({'f':now,'uuid':r['filing_uuid'],'y':r['filing_year'],'t':r['filing_type'],'rid':r['registrant']['id'],'rn':r['registrant']['name'],'cid':r['client']['id'],'cn':r['client']['name'],'inc':r['income'],'exp':r['expenses'],'acts':acts},separators=(',',':'))+'\n')
  out.flush(); u=d['next']; open(state,'w').write(u or '')
  time.sleep(0.3)
print('done',year,ftype,file=sys.stderr)
