import csv,collections,networkx as nx,matplotlib,datetime,sys
matplotlib.use('Agg'); import matplotlib.pyplot as plt
sys.path.insert(0,'..'); from safeio import keep_prev
NOW=datetime.datetime.now().astimezone().strftime('%Y-%m-%d %I:%M %p ET (UTC%z)')
LC={'R':'#c0392b','D':'#2471a3','I':'#7d3c98','mixed':'#9b59b6','unknown':'#95a5a6','':'#95a5a6'}
R=list(csv.DictReader(open('../ranking_money_all_with_pac.csv')))
T=R[:25][::-1]; fig,ax=plt.subplots(figsize=(13,10.5),dpi=90); y=list(range(len(T)))
ax.barh([i+0.2 for i in y],[float(r['direct_plus_pac_score']) for r in T],height=0.4,color=[LC.get(r['party_lean'],'#95a5a6') for r in T],label='direct + PAC score')
ax.barh([i-0.2 for i in y],[float(r['direct_only_score']) for r in T],height=0.4,color='#bdc3c7',label='direct-only score')
ax.set_yticks(y); ax.set_yticklabels([f"{r['lobbyist'].title()} ({r['firm'][:22].title()}) [direct #{r['direct_only_rank']}]" for r in T],fontsize=8.5)
for i,r in zip(y,T): ax.text(float(r['direct_plus_pac_score'])+0.5,i+0.2,f"\\${int(r['lobbyist_to_pac_usd'])/1e3:.0f}K to PACs | \\${int(r['indirect_via_pac_usd'])+int(r['indirect_via_jfc_split_usd']):,} indirect | officer roles {r['n_pac_officer_roles']} | lean {r['party_lean']}",va='center',fontsize=7)
ax.set_xlim(0,155); ax.legend(loc='lower right',fontsize=8)
ax.set_xlabel('direct + PAC = 0.75 x direct-only money score + 0.25 x PAC score; PAC score = percentiles of 0.35 lobbyist \\$ to PACs/party committees\n+ 0.35 indirect pro-rata PAC/JFC \\$ to members + 0.15 registrant LD-203 \\$ (split) + 0.15 PAC officer roles',fontsize=8.5)
ax.set_title(f'Top 25 lobbyists by direct + PAC money score (all parties), generated {NOW}'); plt.tight_layout(); plt.savefig(keep_prev('../ranking_money_all_with_pac_top25.png')); plt.close()
M=list(csv.DictReader(open('../member_totals_all_with_pac.csv')))[:25][::-1]
fig,ax=plt.subplots(figsize=(12,10),dpi=90); y=range(len(M))
d=[int(m['lobbyist_usd_scored'])/1e6 for m in M]; ii=[(int(m['indirect_lobbyist_via_pac_usd'])+int(m['indirect_lobbyist_via_jfc_split_usd']))/1e6 for m in M]
ax.barh(y,d,color=[LC.get(m['party']) for m in M],label='direct lobbyist $ (LD-203 + FEC, scored)')
ax.barh(y,ii,left=d,color='#f5b041',label='indirect lobbyist $ via PACs (pro rata) + JFC split')
ax.set_yticks(list(y)); ax.set_yticklabels([f"{m['member']} ({m['party']}-{m['state']})" for m in M],fontsize=9)
for i,m,a,b in zip(y,M,d,ii): ax.text(a+b+0.02,i,f"PAC direct (all PACs) \\${int(m['pac_direct_usd_all_pacs'])/1e6:.2f}M | IE for \\${int(m['ie_support_usd'])/1e6:.1f}M / against \\${int(m['ie_oppose_usd'])/1e6:.1f}M",va='center',fontsize=7)
ax.set_xlim(0,max(a+b for a,b in zip(d,ii))*1.9); ax.legend(loc='lower right',fontsize=8); ax.set_xlabel('$M, 2023-26')
ax.set_title(f'Top 25 members by lobbyist money incl. indirect PAC money, generated {NOW}'); plt.tight_layout(); plt.savefig(keep_prev('../member_totals_with_pac_top25.png')); plt.close()
Tp=list(csv.DictReader(open('top_pacs_by_lobbyist_money.csv')))[:25][::-1]
fig,ax=plt.subplots(figsize=(12,10),dpi=90); y=range(len(Tp))
ax.barh(y,[int(t['usd_from_universe_lobbyists'])/1e6 for t in Tp],color=[LC.get(t['party_lean'],'#95a5a6') for t in Tp])
ax.set_yticks(list(y)); ax.set_yticklabels([f"{t['name'][:45].title()} [{t['committee_class']}]" for t in Tp],fontsize=8)
for i,t in zip(y,Tp): ax.text(int(t['usd_from_universe_lobbyists'])/1e6+0.03,i,f"{t['n_lobbyists']} lobbyists",va='center',fontsize=8)
ax.set_xlabel('$M from universe lobbyists 2023-26 (FEC itemized + LD-203 self items not duplicating FEC); colour = lean')
ax.set_title(f'Top 25 committees (PACs, party cmtes, JFCs) funded by lobbyists\ngenerated {NOW}'); plt.tight_layout(); plt.savefig(keep_prev('../top_pacs_lobbyist_money_top25.png')); plt.close()
# network: top 40 lobbyists (direct+PAC) -> their top 2 PACs -> each PAC's top 3 member recipients
E=list(csv.DictReader(open('../edges_lobbyist_to_pac_all.csv'))); PM=list(csv.DictReader(open('../edges_pac_to_member_all.csv')))
top=[r['person_id'] for r in R[:40]]; Rb={r['person_id']:r for r in R}
lp=collections.defaultdict(collections.Counter)
for e in E:
  if e['person_id'] in top: lp[e['person_id']][(e['fec_committee_id'],e['committee_name'],e['committee_party_lean'])]+=float(e['usd'])
