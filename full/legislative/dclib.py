# Shared helpers for the DC-wide layers (legislative/, executive/, ethics/, state_events/).
# Org/person matching against the LDA universe already in the repo (lda/ld2_universe, money_all/people_all.csv).
import os,re,csv,json,gzip,glob,shutil,datetime,unicodedata
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .../full
REPO=os.path.dirname(ROOT)
TMP='/workspace/tmp_dcgraph'
NOW=lambda: datetime.datetime.now().astimezone().isoformat(timespec='seconds')
TS=datetime.datetime.now().astimezone().strftime('%Y%m%d_%H%M')
def keep_prev(fn):
  if os.path.exists(fn):
    b,e=os.path.splitext(fn); dst=f'{b}.prev_{TS}{e}'
    if not os.path.exists(dst): shutil.copy2(fn,dst)
  return fn
def wcsv(fn,header,rows):
  keep_prev(fn); n=0
  with open(fn,'w',newline='') as f:
    w=csv.writer(f); w.writerow(header)
    for r in rows: w.writerow(r); n+=1
  return n
SUFFIX=r'\b(INC|INCORPORATED|LLC|L L C|LLP|LP|CORP|CORPORATION|CO|COMPANY|LTD|LIMITED|PLC|NA|N A|THE|AND|OF|USA|US|U S|AMERICA|GROUP|HOLDINGS|PC|PLLC|AG|SA|NV|SE)\b'
def norm_org(s):
  if not s: return ''
  s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().upper()
  s=re.sub(r'\(.*?\)',' ',s); s=s.replace('&',' AND ')
  s=re.sub(r'[^A-Z0-9 ]',' ',s); s=re.sub(SUFFIX,' ',s)
  return re.sub(r'\s+',' ',s).strip()
def norm_person(s):
  s=unicodedata.normalize('NFKD',s or '').encode('ascii','ignore').decode().upper()
  s=re.sub(r'\b(MR|MRS|MS|DR|HON|THE HONORABLE|HONORABLE|JR|SR|II|III|IV|PHD|ESQ|MD|JD)\b\.?',' ',s)
  s=re.sub(r'[^A-Z ]',' ',s); t=s.split()
  t=[x for x in t if len(x)>1]
  return (t[0],t[-1]) if len(t)>=2 else None
_ORG=None
def org_index():
  """norm org name -> dict(kind set, client ids, registrant ids, display, lda lobbyist ids)"""
  global _ORG
  if _ORG is not None: return _ORG
  cache=os.path.join(TMP,'org_index.json')
  if os.path.exists(cache):
    _ORG=json.load(open(cache)); return _ORG
  idx={}
  for fn in sorted(glob.glob(os.path.join(REPO,'lda/ld2_universe/ld2_*.jsonl.gz'))):
    for line in gzip.open(fn,'rt'):
      r=json.loads(line); lobs=set()
      for a in r.get('acts') or []:
        for l in a.get('lob') or []: lobs.add(l[0])
      for kind,nm,i in (('client',r.get('cn'),r.get('cid')),('registrant',r.get('rn'),r.get('rid'))):
        k=norm_org(nm)
        if len(k)<3: continue
        d=idx.setdefault(k,{'name':nm,'kinds':[],'client_ids':[],'registrant_ids':[],'lob':[] ,'n_filings':0})
        if kind not in d['kinds']: d['kinds'].append(kind)
        L=d['client_ids'] if kind=='client' else d['registrant_ids']
        if i not in L: L.append(i)
        d['lob']=sorted(set(d['lob'])|lobs)[:400]; d['n_filings']+=1
  os.makedirs(TMP,exist_ok=True); json.dump(idx,open(cache,'w')); _ORG=idx; return idx
_PEOPLE=None
def people_index():
  """(FIRST,LAST) -> list of (person_id,name,main_registrant,set(lda ids)); also lda id -> person_id"""
  global _PEOPLE
  if _PEOPLE: return _PEOPLE
  byname={}; byid={}
  for r in csv.DictReader(open(os.path.join(ROOT,'money_all/people_all.csv'))):
    ids=r['person_key'].split('|')
    for i in ids: byid[i]=r['person_id']
    for nm in set(r['merged_names'].split('|')+[r['name']]):
      k=norm_person(nm)
      if k: byname.setdefault(k,[]).append((r['person_id'],r['name'],r['main_registrant'],r['registrants']))
  _PEOPLE=(byname,byid); return _PEOPLE
