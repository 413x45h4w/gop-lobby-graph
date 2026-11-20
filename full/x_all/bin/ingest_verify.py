import sys,json,csv,os
sys.path.insert(0,os.path.dirname(__file__)); import xlog
# usage: ingest_verify.py batch_idx result_path [...pairs]
a=sys.argv[1:]
out=xlog.BASE+'member_handle_verification.csv'; new=not os.path.exists(out)
with open(out,'a',newline='') as f:
  w=csv.writer(f)
  if new: w.writerow(['checked_at_ET','batch','handle','status','x_user_id','x_name','x_description','x_created_at'])
  for i in range(0,len(a),2):
    b,p=a[i],a[i+1]; j,rlm,reset,rlt,_=xlog.parse(p)
    hs=open(xlog.BASE+f'req/verify_{b}.txt').read().strip().split(',')
    found={u['username'].lower():u for u in j.get('data',[])}
    errs={(e.get('value') or '').lower():e.get('title','') for e in j.get('errors',[])}
    for h in hs:
      u=found.get(h.lower())
      if u: w.writerow([xlog.now(),b,u['username'],'found',u['id'],u.get('name',''),(u.get('description') or '').replace('\n',' '),u.get('created_at','')])
      else: w.writerow([xlog.now(),b,h,'not_found:'+errs.get(h.lower(),'missing'),'','','',''])
    if not os.environ.get('NOLOG'): xlog.log_call('get_users_by_usernames',f'verify_{b}',f'verify member handle candidates batch {b} ({len(hs)} usernames)',j,rlm,reset,rlt)
    print(b,len(found),'found',len(hs)-len(found),'missing; left',rlm,rlt)
