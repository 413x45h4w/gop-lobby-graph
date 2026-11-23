# Revolving-door layer: (A) LD-2 covered_position parsing, (B) House SOD + Senate Secretary payroll -> staff->office records matched
# to LDA lobbyists by name, (C) former-member lobbyist flags. Inputs: ../ld2/raw/ld2full_*.jsonl.gz, raw/sod_personnel_rows.csv.gz,
# raw/senate_payroll_rows.csv.gz, ../money_all/people_all.csv, raw congress-legislators files.
import gzip,json,glob,re,csv,collections,datetime,sys
import memberlex as ML
NOW=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
P=ML.P
pid_of={}; prow={}
for r in csv.DictReader(open('../money_all/people_all.csv')):
  for lid in r['person_key'].split('|'): pid_of[int(lid)]=r['person_id']
  prow[r['person_id']]=r
scored={r['lda_lobbyist_id'] for r in csv.DictReader(open('../lobbyist_universe_scored.csv'))}
# ---------- committees lexicon ----------
COMM=[  # (regex, house_id, senate_id)
 (r"WAYS (?:AND|&) MEANS|\bW&M\b",'HSWM',None),(r"ENERGY (?:AND|&) COMMERCE|\bE&C\b",'HSIF',None),(r"FINANCIAL SERVICES|\bHFSC\b",'HSBA',None),
 (r"\bFINANCE COMM|COMMITTEE ON FINANCE|\bSFC\b|SENATE FINANCE",None,'SSFI'),(r"APPROPRIATIONS|\bAPPROPS?\b",'HSAP','SSAP'),
 (r"ARMED SERVICES|\bHASC\b|\bSASC\b",'HSAS','SSAS'),(r"JUDICIARY",'HSJU','SSJU'),(r"\bHELP COMM|HEALTH, EDUCATION, LABOR|\bHELP\b COMMITTEE",None,'SSHR'),
 (r"BANKING",None,'SSBK'),(r"ENVIRONMENT (?:AND|&) PUBLIC WORKS|\bEPW\b",None,'SSEV'),(r"COMMERCE, SCIENCE|SENATE COMMERCE",None,'SSCM'),
 (r"FOREIGN RELATIONS|\bSFRC\b",None,'SSFR'),(r"FOREIGN AFFAIRS|\bHFAC\b",'HSFA',None),(r"INTELLIGENCE|\bHPSCI\b|\bSSCI\b",'HLIG','SLIN'),
 (r"BUDGET COMM|COMMITTEE ON (?:THE )?BUDGET",'HSBU','SSBU'),(r"RULES COMM|COMMITTEE ON RULES",'HSRU','SSRA'),(r"AGRICULTURE",'HSAG','SSAF'),
 (r"HOMELAND SECURITY (?:AND|&) GOVERNMENTAL|\bHSGAC\b",None,'SSGA'),(r"HOMELAND SECURITY COMM|COMMITTEE ON HOMELAND",'HSHM',None),
 (r"OVERSIGHT (?:AND|&) (?:GOVERNMENT )?REFORM|OVERSIGHT COMM|COMMITTEE ON OVERSIGHT",'HSGO',None),(r"NATURAL RESOURCES",'HSII',None),
 (r"ENERGY (?:AND|&) NATURAL RESOURCES|\bENR\b",None,'SSEG'),(r"TRANSPORTATION (?:AND|&) INFRASTRUCTURE|\bT&I\b",'HSPW',None),
 (r"EDUCATION (?:AND|&) (?:THE )?(?:WORKFORCE|LABOR)",'HSED',None),(r"VETERANS'? AFFAIRS COMM|VETERANS COMM|COMMITTEE ON VETERANS",'HSVR','SSVA'),
 (r"SMALL BUSINESS COMM|COMMITTEE ON SMALL BUSINESS",'HSSM','SSSB'),(r"SCIENCE, SPACE|SCIENCE COMM",'HSSY',None),(r"HOUSE ADMINISTRATION",'HSHA',None),
 (r"INDIAN AFFAIRS",None,'SLIA'),(r"AGING COMM|COMMITTEE ON AGING",None,'SPAG'),(r"JOINT ECONOMIC",'JSEC','JSEC'),(r"JOINT COMMITTEE ON TAXATION|\bJCT\b",'JSTX','JSTX'),
 (r"ETHICS COMM|COMMITTEE ON ETHICS",'HSSO','SLET')]
