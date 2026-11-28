import json,csv,re,datetime,shutil
R=json.load(open('req/review_20261127_sel.json'))
ACC={
'1631438728576090112':('shoutout','Rep. Dean thanks Howard alum "Jemiah Williams" on her team; same person (LDA covered position: Legislative Aide, Rep. Madeleine Dean; now Holland & Knight); former staffer; text'),
'1882154655083577764':('shoutout','"honored to have had Anna May on my staff for the last 2.5 years"; same person (covered position: Legislative Assistant to Rep. Michael Guest, Homeland Security PSM; now Carlough Solutions); former staffer'),
'2061913361873256690':('shoutout','congratulates "a former fellow of mine, Mark Cruz" on IHS Director nomination; same person (covered: PDAS Indian Affairs; Gallatin Public Affairs); former staffer'),
'1912175565668233407':('shoutout','"Sarah Kidd ... a former intern in my Washington, D.C. office"; same person (covered position: Intern, Rep. Scott Fitzgerald; Penn Hill Group); former intern; text + photo'),
'1888303206897230286':('mention','"Russ Vought + Mark Paoletta + Clarence Thomas = pure awesome"; same person (covered: OMB General Counsel; Schaerr Jaffe); praise, text only'),
'1798833426629578834':('mention','campaign post quotes "NRA-PVF Chair Randy Kozuch" endorsement letter; same person (NRA in-house lobbyist per LD-2); endorsement'),
'1749849462909095993':('shoutout','"sat down with Samuel Kieffer, VP of Public Affairs at the American Farm Bureau Federation" (podcast); same person (AFBF in-house lobbyist per LD-2)'),
'2031013389678387690':('shoutout','"meet with AMAC CEO Rebecca Weber and AMAC Action SVP Andy Mangione" to receive award; likely same person (Andrew Mangione in-house lobbyist, distinctive name); meeting'),
'2079318915688321134':('shoutout','"Elisabeth Gehl & President Emeritus Pierce Bush, of Big Brothers Big Sisters Lone Star joined us in Washington"; same person (Big Brothers Big Sisters of America in-house lobbyist per LD-2); office meeting'),
'1963239397203026377':('shoutout','"my good friend, a beloved Wyoming guy, Rob Wallace"; same person (Rob Wallace Group; former Asst. Secretary of the Interior, Wyoming); text'),
'2052413045826097164':('shoutout','"On @KTAR923 now with my friend Matt Salmon talking about the Governor\'s race"; same person (former Rep. Matt Salmon, MJS Advisors); text'),
'1960725440080835009':('shoutout','birthday wishes to "Melissa Stone" #flapol; likely same person (Florida GOP consultant, Cavalry Strategies); text + photo'),
'1660757873599578117':('shoutout','"Congratulations Melissa Stone! Proud of you and your team!" on @Fla_Pol Florida business spotlight; likely same person (Cavalry Strategies founder); text'),
}
REJ={
'95141':(r'jordan',"namesake: Rep. Jim Jordan (sitting Member), not the Green Mountain Strategies lobbyist"),
'141581':(r'donovan',"not shown to be same person: 'Joe Donovan' thanked alongside New England Council's Jim Brett; link to Donovan Strategies lobbyist unverified, common name"),
'53004':(r'bond',"namesake: fictional James Bond / Lt. Col. James Bond (NC Guard), not the Bond & Associates lobbyist"),
'72033':(r'sweeney',"namesake: Peapack-Gladstone NJ Councilman John Sweeney (deceased), not former Rep. John Sweeney"),
'149124':(r'simmons',"namesake: Rev. Daniel Simmons Sr., Mother Emanuel shooting victim, not the Simmons Energy lobbyist"),
'150467':(r'babbitt',"namesake: late former Flagstaff Mayor Paul Babbitt Jr., not the Holland & Hart lobbyist (former Kelly counsel)"),
'89313':(r'stein',"namesake: Epstein survivor Elizabeth Stein (SOTU guest), not the former Senate HELP staffer lobbyist"),
'62089':(r'todd',"namesake: South Oak Cliff HS football coach Jason Todd, not the in-house lobbyist"),
'150326':(r'.',"namesake/no evidence: Virginia Beach Republican Women's Club post; not shown to be the LeoLabs in-house lobbyist"),
'49258':(r'thompson',"namesake: Georgia Labor Commissioner Bruce Thompson (died Nov 2024), not shown to be CapEDC Advisors lobbyist V Bruce Thompson"),
'7848':(r'napier',"namesake: Virginia Beach City Council candidate John Napier, not the lobbyist John Napier"),
'143936':(r'chambers',"namesake: Irish Minister of State Jack Chambers TD, not the Maynard Nexsen lobbyist"),
'85399':(r'smith',"namesake: SP4 Keith Smith, late Vietnam veteran (bill namesake), not the KH Strategies lobbyist"),
'64906|152614':(r'smith',"namesake: Pettis County MO Prosecuting Attorney Todd Smith, not a lobbyist"),
'153196':(r'riley',"namesake: NYC Council Member Kevin Riley (Bronx), not the American Resort Development Assn in-house lobbyist"),
'141109':(r'bourne',"namesake: Augusta County VA Treasurer David Bourne, not the Albertine Enterprises lobbyist"),
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
  open('req/decisions_20261127.txt','w').write(''.join('|'.join([x[1],x[2],x[3],x[4],x[5]])+'\n' for x in rows))
  print('written')
