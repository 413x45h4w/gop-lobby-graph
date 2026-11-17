import csv,json,collections,datetime,networkx as nx
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
NOW=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
P=json.load(open('pilot_lobbyists.json')); lp={p['lid']:p for p in P}
E=[e for e in csv.DictReader(open('pilot_edges_posts.csv'))]
use=[e for e in E if e['era']=='lobbying_era']
agg=collections.defaultdict(lambda:collections.Counter())
for e in use:
  k=(e['lobbyist_id'],e['member_bioguide'])
  a=agg[k]; a['weight']+=float(e['weight']); a['n_posts']+=1; a[e['edge_type']]+=1; a['dir_'+e['direction']]+=1
  a.setdefault('member_name',0)
mn={e['member_bioguide']:e['member_name'] for e in E}
rows=[]
for (lid,b),a in agg.items():
  rows.append({'lobbyist_id':lid,'lobbyist_name':lp[lid]['name'],'member_bioguide':b,'member_name':mn[b],'weight':round(a['weight'],2),'n_posts':a['n_posts'],
   'photo_together':a['photo_together'],'photo_probable_award':a['photo_probable_award'],'photo_mention_unclear':a['photo_mention_unclear'],'shoutout':a['shoutout'],
   'mention_other':a['mention_other']+a['video_or_gif_mention']+a['list_mention'],'reply':a['reply'],'member_authored':a['dir_member->lobbyist'],'lobbyist_authored':a['dir_lobbyist->member'],'computed_at':NOW})
rows.sort(key=lambda r:-r['weight'])
with open('pilot_edges_weighted.csv','w') as f:
  w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
G=nx.Graph()
for r in rows:
  G.add_node(r['lobbyist_id'],kind='lobbyist'); G.add_node(r['member_bioguide'],kind='member')
  G.add_edge(r['lobbyist_id'],r['member_bioguide'],weight=r['weight'])
pr=nx.pagerank(G,weight='weight') if G.number_of_edges() else {}
# LDA sample stats
lda={}
for l in open('lda/lda_name_checks.jsonl'):
  d=json.loads(l); lda[d['name']]=d['registrants']
ld203=collections.defaultdict(lambda:{'reports':0,'items':0,'amount':0.0,'honorees':set()})
try:
  for l in open('lda/ld203_pilot_contributions.jsonl'):
    d=json.loads(l); x=ld203[d['lid']]; x['reports']+=1
    for it in d['items']:
      x['items']+=1; x['amount']+=float(it.get('amount') or 0); 
      if it.get('honoree_name'): x['honorees'].add(it['honoree_name'].upper())
except FileNotFoundError: pass
LS=json.load(open('ld203_summary.json'))
R=[]
for p in P:
  lid=p['lid']; er=[r for r in rows if r['lobbyist_id']==lid]
  allp=[e for e in E if e['lobbyist_id']==lid]
  reg=lda.get(p['lda_name'],{})
  R.append({'lobbyist_id':lid,'name':p['name'],'firm':p['firm'],'x_handle':p['x_handle'] or '(none found)','handle_confidence':p['handle_conf'],
    'weighted_degree':round(sum(r['weight'] for r in er),2),'distinct_members':len(er),
    'distinct_members_member_authored':len({r['member_bioguide'] for r in er if r['member_authored']>0}),
    'photo_together_posts':sum(r['photo_together'] for r in er),'photo_any_posts':sum(r['photo_together']+r['photo_probable_award']+r['photo_mention_unclear'] for r in er),
    'shoutouts':sum(r['shoutout'] for r in er),'pagerank':round(pr.get(lid,0),4),
    'excluded_posts_colleague_era_or_ambiguous':sum(1 for e in allp if e['era']!='lobbying_era'),
    'lda_filings_naming_lobbyist_2023_26_sample':sum(v['n_filings'] for v in reg.values()),'lda_clients_sample':sum(v['n_clients'] for v in reg.values()),
    'lda_registrants':'; '.join(reg.keys()),
    'ld203_usd_to_current_gop_members_2023_26':round(LS.get(lid,{}).get('usd_to_current_gop_members',0)),'ld203_distinct_gop_members_funded':LS.get(lid,{}).get('distinct_gop_members_funded',0),
    'social_edge_members_also_funded':len(set(r['member_bioguide'] for r in er)&set(LS.get(lid,{}).get('members',[]))),
    'computed_at':NOW})
