# Keep the previous Page's node order and positions; append new nodes (placed at mean of neighbours) and new edges.
import json,sys,collections,random
prev=json.load(open(sys.argv[1])); new=json.load(open('map.json'))
TYN=11
def unb(s): return int(s,36)
def b36(n):
    n=int(n); d='0123456789abcdefghijklmnopqrstuvwxyz'; o=''
    while True:
        o=d[n%36]+o; n//=36
        if n==0: return o
key=lambda n:(n[0],n[1],n[3] if n[0]!='L' else n[3])
def ids(raw):
    E=raw['E']; return sorted(set([e[0] for e in E]+[e[1] for e in E])|set('L'+p for p in raw['sel']))
pk=ids(json.load(open(sys.argv[2]))); nk=ids(json.load(open('raw.json')))
assert len(pk)==len(prev['n']) and len(nk)==len(new['n'])
assert len(set(pk))==len(pk) and len(set(nk))==len(nk)
newpos={k:i for i,k in enumerate(nk)}
order=pk+[k for k in nk if k not in set(pk)]
gone=[k for k in pk if k not in newpos]; assert not gone, gone
oi={k:i for i,k in enumerate(order)}
def parse(es):
    out=[]
    for t in es.split():
        s,d,ty,v=t.split('.'); out.append((unb(s),unb(d),int(ty),unb(v)))
    return out
pe=parse(prev['e']); ne=parse(new['e'])
# new edges in stable index space
ne2={}
for s,d,ty,v in ne: ne2[(oi[nk[s]],oi[nk[d]],ty)]=v
rows=[None]*len(order)
for k,i in oi.items(): rows[i]=list(new['n'][newpos[k]])
# keep old positions
for i,k in enumerate(pk): rows[i][-2:]=prev['n'][i][-2:]
adj=collections.defaultdict(list)
for (s,d,ty) in ne2: adj[s].append(d); adj[d].append(s)
random.seed(11)
for i in range(len(pk),len(order)):
    nb=[j for j in adj[i] if j<len(pk)]
    if not nb: nb=[j for j in adj[i]]
    xs=[rows[j][-2] for j in nb if j<len(pk)] or [500]; ys=[rows[j][-1] for j in nb if j<len(pk)] or [350]
    rows[i][-2]=int(max(20,min(980,sum(xs)/len(xs)+random.uniform(-25,25)))); rows[i][-1]=int(max(20,min(680,sum(ys)/len(ys)+random.uniform(-25,25))))
toks=[]; seen=set()
for s,d,ty,v in pe:
    k=(s,d,ty)
    if k in ne2: toks.append((s,d,ty,ne2[k])); seen.add(k)
for k,v in ne2.items():
    if k not in seen: toks.append((*k,v))
es=' '.join(f'{b36(s)}.{b36(d)}.{ty}.{b36(v)}' for s,d,ty,v in toks)
removed=[k for k in ((s,d,ty) for s,d,ty,v in pe) if k not in ne2]
changed=[(k,v,ne2[k]) for k,v in (((s,d,ty),v) for s,d,ty,v in pe) if k in ne2 and ne2[k]!=v]
print('nodes',len(rows),'edges',len(toks),'removed edges',len(removed),'changed values',len(changed),'appended',len(toks)-len(seen))
json.dump({'n':rows,'e':es},open('map_stable.json','w'),separators=(',',':'),ensure_ascii=False)
json.dump({'removed':removed,'changed':changed},open('stable_diff.json','w'))