COMM=[(re.compile(a),h,s) for a,h,s in COMM]
def committees_in(T):
  T=T.upper(); out=set()
  hs=bool(re.search(r"\bHOUSE\b|\bH\.\b|HASC|HFSC|HPSCI|HFAC",T)); ss=bool(re.search(r"\bSENATE\b|\bSEN\.?\b|SASC|SFC|SSCI|SFRC|HSGAC|EPW",T))
  for rx,h,s in COMM:
    if not rx.search(T): continue
    if h and not s: out.add(h)
    elif s and not h: out.add(s)
    elif h==s: out.add(h)
    else:
      if hs and not ss: out.add(h)
      elif ss and not hs: out.add(s)
      else: out.add(f'{h}|{s}?')
  return out
AG=[(r"WHITE HOUSE|\bEOP\b|EXECUTIVE OFFICE OF THE PRESIDENT",'White House/EOP'),(r"\bOMB\b|OFFICE OF MANAGEMENT AND BUDGET",'OMB'),(r"\bNSC\b|NATIONAL SECURITY COUNCIL",'NSC'),
 (r"\bUSTR\b|TRADE REPRESENTATIVE",'USTR'),(r"\bDOD\b|DEPARTMENT OF DEFENSE|DEFENSE DEPARTMENT|PENTAGON|SECRETARY OF DEFENSE|\bOSD\b",'DoD'),(r"\bARMY\b",'Army'),(r"\bNAVY\b|\bUSMC\b|MARINE CORPS",'Navy/USMC'),(r"AIR FORCE|\bUSAF\b",'Air Force'),
 (r"\bUSDA\b|DEPARTMENT OF AGRICULTURE",'USDA'),(r"\bDOE\b|DEPARTMENT OF ENERGY",'DOE'),(r"\bEPA\b|ENVIRONMENTAL PROTECTION AGENCY",'EPA'),(r"\bHHS\b|HEALTH (?:AND|&) HUMAN SERVICES",'HHS'),
 (r"\bCMS\b|CENTERS FOR MEDICARE",'CMS'),(r"\bFDA\b|FOOD AND DRUG",'FDA'),(r"\bNIH\b",'NIH'),(r"\bCDC\b",'CDC'),(r"TREASURY",'Treasury'),(r"\bIRS\b",'IRS'),(r"\bDOT\b|DEPARTMENT OF TRANSPORTATION",'DOT'),
 (r"\bFAA\b",'FAA'),(r"\bFCC\b",'FCC'),(r"\bFERC\b",'FERC'),(r"\bSEC\b(?! OF)|SECURITIES AND EXCHANGE",'SEC'),(r"\bCFTC\b",'CFTC'),(r"\bDHS\b|DEPARTMENT OF HOMELAND",'DHS'),
 (r"\bDOJ\b|DEPARTMENT OF JUSTICE|JUSTICE DEPARTMENT|\bFBI\b",'DOJ'),(r"STATE DEPARTMENT|DEPARTMENT OF STATE|\bDOS\b",'State'),(r"DEPARTMENT OF COMMERCE|COMMERCE DEPARTMENT|\bDOC\b",'Commerce Dept'),
 (r"DEPARTMENT OF LABOR|\bDOL\b",'DOL'),(r"\bHUD\b|HOUSING AND URBAN",'HUD'),(r"\bVA\b|VETERANS AFFAIRS(?! COMM)|DEPARTMENT OF VETERANS",'VA'),(r"\bDOI\b|DEPARTMENT OF (?:THE )?INTERIOR",'Interior'),
 (r"DEPARTMENT OF EDUCATION|\bED\b DEPT",'Education Dept'),(r"\bNASA\b",'NASA'),(r"\bUSAID\b",'USAID'),(r"\bSBA\b",'SBA'),(r"\bFTC\b|FEDERAL TRADE",'FTC'),(r"\bNRC\b|NUCLEAR REGULATORY",'NRC'),
 (r"\bOSTP\b",'OSTP'),(r"VICE PRESIDENT|\bOVP\b",'Office of the Vice President'),(r"FEDERAL RESERVE|\bFED\b BOARD",'Federal Reserve'),(r"\bFDIC\b",'FDIC'),(r"\bOCC\b|COMPTROLLER OF THE CURRENCY",'OCC'),(r"\bCFPB\b",'CFPB'),(r"\bGAO\b",'GAO'),(r"\bCBO\b",'CBO'),(r"\bCRS\b",'CRS')]
