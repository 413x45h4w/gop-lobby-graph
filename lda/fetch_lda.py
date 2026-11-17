import json,time,urllib.request,urllib.parse,sys,datetime
firms=["Ballard Partners","BGR Government Affairs","Mercury Public Affairs","Continental Strategy","Capitol Counsel","Akin Gump","Brownstein Hyatt","Miller Strategies","Avoq","Cornerstone Government Affairs","Holland & Knight","Squire Patton Boggs","Crossroads Strategies","Williams and Jensen","Javelin Advocacy","Checkmate Government Relations","Tiber Creek Partners","Cove Strategies","Elevate Government Affairs","Fierce Government Relations","Invariant","Lot Sixteen","Thorn Run Partners","Alpine Group","Kadesh","Mehlman Consulting","Arnold & Porter","DLA Piper","Off Hill Strategies","Hilltop Public Solutions"]
out=open('lda_filings_2025_2026.jsonl','a')
def get(u):
  for i in range(6):
    try:
      return json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'Accept':'application/json'}),timeout=60))
    except Exception as e:
      print('err',e,u,file=sys.stderr); time.sleep(10*(i+1))
for f in firms:
  for yr in (2025,2026):
    u="https://lda.gov/api/v1/filings/?"+urllib.parse.urlencode({'filing_year':yr,'registrant_name':f,'page_size':100})
    while u:
      d=get(u)
      if not d: break
      for r in d['results']:
        lobs=[]
        for la in r['lobbying_activities']:
          for l in la['lobbyists']:
            lb=l['lobbyist']; lobs.append([lb['id'],lb['first_name'],lb['last_name'],l['covered_position']])
        out.write(json.dumps({'q':f,'fetched':datetime.datetime.now().isoformat(),'uuid':r['filing_uuid'],'year':r['filing_year'],'period':r['filing_period'],'type':r['filing_type'],'registrant':r['registrant']['name'],'registrant_id':r['registrant']['id'],'client':r['client']['name'],'income':r['income'],'lobbyists':lobs})+'\n')
      u=d['next']; time.sleep(1.5)
  print(f, 'done', file=sys.stderr, flush=True)
