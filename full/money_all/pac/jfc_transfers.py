# OpenFEC /schedules/schedule_b/by_recipient_id/ for every JFC that received universe-lobbyist money: JFC -> recipient committee totals per cycle.
# Used to pass lobbyist JFC money pro rata to participant member committees. Append-only cache; key redacted in api_calls.log.
import fecapi,json,os,csv,datetime
NOW=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
C={r['committee_id']:r for r in csv.DictReader(open('committees_classified.csv'))}
R=[r for r in csv.DictReader(open('lobbyist_to_pac_fec_rows.csv')) if not r['match_confidence'].startswith('low') and r['memo_cd']!='X']
jfc=sorted({r['fec_committee_id'] for r in R if C.get(r['fec_committee_id'],{}).get('committee_class')=='joint_fundraising_committee'})
cache='jfc_transfers_raw.jsonl'; have=set()
if os.path.exists(cache):
  for l in open(cache): have.add(json.loads(l)['_jfc'])
with open(cache,'a') as f:
  for i,c in enumerate(jfc):
    if c in have: continue
    page=1; rows=[]
    while True:
      try: d=fecapi.get('/schedules/schedule_b/by_recipient_id/',{'committee_id':c,'cycle':[2024,2026],'per_page':100,'page':page})
      except RuntimeError as e: rows=None; f.write(json.dumps({'_jfc':c,'_error':str(e)[:80],'_fetched':NOW})+'\n'); break
      rows+=d['results']
      if page>=d['pagination'].get('pages',1): break
      page+=1
    if rows is not None: f.write(json.dumps({'_jfc':c,'_fetched':NOW,'results':rows})+'\n'); f.flush()
    if i%50==0: print(i,len(jfc),fecapi.STATE['remaining'],flush=True)
print('done jfc',len(jfc))
