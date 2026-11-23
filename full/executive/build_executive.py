# Executive layer: OIRA EO 12866 meetings (reginfo.gov) + Biden-era White House visitor records (name matches to lobbyists).
import sys,os,re,json,collections
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','legislative')); import dclib
now=dclib.NOW(); OI=dclib.org_index(); byname,byid=dclib.people_index(); stat=collections.Counter()
GOV=re.compile(r'^(OMB|OIRA|OSTP|NEC|DPC|CEQ|DOL|DOT|EPA|HHS|CMS|FDA|USDA|DOE|DOI|DOJ|DHS|DOD|ED|HUD|TREAS|TREASURY|SBA|SEC|FCC|FTC|FERC|NRC|OPM|GSA|VA|STATE|DOC|NOAA|NIST|FAA|FRA|FMCSA|NHTSA|PHMSA|FTA|FHWA|MARAD|OSHA|MSHA|EBSA|WHD|ETA|OFCCP|IRS|CFPB|FHFA|USTR|CBP|ICE|USCIS|FEMA|TSA|USCG|BLM|FWS|NPS|BOEM|BSEE|OSMRE|USGS|BIA|BOR|APHIS|FSIS|FNS|AMS|RUS|NRCS|FS|CDC|NIH|HRSA|SAMHSA|ACF|IHS|ATF|DEA|BOP|FBI|EOP|WHITE HOUSE|SSA|USPS|CPSC|EEOC|NLRB|PBGC|CPO|USPTO|UST|DOED|SBA ADVOCACY|OSTP|OPM|OVP|NSC|ONDCP|CEA|ONCD|EOP/.*|OMB/.*|EPA/.*|DOT/.*|HHS/.*|USDA/.*|DOI/.*|DOE/.*|DOL/.*)',re.I)
ALIAS={'EEI':'Edison Electric Institute','API':'American Petroleum Institute','NAM':'National Association of Manufacturers','ACC':'American Chemistry Council','AFPM':'American Fuel & Petrochemical Manufacturers','PHRMA':'Pharmaceutical Research and Manufacturers of America','NRECA':'National Rural Electric Cooperative Association','APPA':'American Public Power Association','INGAA':'Interstate Natural Gas Association of America','NMA':'National Mining Association','AGC':'Associated General Contractors of America','NAHB':'National Association of Home Builders','NFIB':'National Federation of Independent Business','IPAA':'Independent Petroleum Association of America','AHIP':"America's Health Insurance Plans",'NRDC':'Natural Resources Defense Council','EDF':'Environmental Defense Fund'}
def orgs_of(s):
  s=ALIAS.get((s or '').strip().upper(),s)
  s=(s or '').strip(); out=[]
  parts=re.split(r'\s+on behalf of\s+|\s+representing\s+|\s+for\s+the\s+|\s*\(on behalf of\s*|\s*/\s*',s,flags=re.I)
  for i,p in enumerate(parts):
    p=p.strip(' )(.,')
    if not p: continue
    k=dclib.norm_org(p)
    role='firm' if (i==0 and len(parts)>1) else ('client' if i>0 else 'org')
    out.append((p,k if k in OI else '',role))
  return out
def person(name,keys):
  k=dclib.norm_person(name)
  if not k or k not in byname: return '',''
  C=byname[k]
  for ok in keys:
    lob={byid.get(str(i)) for i in OI[ok]['lob']}
    hit=[c for c in C if c[0] in lob]
    if hit: return hit[0],'name+org_in_lda'
  if len({c[0] for c in C})==1: return C[0],'name_only_unique'
  return '',''
mt=[];att=[];agg=collections.defaultdict(lambda:[0,set(),set(),set()]);lob=[]
if os.path.exists('raw/oira_meetings.jsonl'):
  for l in open('raw/oira_meetings.jsonl'):
    m=json.loads(l)
    if 'error' in m: stat['oira_error']+=1; continue
    stat['oira_meetings']+=1
    ag=m.get('agency',''); d=m.get('meeting_datetime','')
    iso=(d[6:10]+'-'+d[0:2]+'-'+d[3:5]) if len(d)>=10 else ''
    ro=orgs_of(m.get('requestor_org',''))
    mt.append([m['meeting_id'],iso,d,m.get('rin',''),m.get('title','')[:250],ag,m.get('stage',''),m.get('requestor_org',''),m.get('requestor_name',''),'|'.join(x[1] for x in ro if x[1]),len(m.get('attendees',[])),m['url']])
    for a in m.get('attendees',[]):
      org=a.get('org',''); gov=bool(GOV.fullmatch(org.strip().upper()) or re.fullmatch(r'(OMB|OIRA|DOL|DOT|EPA|HHS|USDA|DOE|DOI|DOJ|DHS|DOD|DOC|VA|ED|HUD|TREASURY|TREAS)\s*[/\-–,].*',org.strip(),re.I) or re.match(r'^(U\.?S\.? )?(Department|Dept\.?|Office of Management|Executive Office)',org.strip(),re.I)) 
      os_=orgs_of(org) if not gov else []
      keys=[x[1] for x in os_ if x[1]]
      p,pm=(person(a['name'],keys) if not gov else ('',''))
      stat['oira_attendees']+=1; stat['oira_attendee_gov']+=gov; stat['oira_attendee_org_match']+=bool(keys); stat['oira_attendee_lobbyist_'+(pm or 'none')]+=1
      att.append([m['meeting_id'],iso,m.get('rin',''),ag,a['name'],org,int(gov),'|'.join(keys),'|'.join(x[2] for x in os_ if x[1]),p[0] if p else '',p[1] if p else '',pm,'high' if pm=='name+org_in_lda' else ('low' if pm else '')])
      for (txt,k,role) in os_:
        if k:
          g=agg[(k,ag)]; g[0]+=1; g[1].add(m['meeting_id']); g[2].add(m.get('rin','')); g[3].add(role)
      if p: lob.append([p[0],p[1],a['name'],org,m['meeting_id'],iso,m.get('rin',''),ag,m.get('title','')[:200],pm,'high' if pm=='name+org_in_lda' else 'low'])
