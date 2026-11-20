"""Build / extend the persistent all-party X query queue (append-only semantics).
- member handles: verified-found handles from member_handle_verification.csv (latest row per handle)
  + accepted rows of member_handle_additions.csv.
- lobbyist universe: full/money_all/people_all.csv (21,408 people: outside + in-house + LD-203-only),
  which contains every person in people_universe_scored.csv and lobbyist_universe_scored.csv.
- If queue.json exists, existing chunks/blocks are kept unchanged; new handles become new chunks that are
  appended to every block's `need`; people not yet in any block are appended as new blocks at the end.
"""
import csv,json,os,re,sys,datetime,collections,shutil
B='/workspace/gop-lobby-graph/full/x_all/'; F='/workspace/gop-lobby-graph/full/'
sys.path.insert(0,F); sys.path.insert(0,F+'x')
import partylex as P
from nicks import NICK as NK
NOW=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
TAG=datetime.datetime.now().strftime('%Y%m%d_%H%M')
M_MAX=500; N_MAX=1024-17-M_MAX   # q = "(" M ") (" N ") -is:retweet"
exec(open(F+'x/pick_names.py').read().split('M=list')[0].split('from nicks import NICK as NK')[1])  # COMMON_LAST / COMMON_FIRST, same lists as GOP layer
# ---------- handles
ver={}
for r in csv.DictReader(open(B+'member_handle_verification.csv')): ver[r['handle'].lower()]=r
mem={r['bioguide']:r for r in csv.DictReader(open(F+'money_all/member_totals_all.csv'))}
cands=list(csv.DictReader(open(B+'member_handle_candidates.csv')))
H=[];seen=set()
old_gop={h.lower() for h,_ in json.load(open(F+'x/member_handles_all.json'))}
for c in cands:
  v=ver.get(c['handle'].lower())
  if v and v['status']=='found' and c['handle'].lower() not in seen:
    seen.add(c['handle'].lower()); H.append(dict(handle=v['handle'],bioguide=c['bioguide'],member=c['member'],party=c['party'],source=c['source'],x_user_id=v['x_user_id']))
for a in csv.DictReader(open(B+'member_handle_additions.csv')):
  if a['accepted']=='1' and a['handle'].lower() not in seen:
    seen.add(a['handle'].lower()); m=mem[a['bioguide']]
    H.append(dict(handle=a['handle'],bioguide=a['bioguide'],member=a['member'],party=m['party'],source='verified profile (member_handle_additions.csv)',x_user_id=a['x_user_id']))
with open(B+'member_handles_all_party.csv','w',newline='') as f:
  w=csv.DictWriter(f,list(H[0].keys())+['in_gop_x_layer','built_at']);w.writeheader()
  for h in H: w.writerow({**h,'in_gop_x_layer':int(h['handle'].lower() in old_gop),'built_at':NOW})
# ---------- names
TITLES=set('MR MR. MRS MRS. MS MS. DR DR. REV REV. HON HON. HONORABLE THE SEN SEN. SENATOR REP REP. AMB AMB. AMBASSADOR GEN GEN. COL COL. ADM ADM. GOV GOV. JUDGE CAPT CAPT. LT MAJ'.split())
SUFF=set('JR JR. SR SR. II III IV V ESQ ESQ. MD M.D. PHD PH.D. CPA J.D. JD'.split())
def variants(name):
  s=name.upper().replace('`','').replace('’',"'")
  nick=None
  m=re.match(r'^\s*([A-Z\.\-\']+)\s*[\("“]+\s*([A-Z\-\']+)\s*[\)"”]+',s)
  if m: nick=m.group(2)
  s=re.sub(r'\([^)]*\)?','',s); s=s.replace(')',''); s=re.sub(r'"[^"]*"','',s); s=s.replace('"','')
  s=re.sub(r'\b(NEE|FORMERLY|AKA)\b\s+\S.*$','',s)
  toks=[t.strip(',.') for t in s.replace(',',' ').split()]
  toks=[t for t in toks if t]
  while len(toks)>2 and (toks[0] in TITLES or toks[0]+'.' in TITLES): toks.pop(0)
  while toks and toks[-1] in SUFF|{t.rstrip('.') for t in SUFF}: toks.pop()
  while toks and len(toks[0].strip('.'))==1 and len(toks)>2: toks.pop(0)
  toks=[t for i,t in enumerate(toks) if i==0 or i==len(toks)-1 or len(t.strip('.'))>1]
  if len(toks)<2 or toks[0] in('N/A','NA','NONE') or not re.match(r"^[A-Z][A-Z\-']+$",toks[-1]) or not re.match(r"^[A-Z][A-Z\-'\.]*$",toks[0]): return None,None,None
  first,last=toks[0].strip('.'),toks[-1]
  if len(first)<2: return None,None,None
  d=lambda x:x.title()
  vs=[d(first)+' '+d(last)]+[d(n)+' '+d(last) for n in NK.get(first,[])[:1]]
  if nick and nick!=first: vs.append(d(nick)+' '+d(last))
  return first,last,list(dict.fromkeys(vs))