AG=[(re.compile(a),b) for a,b in AG]
NEG=re.compile(r"\bNOT (EMPLOYED|WORKED)|\bNEVER (EMPLOYED|WORKED)|\bN/?A\b$|^NONE$",re.I)
SELF=re.compile(r"\b(MEMBER OF CONGRESS|MEMBER,? (?:U\.?S\.? )?HOUSE|MEMBER OF THE (?:U\.?S\.? )?(?:HOUSE|SENATE)|FORMER MEMBER|U\.?S\.? REPRESENTATIVE|UNITED STATES REPRESENTATIVE|U\.?S\.? SENATOR|UNITED STATES SENATOR|^SENATOR$|^CONGRESSMAN$|^CONGRESSWOMAN$|^MEMBER$|MEMBER,? U\.?S\.? CONGRESS|^REPRESENTATIVE\b|ELECTED REPRESENTATIVE|CONGRESSMAN,? \d|CONGRESSWOMAN,? \d|MEMBER OF U\.?S\.? CONGRESS)",re.I)
STAFFW=re.compile(r"STAFF|AIDE|ASSIST|DIRECTOR|\bDIR\b|COUNSEL|CHIEF|ADVIS|\bLA\b|\bLD\b|\bLC\b|SCHEDUL|INTERN|FELLOW|SECRETARY|MANAGER|CORRESPOND|SPECIALIST|DEPUTY|PRESS|CLERK|ANALYST|\bCOS\b|POLICY|LIAISON|COORDINAT|REPRESENTATIVE FOR|CASEWORK|OUTREACH|COMMUNICATIONS",re.I)
clean=lambda s:re.sub(r"[^A-Z\- ]",'',s.upper().replace('.',' ')).strip()
# ---------- (A) covered positions from LD-2 raw ----------
CP=collections.defaultdict(lambda:{'q':set(),'f':None})
LNAME={}; LQ=collections.defaultdict(set)
for fn in sorted(glob.glob('../ld2/raw/ld2full_*.jsonl.gz')):
  for line in gzip.open(fn,'rt'):
    try: d=json.loads(line)
    except: continue
    q=f"{d['y']}{d['t'][:2]}"
    for a in d['acts']:
      for lid,fi,la,cp,new in a['l']:
        LNAME[lid]=(fi or '',la or ''); LQ[lid].add(q)
        if cp and cp.strip():
          x=CP[(lid,cp.strip())]; x['q'].add(q); x['f']=x['f'] or d['uuid']
print('covered (lobbyist,text) pairs',len(CP),file=sys.stderr)
def lobname(lid):
  pid=pid_of.get(lid,''); return pid,(prow[pid]['name'] if pid in prow else ' '.join(LNAME.get(lid,('',''))).strip().upper())
