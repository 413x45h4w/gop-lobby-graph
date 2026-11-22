import csv, json, math, collections, networkx as nx
csv.field_size_limit(10**9)
B='/workspace/gop-lobby-graph/full/'; M=B+'money_all/'
raw=json.load(open('raw.json'))
f=lambda x: float(x) if x not in ('',None) else 0.0
R={r['person_id']:r for r in csv.DictReader(open(M+'ranking_money_all_with_pac.csv'))}
MEM={r['bioguide']:r for r in csv.DictReader(open(M+'member_totals_all_with_pac.csv'))}
TOP={r['fec_committee_id']:r for r in csv.DictReader(open(M+'pac/top_pacs_by_lobbyist_money.csv'))}
CM={r['committee_id']:r for r in csv.DictReader(open(M+'pac/committees_classified.csv'))}
XR={}
for r in csv.DictReader(open(B+'x_all/ranking_x_all_party.csv')): XR[r['person_id']]=r
ACR={'LLC','LLP','PAC','DC','II','III','USA','NRSC','NRCC','DCCC','DSCC','RNC','DNC','AIPAC','LCV','NAB','BGR','S-3','PC','HMP','BHFS-E','LP','PLLC','US','DBA','JFC','AFL-CIO','SEIU','UAW','NEA','PCMA'}
def tc(s):
    o=[]
    for w in s.split():
        core=w.strip('(),;.')
        if core in ACR or '&' in w: o.append(w)
        elif w.startswith('('): o.append('('+w[1:].capitalize())
        else: o.append('-'.join(p.capitalize() for p in w.split('-')))
    return ' '.join(o)
def mcfix(s):
    import re
    return re.sub(r"\b(Mc|O')([a-z])",lambda m:m.group(1)+m.group(2).upper(),s)
nodes=[]; idx={}
def add(nid,row): idx[nid]=len(nodes); nodes.append([nid]+row)
TY=['direct','staff','pacind','jfc','topac','officer','bundling','bundlink','pac2mem','x','ig']
E=raw['E']
used=set([e[0] for e in E]+[e[1] for e in E])|set('L'+p for p in raw['sel'])
lean=lambda s:{'R':'R','D':'D','mixed':'M'}.get(s,'U')
for nid in sorted(used):
    k=nid[0]; i=nid[1:]
    if k=='L':
        r=R[i]; x=XR.get(i,{})
        o=raw['other'].get(i,{})
        add(nid,['L',mcfix(tc(r['lobbyist'])),lean(r['party_lean']),mcfix(tc(r['firm']))[:30].rstrip(' ,('),
          round(f(r['direct_plus_pac_score']),1),int(r['direct_plus_pac_rank']),round(f(r['direct_only_score']),1),int(r['direct_only_rank']),
          round(f(r['usd_to_members'])),int(f(r['n_members_funded'])),round(f(r['lobbyist_to_pac_usd'])),round(f(r['indirect_via_pac_usd'])),round(f(r['indirect_via_jfc_split_usd'])),
          round(f(r['bundled_usd_to_members'])),int(f(r['n_pac_officer_roles'])),f(x.get('x_weighted_degree','')),r['former_member_party'] or '',round(f(r['attrib_lobbying_usd_2023_26']))])
    elif k=='M':
        r=MEM[i]
        add(nid,['M',r['member'],r['party'],r['chamber'][0]+'-'+r['state']+('' if r['chamber']=='Senate' else '-'+r['district']),
          round(f(r['lobbyist_usd_scored'])),round(f(r['indirect_lobbyist_via_pac_usd'])),round(f(r['indirect_lobbyist_via_jfc_split_usd'])),int(r['n_lobbyists_giving']),int(r['rank_direct_plus_indirect']),round(f(r['bundled_usd_form3l']))])
    elif k=='C':
        t=TOP.get(i,{}); c=CM.get(i,{})
        nm=(t.get('name') or c.get('name') or i).replace('POLITICAL ACTION COMMITTEE','PAC').replace('POLITICAL ACTION COMMIT','PAC').split(' (AKA')[0].split('; AKA')[0]
        add(nid,['C',mcfix(tc(nm))[:52].strip(),lean(t.get('party_lean') or c.get('party_lean','')),(t.get('committee_class') or c.get('committee_class','')).replace('_',' '),round(f(t.get('usd_from_universe_lobbyists',''))),int(f(t.get('n_lobbyists','')))])
    else:
        add(nid,['B',mcfix(tc(raw['bnames'][nid]))[:64],'U','Form 3L bundler',0,0])
# bundler totals
for e in E:
    if e[2]=='bundling': nodes[idx[e[0]]][5]+=round(e[3])
# layout
G=nx.Graph()
for n in nodes: G.add_node(n[0])
for s,t,ty,v in E:
    w={'staff':2,'x':2,'ig':2,'officer':2,'bundlink':1}.get(ty, min(3,0.3+math.log10(1+v)/2.2))
    if G.has_edge(s,t): G[s][t]['weight']+=w
    else: G.add_edge(s,t,weight=w)
init={}
import random; random.seed(7)
for n in nodes:
    a=random.random()*2*math.pi
    rad={'M':1.0,'L':0.55,'C':0.25,'B':0.25}[n[1]]
    p=n[3]
    if n[1]=='M': a=(math.pi*(0.5+random.random()) if p=='D' else (math.pi*(1.5+random.random()) if p=='R' else random.random()*6.28))
    init[n[0]]=(rad*math.cos(a),rad*math.sin(a))
pos=nx.spring_layout(G,pos=init,weight='weight',k=1.6/math.sqrt(len(nodes)),iterations=300,seed=7)
import numpy as np
ids=[n[0] for n in nodes]
def spread(vals):
    v=np.array(vals); r=v.argsort().argsort()/(len(v)-1)
    lo,hi=np.percentile(v,1),np.percentile(v,99); lin=np.clip((v-lo)/(hi-lo),0,1)
    return 0.6*r+0.4*lin
X=spread([pos[i][0] for i in ids]); Y=spread([pos[i][1] for i in ids])
for n,a,b in zip(nodes,X,Y): n.append(int(round(20+960*a))); n.append(int(round(20+660*b)))
import numpy as np
def b36(n):
    n=int(n); d='0123456789abcdefghijklmnopqrstuvwxyz'; o=''
    while True:
        o=d[n%36]+o; n//=36
        if n==0: return o
es=' '.join(b36(idx[s])+'.'+b36(idx[t])+'.'+str(TY.index(ty))+'.'+b36(round(v*4) if ty=='x' else round(v)) for s,t,ty,v in E)
out={'n':[n[1:] for n in nodes],'e':es}
s=json.dumps(out,separators=(',',':'),ensure_ascii=False)
open('map.json','w').write(s); print(len(s), len(nodes), collections.Counter(n[1] for n in nodes))
