# All-party wrapper around ../gopnames.match with an extra false-positive safeguard found while spot-checking the all-party LD-203 build.
# A 'unique_last' (surname-only) match is REJECTED when, in ANY text (honoree, payee), the surname is directly preceded by a given name that
#  (a) together with the surname names a DIFFERENT legislator (current or historical since 1990), e.g. 'Markwayne Mullin' -> not Rep. Kevin Mullin,
#      'Will Hurd' -> not Rep. Jeff Hurd, 'Mark Green' -> not Rep. Al Green; or
#  (b) is not plausibly the member's own given name (not a nickname-table variant, no shared 3-letter prefix, edit distance > 2, not in the member's
#      official full name), e.g. 'Kevin Bishop' -> not Rep. Sanford Bishop, 'Janet Mills' -> not Rep. Cory Mills.
# Only tokens that are known given names (legislator first names, nickname table, LD-203 filer first names) count as a preceding given name.
# Spelling variants such as 'Jamie Comer', 'Bryan/Brian Steil', 'Suzan/Susan DelBene', 'Moore Capito' are kept.
import sys; sys.path.insert(0,'..')
import gopnames as G, partylex as PL
from nicks import NICK
NV={}
for k,vs in NICK.items():
  for v in vs: NV.setdefault(k,set()).add(v); NV.setdefault(v,set()).add(k)
for a,b in G.NICKP: NV.setdefault(a,set()).add(b); NV.setdefault(b,set()).add(a)
import json,glob,gzip
GIVEN=set(NV)|{f for p in PL.PEOPLE for f in p['firsts']}
for fn in glob.glob('/workspace/gop-lobby-graph/lda/ld203_universe/*.jsonl.gz'):
  for line in gzip.open(fn,'rt'):
    d=json.loads(line)
    if d.get('fn'): GIVEN.add(G.norm(d['fn']).split()[0] if G.norm(d['fn']).split() else '')
GIVEN-={'','CONG','CONGRESSMAN','CONGRESSWOMAN','SENATOR','REP','SEN','HON','NATIONAL','WINRED','FRIENDS','TEAM','ELECT','DR','MR','MRS','MS','FOR','THE'}
def ed(a,b):
  p=list(range(len(b)+1))
  for i,ca in enumerate(a,1):
    c=[i]
    for j,cb in enumerate(b,1): c.append(min(p[j]+1,c[j-1]+1,p[j-1]+(ca!=cb)))
    p=c
  return p[-1]
def plausible(prev,mem):
  for f in mem['firsts']:
    if f.startswith(prev) or prev.startswith(f): return True
    if prev in NV.get(f,()) : return True
    if len(prev)>=3 and len(f)>=3 and prev[:3]==f[:3]: return True
    if ed(prev,f)<=2: return True
  return prev in G.norm(mem['name']).split()
CMTW={'FOR','PAC','VICTORY','LEADERSHIP','FUND','COMMITTEE','CONGRESS','SENATE','TEAM','ACTION','MAJORITY'}
def match(hon,payee):
  m=G.match(hon,payee)
  if not m or m[2]!='unique_last': return m,''
  mem=[x for x in G.MEM if x['bio']==m[0]][0]
  # added 2026-11-18 (PAC layer): surname used as an ordinary word after AND/THE ('Georgia Safe and Strong' is not Rep. Dale Strong)
  for t in (hon,payee):
    toks=G.norm(t).split()
    for i,w in enumerate(toks):
      if w==mem['last'] and i>0 and toks[i-1] in ('AND','THE') and not (i+1<len(toks) and toks[i+1] in CMTW):
        return None,f"surname {mem['last']} used after '{toks[i-1]}' in '{t}', not a name (would have matched {mem['name']})"
  for t in (hon,payee):
    toks=G.norm(t).split()
    for i,w in enumerate(toks):
      if w==mem['last'] and i>0:
        prev=toks[i-1]
        if prev in G.ALLOWED_PREV or len(prev)<2 or prev not in GIVEN: continue
        other=[p for p in PL.BYLAST.get(mem['last'],[]) if prev in p['firsts'] and p['bio']!=mem['bio']]
        if other: return None,f"surname {mem['last']} preceded by '{prev}' = different legislator {other[0]['full']} ({other[0]['bio']}) in '{t}' (would have matched {mem['name']})"
        if not plausible(prev,mem): return None,f"surname {mem['last']} preceded by conflicting given name '{prev}' in '{t}' (would have matched {mem['name']})"
  return m,''
