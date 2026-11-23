from common import *
s1=load('s1_lob'); s2=load('s2')
LM=s1['LM']; MM=s2['MM']; OM=s2['OM']; FM=s1['FM']
R={r['person_id']:r for r in rd('money_all/ranking_money_all_with_pac.csv')}
MEM={r['bioguide']:r for r in rd('money_all/member_totals_all_with_pac.csv')}
g=lambda d,k: d.get(k,0.0)
# ---- lobbyists
LW=[('money',.35),('ld2',.15),('clients',.05),('bills',.10),('revolving',.10),('oira',.05),('spac',.05),('fara',.05),('testimony',.025),('boards990',.025),('x',.05)]
raw={c:{} for c,_ in LW}
for p,r in R.items():
    m=LM.get(p,{})
    raw['money'][p]=f(r['direct_plus_pac_score'])
    raw['ld2'][p]=g(m,'ld2_usd'); raw['clients'][p]=g(m,'n_clients'); raw['bills'][p]=g(m,'n_bills')
    fm=FM.get(p); raw['revolving'][p]=g(m,'staff_high')+0.5*g(m,'staff_medium')+(3 if fm and fm[0]=='high' else 0)
    raw['oira'][p]=g(m,'oira_high'); raw['spac'][p]=g(m,'spac_high')+g(m,'spac_medium')
    raw['fara'][p]=g(m,'fara_high')+g(m,'fara_medium'); raw['testimony'][p]=g(m,'wit_high')
    raw['boards990'][p]=g(m,'off990_high')+g(m,'board'); raw['x'][p]=g(m,'x_w')
pc={c:pctile(raw[c]) for c,_ in LW}
LS={p:100*sum(w*pc[c][p] for c,w in LW) for p in R}
# ---- members
MW=[('lobby',.30),('ie',.15),('exstaff',.15),('clients',.15),('fara',.10),('travel',.05),('trades',.05),('x',.05)]
xm=collections.Counter(b for (p,b) in s1['xe'])
mraw={c:{} for c,_ in MW}
for b,r in MEM.items():
    m=MM.get(b,{})
    mraw['lobby'][b]=f(r['lobbyist_direct_plus_indirect_usd']); mraw['ie'][b]=g(m,'ie_support')+g(m,'ie_oppose')
    mraw['exstaff'][b]=g(m,'staff_high')+0.5*g(m,'staff_medium'); mraw['clients'][b]=g(m,'clients_spons')
    mraw['fara'][b]=g(m,'fara_high')+0.5*g(m,'fara_medium'); mraw['travel'][b]=g(m,'trips'); mraw['trades'][b]=g(m,'th_orgs'); mraw['x'][b]=xm.get(b,0)
mpc={c:pctile(mraw[c]) for c,_ in MW}
MS={b:100*sum(w*mpc[c][b] for c,w in MW) for b in MEM}
# ---- orgs
OW=[('ld2',.40),('sponsors',.15),('spac',.15),('oira',.10),('witness',.05),('travel',.05),('members_own',.05),('bills',.05)]
oraw={c:{} for c,_ in OW}
for k,m in OM.items():
    oraw['ld2'][k]=g(m,'ld2_usd'); oraw['sponsors'][k]=g(m,'spons_members'); oraw['spac'][k]=g(m,'spac'); oraw['oira'][k]=g(m,'oira')
    oraw['witness'][k]=g(m,'witness'); oraw['travel'][k]=g(m,'travel'); oraw['members_own'][k]=g(m,'members_trade')+g(m,'members_hold'); oraw['bills'][k]=g(m,'n_bills')
opc={c:pctile(oraw[c]) for c,_ in OW}
OS={k:100*sum(w*opc[c][k] for c,w in OW) for k in OM}
save('s3',{'LS':LS,'MS':MS,'OS':OS,'LW':LW,'MW':MW,'OW':OW,'raw':raw,'mraw':mraw,'oraw':oraw})
top=sorted(LS,key=lambda p:-LS[p])[:25]
for i,p in enumerate(top): print(i+1,R[p]['lobbyist'],R[p]['firm'][:30],round(LS[p],1),'money',R[p]['direct_plus_pac_rank'],{c:round(pc[c][p],2) for c,_ in LW})
print()
for i,b in enumerate(sorted(MS,key=lambda b:-MS[b])[:15]): print(i+1,MEM[b]['member'],MEM[b]['party'],round(MS[b],1),MEM[b]['rank_direct_plus_indirect'])
print()
for i,k in enumerate(sorted(OS,key=lambda k:-OS[k])[:20]): print(i+1,s2['ON'].get(k,k),round(OS[k],1),{c:round(oraw[c][k]) for c,_ in OW})
