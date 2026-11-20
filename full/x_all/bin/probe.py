"""List-membership probe (negative): for each chunk, query (from:remaining) -list:LIST since 2022-11-17.
Any author returned is OFF the list -> removed from remaining; repeat until 0 results -> remaining are ON list (or never post).
usage: probe.py next K            -> prints '<pid>\t<query>'
       probe.py ingest <pid> <path> ...
State: list_probe_state.json ; observations appended to list_membership_obs.csv"""
import sys,os,csv,json,collections
sys.path.insert(0,os.path.dirname(__file__)); import xlog
B=xlog.BASE; LIST='34179516'; SP=B+'list_probe_state.json'
Q=json.load(open(B+'queue.json'))
uid={r['x_user_id']:r['handle'] for r in csv.DictReader(open(B+'member_handles_all_party.csv'))}
S=json.load(open(SP)) if os.path.exists(SP) else {'list_id':LIST,'start_time':'2022-11-17T00:00:00Z','chunks':{c:{'remaining':v['handles'],'off':[],'iters':0,'finished':False} for c,v in Q['chunks'].items()}}
def q(c): return '('+' OR '.join('from:'+h for h in S['chunks'][c]['remaining'])+f') -list:{LIST} -is:retweet'
if sys.argv[1]=='next':
  K=int(sys.argv[2]); n=0
  for c,v in S['chunks'].items():
    if not v['finished'] and v['remaining'] and n<K: print(f"{c}.i{v['iters']}"+(' RECENCY' if v.get('recency') else '')+f"\t{q(c)}"); n+=1
else:
  a=sys.argv[2:]; out=B+'list_membership_obs.csv'
  with open(out,'a',newline='') as f:
    w=csv.writer(f)
    for i in range(0,len(a),2):
      pid,p=a[i],a[i+1]; c=pid.split('.')[0]; v=S['chunks'][c]
      j,rlm,reset,rlt,_=xlog.parse(p)
      if 'data' not in j and 'meta' not in j: print('ERR',pid,str(j)[:200]); continue
      cnt=collections.Counter(x.get('author_id') for x in j.get('data',[]) or [])
      hs=[uid.get(au,'?'+au) for au in cnt]
      for au,n in cnt.items(): w.writerow([xlog.now(),LIST,c,'neg_iter'+str(v['iters']),uid.get(au,'?'),au,n,sum(cnt.values()),int(bool((j.get('meta') or {}).get('next_token')))])
      xlog.log_call('search_posts_all','listprobe_'+pid,f'list membership negative probe chunk {c} iter {v["iters"]}: {len(v["remaining"])} handles -list:{LIST} since 2022-11-17',j,rlm,reset,rlt)
      low={h.lower() for h in hs}
      v['off']+= [h for h in v['remaining'] if h.lower() in low]
      v['remaining']=[h for h in v['remaining'] if h.lower() not in low]
      v['iters']+=1
      nt=(j.get('meta') or {}).get('next_token')
      if not cnt and not nt: v['finished']=True
      if not cnt and nt: v['recency']=True; print(pid,'zero page but next_token -> retry with recency sort')
      if any(h.startswith('?') for h in hs) : print('unknown author ids',hs)
      print(pid,'off:',[h for h in hs],'remaining',len(v['remaining']),'left',rlm,rlt)
  json.dump(S,open(SP,'w'),indent=0)
  fin=sum(1 for v in S['chunks'].values() if v['finished'] or not v['remaining']); off=sum(len(v['off']) for v in S['chunks'].values())
  print('chunks finished',fin,'/',len(S['chunks']),'off-list so far',off)
