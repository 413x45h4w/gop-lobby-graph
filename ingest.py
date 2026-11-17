# usage: python3 ingest.py <result_file> <query_set> <chunk_idx> <page>
import json,sys,datetime,os,hashlib
f,qs,ci,pg=sys.argv[1:5]
t=open(f).read()
import re
m=re.search(r'Full text: (\S+?\.txt)',t)
if m: t=open(m.group(1)).read()
try: d=json.loads(t[t.index('{'):t.rindex('}')+1])
except Exception as e: print('PARSE FAIL',t[:300]); sys.exit(1)
now=datetime.datetime.now().astimezone().isoformat()
users={u['id']:u['username'] for u in d.get('includes',{}).get('users',[])}
media={m['media_key']:m for m in d.get('includes',{}).get('media',[])}
n=0
with open('x_posts_raw.jsonl','a') as out:
  for p in d.get('data',[]):
    p['_author_username']=users.get(p['author_id'])
    p['_media']=[media.get(k,{'media_key':k}) for k in p.get('attachments',{}).get('media_keys',[])]
    p['_fetched']=now; p['_query_set']=qs; p['_chunk']=int(ci); p['_page']=int(pg)
    out.write(json.dumps(p)+'\n'); n+=1
with open('x_call_log.csv','a') as lg:
  lg.write(f"{now},{qs},{ci},{pg},{n},{d.get('meta',{}).get('oldest_id','')},{d.get('meta',{}).get('next_token','')}\n")
m=d.get('meta',{})
print('n',n,'next',m.get('next_token'),'dates',[p['created_at'][:10] for p in d.get('data',[])][:3],'...',[p['created_at'][:10] for p in d.get('data',[])][-1:])
