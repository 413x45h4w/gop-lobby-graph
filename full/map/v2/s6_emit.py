from common import *
import networkx as nx, numpy as np, random
s1=load('s1_lob'); s2=load('s2'); s3=load('s3'); s4=load('s4'); s5=load('s5')
LM=s1['LM']; FM=s1['FM']; MM=s2['MM']; OM=s2['OM']; NODE=s5['NODE']; E=s5['E']
R={r['person_id']:r for r in rd('money_all/ranking_money_all_with_pac.csv')}
MEM={r['bioguide']:r for r in rd('money_all/member_totals_all_with_pac.csv')}
ACR={'LLC','LLP','PAC','DC','II','III','USA','US','NRSC','NRCC','DCCC','DSCC','RNC','DNC','AIPAC','LCV','NAB','BGR','S-3','PC','HMP','LP','PLLC','DBA','JFC','AFL-CIO','SEIU','UAW','NEA','PCMA','CVS','AT&T','EPA','HHS','USDA','HUD','FTC','FCC','SEC','SBA','CFPB','NRC','FERC','USTR','EOP','AFP','CLF','SLF','HMP','FF','UDP','CPI','RJC','NAR','API','ITI','IBM','GE','GM','BP','AARP','ACLU','AFSCME','DGA','RGA','RSLC','DLCC','DAGA','RAGA','PHRMA','NEA','AFT','IAFF','BCBS','AHIP','NRA','LGBTQ','US-ISRAEL','NRECA','CTA','WFP','SMP','PAC,'}
def tc(s):
    o=[]
    for w in s.split():
        core=w.strip('(),;.\'"')
        if core.upper() in ACR or (w.isupper() and len(core)<=3 and core.isalpha() and core not in('THE','AND','FOR','OF','INC','CO','ON','IN','TO','A')) or '&' in w: o.append(w.upper() if core.upper() in ACR else w)
        elif w.startswith('('): o.append('('+'-'.join(p.capitalize() for p in w[1:].split('-')))
        else: o.append('-'.join(p.capitalize() for p in w.split('-')))
    s=' '.join(o)
    s=re.sub(r"\b(Mc|O')([a-z])",lambda m:m.group(1)+m.group(2).upper(),s)
    return s
def nm(n):
    x=n['name']
    if n['kind']=='M': return x
    if n['kind'] in 'AU': return x
    if x.isupper() or n['kind'] in 'LKNSCBRWF': x=tc(x.lower().upper()) if x.isupper() else x
    return x.replace('|','/')[:48].strip(' ,')
g=lambda d,k: d.get(k,0)
DCR=s4['DCRANK']
MSR={b:i+1 for i,b in enumerate(sorted(MEM,key=lambda b:-s3['MS'][b]))}
OK=[k for k in OM if OM[k].get('ld2_usd',0)>0]
OSR={k:i+1 for i,k in enumerate(sorted(OK,key=lambda k:-s3['OS'][k]))}
def metrics(i,n):
    k=n['kind']; x=i[1:]
    if k=='L':
        r=R[x]; m=LM.get(x,{}); fm=FM.get(x)
        H=lambda v: f(v)/100; K_=lambda v: v/1000
        return [DCR[x],round(f(r['direct_plus_pac_score'])*10),int(r['direct_plus_pac_rank']),round(f(r['direct_only_score'])*10),g(m,'x_w')*4,K_(g(m,'ld2_usd')),g(m,'n_clients'),g(m,'n_bills'),g(m,'n_agencies'),H(r['usd_to_members']),f(r['n_members_funded']),H(r['lobbyist_to_pac_usd']),(f(r['indirect_via_pac_usd'])+f(r['indirect_via_jfc_split_usd']))/100,
                g(m,'staff_high'),g(m,'staff_medium'),(2 if fm and fm[0]=='high' else 1 if fm else 0),(g(m,'spac_high')+g(m,'spac_medium'))/100,g(m,'fara_high'),g(m,'fara_medium'),g(m,'oira_high'),g(m,'oira_low'),g(m,'wh_low'),g(m,'wit_high'),g(m,'wit_low'),g(m,'off990_high')+g(m,'off990_medium'),g(m,'spac_low')/100]
    if k=='M':
        r=MEM[x]; m=MM.get(x,{})
        xt=sum(1 for (p,b) in s1['xe'] if b==x)
        return [int(r['rank_direct_plus_indirect']),f(r['lobbyist_usd_scored'])/100,f(r['indirect_lobbyist_via_pac_usd'])/100,f(r['indirect_lobbyist_via_jfc_split_usd'])/100,int(r['n_lobbyists_giving']),g(m,'ie_support')/1000,g(m,'ie_oppose')/1000,g(m,'staff_high'),g(m,'staff_medium'),g(m,'clients_spons'),g(m,'fara_high'),g(m,'fara_medium'),(g(m,'faracontrib_high')+g(m,'faracontrib_medium'))/100,g(m,'trips'),g(m,'th_orgs'),g(m,'trade_tx'),g(m,'n_comm'),g(m,'caucus'),g(m,'codel'),xt,MSR[x]]
    if k=='K':
        m=OM.get(x,{})
        return [OSR.get(x,0),g(m,'ld2_usd')/1000,g(m,'n_bills'),g(m,'spons_members'),g(m,'spac')/1000,g(m,'oira'),g(m,'witness'),g(m,'travel'),g(m,'members_trade'),g(m,'members_hold'),g(m,'dockets'),g(m,'comments'),g(m,'n_agencies')]
    if k=='F': return [n.get('nmem',0),1 if n.get('gov') else 0]
    if k=='S': return [n.get('ie',0)/1000,n.get('usd',0)/100]
    if k=='C': return [n.get('usd',0)/100,n.get('nlob',0)]
    if k=='W': return [n.get('nclients',0),1 if n.get('law') else 0]
    return [n['score']/1000 if k in 'NB' else n['score']]
