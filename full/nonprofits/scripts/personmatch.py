# Shared person matcher for nonprofits/, boards/ and 527 data (name-only sources: 990 officers, SEC directors, 527 contributors).
# Lobbyists: people_all.csv person_id; names from LD-2/LD-203 (first+last as filed) incl. nickname variants (full/nicks.py).
# Confidence:
#   high_org_link   : name matches exactly one lobbyist AND the org (normalized) is that lobbyist's LDA client or registrant (2023-26)
#   medium_unique   : name matches exactly one lobbyist in the 21,4k universe, AND that (last,first) key is rare (<=1 lobbyist) and last name is not among the 2,000 most common US-style surnames in the FEC indiv sample; no org link
#   low_name_only   : name matches but common surname or several candidates -> NOT an edge, written to ambiguous files only
# Members/former members: congress-legislators current+historical (terms since 1990); exact first(or nickname/official first)+last.
#   high_title_or_org : name match + title/org text mentions Congress/Senator/Rep/Former Member/Governor
#   medium_name_former_member : unique FORMER legislator name, uncommon surname, no context
#   low_name_only : current-member namesake risk, common surname, or several legislators share the name (ambiguous files only)
import csv,gzip,json,glob,re,sys,collections,unicodedata
sys.path.insert(0,'/workspace/gop-lobby-graph/full'); sys.path.insert(0,'/workspace/gop-lobby-graph/full/boards/scripts')
from nicks import NICK
from orgnorm import key as okey
import partylex as PL
TIT={'MR','MRS','MS','DR','HON','THE','HONORABLE','REV','SIR','PROF','AMB','GEN','ADM','COL','SEN','REP','SENATOR','CONGRESSMAN','JR','SR','II','III','IV','V','PHD','MD','ESQ','CPA','JD','MBA','DDS','RN','CFA','PE','DVM','LLM','EDD','USN','USA','USMC','USAF','RET','DECEASED','FORMER','EX','OFFICIO'}
def nm(s):
  s=unicodedata.normalize('NFKD',s or '').encode('ascii','ignore').decode().upper()
  s=re.sub(r'\(.*?\)','',s)
  if ',' in s:
    a,b=s.split(',',1)
    bt=[t for t in re.split(r'[^A-Z\-\']+',b) if t and t not in TIT]
    at=[t for t in re.split(r'[^A-Z\-\']+',a) if t and t not in TIT]
    if bt and at and len(at)<=3: return at[-1] if len(at)==1 else ' '.join(at), bt[0], bt[1:]
  t=[x for x in re.split(r'[^A-Z\-\']+',s) if x and x not in TIT]
  if len(t)<2: return None
  return t[-1], t[0], t[1:-1]
def variants(f):
  v={f}|set(NICK.get(f,[]))|{k for k,vs in NICK.items() if f in vs}
  return v
P={r['person_id']:r for r in csv.DictReader(open('/workspace/gop-lobby-graph/full/money_all/people_all.csv'))}
lid2p={i:r['person_id'] for r in P.values() for i in r['person_key'].split('|')}
IDX=collections.defaultdict(set); ORGS=collections.defaultdict(set)
for fn in glob.glob('/workspace/gop-lobby-graph/lda/ld2_universe/*.jsonl.gz'):
  for line in gzip.open(fn,'rt'):
    d=json.loads(line)
    if d['y']<2023: continue
    ck=okey(d['cn']); rk=okey(d['rn'])
    for a in d['acts']:
      for lid,fi,la,_ in a['lob']:
        p=lid2p.get(str(lid))
        if not p or not fi or not la: continue
        r=nm(f"{fi} {la}")
        if r: 
          for f in variants(r[1]): IDX[(r[0],f)].add(p)
        if ck: ORGS[p].add(ck)
        if rk: ORGS[p].add(rk)
for p,r in P.items():
  x=nm(r['name'])
  if x:
    for f in variants(x[1]): IDX[(x[0],f)].add(p)
