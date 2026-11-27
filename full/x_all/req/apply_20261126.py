
import json,csv,re,datetime,shutil
R=json.load(open('req/review_20261126.json'))
ACC={
'1728538614521360459':('shoutout','"My friend David Friedman speaks the truth"; same person (registered as Mr. David Friedman; covered position U.S. Ambassador to Israel 2017-2021); text'),
'1788586939358011625':('mention','quotes "former U.S Ambassador to Israel David Friedman"; same person (LD-2 covered position U.S. Amb. to Israel 2017-2021); text only'),
'1991532348702355830':('shoutout','"we met with Maggie Collins and Mark Bednar to discuss our efforts to keep the 2026 FIFA World Cup in KC"; likely same person (Monument Advocacy lobbyist, distinctive name); office meeting; text + photo'),
'2021648061630754857':('shoutout','"sit down with John Calvelli and Colin Sheldon from @theWCS"; same person (Wildlife Conservation Society in-house lobbyist per LD-2 and OIRA records); office meeting'),
'1878834751525835140':('mention','congratulates "Governor Patrick Morrisey and First Lady Denise Morrisey" on inauguration; same person (Denise Henry Morrisey, Capitol Counsel lobbyist); text only'),
'1846299393982709933':('not_relationship','"Tom Latham Award" named for former Rep. Tom Latham (Hecht Latham Spencer lobbyist); award-name reference, no interaction'),
'1890386954354602377':('not_relationship','council seat "recently vacated by Joe Borelli" (same person, now Chartwell Strategy Group); reference only, no relationship evidence'),
}
REJ={
'95141':(r'jordan',"namesake: Rep. Jim Jordan (sitting Member) or Bishop James Jordan Jr., not the Green Mountain Strategies lobbyist"),
'60141':(r'morrisey',"author: @wvgovernor is now Gov. Morrisey's office account, not a member of Congress (handle was mapped to Sen. Justice)"),
'404':(r"o'connor","namesake: Dr. Kevin O'Connor, Biden's White House physician, not the IAFF in-house lobbyist"),
'141651':(r'reynolds',"namesake: Mike Reynolds of Hero Agriculture (veterans group), not the Baker Donelson aviation lobbyist"),
'138853':(r'jeff last',"not a name: 'When Jeff last ran' (Jeff DeWit), not the Bristol-Myers Squibb in-house lobbyist"),
'154159':(r'hayes',"namesake: MSNBC host Chris Hayes, not the Thorn Run Partners lobbyist"),
'24868':(r'cole',"namesake: Georgia football player Chris Cole, not the ICBA in-house lobbyist"),
'121455':(r'rivers',"namesake: Sgt. William Rivers, fallen Army Reserve soldier, not the WP Rivers and Associates lobbyist"),
'139686':(r'casey',"namesake: constituent environmental advocate Tom Casey (lead-free tackle), not the Academy of Managed Care Pharmacy in-house lobbyist"),
'103501':(r'anderson',"namesake: Buffalo jazz festival host Sheila Anderson, not the Campion Advocacy Fund in-house lobbyist"),
'145295':(r'barnett',"namesake: Palm Beach County Commissioner Michael Barnett, not the Powers Pyles Sutter & Verville lobbyist"),
'152117':(r'lane',"namesake: Delta County CO Commissioner Mike Lane, not the Kiley & Associates lobbyist"),
'139333':(r"o'reilly","namesake (likely): former Herndon VA Mayor Mike O'Reilly, not shown to be The Nature Conservancy in-house lobbyist"),
'68125|150760':(r'solomon',"namesake (likely): Maryland Del. Jared Solomon, not shown to be the Bose Public Affairs (Indianapolis) lobbyist"),
'83012':(r'strickland',"namesake: Baldwin County GA Commission Chairman Andrew Strickland, not the American Psychological Association in-house lobbyist"),
'142529':(r'andrew do',"namesake: Orange County CA Supervisor Andrew Do, not the Covington & Burling lobbyist"),
'66478':(r'mason',"namesake: Jon Mason, Nashua Community College workforce director, not the AANA in-house lobbyist"),
'137998':(r'bradley',"namesake: late LA Mayor Tom Bradley (post office / Getty House), not the Tom Bradley Health Policy lobbyist"),
}
now=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
rows=[];miss=[]
for r in R:
  p=r['post_id']; pid=r['person_ids']
  if p in ACC:
    et,why=ACC[p]; rows.append([now,p,pid,'accept',et,why]); continue
  if pid in REJ:
    kw,why=REJ[pid]
    if r['tier']=='X_member' or re.search(kw,r['text'],re.I): rows.append([now,p,pid,'reject','',why]); continue
  miss.append((p,pid,r['matched'],r['text'][:200]))
print('rows',len(rows),'acc',sum(1 for x in rows if x[3]=='accept'),'miss',len(miss))
for m in miss: print(m)
if not miss:
  fn='review_decisions.csv'; shutil.copy(fn,'review_decisions.prev_'+datetime.datetime.now().strftime('%Y%m%d_%H%M')+'.csv')
  with open(fn,'a',newline='') as f: csv.writer(f).writerows(rows)
  open('req/decisions_20261126.txt','w').write(''.join('|'.join([x[1],x[2],x[3],x[4],x[5]])+'\n' for x in rows))
  print('written')
