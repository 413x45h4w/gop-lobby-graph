# OIRA EO 12866 meetings (reginfo.gov public calendar) 2023-01..2026-11 -> raw/oira_meetings.jsonl (resumable, append-only)
import requests,re,html,json,os,time,datetime,calendar
OUT='raw/oira_meetings.jsonl'; done=set()
if os.path.exists(OUT):
  for l in open(OUT): done.add(json.loads(l)['meeting_id'])
s=requests.Session(); s.headers['User-Agent']='Mozilla/5.0 (research; gop-lobby-graph)'
B='https://www.reginfo.gov/public/do/'
def L(t):
  t=re.sub(r'<script.*?</script>|<style.*?</style>','',t,flags=re.S)
  return [l.strip() for l in html.unescape(re.sub(r'<[^>]+>','\n',t)).split('\n') if l.strip()]
def detail(href):
  t=s.get(B+href.split('/public/do/')[1],timeout=60).text; i=t.find('maincontent'); x=L(t[i:])
  def after(k):
    try: return x[x.index(k)+1]
    except ValueError: return ''
  att=[]; raw_att=[]
  if 'List of Attendees' in x:
    raw_att=x[x.index('List of Attendees')+1:]
    raw_att=raw_att[:next((i for i,v in enumerate(raw_att) if v.startswith('Something went wrong') or v=='Reginfo.gov'),len(raw_att))]
  x=[v.replace('\xa0',' ') for v in x]
  if 'List of Attendees' in x:
    k=x.index('List of Attendees')+2
    while k+2<len(x) and x[k]=='•':
      nm=x[k+1]; org=''
      if k+2<len(x) and x[k+2].startswith('- '): org=x[k+2][2:]; k+=1
      mode=x[k+2] if k+2<len(x) and x[k+2]!='•' else ''
      att.append({'name':nm,'org':org,'participation':mode}); k+=3 if mode else 2
  docs=[]
  if 'List of Documents' in x:
    k=x.index('List of Documents')+1
    while k<len(x) and x[k] not in ('Attendees:',): docs.append(x[k]); k+=1
  rq=after("Requestor:"); rn=''
  if "Requestor's" in x: rn=x[x.index("Requestor's")+2]
  return {'rin':after('RIN:'),'title':after('Title:'),'agency':after('Agency/Subagency:'),'stage':after('Stage of Rulemaking:'),'meeting_datetime':after('Meeting Date/Time:'),'requestor_org':rq,'requestor_name':rn,'documents':docs,'attendees':att,'attendee_lines':raw_att}
s.get(B+'eom12866Search')
f=open(OUT,'a'); n=0
d0=datetime.date(2023,1,1)
while d0<=datetime.date(2026,11,30):
  last=calendar.monthrange(d0.year,d0.month)[1]
  r=s.get(B+f'eom12866Search?pubId=&ajaxReq=true&view=month&searchStartDate={d0.month}/1/{d0.year}&searchEndDate={d0.month}/{last}/{d0.year}',timeout=60).json()
  def flat(o):
    if isinstance(o,dict): yield o
    elif isinstance(o,list):
      for z in o: yield from flat(z)
  days=sorted({(x['meetingMonth'],x['meetingDate'],x['meetingYear']) for x in flat(r) if x.get('type_Cd')=='C'})
  for m,dd,y in days:
    t=s.get(B+f'eom12866SearchResults?pubId=&viewType=month&typeCd=C&searchCalendarDate={m}/{dd}/{y}',timeout=60).text
    for href in dict.fromkeys(re.findall(r'href="(/public/do/viewEO12866Meeting\?[^"]+)"',t)):
      href=html.unescape(href); mid=re.search(r'meetingId=(\d+)',href).group(1)
      if mid in done: continue
      for a in range(3):
        try: rec=detail(href); break
        except Exception as e: time.sleep(5); rec={'error':str(e)[:200]}
      rec.update({'meeting_id':mid,'url':'https://www.reginfo.gov'+href,'list_date':f'{y}-{m:02d}-{dd:02d}','fetched_at':datetime.datetime.now().astimezone().isoformat(timespec='seconds')})
      f.write(json.dumps(rec)+'\n'); f.flush(); done.add(mid); n+=1; time.sleep(0.4)
  print(d0, len(days),'days; total new',n,flush=True)
  d0=(d0.replace(day=28)+datetime.timedelta(days=4)).replace(day=1)
print('DONE')
