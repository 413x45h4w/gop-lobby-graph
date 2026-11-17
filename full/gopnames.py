# current-member name matcher (all parties, so ambiguous surnames are detected); returns bioguide of current GOP member or None
import json,re,unicodedata
def norm(s): return re.sub(r'[^A-Z ]',' ',unicodedata.normalize('NFKD',s or '').encode('ascii','ignore').decode().upper())
L=json.load(open('/workspace/gop-lobby-graph/raw/legislators-current.json'))
NICKP=[('JAMES','JIM'),('ROBERT','ROB'),('ROBERT','BOB'),('WILLIAM','BILL'),('MICHAEL','MIKE'),('THOMAS','TOM'),('RICHARD','RICK'),('JOSEPH','JOE'),('DANIEL','DAN'),('DAVID','DAVE'),('STEPHEN','STEVE'),('STEVEN','STEVE'),('CHARLES','CHUCK'),('JOHN','JACK'),('RANDALL','RANDY'),('JENNIFER','JEN'),('CHRISTOPHER','CHRIS'),('ANDREW','ANDY'),('GREGORY','GREG'),('TIMOTHY','TIM'),('EDWARD','ED'),('ANTHONY','TONY'),('KENNETH','KEN'),('GERALD','JERRY'),('MATTHEW','MATT'),('NICHOLAS','NICK'),('ZACHARY','ZACH'),('THEODORE','TED'),('RAFAEL','TED'),('DONALD','DON'),('ELIZABETH','LIZ'),('PATRICK','PAT'),('BENJAMIN','BEN'),('SAMUEL','SAM'),('BRADLEY','BRAD'),('ABRAHAM','ABE'),('VERN','VERNON'),('DOUGLAS','DOUG'),('LAWRENCE','LARRY'),('ALBERT','AL'),('MARKWAYNE','MARKWAYNE')]
MEM=[]
for l in L:
  n=l['name']; firsts={norm(n.get('first')).strip()}
  if n.get('nickname'): firsts.add(norm(n['nickname']).strip())
  if n.get('middle') and l['name'].get('first','').endswith('.'): firsts.add(norm(n['middle']).strip())
  of=norm(n.get('official_full','')).split()
  if of: firsts.add(of[0])
  for f in list(firsts):
    for a,b in NICKP:
      if f==a: firsts.add(b)
      if f==b: firsts.add(a)
  last=norm(n['last']).strip()
  MEM.append(dict(bio=l['id']['bioguide'],party=l['terms'][-1]['party'],last=last,lastparts=last.split(),firsts={f for f in firsts if f},name=n.get('official_full') or n['first']+' '+n['last'],fec=l['id'].get('fec',[])))
from collections import Counter
LASTC=Counter(m['last'] for m in MEM)
ALLOWED_PREV=set('REP REPRESENTATIVE SEN SENATOR CONGRESSMAN CONGRESSWOMAN HON HONORABLE THE FOR OF FRIENDS CITIZENS TEAM ELECT RE LEADER WHIP CHAIRMAN SPEAKER DR MR MRS MS JR II III AND KEEP'.split())
ALLOWED_NEXT=set(' FOR PAC VICTORY LEADERSHIP MAJORITY FUND COMMITTEE CONGRESS SENATE JR II III IV PRIMARY GENERAL ACTION FRIENDS INC LLC TEAM NOW AMERICA PEOPLE'.split())|{''}
def match(*texts):
  """match honoree/payee text to a current member. returns (bio,party,method) or None"""
  for t in texts:
    T=' '+norm(t)+' '; toks=set(T.split())
    hits=[]
    for m in MEM:
      if ' '+m['last']+' ' not in T: continue
      if m['firsts']&toks: hits.append((m,'first+last'))
      elif LASTC[m['last']]==1 and len(m['last'])>3:
        i=T.index(' '+m['last']+' '); prev=T[:i].split()[-1:] ; prev=prev[0] if prev else ''
        nxt=T[i+len(m['last'])+2:].split()[:1]; nxt=nxt[0] if nxt else ''
        okprev = nxt in ALLOWED_NEXT and (prev=='' or prev in ALLOWED_PREV or any(f.startswith(prev) or prev.startswith(f) for f in m['firsts'] if len(prev)>=2))
        if okprev: hits.append((m,'unique_last'))
    strong=[h for h in hits if h[1]=='first+last']
    if len(strong)==1: return strong[0][0]['bio'],strong[0][0]['party'],'first+last'
    if not strong and len(hits)==1: return hits[0][0]['bio'],hits[0][0]['party'],'unique_last'
  return None
if __name__=='__main__':
  for t in ['Senator Josh Hawley','The Honorable Celeste Maloy','John Kennedy Primary','Brian Babin','Mike Johnson','Johnson','Scalise for Congress','Sen. Jon Tester','Rick Scott','Speaker Johnson']: print(t,match(t))