LDN=json.load(open(F+'x/lda_nicknames.json'))
people=list(csv.DictReader(open(F+'money_all/people_all.csv')))
lean={r['person_key']:r for r in csv.DictReader(open(F+'money_all/ranking_money_all.csv'))}
top300_ids=set()
for r in csv.DictReader(open(F+'selected_top300.csv')): top300_ids|=set(r['person_key'].split('|'))
recs=[]
for p in people:
  first,last,vs=variants(p['name'])
  ids=p['person_key'].split('|')
  rec=dict(person_key=p['person_key'],name=p['name'],kind=p['lobbyist_kind'],usd=int(float(p['attrib_lobbying_usd_2023_26'] or 0)),
     ld203=int(float(p['ld203_R_usd'] or 0))+int(float(p['ld203_D_usd'] or 0)),gop300=int(bool(set(ids)&top300_ids)),
     party_lean=lean.get(p['person_key'],{}).get('party_lean',''),former=p['former_member_party'])
  if not vs: rec['excluded']='unparseable_name'
  else:
    for i in ids:
      if i in LDN: vs=list(dict.fromkeys(vs+[LDN[i].title()+' '+last.title()]))
    legis=[x for x in P.BYLAST.get(last,[]) if first in x['firsts']]
    if legis and not p['former_member_party']: rec['excluded']='legislator_namesake'
    elif last in COMMON_LAST and first in COMMON_FIRST: rec['excluded']='common_name'
    else: rec['variants']=vs
  recs.append(rec)
def tier(r): return 'A0_gop300_new_handles' if r['gop300'] else ('C_paid' if r['usd']>0 else 'D_longtail')
recs.sort(key=lambda r:(0 if r['gop300'] else (1 if r['usd']>0 else 2),-r['usd'],-r['ld203'],r['name']))
# ---------- queue (extend if exists)
Q=json.load(open(B+'queue.json')) if os.path.exists(B+'queue.json') else None
if Q: shutil.copy(B+'queue.json',B+f'queue.prev_{TAG}.json')
else: Q=dict(version=3,created_at=NOW,chunks={},blocks=[],excluded=[],notes='see README.md')
have={h.lower() for c in Q['chunks'].values() for h in c['handles']}
def mk_chunks(hs,prefix):
  out=[];cur=[]
  for h in hs:
    t=' OR '.join('from:'+x for x in cur+[h])
    if len(t)>M_MAX: out.append(cur);cur=[h]
    else: cur.append(h)
  if cur: out.append(cur)
  ids=[]
  for c in out:
    cid=f'{prefix}{len(Q["chunks"])}'; Q['chunks'][cid]=dict(handles=c,set=prefix,added_at=NOW); ids.append(cid)
  return ids
