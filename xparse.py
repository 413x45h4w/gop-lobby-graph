import json,sys
def load(f):
  t=open(f).read(); return json.loads(t[t.index('{'):t.rindex('}')+1])
if __name__=='__main__':
  d=load(sys.argv[1])
  for u in d.get('data',[]): print(u['username'],'|',u['name'],'|',u['public_metrics']['followers_count'],u['public_metrics']['tweet_count'],'|',u.get('verified_type'),'|',u.get('description','')[:100].replace('\n',' '))
  print('missing:',[e.get('value') for e in d.get('errors',[])])
