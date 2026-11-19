import csv,collections,networkx as nx,matplotlib,datetime
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from safeio import keep_prev
NOW=datetime.datetime.now().astimezone().strftime('%Y-%m-%d %I:%M %p ET (UTC%z)')
R=list(csv.DictReader(open('ranking_money_all.csv')))
Pp=list(csv.DictReader(open('edges_money_pairs_all.csv')))
LC={'R':'#c0392b','D':'#2471a3','I':'#7d3c98','mixed':'#9b59b6','unknown':'#95a5a6'}
top=[r['person_id'] for r in R[:50]]; Rb={r['person_id']:r for r in R}
byp=collections.defaultdict(list)
for p in Pp:
  if p['person_id'] in top: byp[p['person_id']].append(p)
G=nx.Graph()
for pid in top: G.add_node('L'+pid,kind='L',label=Rb[pid]['lobbyist'].title(),size=float(Rb[pid]['money_score']),lean=Rb[pid]['party_lean'])
for pid,ps in byp.items():
  ps.sort(key=lambda p:-int(p['total_usd']))
  for p in ps[:3]+[q for q in ps[3:] if q['former_employer_tie']=='True']:
    G.add_node('M'+p['bioguide'],kind='M',label=p['member'],party=p['member_party'])
    G.add_edge('L'+pid,'M'+p['bioguide'],kind='fe' if p['former_employer_tie']=='True' else 'money',usd=int(p['total_usd']))
pos=nx.spring_layout(G,k=0.7,seed=11,iterations=300)
fig,ax=plt.subplots(figsize=(24,17),dpi=80)
for kind,col,sty in [('money','#7f8c8d','solid'),('fe','#16a085','dashed')]:
  es=[(u,v) for u,v,d in G.edges(data=True) if d['kind']==kind]
  nx.draw_networkx_edges(G,pos,edgelist=es,width=[0.5+min(G[u][v]['usd'],30000)/6000 for u,v in es],edge_color=col,style=sty,alpha=0.6,ax=ax)
Ln=[n for n,d in G.nodes(data=True) if d['kind']=='L']; Mn=[n for n,d in G.nodes(data=True) if d['kind']=='M']
nx.draw_networkx_nodes(G,pos,nodelist=Ln,node_shape='s',node_color=[LC.get(G.nodes[n]['lean'],'#95a5a6') for n in Ln],node_size=[G.nodes[n]['size']*5 for n in Ln],ax=ax,edgecolors='#f39c12',linewidths=2.5,alpha=0.9)
nx.draw_networkx_nodes(G,pos,nodelist=Mn,node_color=[LC.get(G.nodes[n]['party'],'#95a5a6') for n in Mn],node_size=[60+40*G.degree(n) for n in Mn],ax=ax,alpha=0.85)
nx.draw_networkx_labels(G,pos,{n:G.nodes[n]['label'] for n in Ln},font_size=9,font_weight='bold',ax=ax)
nx.draw_networkx_labels(G,pos,{n:G.nodes[n]['label'] for n in Mn if G.degree(n)>=3},font_size=10,font_weight='bold',font_color='#1b2631',bbox=dict(facecolor='white',alpha=0.75,edgecolor='none',pad=1),ax=ax)
ax.set_title(f'Top 50 lobbyists (all parties, all-party money score) and current members of Congress, generated {NOW}\n'
 'squares (orange border) = lobbyist, colour = party lean (red R, blue D, purple mixed, grey unknown), size = money score; circles = member, colour = party (purple = Independent), size = degree, labelled if degree>=3\n'
 'grey = LD-203/FEC contributions 2023-26 (top 3 recipients per lobbyist, width = $); green dashed = former employer (covered position)',fontsize=12)
ax.axis('off'); plt.tight_layout(); plt.savefig(keep_prev('network_top50_all.png')); plt.close()
T=R[:25][::-1]
fig,ax=plt.subplots(figsize=(13,10.5),dpi=90); y=range(len(T))
ax.barh(y,[float(r['money_score']) for r in T],color=[LC.get(r['party_lean'],'#95a5a6') for r in T])
ax.set_yticks(list(y)); ax.set_yticklabels([f"{r['lobbyist'].title()} ({r['firm'][:24].title()})" for r in T],fontsize=9)
for i,r in zip(y,T): ax.text(float(r['money_score'])+0.5,i,f"\\${int(r['attrib_lobbying_usd_2023_26'])/1e6:.1f}M lobbying \\$ | \\${int(r['usd_to_members'])/1e3:.0f}K to {r['n_members_funded']} members (R share {r['member_giving_R_share'] or 'n/a'}) | lean {r['party_lean']}",va='center',fontsize=7.5)
ax.set_xlim(0,150); ax.set_xlabel('All-party money score (percentiles over 21,417 lobbyists): 0.315 lobbying \\$ (income or in-house expense) + 0.315 \\$ to members\n+ 0.18 members funded + 0.09 former-employer members + 0.10 Form 3L bundling. Bar colour = party lean (red R, blue D, purple mixed).',fontsize=9)
ax.set_title(f'Top 25 lobbyists, all parties, by money score (LDA LD-2/LD-203 + FEC + Form 3L, 2023-2026)\ngenerated {NOW}')
plt.tight_layout(); plt.savefig(keep_prev('ranking_money_all_top25.png')); plt.close()
# members chart
Mt=list(csv.DictReader(open('member_totals_all.csv')))[:25][::-1]
fig,ax=plt.subplots(figsize=(12,10),dpi=90); y=range(len(Mt))
ax.barh(y,[int(m['lobbyist_usd_scored'])/1e6 for m in Mt],color=[LC.get(m['party'],'#95a5a6') for m in Mt])
ax.set_yticks(list(y)); ax.set_yticklabels([f"{m['member']} ({m['party']}-{m['state']}, {m['chamber']})" for m in Mt],fontsize=9)
for i,m in zip(y,Mt): ax.text(int(m['lobbyist_usd_scored'])/1e6+0.02,i,f"{m['n_lobbyists_giving']} lobbyists",va='center',fontsize=8)
ax.set_xlabel('Scored lobbyist money 2023-26, $M (LD-203 + FEC, capped $7,000/item, party/PAC items at 0.5)'); ax.set_title(f'Top 25 members by lobbyist money, generated {NOW}')
plt.tight_layout(); plt.savefig(keep_prev('member_totals_top25.png')); plt.close()
print(G.number_of_nodes(),G.number_of_edges())