parsed=[]; staff_edges=[]; comm_edges=[]; agency_edges=[]; selfflags=collections.defaultdict(list); amb=[]
for (lid,cp),x in CP.items():
  pid,nm=lobname(lid)
  for seg in re.split(r'\s*(?:;|\|\||\n)\s*',cp):
    seg=seg.strip()
    if not seg or len(seg)<3: continue
    neg=bool(NEG.search(seg)); sf=bool(SELF.search(seg)) and not STAFFW.search(seg) and not re.search(r'OFFICE OF|EMPLOYEES? OF|\bTO (?:U\.?S\.? )?(?:SEN|REP)',seg,re.I)
    mem=ML.find(seg); coms=committees_in(seg); ags=sorted({b for rx,b in AG if rx.search(seg.upper())})
    resolved=[m for m in mem if m[0]]; unresolved=[m for m in mem if not m[0]]
    kinds=[]
    if sf: kinds.append('self_member')
    if resolved or unresolved: kinds.append('member_office')
    if coms: kinds.append('committee')
    if ags: kinds.append('executive_agency')
    if not kinds: kinds.append('other_or_unparsed')
    parsed.append([pid,lid,nm,str(lid) in scored,seg[:300],'|'.join(kinds),'|'.join(m[0] for m in resolved),'|'.join(m[3] for m in unresolved),'|'.join(sorted(coms)),'|'.join(ags),neg,min(x['q']),max(x['q']),x['f'],NOW])
    if neg: continue
    contact_list=len(mem)>=3 and not STAFFW.search(seg)
    for b,n,how,mt in resolved:
      if sf and not STAFFW.search(seg): continue   # self-identified member (handled in C)
      conf='high' if how=='first+last' else 'medium'
      if contact_list: conf='rejected_contact_list'
      staff_edges.append(dict(person_id=pid,lda_lobbyist_id=lid,lobbyist=nm,in_lobbyist_universe_scored=str(lid) in scored,bioguide=b,member=P[b]['name'],member_party=P[b]['party'],member_current=P[b]['current'],
        member_chamber_last=P[b]['chamber_last'],source='ld2_covered_position',office_or_title=seg[:300],staff_period='',match_how=how,confidence=conf,evidence=x['f'],first_quarter_listed=min(x['q']),computed_at=NOW))
    for b,n,how,mt in unresolved: amb.append([pid,lid,nm,seg[:300],mt,n,x['f']])
    for c in coms: comm_edges.append([pid,lid,nm,c,seg[:300],'ld2_covered_position','medium' if '?' in c else 'high',x['f'],NOW])
    for a in ags: agency_edges.append([pid,lid,nm,a,seg[:300],x['f'],NOW])
    if sf:
      ln=clean(LNAME.get(lid,('',''))[1])
      if not any(m[0] and ln and ln not in P[m[0]]['lasts'] for m in mem): selfflags[lid].append(seg[:200])
# ---------- (B) payroll ----------
NICK={}
for a,b in (('BOB','ROBERT'),('BILL','WILLIAM'),('JIM','JAMES'),('MIKE','MICHAEL'),('TOM','THOMAS'),('CHUCK','CHARLES'),('DICK','RICHARD'),('JOE','JOSEPH'),('DAN','DANIEL'),('DAVE','DAVID'),('STEVE','STEVEN'),('BEN','BENJAMIN'),('CHRIS','CHRISTOPHER'),('MATT','MATTHEW'),('PAT','PATRICK'),('DOUG','DOUGLAS'),('GREG','GREGORY'),('TIM','TIMOTHY'),('ROB','ROBERT'),('JEFF','JEFFREY'),('ANDY','ANDREW'),('RICK','RICHARD'),('DON','DONALD'),('RON','RONALD'),('KEN','KENNETH'),('LIZ','ELIZABETH'),('BETH','ELIZABETH'),('JON','JONATHAN'),('NICK','NICHOLAS'),('ALEX','ALEXANDER'),('SAM','SAMUEL'),('TONY','ANTHONY'),('KATIE','KATHERINE'),('KATE','KATHERINE'),('JOHNNY','JOHN'),('ZACH','ZACHARY'),('JAKE','JACOB'),('WILL','WILLIAM'),('MAX','MAXWELL'),('JOSH','JOSHUA'),('NATE','NATHAN'),('TED','EDWARD'),('ED','EDWARD'),('LARRY','LAWRENCE'),('JERRY','GERALD'),('BRAD','BRADLEY'),('FRED','FREDERICK'),('PETE','PETER'),('MARTY','MARTIN'),('TERRY','TERRENCE')):
  NICK[a]=b
canon=lambda f:NICK.get(f,f)
clean=lambda s:re.sub(r"[^A-Z\- ]",'',s.upper().replace('.',' ')).strip()
LK=collections.defaultdict(set)   # (last,first) -> person ids
for lid,(fi,la) in LNAME.items():
  f=clean(fi).split(); l=clean(la)
  if f and l: LK[(l,canon(f[0]))].add(pid_of.get(lid,f'lda{lid}'))
for pid,r in prow.items():
  for nm in r['merged_names'].split('|'):
    t=clean(nm).split()
    if len(t)>=2: LK[(t[-1],canon(t[0]))].add(pid)
