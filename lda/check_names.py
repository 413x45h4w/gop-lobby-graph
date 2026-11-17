import json,urllib.request,urllib.parse,time,sys,datetime
names=[l.strip() for l in sys.argv[1].split(';')]
out=open('lda_name_checks.jsonl','a')
for n in names:
  last,first=n.split(',')
  res={}
  for yr in (2023,2024,2025,2026):
    u="https://lda.gov/api/v1/filings/?"+urllib.parse.urlencode({'filing_year':yr,'lobbyist_name':last,'page_size':100})
    try: d=json.load(urllib.request.urlopen(u,timeout=60))
    except Exception as e: print(n,yr,'err',e); continue
    for r in d['results']:
      for la in r['lobbying_activities']:
        for l in la['lobbyists']:
          lb=l['lobbyist']
          if lb['last_name'].upper()==last.upper() and lb['first_name'].upper().startswith(first.upper()):
            k=(r['registrant']['name']); e=res.setdefault(k,{'filings':set(),'income':0,'cp':set(),'years':set(),'clients':set()})
            if r['filing_uuid'] not in e['filings']:
              e['filings'].add(r['filing_uuid']); e['income']+=float(r['income'] or 0)
            e['years'].add(yr); e['clients'].add(r['client']['name'])
            if l['covered_position']: e['cp'].add(l['covered_position'][:200])
    time.sleep(1)
  summ={k:{'n_filings':len(v['filings']),'income_sum_attrib':v['income'],'years':sorted(v['years']),'n_clients':len(v['clients']),'covered':sorted(v['cp'])[:3]} for k,v in res.items()}
  out.write(json.dumps({'name':n,'checked':datetime.datetime.now().isoformat(),'note':'first page (100) of filings per year matched by lobbyist_name; counts are lower bounds','registrants':summ})+'\n'); out.flush()
  print(n, json.dumps(summ)[:600])
