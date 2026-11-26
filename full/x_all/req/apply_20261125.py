
import json,csv,re,datetime,shutil
R=json.load(open('req/review_20261125.json'))
ACC={
'1999159189906595931':('mention','Rep. Mike Flood welcomes "Mike Flood of @USChamber" testifying at Financial Services hearing; same person (U.S. Chamber in-house lobbyist per LD-2); text'),
'1986593367409492295':('mention','hearing witness "Tarren Bragdon" on Medicaid; same person (FGA Action in-house lobbyist, FGA CEO); distinctive name; text only'),
'1747645156940026019':('mention','"@sbaprolife\'s legislative director, Jamie Dangers, joined my podcast"; LD-2: Susan B. Anthony List in-house; text'),
'2055447379508125976':('shoutout','"Great having Jamie Dangers in Louisiana to announce a critical pro-life endorsement from @sbaprolife"; LD-2: SBA List in-house; campaign event'),
'2054708053962797434':('shoutout','campaign meet and greet "with special guest Jamie Dangers from @sbaprolife"; LD-2: SBA List in-house'),
'1864484045016428853':('shoutout','congratulates Gail Slater as next AAG for antitrust, "look forward to working with Gail"; same person (former Roku in-house lobbyist); distinctive name; post-lobbying government role'),
'1899805138740469929':('mention','Senate confirmation of Gail Slater as AAG Antitrust; same person (former Roku in-house lobbyist); post-lobbying government role'),
'1864389362462687427':('list_mention','list of Trump nominees including Gail Slater; same person (former Roku in-house lobbyist); post-lobbying government role'),
'2023434669476528624':('mention','statement on Gail Slater pushed out of DOJ Antitrust; same person (former Roku in-house lobbyist); post-lobbying government role'),
'2022063107456254014':('mention','statement on departure of Gail Slater from DOJ; same person (former Roku in-house lobbyist); post-lobbying government role'),
'1665154877624909824':('shoutout','"former Senator and current US Ambassador to the Vatican Joe Donnelly ... Proud to call Joe a dear friend"; same person (former Member, Akin Gump lobbyist); text + photo'),
'2067062153186795745':('mention','quotes "CMF CEO Jen Daulby" praising Kiley office; likely same person (distinctive name; CMF bio: former Hill/committee staff and private sector, consistent with OGR lobbyist); text'),
'1838968382789431398':('list_mention','#TeamScott endorsement list incl. "Hialeah Mayor Esteban Bovo"; same person (Corcoran Partners bio: Esteban L. Bovo Jr., former Miami-Dade commissioner)'),
}
REJ={
'49637':(r'cohen',"namesake: Trump's former lawyer Michael Cohen, not the RenRe North America in-house lobbyist"),
'154226':(r'flood',"namesake: 'Mike Flood' here is the sitting Member of Congress (Rep. Mike Flood), not the U.S. Chamber in-house lobbyist"),
'72006':(r'cia|brennan',"namesake: former CIA Director John Brennan, not the Bluebird Strategies lobbyist"),
'148154':(r'marine|abbey|13|hero|kabul|afghan|fallen|hoover',"namesake: SSgt Taylor Hoover, Abbey Gate fallen Marine, not the Cogent Strategies lobbyist"),
'28500':(r'adler',"namesake: David Adler detained in Israel (flotilla), not the ASTRO in-house lobbyist"),
'143718':(r'paul weiss',"not a person: Paul Weiss law firm name, not the Prime Policy Group lobbyist"),
'145022|72938':(r'franklin',"namesake: Woodbridge Supervisor Margaret Franklin (VA HD-23 candidate), not the Michael Best / Fulcrum lobbyist"),
'68556':(r'sherman',"namesake: founding father Roger Sherman, not the Waneta Strategies lobbyist"),
'98414':(r'kane',"namesake: Freehold Borough NJ Mayor Kevin Kane, not the Google in-house lobbyist"),
'41964':(r'mcnulty',"namesake: Warren County NY Republican Chairman Tim McNulty, not the Carnegie Mellon in-house lobbyist"),
'138230':(r'morris',"namesake: WV advisory council appointee / TN GOP committee candidate Chris Morris, not the NAM in-house lobbyist"),
'137985':(r'rice',"namesake: late NJ State Senator Ron Rice, not the charter-schools alliance in-house lobbyist"),
'139460':(r'weber',"namesake: NY State Senator Bill Weber, not the PBS in-house lobbyist"),
'64868':(r'moore',"namesake (likely): Phil Moore of Mississippi Automobile Dealers Association, not shown to be the Southwest Airlines in-house lobbyist"),
'149249':(r'kim',"namesake: student art competition winner Grace Kim, not the Outokumpu in-house lobbyist"),
'145294':(r'miller',"namesake: Lt. Corey Miller, police officer, not the IIABA in-house lobbyist"),
'58980':(r'smith',"namesake: Pastor Matt Smith, Middle River Friends Church, not the Atlas Advocacy lobbyist"),
'45763':(r'maddox',"namesake: Arkansas state legislator John Maddox, not the Caesars in-house lobbyist"),
'15827':(r'ryan',"not a person: John Ryan Brewery (Williamsport PA venue), not the Capitol Consultants lobbyist"),
'53642':(r'murphy',"namesake: member's late grandmother Anne Murphy, not the Cargill in-house lobbyist"),
'47071|140029':(r'hall',"namesake (likely): West Slope COGA board president Stuart Hall, not shown to be the Van Ness Feldman lobbyist"),
'66572':(r'doyle',"namesake: Kearny NJ Mayor Carol Jean Doyle, not the Teach For America in-house lobbyist"),
'143887':(r'mcnally',"namesake: Colorado Mayor Nancy McNally, not the Van Ness Feldman lobbyist"),
'151383':(r'camp',"namesake: 'Dave Camp Breakfast' named for former Rep. Dave Camp (Midland MI), not shown to be the 162 Strategies lobbyist"),
}
now=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
rows=[];miss=[]
for r in R:
  p=r['post_id']; pid=r['person_ids']
  if p in ACC: et,why=ACC[p]; rows.append([now,p,pid,'accept',et,why]); continue
  if pid in REJ:
    kw,why=REJ[pid]
    if r['tier']=='X_member' or re.search(kw,r['text'],re.I): rows.append([now,p,pid,'reject','',why]); continue
  miss.append((p,pid,r['matched'],r['text'][:200]))
print('rows',len(rows),'acc',sum(1 for x in rows if x[3]=='accept'),'miss',len(miss))
for m in miss: print(m)
if not miss:
  fn='review_decisions.csv'; shutil.copy(fn,'review_decisions.prev_'+datetime.datetime.now().strftime('%Y%m%d_%H%M')+'.csv')
  with open(fn,'a',newline='') as f: csv.writer(f).writerows(rows)
  open('req/decisions_20261125.txt','w').write(''.join('|'.join([x[1],x[2],x[3],x[4],x[5]])+'\n' for x in rows))
  print('written')