pid_lids=collections.defaultdict(set)
for lid,p in pid_of.items(): pid_lids[p].add(lid)
def first_q(pid): 
  qs=set().union(*[LQ[l] for l in pid_lids.get(pid,[])]) if pid in pid_lids else set()
  return (min(qs),max(qs)) if qs else ('','')
MON={m:i for i,m in enumerate(['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC'],1)}
def dparse(s):
  m=re.match(r'(\d{1,2})-([A-Za-z]{3})-(\d{2,4})',s or '')
  if m: y=int(m.group(3)); y=y+2000 if y<100 else y; return f"{y:04d}-{MON.get(m.group(2).upper(),1):02d}-{int(m.group(1)):02d}"
  m=re.match(r'(\d{1,2})/(\d{1,2})/(\d{2,4})',s or '')
  if m: y=int(m.group(3)); y=y+2000 if y<100 else y; return f"{y:04d}-{int(m.group(1)):02d}-{int(m.group(2)):02d}"
  return ''
off_cache={}
def house_office(o):
  if o in off_cache: return off_cache[o]
  m=re.match(r'^(?:FISCAL YEAR )?(\d{4})\s+(.*)$',o.strip()); yr=int(m.group(1)) if m else None; rest=(m.group(2) if m else o).strip()
  res=('institutional',rest,None)
  mh=re.match(r'^HON\.?\s+(.*)$',rest)
  if mh:
    nm=re.sub(r'"[^"]*"','',mh.group(1)); nm=re.sub(r'\b(JR|SR|II|III|IV)\b\.?','',nm).replace(',',' ')
    t=[x for x in clean(nm).split() if len(x)>1]
    b=None
    if t:
      for sl in (2,1):
        if len(t)>sl or (sl==1 and t):
          sur=' '.join(t[-sl:]) if len(t)>=sl else t[-1]
          b,n,how=ML.resolve(sur,t[0] if len(t)>sl else None,'rep',yr)
          if b: break
    res=('member_office',rest,b)
  else:
    c=committees_in('HOUSE '+rest)
    if c and 'COMMITTEE' in rest or rest.startswith('PERMANENT SELECT') : res=('committee',rest,'|'.join(sorted(c)) or None)
    elif re.search(r'SPEAKER|MAJORITY LEADER|MINORITY LEADER|WHIP|CAUCUS|CONFERENCE',rest): res=('leadership',rest,None)
  off_cache[o]=(yr,)+res; return off_cache[o]
SENCOMM={'JUDICIARY':'SSJU','APPROPRIATIONS':'SSAP','FINANCE':'SSFI','HEALTH':'SSHR','COMMERCE':'SSCM','FOREIGN RELATIONS':'SSFR','BANKING':'SSBK','ARMED SERVICES':'SSAS','HOMELAND SECURITY & GOVERNMENTAL AFFAIRS':'SSGA','HOMELAND SECURITY AND GOVERNMENTAL AFFAIRS':'SSGA',
 'ENERGY AND NATURAL RESOURCES':'SSEG','ENERGY & NATURAL RESOURCES':'SSEG','ENVIRONMENT AND PUBLIC WORKS':'SSEV','ENVIRONMENT & PUBLIC WORKS':'SSEV','AGRICULTURE':'SSAF','BUDGET':'SSBU','INTELLIGENCE':'SLIN','RULES AND ADMINISTRATION':'SSRA','RULES & ADMINISTRATION':'SSRA',
 'VETERANS':'SSVA',"VETERANS' AFFAIRS":'SSVA','SMALL BUSINESS':'SSSB','INDIAN AFFAIRS':'SLIA','AGING':'SPAG','ETHICS':'SLET'}
def senate_office(o):
  if o in off_cache: return off_cache[o]
  o2=o.strip().strip('"').upper()
  if o2.startswith('SENATOR '):
    t=[x for x in clean(re.sub(r'\b(JR|SR|II|III)\b','',o2[8:]).replace(',',' ')).split() if len(x)>1]
    b=None
    for sl in (2,1):
      if len(t)>sl:
        b,n,how=ML.resolve(' '.join(t[-sl:]),t[0],'sen')
        if b: break
    if not b and t: b,n,how=ML.resolve(t[-1],None,'sen')
    r=(None,'member_office',o2,b)
  else:
    k=next((v for kk,v in SENCOMM.items() if o2.startswith(kk)),None)
    if k: r=(None,'committee',o2,k)
    elif re.search(r'LEADER|WHIP|CONFERENCE|POLICY COMMITTEE|SECRETARY FOR THE M',o2): r=(None,'leadership',o2,None)
    else: r=(None,'institutional',o2,None)
  off_cache[o]=r; return r
