import csv,json
N=json.load(open('xA_names.json'))['names']
mem=[];seen=set()
for r in csv.DictReader(open('../../nodes_gop_members.csv')):
  hs=[r['x_handle']]+[h for h in __import__('re').split(r'[|;, ]+',r['x_handles_alt_wikidata'] or '') if h]
  for h in hs:
    if h and h.lower() not in seen: seen.add(h.lower()); mem.append((h,r['bioguide']))
for h,b in [('SpeakerJohnson','J000299'),('GOPMajorityWhip','E000294'),('LeaderJohnThune','T000250'),('SenJohnThune','T000250')]:
  if h.lower() not in seen: seen.add(h.lower()); mem.append((h,b))
strs=[(pid,v) for pid,_,vs in N for v in vs]
# name blocks ~420 chars
blocks=[];cur=[]
for s in strs:
  t=' OR '.join(f'"{x[1]}"' for x in cur+[s])
  if len(t)>430: blocks.append(cur); cur=[s]
  else: cur.append(s)
blocks.append(cur)
Q=[]
for bi,b in enumerate(blocks):
  nm='('+' OR '.join(f'"{x[1]}"' for x in b)+')'
  i=0
  while i<len(mem):
    j=i; 
    while j<len(mem) and len('(' + ' OR '.join('from:'+h for h,_ in mem[i:j+1])+') '+nm+' -is:retweet')<=1024: j+=1
    q='('+' OR '.join('from:'+h for h,_ in mem[i:j])+') '+nm+' -is:retweet'
    Q.append(dict(id=f'A{bi}_{len(Q)}',block=bi,members=[h for h,_ in mem[i:j]],q=q)); i=j
json.dump(Q,open('qA.json','w'))
json.dump(mem,open('member_handles_all.json','w'))
print(len(mem),'handles',len(blocks),'blocks',len(Q),'queries',[len(b) for b in blocks])
