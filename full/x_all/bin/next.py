"""Print the next K pending queries. qid = <block>.<need>[.p<page>], need = L0 | O<n> | O<n>:a|b (half of a K-block's names).
Order: follow-up pages; then leftover items of v2 B-blocks; phase 1 = the list: query (L0) of every block in queue order;
phase 2 = off-list from: chunks block by block. Default output is compact (block name-strings once + qids); FULL=1 prints full queries.
Every query is sent with start_time=queue['start_time'] (full-archive window) and max_results 25."""
import json,sys,os
B='/workspace/gop-lobby-graph/full/x_all/'
K=int(sys.argv[1]) if len(sys.argv)>1 else 8
Q=json.load(open(B+'queue.json')); S=json.load(open(B+'state.json'))
done=S['done']; out=[]
BL={b['id']:b for b in Q['blocks']}
def names_for(bid,need):
  b=BL[bid]
  if ':' in need: return b['halves']['ab'.index(need.split(':')[1])]
  return b['names']
def q(bid,need):
  cid=need.split(':')[0]; ch=Q['chunks'][cid]; nm='('+' OR '.join(f'"{x}"' for x in names_for(bid,need))+')'
  if ch.get('type')=='list': s=f"list:{ch['list_id']} {nm} -is:retweet"
  else: s='('+' OR '.join('from:'+h for h in ch['handles'])+') '+nm+' -is:retweet'
  assert len(s)<=1024,(bid,need,len(s)); return s
for f in S.get('followups',[]):
  if f['qid'] not in done and not f.get('skipped') and len(out)<K: out.append((f['qid'],f['block'],f['chunk'],f['next_token']))
def add(b,c):
  i=f"{b['id']}.{c}"
  if i not in done and len(out)<K and all(o[0]!=i for o in out): out.append((i,b['id'],c,''))
for b in Q['blocks']:
  if b['id'].startswith('B'):
    for c in b['need']: add(b,c)
for b in Q['blocks']:
  if 'L0' in b['need']: add(b,'L0')
for b in Q['blocks']:
  for c in b['need']: add(b,c)
open(B+'req/last_round.txt','w').write(''.join(o[0]+'\n' for o in out))
if os.environ.get('FULL')=='1':
  for i,bid,c,t in out: print(i+'\t'+q(bid,c)+('\tNEXT_TOKEN='+t if t else ''))
else:
  seen=set()
  for i,bid,c,t in out:
    q(bid,c); key=(bid,c.split(':')[1] if ':' in c else 'ALL')
    if key not in seen: seen.add(key); print(f'{bid}[{key[1]}]','('+' OR '.join(f'"{x}"' for x in names_for(bid,c))+')')
  print('QIDS',' '.join(o[0]+('[NT='+o[3]+']' if o[3] else '') for o in out))