# Senate report period: reports listed newest-first on senate.gov; each covers 6 months (Oct1-Mar31 / Apr1-Sep30).
# Anchor verified from 118sdoc13 text ('04/01/2024 THRU 09/30/2024'); index 0 = 2025-10-01..2026-03-31.
_su=[]; [_su.append(re.sub(r'-[12]\.pdf$','',u.strip().split('/')[-1])) for u in open('raw/senate_secsen_urls.txt') if re.sub(r'-[12]\.pdf$','',u.strip().split('/')[-1]) not in _su]
SENPER={}
for i,d in enumerate(_su):
  half=i%2; yr=2025-i//2
  SENPER[d]=(f'{yr}-10-01',f'{yr+1}-03-31') if half==0 else (f'{yr}-04-01',f'{yr}-09-30')
assert SENPER.get('GPO-CDOC-118sdoc13')==('2024-04-01','2024-09-30'),SENPER.get('GPO-CDOC-118sdoc13')
ST=collections.defaultdict(lambda:{'start':'9999','end':'0000','usd':0.0,'titles':collections.Counter(),'src':set(),'raw':set()})
for row in csv.reader(gzip.open('raw/sod_personnel_rows.csv.gz','rt')):
  f,o,v,title,s,e,amt,c=row
  yr,kind,oname,key=house_office(o)
  t=clean(v).split()
  if len(t)<2: continue
  keys={(t[0],canon(t[1]))}
  if len(t)>=3: keys.add((t[0]+' '+t[1],canon(t[2]))); keys.add((t[0]+'-'+t[1],canon(t[2])))
  sd=dparse(s); ed=dparse(e)
  for k in keys:
    x=ST[(k,'House',kind,oname if kind!='member_office' else key or oname)]
    if sd: x['start']=min(x['start'],sd)
    if ed: x['end']=max(x['end'],ed)
    try: x['usd']+=float(amt)
    except: pass
    x['titles'][title]+=1; x['src'].add('house_sod:'+f); x['raw'].add(v)
for row in csv.reader(gzip.open('raw/senate_payroll_rows.csv.gz','rt')):
  f,o,v,title,amt=row
  _,kind,oname,key=senate_office(o)
  if ',' not in v: continue
  la,fi=v.split(',',1); la=clean(la); ft=clean(fi).split()
  if not la or not ft: continue
  k=(la,canon(ft[0]))
  x=ST[(k,'Senate',kind,key or oname)]
  m=re.search(r'GPO-CDOC-(\d{3})sdoc(\d+)',f); x['src'].add(f'senate_secsen:{m.group(1)}sdoc{m.group(2)}' if m else f)
  ps,pe=SENPER.get(re.sub(r'-[12]\.pdf$','',f),('',''))
  if ps: x['start']=min(x['start'],ps); x['end']=max(x['end'],pe)
  try: x['usd']+=float(amt)
  except: pass
  x['titles'][re.sub(r'\s+(TO|FROM) [A-Z]{3}\.? \d+.*$','',title)]+=1; x['raw'].add(v)