n1=dclib.wcsv('oira_meetings.csv',['meeting_id','date','meeting_datetime','rin','rule_title','agency','stage','requestor_org','requestor_name','requestor_lda_org_keys','n_attendees','url'],mt)
n2=dclib.wcsv('oira_attendees.csv',['meeting_id','date','rin','agency','attendee','attendee_org','is_government','lda_org_keys','lda_org_roles','lobbyist_person_id','lobbyist','person_match_type','person_match_confidence'],att)
n3=dclib.wcsv('edges_org_to_agency_oira.csv',['lda_org_key','lda_org_name','agency','n_attendee_rows','n_meetings','rins','roles','confidence','built_at'],[[k,OI[k]['name'],a,v[0],len(v[1]),'|'.join(sorted(v[2]))[:300],'|'.join(sorted(v[3])),'high',now] for (k,a),v in sorted(agg.items(),key=lambda x:-len(x[1][1]))])
n4=dclib.wcsv('edges_lobbyist_to_agency_oira.csv',['lobbyist_person_id','lobbyist','attendee_as_listed','attendee_org','meeting_id','date','rin','agency','rule_title','match_type','confidence'],lob)
# White House (Biden archive) visitor records
MI=collections.defaultdict(set)
for l in open('raw/wh_visitor_lobbyist_name_matches.jsonl'):
  r=json.loads(l); MI[(r['first'].upper(),r['last'].upper())].add((r['mid'] or '').upper()[:1])
wh=[];wagg=collections.defaultdict(lambda:[0,set(),set(),''])
for l in open('raw/wh_visitor_lobbyist_name_matches.jsonl'):
  r=json.loads(l); stat['wh_name_match_rows']+=1
  tour=(r['visitee_last'],r['visitee_first'])==('Office','Visitors') or 'TOUR' in r['room'].upper()
  try: big=int(r['total_people'] or 0)>50
  except ValueError: big=False
  c=sorted(set(r['cand']))
  if tour: stat['wh_tour_excluded']+=1; continue
  if len(c)!=1: stat['wh_ambiguous_name_excluded']+=1; continue
  nmi=len({x for x in MI[(r['first'].upper(),r['last'].upper())] if x})
  if nmi>1: stat['wh_multi_middle_initial_excluded']+=1; continue
  stat['wh_kept']+=1
  pid=c[0]; d=r['appt_start'].split(' ')[0]
  wh.append([pid,r['first']+' '+r['last'],r['mid'],d,(r['visitee_first']+' '+r['visitee_last']).strip(),r['location'],r['room'],r['total_people'],int(big),r['file'],'low (name-only; visitor first+last equals exactly one LDA lobbyist; <=1 middle initial seen for that name; tours excluded)'])
  g=wagg[(pid,(r['visitee_first']+' '+r['visitee_last']).strip())]; g[0]+=1; g[1].add(d); g[3]=r['first']+' '+r['last']
n5=dclib.wcsv('wh_visits_lobbyist_name_matches.csv',['lobbyist_person_id','visitor_name','visitor_middle_initial','appt_start_date','visitee','location','room','total_people_in_appt','large_event_gt50','source_file','confidence'],wh)
n6=dclib.wcsv('edges_lobbyist_to_wh_visitee.csv',['lobbyist_person_id','visitor_name','visitee','n_visits','first_date','last_date','confidence','built_at'],[[k[0],v[3],k[1],v[0],min(v[1]),max(v[1]),'low',now] for k,v in sorted(wagg.items(),key=lambda x:-x[1][0])])
json.dump({**stat,'oira_meetings_rows':n1,'oira_attendee_rows':n2,'org_agency_edges':n3,'lobbyist_oira_rows':n4,'wh_rows':n5,'wh_edges':n6,'built_at':now},open('executive_stats.json','w'),indent=1)
print(json.load(open('executive_stats.json')))
