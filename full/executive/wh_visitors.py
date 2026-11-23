# Biden White House WAVES visitor records 2023-01..2024-08 (bidenwhitehouse.archives.gov; final published release)
# streamed, never stored whole; keep only rows whose visitor first+last name equals a name in the lobbyist universe.
import sys,os,csv,io,re,json,urllib.request,collections
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','legislative')); import dclib
byname,_=dclib.people_index()
html=urllib.request.urlopen('https://bidenwhitehouse.archives.gov/disclosures/visitor-logs/').read().decode()
urls=[u for u in dict.fromkeys(re.findall(r'href="(https://bidenwhitehouse[^"]+WAVES[^"]+\.csv)"',html,re.I)) if re.search(r'/(2023|2024)\.\d\d',u)]
OUT='raw/wh_visitor_lobbyist_name_matches.jsonl'; stat=[]
doneu=set()
if os.path.exists('raw/wh_files_done.json'): doneu=set(json.load(open('raw/wh_files_done.json')))
def col(h,*c):
  H=[re.sub(r'[^a-z]','',x.lower()) for x in h]
  for k in c:
    if k in H: return H.index(k)
  return None
with open(OUT,'a') as f:
  for u in urls:
    if u in doneu: continue
    r=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'research'}),timeout=300)
    rd=csv.reader(io.TextIOWrapper(r,encoding='latin-1',newline=''))
    h=next(rd); iL=col(h,'lastname','namelast'); iF=col(h,'firstname','namefirst'); iM=col(h,'middleinitial','namemid')
    iS=col(h,'appointmentstartdate','apptstartdate'); iVL=col(h,'visiteelastname','visiteenamelast'); iVF=col(h,'visiteefirstname','visiteenamefirst')
    iLoc=col(h,'meetinglocation','meetingloc'); iRm=col(h,'meetingroom'); iN=col(h,'totalpeople'); iD=col(h,'description')
    n=m=0
    for row in rd:
      n+=1
      try: k=dclib.norm_person(row[iF]+' '+row[iL])
      except Exception: continue
      if not k or k not in byname: continue
      m+=1; g=lambda i: row[i] if i is not None and i<len(row) else ''
      f.write(json.dumps({'file':u.rsplit('/',1)[1],'last':g(iL),'first':g(iF),'mid':g(iM),'appt_start':g(iS),'visitee_last':g(iVL),'visitee_first':g(iVF),'location':g(iLoc),'room':g(iRm),'total_people':g(iN),'description':g(iD),'cand':[c[0] for c in byname[k]]})+'\n')
    stat.append({'file':u,'rows':n,'name_matches':m}); doneu.add(u); print(u.rsplit('/',1)[1],n,m,flush=True)
    json.dump(sorted(doneu),open('raw/wh_files_done.json','w'))
    with open('raw/wh_file_stats.jsonl','a') as s: s.write(json.dumps(stat[-1])+'\n')
print('DONE')