print('staff records',len(ST),file=sys.stderr)
# senate report period -> approximate dates from doc number (semiannual; 112th..119th) not parsed; senate staff_period left as report ids.
cov_by_pid=collections.defaultdict(set)
for e in staff_edges: cov_by_pid[e['person_id']].add(e['bioguide'])
comm_by_pid=collections.defaultdict(set)
for r_ in comm_edges: comm_by_pid[r_[0]].update(r_[3].replace('?','').split('|'))
cands=[]
staffname_n=collections.Counter(k for (k,ch,kind,o) in ST)
for (k,ch,kind,o),x in ST.items():
  pids=LK.get(k)
  if not pids: continue
  for pid in pids:
    fq,lq=first_q(pid)
    bio=o if kind=='member_office' and o in P else ''
    comm=o if kind=='committee' else ''
    corroborated=(bio and bio in cov_by_pid.get(pid,set())) or (comm and any(c in comm_by_pid.get(pid,set()) for c in comm.split('|')))
    overlap=''
    if x['end']!='0000' and fq:
      fy,fqq=int(fq[:4]),int(fq[5]); lob_start=f"{fy}-{(fqq-1)*3+1:02d}-01"
      if x['end']>lob_start and x['end']>=f"{fy}-{(fqq-1)*3+1:02d}-01" and x['start']<f"{lq[:4]}-12-31" and x['end'][:7]>lob_start[:7]:
        overlap='payroll_overlaps_lda_lobbying_period'
    if corroborated: conf='high'
    elif len(pids)==1 and not overlap and x['usd']>0: conf='medium'
    else: conf='low'
    cands.append(dict(person_id=pid,lobbyist=prow[pid]['name'] if pid in prow else '',in_lobbyist_universe_scored=pid in scored,staff_name_raw='|'.join(sorted(x['raw']))[:120],chamber=ch,office_kind=kind,
      bioguide=bio,member=P[bio]['name'] if bio else '',member_party=P[bio]['party'] if bio else '',member_current=P[bio]['current'] if bio else '',committee=comm,office=o if not bio else P[bio]['name'],
      staff_start=x['start'] if x['start']!='9999' else '',staff_end=x['end'] if x['end']!='0000' else '',payroll_usd=round(x['usd']),top_titles='|'.join(t for t,_ in x['titles'].most_common(3))[:200],
      lda_first_quarter=fq,lda_last_quarter=lq,n_people_with_name=len(pids),corroborated_by_covered_position=bool(corroborated),timeline_flag=overlap,confidence=conf,sources='|'.join(sorted(x['src']))[:300],computed_at=NOW))
def W(fn,rows,hdr=None):
  rows=list(rows)
  if not rows: print('EMPTY',fn,file=sys.stderr); return 0
  op=gzip.open(fn,'wt',newline='') if fn.endswith('.gz') else open(fn,'w',newline='')
  with op as f:
    if isinstance(rows[0],dict): w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    else: w=csv.writer(f); w.writerow(hdr); w.writerows(rows)
  print(fn,len(rows),file=sys.stderr); return len(rows)
cnt={}
cnt['covered_position_parsed']=W('covered_position_parsed.csv.gz',parsed,['person_id','lda_lobbyist_id','lobbyist','in_lobbyist_universe_scored','segment','kinds','member_bioguides','unresolved_member_mentions','committees','agencies','negated','first_quarter','last_quarter','sample_filing_uuid','computed_at'])
cnt['covered_position_ambiguous_member']=W('covered_position_ambiguous_member.csv',amb,['person_id','lda_lobbyist_id','lobbyist','segment','mention','n_candidate_members','sample_filing_uuid'])
# merge covered-position + payroll into one former-staffer->member edge table
pay=[c for c in cands if c['bioguide'] and c['confidence'] in ('high','medium')]
E=[]
for e in staff_edges: E.append(e)
for c in pay:
  E.append(dict(person_id=c['person_id'],lda_lobbyist_id='',lobbyist=c['lobbyist'],in_lobbyist_universe_scored=c['in_lobbyist_universe_scored'],bioguide=c['bioguide'],member=c['member'],member_party=c['member_party'],member_current=c['member_current'],
    member_chamber_last=P[c['bioguide']]['chamber_last'],source=f"{c['chamber'].lower()}_payroll",office_or_title=c['top_titles'],staff_period=f"{c['staff_start']}..{c['staff_end']}",match_how='name_match_payroll',confidence=c['confidence'],evidence=c['sources'],first_quarter_listed=c['lda_first_quarter'],computed_at=NOW))
cnt['edges_former_staffer_member']=W('edges_former_staffer_member.csv',E)
# pair-level summary
PS=collections.defaultdict(lambda:{'src':set(),'conf':set(),'row':None})
for e in E:
  if e['confidence'].startswith('rejected'): continue
  k=(e['person_id'],e['bioguide']); PS[k]['src'].add(e['source']); PS[k]['conf'].add(e['confidence']); PS[k]['row']=PS[k]['row'] or e
