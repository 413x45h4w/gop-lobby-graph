import sys,json,datetime,csv
# usage: log.py '<json list of [qid,count,reads_left,note]>' ; hits via hits_rest_raw.jsonl appended separately
now=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
rows=json.loads(sys.argv[1])
n=sum(1 for _ in open('calls_rest.csv'))
with open('calls_rest.csv','a') as f:
  w=csv.writer(f)
  for i,r in enumerate(rows): w.writerow([n+i,r[0],now,r[1],'',r[2],r[3] if len(r)>3 else ''])
p=json.load(open('state.json')) if __import__('os').path.exists('state.json') else {'done':[]}
p['done']+= [r[0] for r in rows]; p['updated_at']=now
json.dump(p,open('state.json','w'))
print(len(p['done']),'done')
