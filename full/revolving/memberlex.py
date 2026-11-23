# Member lexicon for the ld2/revolving/fara layers: every legislator with a term ending on/after SINCE (default 2009-01-03),
# keyed by bioguide. Conservative name finder: title-anchored surname (+optional first) or exact full name.
import json,re,collections,unicodedata
UA=lambda s:unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode()
R='/workspace/gop-lobby-graph/raw/'
CUR=json.load(open(R+'legislators-current.json')); HIS=json.load(open(R+'legislators-historical.json'))
CURRENT={l['id']['bioguide'] for l in CUR}
PARTY={'Republican':'R','Democrat':'D','Independent':'I'}
def _people(since='2009-01-03'):
  out={}
  for l in CUR+HIS:
    ts=[t for t in l['terms'] if t['end']>=since]
    if not ts: continue
    n=l['name']; firsts={UA(n['first']).upper().strip('.')}
    if n.get('middle'): firsts.add(UA(n['middle']).upper().strip('.'))
    if n.get('nickname'): firsts.add(n['nickname'].upper())
    if n.get('official_full'): firsts.add(n['official_full'].split()[0].upper().strip('.'))
    for nick,full in (('BOB','ROBERT'),('BILL','WILLIAM'),('JIM','JAMES'),('MIKE','MICHAEL'),('TOM','THOMAS'),('CHUCK','CHARLES'),('DICK','RICHARD'),('JOE','JOSEPH'),('DAN','DANIEL'),('DAVE','DAVID'),('STEVE','STEVEN'),('TED','EDWARD'),('BEN','BENJAMIN'),('CHRIS','CHRISTOPHER'),('MATT','MATTHEW'),('PAT','PATRICK'),('DOUG','DOUGLAS'),('GREG','GREGORY'),('TIM','TIMOTHY'),('ROB','ROBERT'),('ED','EDWARD'),('JEFF','JEFFREY'),('ANDY','ANDREW'),('RICK','RICHARD'),('DON','DONALD'),('RON','RONALD'),('KEN','KENNETH'),('LIZ','ELIZABETH'),('BETH','ELIZABETH'),('JON','JONATHAN'),('JOHNNY','JOHN'),('DREW','ANDREW'),('RANDY','RANDALL'),('TRENT','CHESTER')):
      if nick in firsts: firsts.add(full)
      if full in firsts: firsts.add(nick)
    last=UA(n['last']).upper()
    out[l['id']['bioguide']]=dict(bio=l['id']['bioguide'],last=last,lasts={last,last.replace(' ',''),last.split()[-1]} if ' ' in last else {last},firsts=firsts,
      name=n.get('official_full') or f"{n['first']} {n['last']}",party=PARTY.get(ts[-1].get('party'),'O'),current=l['id']['bioguide'] in CURRENT,
      terms=[(t['type'],t['start'],t['end'],t['state']) for t in ts],chamber_last='Senate' if ts[-1]['type']=='sen' else 'House',state=ts[-1]['state'])
  return out
P=_people()
BYLAST=collections.defaultdict(list)
for p in P.values():
  for la in p['lasts']: BYLAST[la].append(p)
def served(p,chamber=None,year=None):
  for ty,s,e,st in p['terms']:
    if chamber and ty!=chamber: continue
    if year and not (int(s[:4])<=year<=int(e[:4])): continue
    return True
  return False
def resolve(last,first=None,chamber=None,year=None,state=None):
  """returns (bioguide or None, n_candidates, how)"""
  c=BYLAST.get(last.upper(),[])
  if chamber: c=[p for p in c if served(p,chamber)]
  if year: 
    c2=[p for p in c if served(p,chamber,year)]
    if c2: c=c2
  if state:
    c2=[p for p in c if any(t[3]==state for t in p['terms'])]
    if c2: c=c2
  if first:
    f=first.upper().strip('.')
    c2=[p for p in c if f in p['firsts']]
    if c2: c=c2; how='first+last'
    else: how='last_only_first_mismatch'
  else: how='last_only'
  if len(c)==1: return c[0]['bio'],1,how
  return None,len(c),how
TITLE=re.compile(r"\b(SENATOR|SEN\.?|REP\.?|REPRESENTATIVE|CONGRESSMAN|CONGRESSWOMAN|CONG\.|HON\.?|LEADER|SPEAKER|WHIP|OFFICE OF)\s+((?:(?!(?:SENATOR|SEN|REP|REPRESENTATIVE|CONGRESSMAN|CONGRESSWOMAN|OFFICE)\b)[A-Z][A-Z\.'\-]*\s?){1,4})")
STOP={'THE','OF','AND','STAFF','OFFICE','COMMITTEE','FOR','ON','MAJORITY','MINORITY','DEMOCRATIC','REPUBLICAN','CHIEF','LEGISLATIVE','SENIOR','HOUSE','SENATE','US','U','S','FROM','TO','IN','AT','REP','SEN','SENATOR','DR','MR','MS','MRS','JR','SR','II','III'}
def find(text,year=None,current_only=False):
  """list of (bioguide|None, n_candidates, how, matched_text). Title-anchored ('Senator X', 'Rep. First Last', 'Office of ...')."""
  T=re.sub(r'\s+',' ',text).upper(); out=[]; seen=set()
  for m in TITLE.finditer(T):
    title=m.group(1); raw=[t.strip('.') for t in m.group(2).replace('.',' ').split()]
    toks=[]
    for t in raw:
      if t in STOP and toks: break
      if t in STOP: continue
      if len(t)==1: continue   # middle initials
      toks.append(t)
    if not toks: continue
    ch='sen' if title.startswith('SEN') else ('rep' if title[:3] in ('REP','CON') else None)
    best=None
    for end in range(len(toks),0,-1):
      for sl in (3,2,1):
        if end-sl<0: continue
        sur=' '.join(toks[end-sl:end])
        if sur not in BYLAST: continue
        first=toks[0] if end-sl>0 else None
        b,n,how=resolve(sur,first,ch,year)
        if b: best=(b,1,how,(title+' '+' '.join(toks[:end])).title()); break
        if n>1 and best is None: best=(None,n,how,(title+' '+' '.join(toks[:end])).title())
      if best and best[0]: break
    if not best: continue
    if best[0]:
      if best[0] in seen or (current_only and not P[best[0]]['current']): continue
      seen.add(best[0])
    out.append(best)
  return out