SURN=collections.Counter(k[0] for k in IDX)
LEG=collections.defaultdict(list)
for l in json.load(open('/workspace/gop-lobby-graph/raw/legislators-current.json'))+json.load(open('/workspace/gop-lobby-graph/raw/legislators-historical.json')):
  ts=[t for t in l['terms'] if t['end']>='1990-01-01']
  if not ts: continue
  n=l['name']; last=nm('X '+n['last'])[0] if nm('X '+n['last']) else n['last'].upper()
  firsts={n['first'].upper().strip('.')}
  if n.get('nickname'): firsts.add(n['nickname'].upper())
  if n.get('official_full'): firsts.add(n['official_full'].split()[0].upper().strip('.'))
  if n['first'].endswith('.') and n.get('middle'): firsts.add(n['middle'].upper())
  fs=set()
  for f in firsts: fs|=variants(f)
  cur=ts[-1]['end']>='2026-01-03'
  rec=dict(bioguide=l['id']['bioguide'],name=n.get('official_full') or n['first']+' '+n['last'],party=ts[-1].get('party',''),current=cur,last_term_end=ts[-1]['end'],middle=(n.get('middle') or '').upper()[:1])
  for f in fs: LEG[(last,f)].append(rec)
# tightened 2026-11-22: bare 'REPRESENTATIVE'/'GOVERNOR' matched trade-association titles (e.g. NAR regional reps, boards of governors)
CONGW=re.compile(r"\bCONGRESS(MAN|WOMAN|IONAL)?\b|\bSENATOR\b|\bU\.?S\.? SENATE\b|\bHOUSE OF REPRESENTATIVES\b|\bFORMER MEMBER OF (CONGRESS|THE HOUSE)|\b(FORMER|RET\.?) (U\.?S\.? )?(REP\.?|SEN\.?)\s",re.I)
def match_lobbyist(fullname,org_name='',org_keys=()):
  x=nm(fullname)
  if not x: return None
  c=IDX.get((x[0],x[1]),set())
  if not c: return None
  oks={okey(org_name)}|set(org_keys); oks.discard('')
  if len(c)==1:
    p=next(iter(c))
    if oks & ORGS[p]: return dict(person_id=p,name=P[p]['name'],firm=P[p]['main_registrant'],confidence='high_org_link',basis='name + org is LDA client/registrant of this lobbyist')
    if SURN[x[0]]<=3 and len(x[0])>=4: return dict(person_id=p,name=P[p]['name'],firm=P[p]['main_registrant'],confidence='medium_unique',basis=f'unique name in lobbyist universe; surname shared by {SURN[x[0]]} lobbyist name keys; no org link')
    return dict(person_id=p,name=P[p]['name'],firm=P[p]['main_registrant'],confidence='low_name_only',basis='name match only, common surname')
  linked=[p for p in c if oks & ORGS[p]]
  if len(linked)==1: p=linked[0]; return dict(person_id=p,name=P[p]['name'],firm=P[p]['main_registrant'],confidence='high_org_link',basis=f'{len(c)} same-name lobbyists; only this one lobbies for/at this org')
  return dict(person_id='|'.join(sorted(c)),name=fullname,firm='',confidence='low_name_only',basis=f'{len(c)} same-name lobbyists')
def match_member(fullname,context=''):
  x=nm(fullname)
  if not x: return None
  c=LEG.get((x[0],x[1]),[])
  c=list({r['bioguide']:r for r in c}.values())
  if not c: return None
  mid=x[2][0][:1] if x[2] else ''
  if mid: 
    c2=[r for r in c if not r['middle'] or r['middle']==mid]
    if c2: c=c2
    else: return None
  if len(c)>1: return dict(bioguide='|'.join(r['bioguide'] for r in c),name=fullname,confidence='low_name_only',basis=f'{len(c)} legislators share the name')
  r=c[0]
  # refined 2026-11-22 after spot check: sitting members rarely hold outside board/officer roles, so a bare name match to a CURRENT member is treated as a likely namesake;
  # former members with a common surname (>12 lobbyist name keys share it) are likewise demoted. Demoted matches go to ambiguous files, not edges.
  if CONGW.search(context or ''): conf,basis='high_title_or_org','exact legislator name + congressional title/context'
  elif r['current']: conf,basis='low_name_only','name equals a CURRENT member with no congressional context (likely namesake)'
  elif SURN[x[0]]>12: conf,basis='low_name_only',f'former member name but common surname ({SURN[x[0]]} lobbyist name keys)'
  else: conf,basis='medium_name_former_member','exact former-member name, uncommon surname; no title context (verify: could be a namesake)'
  return dict(bioguide=r['bioguide'],name=r['name'],party=r['party'],current=r['current'],last_term_end=r['last_term_end'],confidence=conf,basis=basis)