ids=[i for i,n in NODE.items()]
order={'M':0,'L':1,'K':2,'S':3,'C':4,'N':5,'F':6,'R':7,'A':8,'H':9,'W':10,'U':11,'B':12}
ids.sort(key=lambda i:(not NODE[i]['draw'],order[NODE[i]['kind']],-NODE[i]['score']))
def _keep(i):
    n=NODE[i]
    return n['draw'] or not (n['kind'] in 'LK' and ((n['kind']=='L' and DCR[i[1:]]>220) or (n['kind']=='K' and OSR.get(i[1:],999)>130)))
ids=[i for i in ids if _keep(i)]
idx={i:j for j,i in enumerate(ids)}
drawn=[i for i in ids if NODE[i]['draw']]
# layout
G=nx.Graph(); G.add_nodes_from(drawn)
for s,t,ty,v,c in E:
    w={'staff':2,'x':2,'ig':2,'officer':2,'bundlink':1,'roster':1.5,'caucus':0.5,'cospon':0.5,'codel':0.5}.get(ty, min(3,0.3+math.log10(1+v)/2.2))
    if G.has_edge(s,t): G[s][t]['weight']+=w
    else: G.add_edge(s,t,weight=w)
random.seed(7)
init={i:((1 if NODE[i]['lean']=='R' else -1 if NODE[i]['lean']=='D' else 0)*0.5+random.uniform(-.3,.3),random.uniform(-.5,.5)) for i in drawn}
pos=nx.spring_layout(G,pos=init,weight='weight',k=1.7/math.sqrt(len(drawn)),iterations=300,seed=7)
def spread(vals):
    v=np.array(vals); r=v.argsort().argsort()/(len(v)-1)
    lo,hi=np.percentile(v,1),np.percentile(v,99); lin=np.clip((v-lo)/(hi-lo),0,1)
    return 0.6*r+0.4*lin
X=spread([pos[i][0] for i in drawn]); Y=spread([pos[i][1] for i in drawn])
XY={i:(int(round(20+960*a)),int(round(20+660*b))) for i,a,b in zip(drawn,X,Y)}
def b36(n):
    n=int(round(n)); 
    if n<0: return '-'+b36(-n)
    d='0123456789abcdefghijklmnopqrstuvwxyz'; o=''
    while True:
        o=d[n%36]+o; n//=36
        if n==0: return o
rows=[]
for i in ids:
    n=NODE[i]; x,y=XY.get(i,('',''))
    sub=n['sub'] or ''
    if n['kind'] in 'LK': sub=tc(sub)[:30].strip(' ,(') if sub.isupper() else sub[:30]
    rows.append('|'.join([n['kind'],nm(n),n['lean'],sub.replace('|','/'),(b36(x) if x!='' else ''),(b36(y) if y!='' else ''),(b36(n['score']*10) if n['kind'] in 'LMK' else ''),re.sub(r'(\.0)+$','','.'.join(b36(v) for v in metrics(i,n)))]))
TYS=['direct','pacind','jfc','topac','pac2mem','officer','bundling','bundlink','client','clientbill','sponsreach','clientagency','sponsor','billcomm','staff','staffcomm','formeragency','fprincipal','faraagent','faracontact','faracontrib','iesup','ieopp','lobspac','clientspac','npspac','grant','schedc','c527','off990','interlock','roster','cospon','witness','orgwitness','caucus','oira','oiral','whvisit','docket','trade','holding','travel','codel','x','ig']
assert set(e[2] for e in E)<=set(TYS), set(e[2] for e in E)-set(TYS)
toks=[]
for s,t,ty,v,c in sorted(E,key=lambda e:(TYS.index(e[2]),idx[e[0]])):
    vv=v*4 if ty=='x' else v
    toks.append(f"{b36(idx[s])}.{b36(idx[t])}.{b36(TYS.index(ty))}.{b36(vv)}"+('' if c==0 else '.'+str(c)))
out={'rows':rows,'es':' '.join(toks),'TYS':TYS,'ndrawn':len(drawn)}
json.dump(out,open(OUT+'map_v2.json','w'),ensure_ascii=False,separators=(',',':'))
json.dump({'ids':ids},open(OUT+'map_v2_ids.json','w'))
print('rows',len(rows),'drawn',len(drawn),'edges',len(toks))
print('bytes rows',sum(len(r)+3 for r in rows),'edges',len(out['es']))
print(collections.Counter(r.split('|')[0] for r in rows[:len(drawn)]))
