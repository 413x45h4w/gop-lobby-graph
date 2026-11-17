import json,urllib.request,urllib.parse,time,datetime,csv
P=json.load(open('../pilot_lobbyists.json'))
out=open('ld203_pilot_contributions.jsonl','a')
for p in P:
  last,first=p['lda_name'].split(',')
  for yr in (2023,2024,2025,2026):
    u="https://lda.gov/api/v1/contributions/?"+urllib.parse.urlencode({'lobbyist_name':last,'filing_year':yr,'page_size':100})
    while u:
      try: d=json.load(urllib.request.urlopen(u,timeout=60))
      except Exception as e: print('err',e); time.sleep(5); break
      for r in d['results']:
        lb=r.get('lobbyist') or {}
        if r.get('filer_type')!='lobbyist' or (lb.get('last_name') or '').upper()!=last or not (lb.get('first_name') or '').upper().startswith(first[:3]): continue
        out.write(json.dumps({'lid':p['lid'],'fetched':datetime.datetime.now().isoformat(),'filing_uuid':r['filing_uuid'],'year':yr,'period':r['filing_period'],'lobbyist':lb,'registrant':(r.get('registrant') or {}).get('name'),'no_contributions':r['no_contributions'],'items':r.get('contribution_items',[])})+'\n')
      u=d.get('next'); time.sleep(1)
  print(p['name'],'done',flush=True)