def last_key(last):
  k=norm_person('XX '+(last or '')); return k[1] if k else (last or '').upper()
def match_org(name):
  k=norm_org(name); idx=org_index()
  if k in idx: return k,idx[k],'exact_norm'
  return k,None,None
_MEM=None
def members():
  """bioguide -> dict(name,party,state,chamber current) incl. historical since 2021"""
  global _MEM
  if _MEM: return _MEM
  M={}
  for fn,cur in ((os.path.join(REPO,'raw/legislators-historical.json'),0),(os.path.join(TMP,'lc.json') if os.path.exists(os.path.join(TMP,'lc.json')) else os.path.join(REPO,'raw/legislators-current.json'),1)):
    for p in json.load(open(fn)):
      t=p['terms'][-1]
      if not cur and t['end']<'2021-01-01': continue
      nm=p['name']; M[p['id']['bioguide']]={'name':nm.get('official_full') or f"{nm['first']} {nm['last']}",'first':nm['first'],'last':nm['last'],'nick':nm.get('nickname',''),
        'party':(t.get('party') or '')[:1],'state':t['state'],'chamber':'House' if t['type']=='rep' else 'Senate','current':cur,'district':t.get('district',''),
        'chambers':sorted({'House' if x['type']=='rep' else 'Senate' for x in p['terms'] if x['end']>='2021-01-01'}),'districts':sorted({str(x.get('district','')) for x in p['terms'] if x['type']=='rep' and x['end']>='2021-01-01'})}
  _MEM=M; return M
_MNAME=None
_N=[('MICHAEL','MIKE'),('WILLIAM','BILL'),('ROBERT','BOB'),('JAMES','JIM'),('THOMAS','TOM'),('RICHARD','RICK'),('RICHARD','DICK'),('CHARLES','CHUCK'),('JOSEPH','JOE'),('DANIEL','DAN'),('DAVID','DAVE'),('EDWARD','ED'),('GERALD','JERRY'),('GREGORY','GREG'),('KENNETH','KEN'),('ANTHONY','TONY'),('STEVEN','STEVE'),('STEPHEN','STEVE'),('TIMOTHY','TIM'),('ANDREW','ANDY'),('BENJAMIN','BEN'),('CHRISTOPHER','CHRIS'),('DONALD','DON'),('DOUGLAS','DOUG'),('FREDERICK','FRED'),('GERALD','GERRY'),('JEFFREY','JEFF'),('JONATHAN','JON'),('JOHN','JACK'),('LAWRENCE','LARRY'),('MATTHEW','MATT'),('NICHOLAS','NICK'),('PATRICK','PAT'),('PETER','PETE'),('RAYMOND','RAY'),('RONALD','RON'),('SAMUEL','SAM'),('ZACHARY','ZACH'),('ALEXANDRIA','ALEX'),('KATHERINE','KATHY'),('KATHERINE','KATIE'),('ELIZABETH','LIZ'),('ELIZABETH','BETH'),('PATRICIA','PAT'),('DEBORAH','DEBBIE'),('SUSAN','SUE'),('MARGARET','MAGGIE'),('ABIGAIL','ABBY'),('BRADLEY','BRAD'),('BRANDON','BRAD'),('VINCENT','VINCE'),('THEODORE','TED'),('RAFAEL','TED'),('JAMES','JAMIE'),('ROBERT','BOBBY'),('WILLIAM','BILLY'),('ALBERT','AL'),('LOUIS','LOU'),('EUGENE','GENE'),('HAROLD','HAL'),('CHARLES','CHARLIE')]
NICK={}
for a,b in _N: NICK.setdefault(a,[]).append(b); NICK.setdefault(b,[]).append(a)
def member_by_name(first,last,state=None):
  global _MNAME
  if _MNAME is None:
    _MNAME={}
    for b,m in members().items():
      L=norm_person('XX '+m['last'])[1] if norm_person('XX '+m['last']) else m['last'].upper()
      for f in {m['first'],m['nick']}:
        if f: _MNAME.setdefault((f.upper().split()[0],L),[]).append(b)
      _MNAME.setdefault(('*',L),[]).append(b)
  c=_MNAME.get((first.upper(),last.upper()),[])
  if not c:
    for f2 in NICK.get(first.upper(),[]):
      c=c or _MNAME.get((f2,last.upper()),[])
  if state: c=[b for b in c if members()[b]['state']==state] or c
  return c