pg=collections.defaultdict(collections.Counter); pn={}
for r in PM:
  if r['category'] in ('direct_contribution','direct_inkind'): pg[r['committee_id']][(r['bioguide'],r['member'],r['member_party'])]+=float(r['usd'])
G=nx.Graph()
for pid in top:
  G.add_node('L'+pid,kind='L',label=Rb[pid]['lobbyist'].title(),lean=Rb[pid]['party_lean'])
  for (c,n,l),u in lp[pid].most_common(2):
    G.add_node('P'+c,kind='P',label=n[:28].title(),lean=l); G.add_edge('L'+pid,'P'+c,kind='lp',usd=u)
for n,d in list(G.nodes(data=True)):
  if d['kind']=='P':
    for (b,mn,mp),u in pg[n[1:]].most_common(3): G.add_node('M'+b,kind='M',label=mn,lean=mp); G.add_edge(n,'M'+b,kind='pm',usd=u)
pos=nx.spring_layout(G,k=0.6,seed=5,iterations=300)
fig,ax=plt.subplots(figsize=(24,17),dpi=80)
for kind,col in (('lp','#f39c12'),('pm','#7f8c8d')):
  es=[(u,v) for u,v,d in G.edges(data=True) if d['kind']==kind]
  nx.draw_networkx_edges(G,pos,edgelist=es,width=[0.6+min(G[u][v]['usd'],50000)/10000 for u,v in es],edge_color=col,alpha=0.6,ax=ax)
for kind,shape,sz in (('L','s',260),('P','D',380),('M','o',140)):
  ns=[n for n,d in G.nodes(data=True) if d['kind']==kind]
  nx.draw_networkx_nodes(G,pos,nodelist=ns,node_shape=shape,node_color=[LC.get(G.nodes[n]['lean'],'#95a5a6') for n in ns],node_size=[sz+30*G.degree(n) for n in ns],edgecolors='k',alpha=0.85,ax=ax)
nx.draw_networkx_labels(G,pos,{n:d['label'] for n,d in G.nodes(data=True) if d['kind']!='M' or G.degree(n)>=2},font_size=8,ax=ax)
ax.set_title(f'PAC layer: top 40 lobbyists (direct + PAC score) -> their 2 largest committees -> each committee\'s top 3 member recipients, generated {NOW}\n'
 'squares = lobbyists, diamonds = PACs/party committees/JFCs, circles = members; colour = party lean (red R, blue D, purple mixed/I, grey unknown); orange = lobbyist $ to committee, grey = committee direct contributions (pas2)',fontsize=12)
ax.axis('off'); plt.tight_layout(); plt.savefig(keep_prev('../network_pac_layer_top40.png')); plt.close()
print('ok',G.number_of_nodes())
