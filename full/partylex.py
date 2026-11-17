# party lexicon from congress-legislators (current + historical, terms since 1990)
import json,re,collections
def load():
  L=json.load(open('/workspace/gop-lobby-graph/raw/legislators-current.json'))+json.load(open('/workspace/gop-lobby-graph/raw/legislators-historical.json'))
  people=[]
  for l in L:
    ts=[t for t in l['terms'] if t['end']>='1990-01-01']
    if not ts: continue
    parties={t.get('party') for t in ts}
    n=l['name']; firsts={n['first'].upper()}
    if n.get('nickname'): firsts.add(n['nickname'].upper())
    if n.get('official_full'): firsts.add(n['official_full'].split()[0].upper().strip('.'))
    people.append({'bio':l['id']['bioguide'],'last':n['last'].upper(),'firsts':firsts,'party':'R' if parties=={'Republican'} else ('D' if parties<= {'Democrat','Independent'} and 'Democrat' in parties else 'X'),
      'sen':any(t['type']=='sen' for t in ts),'rep':any(t['type']=='rep' for t in ts),'current':l in L[:0] ,'full':n.get('official_full') or n['first']+' '+n['last']})
  return people
PEOPLE=load()
BYLAST=collections.defaultdict(list)
for p in PEOPLE: BYLAST[p['last']].append(p)
RKW=re.compile(r"\b(REPUBLICAN|GOP|RNC|NRCC|NRSC|TRUMP|PENCE|VANCE|MCCONNELL|MCCARTHY|SCALISE|BOEHNER|PAUL RYAN|SPEAKER RYAN|SPEAKER JOHNSON|THUNE|WINRED|MAGA)\b")
DKW=re.compile(r"\b(DEMOCRAT\w*|DCCC|DSCC|DNC|PELOSI|SCHUMER|REID|OBAMA|BIDEN|HARRIS|CLINTON|JEFFRIES|HOYER|ACTBLUE)\b")
TITLE=re.compile(r"\b(?:SEN\.?|SENATOR|REP\.?|REPRESENTATIVE|CONGRESSMAN|CONGRESSWOMAN|CONG\.|LEADER|SPEAKER|WHIP|CHAIRMAN|MEMBER|MR\.|MS\.|MRS\.|HON\.?)\s+((?:[A-Z][A-Z\.'\-]+\s+){0,3}[A-Z][A-Z'\-]+)")
def people_in(text):
  """return list of legislator dicts named in text (title + [first] last), conservative"""
  T=text.upper(); out=[]
  for m in TITLE.finditer(T):
    toks=m.group(1).replace('.',' ').split()
    if not toks: continue
    last=toks[-1]; cands=BYLAST.get(last,[])
    if len(toks)>1:
      c2=[p for p in cands if toks[0] in p['firsts']]
      if c2: cands=c2
    if len(cands)==1: out.append(cands[0])
    elif cands and len({c['party'] for c in cands})==1: out.append(dict(cands[0],ambiguous=True))
  # also "FIRST LAST" without title, only if exact first+last unique
  return out
def party_of_text(text):
  ps=[p['party'] for p in people_in(text)]
  T=text.upper(); r=ps.count('R')+(1 if RKW.search(T) else 0); d=ps.count('D')+(1 if DKW.search(T) else 0)
  return r,d
_full={}
for p in PEOPLE:
  for f in p['firsts']:
    _full.setdefault(f+' '+p['last'],[]).append(p)
_FULLRX=re.compile(r"\b("+"|".join(sorted((re.escape(k) for k in _full),key=len,reverse=True))+r")\b")
_old_people_in=people_in
def people_in(text):
  out=_old_people_in(text); seen={p['bio'] for p in out}
  T=re.sub(r'\s+',' ',text.upper().replace('.',' '))
  T=re.sub(r'\b([A-Z]) ',' ',T)  # drop middle initials
  T=re.sub(r'\s+',' ',T)
  for m in _FULLRX.finditer(T):
    c=_full[m.group(1)]
    if len(c)==1 and c[0]['bio'] not in seen: out.append(c[0]); seen.add(c[0]['bio'])
  return out
def party_of_text(text):
  ps=[p['party'] for p in people_in(text)]
  T=text.upper(); r=ps.count('R')+(1 if RKW.search(T) else 0); d=ps.count('D')+(1 if DKW.search(T) else 0)
  return r,d