rank={'high':3,'medium':2,'low':1}
pairs=[dict(person_id=k[0],lobbyist=v['row']['lobbyist'],bioguide=k[1],member=v['row']['member'],member_party=v['row']['member_party'],member_current=v['row']['member_current'],
  sources='|'.join(sorted(v['src'])),n_sources=len(v['src']),best_confidence=max(v['conf'],key=lambda c:rank.get(c,0)),computed_at=NOW) for k,v in PS.items()]
for p in pairs:
  if p['n_sources']>=2: p['best_confidence']='high'
cnt['former_staffer_member_pairs']=W('former_staffer_member_pairs.csv',sorted(pairs,key=lambda p:(-p['n_sources'],p['lobbyist'])))
cnt['payroll_name_matches_all']=W('payroll_name_matches_all.csv.gz',cands)
cnt['edges_former_staffer_committee']=W('edges_former_staffer_committee.csv',comm_edges+[[c['person_id'],'',c['lobbyist'],c['committee'],c['top_titles'],f"{c['chamber'].lower()}_payroll {c['staff_start']}..{c['staff_end']}",c['confidence'],c['sources'][:200],NOW] for c in cands if c['committee'] and c['confidence'] in ('high','medium')],
  ['person_id','lda_lobbyist_id','lobbyist','committee_ids','text','source','confidence','evidence','computed_at'])
cnt['edges_lobbyist_former_agency']=W('edges_lobbyist_former_agency.csv',agency_edges,['person_id','lda_lobbyist_id','lobbyist','agency','covered_position_segment','sample_filing_uuid','computed_at'])
# ---------- (C) former members ----------
PALL=ML._people('1970-01-01'); FULLK=collections.defaultdict(set)
for b,p in PALL.items():
  for f in p['firsts']:
    for l in p['lasts']: FULLK[(l,f)].add(b)

FM=[]
for lid in set(LNAME)|set(selfflags):
  fi,la=LNAME.get(lid,('',''))
  pid,nm=lobname(lid)
  f=clean(fi).split(); l=clean(la)
  b=None;how=''
  if f and l:
    c=set()
    for ft in f:
      c=FULLK.get((l,ft),set()) or FULLK.get((l,canon(ft)),set())
      if c: break
    if len(c)==1: b=next(iter(c))
  sf=selfflags.get(lid)
  if not (b or sf): continue
  lastonly=False
  if sf and not b and l:
    c=set().union(*[v for (ll,ff),v in FULLK.items() if ll==l]) if any(ll==l for (ll,ff) in FULLK) else set()
    c={x for x in c if not PALL[x]['current']}
    if len(c)==1: b=next(iter(c)); lastonly=True
  if b and sf: conf='self_identified_lastname_match' if lastonly else 'high'
  elif sf: conf='self_identified_name_unmatched'
  else: conf='name_only_unverified'
  FM.append(dict(person_id=pid,lda_lobbyist_id=lid,lobbyist=nm,in_lobbyist_universe_scored=str(lid) in scored,self_identified=bool(sf),self_id_text=(sf or [''])[0],bioguide=b or '',member=PALL[b]['name'] if b else '',
    member_party=PALL[b]['party'] if b else '',chambers='|'.join(sorted({t[0] for t in PALL[b]['terms']})) if b else '',last_term_end=max(t[2] for t in PALL[b]['terms']) if b else '',still_current=PALL[b]['current'] if b else '',confidence=conf,computed_at=NOW))
FM=[x for x in FM if not (x['confidence']=='name_only_unverified' and (x['still_current'] or x['last_term_end']<'1995'))]
_seen=set(); FM=[x for x in sorted(FM,key=lambda x:x['confidence']!='high') if not ((x['person_id'] or x['lda_lobbyist_id']) in _seen or _seen.add(x['person_id'] or x['lda_lobbyist_id']))]
cnt['former_member_lobbyists']=W('former_member_lobbyists.csv',sorted(FM,key=lambda x:(x['confidence']!='high',x['lobbyist'])))
json.dump(dict(counts=cnt,confidence=collections.Counter(e['confidence'] for e in E),payroll_confidence=collections.Counter(c['confidence'] for c in cands),computed_at=NOW),open('build_stats_revolving.json','w'),indent=1,default=str)
