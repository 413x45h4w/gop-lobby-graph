import csv, json, gzip, collections, math, sys
csv.field_size_limit(10**9)
B='/workspace/gop-lobby-graph/full/'
M=B+'money_all/'
R={}; key2pid={}
for r in csv.DictReader(open(M+'ranking_money_all_with_pac.csv')):
    R[r['person_id']]=r
    for k in r['person_key'].split('|'): key2pid[k]=r['person_id']
f=lambda x: float(x) if x not in ('',None) else 0.0
rows=list(R.values())
by_dp=sorted(rows,key=lambda r:-f(r['direct_plus_pac_score']))
by_d=sorted(rows,key=lambda r:-f(r['direct_only_score']))
by_usd=sorted(rows,key=lambda r:-f(r['usd_to_members']))
sel=set(r['person_id'] for r in by_dp[:120])|set(r['person_id'] for r in by_d[:40])|set(r['person_id'] for r in by_usd[:20])
xrows=list(csv.DictReader(open(B+'x_all/x_edges_all_party.csv')))
xpid=lambda p: key2pid.get(p,p)
xs=set(xpid(x['person_id']) for x in xrows if f(x['weight_raw'])>0)
missing=[p for p in xs if p not in R]
print('x persons',len(xs),'missing in ranking',missing)
sel|=xs
miller=[r['person_id'] for r in rows if r['lobbyist']=='JEFFREY MILLER' and 'MILLER STRATEGIES' in r['firm']]; print('miller',miller)
sel|=set(miller)
# GOP300 combined top 20 (IG queue / previous graph)
comb=list(csv.DictReader(open(B+'ranking_combined.csv')))
sel|=set(xpid(c['person_id']) for c in comb[:20] if xpid(c['person_id']) in R)
print('lobbyists selected',len(sel))
MEM={r['bioguide']:r for r in csv.DictReader(open(M+'member_totals_all_with_pac.csv'))}
name2bio={r['member'].lower():b for b,r in MEM.items()}
E=collections.defaultdict(float)  # (src,dst,type)->val
other=collections.defaultdict(lambda: collections.defaultdict(lambda:[0,0.0]))  # pid->type->[n,usd] for dropped
def keep_top(pid, typ, items, k, minv):
    items=sorted(items,key=lambda t:-t[1])
    for i,(dst,v) in enumerate(items):
        if i<k and v>=minv: E[('L'+pid,dst,typ)]+=v
        else:
            o=other[pid][typ]; o[0]+=1; o[1]+=v
# direct pairs
dp=collections.defaultdict(list); fe=collections.defaultdict(list)
for r in csv.DictReader(open(M+'edges_money_pairs_all.csv')):
    if r['person_id'] in sel and f(r['total_usd'])>0: dp[r['person_id']].append(('M'+r['bioguide'],f(r['total_usd'])))
for r in csv.DictReader(open(M+'edges_former_employer_all.csv')):
    if r['person_id'] in sel and r['ambiguous']=='False': E[('L'+r['person_id'],'M'+r['bioguide'],'staff')]=1
for p,it in dp.items(): keep_top(p,'direct',it,6,500)
# indirect
ip=collections.defaultdict(list); jp=collections.defaultdict(list)
with open(M+'edges_indirect_lobbyist_pac_member.csv') as fh:
    for r in csv.DictReader(fh):
        p=r['person_id']
        if p not in sel: continue
        a=f(r['indirect_pac_direct_usd']); j=f(r['jfc_split_usd'])
        if a>0: ip[p].append(('M'+r['bioguide'],a))
        if j>0: jp[p].append(('M'+r['bioguide'],j))