R.sort(key=lambda r:(-r['weighted_degree'],-r['distinct_members']))
for i,r in enumerate(R,1): r['rank_social']=i
with open('pilot_lobbyist_ranking.csv','w') as f:
  w=csv.DictWriter(f,fieldnames=['rank_social']+[k for k in R[0] if k!='rank_social']); w.writeheader(); w.writerows(R)
for r in R: print(r['rank_social'],r['name'],r['weighted_degree'],r['distinct_members'],r['distinct_members_member_authored'],r['photo_together_posts'],r['pagerank'],r['lda_filings_naming_lobbyist_2023_26_sample'],r['ld203_usd_to_current_gop_members_2023_26'],r['ld203_distinct_gop_members_funded'],r['social_edge_members_also_funded'])
# plot
import math
fig,(ax,ax2)=plt.subplots(1,2,figsize=(20,11),gridspec_kw={'width_ratios':[1.6,1]})
comps=sorted(nx.connected_components(G),key=len,reverse=True)
main=G.subgraph(comps[0]); pos=nx.spring_layout(main,weight=None,seed=7,k=0.9/math.sqrt(main.number_of_nodes()),iterations=300)
for i,c in enumerate(comps[1:]):
  ang=2*math.pi*i/max(1,len(comps)-1)+0.4; cx,cy=1.45*math.cos(ang),1.45*math.sin(ang)
  sub=nx.spring_layout(G.subgraph(c),seed=1,scale=0.12)
  for n,(x,y) in sub.items(): pos[n]=(cx+x,cy+y)
lob=[n for n in G if G.nodes[n]['kind']=='lobbyist']; mem=[n for n in G if G.nodes[n]['kind']=='member']
nx.draw_networkx_edges(G,pos,ax=ax,width=[0.3+0.35*G[u][v]['weight'] for u,v in G.edges()],alpha=0.35,edge_color='#777')
nx.draw_networkx_nodes(G,pos,ax=ax,nodelist=mem,node_size=[30+18*G.degree(n,weight='weight') for n in mem],node_color='#d62728',alpha=0.8)
nx.draw_networkx_nodes(G,pos,ax=ax,nodelist=lob,node_size=[250+90*math.sqrt(G.degree(n,weight='weight')) for n in lob],node_color='#1f77b4',node_shape='s',alpha=0.9)
top=sorted(mem,key=lambda n:-G.degree(n,weight='weight'))[:18]
nx.draw_networkx_labels(G,{k:(v[0],v[1]+0.035) for k,v in pos.items()},ax=ax,labels={n:mn[n] for n in top},font_size=7.5,font_color='#7a0000')
nx.draw_networkx_labels(G,{k:(v[0],v[1]-0.05) for k,v in pos.items()},ax=ax,labels={n:lp[n]['name'] for n in lob},font_size=10,font_weight='bold',font_color='#0b3d91')
ax.set_title(f"X social graph (lobbying-era posts only): {G.number_of_edges()} member-lobbyist pairs, {len(use)} post-edges\nEdge weight: photo w/ co-presence caption=3, award photo=2, unclear photo=1.5, shout-out=1, other=0.5\n9 of 15 pilot lobbyists have ZERO edges (no active X account or no member tags)",fontsize=10)
ax.axis('off')
names=[r['name'] for r in R][::-1]
ax2.barh([i+0.2 for i in range(len(names))],[r['distinct_members'] for r in R][::-1],height=0.4,color='#1f77b4',label='Distinct GOP members linked on X (lobbying era)')
ax2.barh([i-0.2 for i in range(len(names))],[r['ld203_distinct_gop_members_funded'] for r in R][::-1],height=0.4,color='#2ca02c',label='Distinct current GOP members funded per LD-203 (2023-26)')
ax2.set_yticks(range(len(names))); ax2.set_yticklabels(names,fontsize=9); ax2.legend(fontsize=8,loc='lower right')
ax2.set_title('X visibility vs. disclosed money ties (LD-203 FECA items, name-matched)',fontsize=10)
fig.suptitle(f"PILOT (feasibility, not a final ranking): GOP members of Congress x 15 GOP-aligned registered lobbyists, X posts Nov 17 2022 - Nov 17 2026\nSources: X full-archive search via public-read API (captions/@tags/alt text only; no image or face analysis); LDA (lda.gov) LD-1/LD-2/LD-203; unitedstates/congress-legislators; Wikidata. Generated {NOW}",fontsize=11)
plt.tight_layout(rect=[0,0,1,0.92]); plt.savefig('pilot_network.png',dpi=100)
print('nodes',G.number_of_nodes(),'edges',G.number_of_edges())