# v2: handles ON the C-SPAN Members-of-Congress list are covered by one `list:` query per block;
# only OFF-list handles (list_probe_state.json: off + uncertain) get from: chunks. New handles added later
# (never probed) are treated as off-list.
LP=json.load(open(B+'list_probe_state.json'))
OFF={h.lower() for v in LP['chunks'].values() for h in v['off']+v.get('uncertain',[])}
PROBED={h.lower() for v in LP['chunks'].values() for h in v['off']+v.get('uncertain',[])+v['remaining']}
ONL=[h['handle'] for h in H if h['handle'].lower() in PROBED and h['handle'].lower() not in OFF]
newH=[h['handle'] for h in H if h['handle'].lower() not in have and (h['handle'].lower() in OFF or h['handle'].lower() not in PROBED)]
first_build=not Q['blocks']
if first_build:
  Q['version']=2; Q['list_id']=LP['list_id']; Q['start_time']=LP['start_time']
  Q['chunks']['L0']=dict(type='list',list_id=LP['list_id'],handles=ONL,set='L',added_at=NOW)
  # one stream: old-GOP-layer handles first, then new; any chunk containing a new handle is set 'N' (needed by A0)
  ordered=sorted(newH,key=lambda h:h.lower() not in old_gop)
  ids=mk_chunks(ordered,'O'); g=[];n=[]
  for c in ids:
    hs=Q['chunks'][c]['handles']; st='N' if any(h.lower() not in old_gop for h in hs) else 'G'
    Q['chunks'][c]['set']=st; (n if st=='N' else g).append(c)
else:
  n=mk_chunks(newH,'N') if newH else []
  for b in Q['blocks']: b['need']+= n
  g=[]
allc=list(Q['chunks'].keys()); nonold=['L0']+[c for c,v in Q['chunks'].items() if v['set']=='N']
inq={pk for b in Q['blocks'] for pk in b['persons']}|{e['person_key'] for e in Q['excluded']}
strings_in_q={s.lower():b['id'] for b in Q['blocks'] for s in b['names']}
pend=collections.OrderedDict()
for r in recs:
  if r['person_key'] in inq: continue
  if 'excluded' in r: Q['excluded'].append(dict(person_key=r['person_key'],name=r['name'],reason=r['excluded'],tier=tier(r),added_at=NOW)); continue
  pend.setdefault(tier(r),[]).append(r)
nb=len(Q['blocks'])
# v3 blocks ("K"): two name-halves (each <= H_MAX chars) per block. The list: query carries both halves
# (fits 1024); each off-list from: chunk is queried once per half (need ids "O7:a"/"O7:b").
H_MAX=(1024-len('list:34179516 () -is:retweet')-4)//2   # 496
assert 17+M_MAX+H_MAX<=1024
nk=sum(1 for b in Q['blocks'] if b['id'].startswith('K'))
for t,rs in pend.items():
  halves=[];cur=[];curp=[]
  def flush():
    if cur: halves.append((list(cur),list(curp)))
  for r in rs:
    vs=[v for v in r['variants'] if v.lower() not in strings_in_q and v not in cur]
    if not vs:
      if cur: curp.append(r['person_key'])
      elif halves: halves[-1][1].append(r['person_key'])
      elif Q['blocks']: Q['blocks'][-1]['persons'].append(r['person_key'])
      continue
    t2=' OR '.join(f'"{x}"' for x in cur+vs)
    if len(t2)>H_MAX: flush(); cur=[];curp=[]
    cur+=vs; curp.append(r['person_key'])
    for v in vs: strings_in_q[v.lower()]='pending'
  flush()
  base=nonold if t.startswith('A0') else allc
  for i in range(0,len(halves),2):
    hv=halves[i:i+2]; sides='ab'[:len(hv)]
    need=['L0']+[f'{c}:{x}' for c in base if c!='L0' for x in sides]
    Q['blocks'].append(dict(id=f'K{nk}',tier=t,names=[n for h in hv for n in h[0]],halves=[h[0] for h in hv],persons=[p for h in hv for p in h[1]],need=need,added_at=NOW)); nk+=1
json.dump(Q,open(B+'queue.json','w'))
json.dump({r['person_key']:{k:r[k] for k in ('name','kind','usd','gop300','party_lean','former')} for r in recs},open(B+'persons_index.json','w'))
tot=sum(len(b['need']) for b in Q['blocks'])
print('handles',len(H),'chunks',len(Q['chunks']),collections.Counter(v['set'] for v in Q['chunks'].values()),'blocks',len(Q['blocks']),collections.Counter(b['tier'] for b in Q['blocks']),
 'excluded',collections.Counter(e['reason'] for e in Q['excluded']),'total block-chunk queries',tot)