for p,it in ip.items(): keep_top(p,'pacind',it,3,100)
for p,it in jp.items(): keep_top(p,'jfc',it,3,100)
# committees
TOP=list(csv.DictReader(open(M+'pac/top_pacs_by_lobbyist_money.csv')))
CM={r['committee_id']:r for r in csv.DictReader(open(M+'pac/committees_classified.csv'))}
csel=set(r['fec_committee_id'] for r in TOP[:40])
off=[r for r in csv.DictReader(open(M+'edges_lobbyist_pac_officer.csv')) if r['person_id'] in sel]
for r in off: csel.add(r['fec_committee_id']); E[('L'+r['person_id'],'C'+r['fec_committee_id'],'officer')]=1
print('officer edges',len(off))
lp=collections.defaultdict(lambda: collections.defaultdict(float))
for r in csv.DictReader(open(M+'edges_lobbyist_to_pac_all.csv')):
    if r['person_id'] in sel: lp[r['person_id']][r['fec_committee_id']]+=f(r['usd'])
for p,d in lp.items():
    it=[('C'+c,v) for c,v in d.items() if c in csel]
    rest=[(c,v) for c,v in d.items() if c not in csel]
    keep_top(p,'topac',it,4,250)
    o=other[p]['topac']; o[0]+=len(rest); o[1]+=sum(v for c,v in rest)
# committee -> member direct contributions (top 6 per committee)
cm=collections.defaultdict(lambda: collections.defaultdict(float))
for r in csv.DictReader(open(M+'edges_pac_to_member_all.csv')):
    if r['committee_id'] in csel and r['category'] in ('direct_contribution','direct_inkind'): cm[r['committee_id']][r['bioguide']]+=f(r['usd'])
for c,d in cm.items():
    for b,v in sorted(d.items(),key=lambda t:-t[1])[:6]: E[('C'+c,'M'+b,'pac2mem')]+=v
# bundling: bundler org PAC -> member
bund=collections.defaultdict(float); bnames={}
for r in csv.DictReader(open(M+'edges_bundling_all.csv')):
    if r['scored']!='True': continue
    k='B'+(r['matched_registrant'] or r['bundler'])[:60]; bnames[k]=(r['matched_registrant'] or r['bundler']); bund[(k,'M'+r['member_bioguide'])]+=f(r['bundled_usd'])
    for p in r['matched_person_ids'].split('|'):
        if p in sel: E[('L'+p,k,'bundlink')]=1
for (k,m),v in bund.items(): E[(k,m,'bundling')]+=v
# X
xe=collections.defaultdict(lambda:[0.0,0,0,[]])
for x in xrows:
    w=f(x['weight_raw'])
    if w<=0: continue
    k=(xpid(x['person_id']),x['member_bioguide']); e=xe[k]; e[0]+=w; e[1]+=1; e[2]+= x['edge_type']=='photo_together'; e[3].append(x['lobbying_era'][:7])
for (p,b),e in xe.items(): E[('L'+p,'M'+b,'x')]+=e[0]
# IG
ig=list(csv.DictReader(open(B+'instagram/edges_instagram.csv')))
nig=0
for r in ig:
    for nm in r['members_named'].split(';'):
        b=name2bio.get(nm.strip().lower())
        if not b:
            t=nm.strip().lower().split(); c=[bb for n,bb in name2bio.items() if n.split()[0]==t[0] and n.split()[-1]==t[-1]]
            b=c[0] if len(c)==1 else None
        if not b: print('IG unmatched',nm); continue
        E[('L'+miller[0],'M'+b,'ig')]+=1; nig+=1
print('ig edges',nig)
# nodes
used=set()
for (s,t,ty) in E: used.add(s); used.add(t)
json.dump({'E':[[s,t,ty,v] for (s,t,ty),v in E.items()],'other':{p:{t:v for t,v in d.items()} for p,d in other.items()},'sel':sorted(sel),'csel':sorted(csel),'bnames':bnames,'xe':{p+'|'+b:e for (p,b),e in xe.items()}},open('/workspace/mapbuild/raw.json','w'))
print('edges',len(E),collections.Counter(t for (_,_,t) in E),'nodes used',len(used))
