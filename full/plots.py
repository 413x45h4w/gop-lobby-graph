import csv,collections,networkx as nx,matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
C=list(csv.DictReader(open('ranking_combined.csv')))
Mo={r['person_id']:r for r in csv.DictReader(open('ranking_money.csv'))}
P=list(csv.DictReader(open('edges_money_pairs.csv')))
X=[e for e in csv.DictReader(open('x/x_edges_handreviewed.csv')) if e['weight_raw']!='0' and e['lobbying_era'].startswith('in_era')]
top=[r['person_id'] for r in C[:50]]
byp=collections.defaultdict(list)
for p in P:
  if p['person_id'] in top: byp[p['person_id']].append(p)
G=nx.Graph()
for pid in top:
  G.add_node('L'+pid,kind='L',label=Mo[pid]['lobbyist'].title(),size=float(Mo[pid]['money_score']))
for pid,ps in byp.items():
  ps.sort(key=lambda p:-int(p['total_usd']))
  for p in ps[:3]+[q for q in ps[3:] if q['former_employer_tie']=='True']:
    G.add_node('M'+p['bioguide'],kind='M',label=p['member'])
    G.add_edge('L'+pid,'M'+p['bioguide'],kind='fe' if p['former_employer_tie']=='True' else 'money',usd=int(p['total_usd']))
for e in X:
  if e['person_id'] in top:
    G.add_node('M'+e['member_bioguide'],kind='M',label=e['member_name'])
    G.add_edge('L'+e['person_id'],'M'+e['member_bioguide'],kind='x',usd=0)
pos=nx.spring_layout(G,k=0.8,seed=7,iterations=200)
fig,ax=plt.subplots(figsize=(22,16),dpi=80)
for kind,col,sty in [('money','#7f8c8d','solid'),('fe','#2980b9','dashed'),('x','#e74c3c','solid')]:
  es=[(u,v) for u,v,d in G.edges(data=True) if d['kind']==kind]
  ws=[0.5+min(G[u][v]['usd'],30000)/6000 if kind!='x' else 3 for u,v in es]
  nx.draw_networkx_edges(G,pos,edgelist=es,width=ws,edge_color=col,style=sty,alpha=0.6,ax=ax)
L=[n for n,d in G.nodes(data=True) if d['kind']=='L']; Mn=[n for n,d in G.nodes(data=True) if d['kind']=='M']
nx.draw_networkx_nodes(G,pos,nodelist=L,node_color='#f39c12',node_size=[G.nodes[n]['size']*6 for n in L],ax=ax,edgecolors='k')
nx.draw_networkx_nodes(G,pos,nodelist=Mn,node_color='#c0392b',node_size=[60+40*G.degree(n) for n in Mn],ax=ax,alpha=0.85)
nx.draw_networkx_labels(G,pos,{n:G.nodes[n]['label'] for n in L},font_size=9,font_weight='bold',ax=ax)
nx.draw_networkx_labels(G,pos,{n:G.nodes[n]['label'] for n in Mn if G.degree(n)>=3},font_size=10,font_weight='bold',font_color='#7b241c',bbox=dict(facecolor='white',alpha=0.75,edgecolor='none',pad=1),ax=ax)
ax.set_title('Top 50 GOP-aligned lobbyists (combined score) and current GOP members\norange = lobbyist (size = money score); red = member (size = degree, labeled if degree>=3)\ngrey = LD-203/FEC contributions 2023-26 (top 3 recipients per lobbyist, width = $), blue dashed = former employer, red = in-era X edge',fontsize=12)
ax.axis('off'); plt.tight_layout(); plt.savefig('network_top50.png'); plt.close()
# ranking chart
Mr=list(csv.DictReader(open('ranking_money.csv')))[:25][::-1]
fig,ax=plt.subplots(figsize=(12,10),dpi=90)
y=range(len(Mr))
ax.barh(y,[float(r['money_score']) for r in Mr],color='#2c3e50')
ax.set_yticks(list(y)); ax.set_yticklabels([f"{r['lobbyist'].title()} ({r['firm'][:22].title()})" for r in Mr],fontsize=9)
for i,r in zip(y,Mr): ax.text(float(r['money_score'])+0.5,i,f"\\${int(r['attrib_income_2023_26'])/1e6:.1f}M income | \\${int(r['usd_to_gop_members'])/1e3:.0f}K to {r['n_members_funded']} members",va='center',fontsize=8)
ax.set_xlim(0,130); ax.set_xlabel('Money score v2 (percentiles): 0.315 income + 0.315 \\$ to members + 0.18 members funded\n+ 0.09 former employer + 0.10 Form 3L bundling (no in-scope match, so rescaled /0.9)',fontsize=9)
ax.set_title('Top 25 GOP-aligned lobbyists by money score (LDA LD-2/LD-203 + FEC, 2023-2026)')
plt.tight_layout(); plt.savefig('ranking_money_top25.png'); plt.close()
print(G.number_of_nodes(),G.number_of_edges())
