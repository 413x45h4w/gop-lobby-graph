import json,sys,time,urllib.request,urllib.parse,datetime,os
year,per=sys.argv[1],sys.argv[2]
fn=f'ld203_{year}_{per}.jsonl'; state=fn+'.next'
u=open(state).read().strip() if os.path.exists(state) else "https://lda.gov/api/v1/contributions/?"+urllib.parse.urlencode({'filing_year':year,'filing_period':per,'page_size':25})
out=open(fn,'a')
while u:
  for i in range(8):
    try: d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'Accept':'application/json'}),timeout=60)); break
    except Exception as e: print('err',e,file=sys.stderr,flush=True); time.sleep(15*(i+1))
  else: sys.exit(1)
  now=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
  for r in d['results']:
    lb=r.get('lobbyist') or {}; rg=r.get('registrant') or {}
    out.write(json.dumps({'f':now,'uuid':r['filing_uuid'],'y':r['filing_year'],'p':r['filing_period'],'ft':r['filer_type'],'lid':lb.get('id'),'fn':lb.get('first_name'),'ln':lb.get('last_name'),'rid':rg.get('id'),'rn':rg.get('name'),'none':r['no_contributions'],'pacs':r.get('pacs'),
      'items':[[it.get('contribution_type'),it.get('contributor_name'),it.get('payee_name'),it.get('honoree_name'),it.get('amount'),it.get('date')] for it in (r.get('contribution_items') or [])]},separators=(',',':'))+'\n')
  out.flush(); u=d['next']; open(state,'w').write(u or ''); time.sleep(0.3)
print('done',file=sys.stderr)
