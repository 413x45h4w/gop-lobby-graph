"""usage: ingest_listmem.py <chunk> <neg|pos> <path> ...  -> list_membership_obs.csv (append-only)"""
import sys,os,csv,json,collections
sys.path.insert(0,os.path.dirname(__file__)); import xlog
B=xlog.BASE; LIST='34179516'
Q=json.load(open(B+'queue.json'))
uid={}
for r in csv.DictReader(open(B+'member_handles_all_party.csv')): uid[r['x_user_id']]=r['handle']
out=B+'list_membership_obs.csv'; new=not os.path.exists(out)
a=sys.argv[1:]
with open(out,'a',newline='') as f:
  w=csv.writer(f)
  if new: w.writerow(['observed_at_ET','list_id','chunk','query_kind','handle','x_user_id','n_posts_in_sample','sample_size','has_next_token'])
  for i in range(0,len(a),3):
    cid,kind,p=a[i],a[i+1],a[i+2]
    j,rlm,reset,rlt,_=xlog.parse(p)
    c=collections.Counter(x.get('author_id') for x in j.get('data',[]) or [])
    nt=bool((j.get('meta') or {}).get('next_token'))
    for au,n in c.items(): w.writerow([xlog.now(),LIST,cid,kind,uid.get(au,'?'),au,n,len(j.get('data',[]) or []),int(nt)])
    if not c: w.writerow([xlog.now(),LIST,cid,kind,'(none)','',0,0,int(nt)])
    xlog.log_call('search_posts_all',f'listmem_{cid}_{kind}',f'list membership probe: chunk {cid} handles {"NOT " if kind=="neg" else ""}on list:{LIST}, since 2026-08-01, max 500',j,rlm,reset,rlt)
    print(cid,kind,'authors',len(c),'posts',sum(c.values()),'next',nt,'left',rlm,rlt,[uid.get(x,'?') for x in c])
