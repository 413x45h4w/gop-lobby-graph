# select drawn core + indexed entities; collect candidate edges among them
from common import *
s1=load('s1_lob'); s2=load('s2'); s3=load('s3')
LM=s1['LM']; T=s1['T']; FM=s1['FM']; MM=s2['MM']; OM=s2['OM']; ON=s2['ON']; E2=s2['E2']
LS,MS,OS=s3['LS'],s3['MS'],s3['OS']
R={}; key2pid={}
for r in rd('money_all/ranking_money_all_with_pac.csv'):
    R[r['person_id']]=r
    for k in r['person_key'].split('|'): key2pid[k]=r['person_id']
P=lambda p: key2pid.get(p,p)
MEM={r['bioguide']:r for r in rd('money_all/member_totals_all_with_pac.csv')}
# ---------- lobbyists
byDC=sorted(R,key=lambda p:-LS[p]); byMoney=sorted(R,key=lambda p:-f(R[p]['direct_plus_pac_score']))
DCRANK={p:i+1 for i,p in enumerate(byDC)}
Ldraw=list(dict.fromkeys(byDC[:150]+byMoney[:20]))
miller=[p for p in R if R[p]['lobbyist']=='JEFFREY MILLER' and 'MILLER STRATEGIES' in R[p]['firm']]
xl=set(p for (p,b) in s1['xe'])
Ldraw+= [p for p in miller if p not in Ldraw]
Ldraw+= [p for p in sorted(xl,key=lambda p:-LS.get(p,0)) if p in R and p not in Ldraw]
Lidx=list(dict.fromkeys(Ldraw+byDC[:350]))
print('L draw',len(Ldraw),'idx',len(Lidx))
# ---------- members
byMS=sorted(MEM,key=lambda b:-MS[b])
xm=set(b for (p,b) in s1['xe'])
Mdraw=list(dict.fromkeys(byMS[:280]+[b for b in byMS if b in xm]))
# ---------- clients
OK=[k for k in OM if OM[k].get('ld2_usd',0)>0]
byOS=sorted(OK,key=lambda k:-OS[k])
Kdraw=byOS[:90]; Kidx=byOS[:220]
save('s4',{'Ldraw':Ldraw,'Lidx':Lidx,'Mdraw':Mdraw,'Kdraw':Kdraw,'Kidx':Kidx,'DCRANK':DCRANK,'miller':miller})
for k in Kdraw[:5]: print(ON[k])
