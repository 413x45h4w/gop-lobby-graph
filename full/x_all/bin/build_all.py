"""build_all.py: rebuild the combined all-party X layer from hand-review decisions.
Inputs : ../x/x_edges_handreviewed.csv (GOP layer, unchanged), review_decisions.csv + review_triage.csv (x_all layer),
         ../people_universe_scored.csv / ../lobbyist_universe_scored.csv (first_quarter_seen, registrant), persons_index.json (party_lean).
Outputs: x_edges_all_party.csv, x_hits_rejected_all.csv, ranking_x_all_party.csv, network_all_party.png (each with a .prev_ copy before overwrite).
Weights follow the GOP layer: photo_together 3, photo_mention_unclear 1.5, shoutout 1, mention 0.5, list_mention 0.25, not_relationship 0.
Scoring counts in-era edges only (post date on/after the lobbyist's first LDA quarter), one edge per (conversation, person, member)."""
import csv,json,os,shutil,datetime,collections,re
B='/workspace/gop-lobby-graph/full/x_all/'; F='/workspace/gop-lobby-graph/full/'
csv.field_size_limit(10**8)
NOW=datetime.datetime.now().astimezone(); TS=NOW.strftime('%Y%m%d_%H%M'); NOWS=NOW.isoformat(timespec='seconds')
W={'photo_together':3,'photo_mention_unclear':1.5,'shoutout':1,'mention':0.5,'list_mention':0.25,'not_relationship':0}
P=json.load(open(B+'persons_index.json'))
INFO={}
for fn,key in (('people_universe_scored.csv','person_key'),('lobbyist_universe_scored.csv','lda_lobbyist_id')):
  for r in csv.DictReader(open(F+fn)): INFO.setdefault(r[key],r)
FQ=json.load(open(B+'first_quarter_ld2_scan.json')) if os.path.exists(B+'first_quarter_ld2_scan.json') else {}  # earliest LD-2 quarter (2022Q4+ scan) for persons lacking first_quarter_seen
MH={r['bioguide']:r for r in csv.DictReader(open(B+'member_handles_all_party.csv'))}
def era(pid,date):
  fq=(INFO.get(pid) or {}).get('first_quarter_seen','') or min([FQ[x] for x in re.split(r'\D+',pid) if x in FQ] or [''])
  m=re.match(r'(\d{4})\D*Q?(\d)',fq or '')
  if not m: return 'unknown_era'
  y,q=int(m.group(1)),int(m.group(2)); start=f'{y}-{3*(q-1)+1:02d}-01'
  return 'in_era' if date[:10]>=start else f'pre_lobbying (first LDA qtr {y}Q{q})'
def save(fn,rows,fields):
  if os.path.exists(B+fn): shutil.copy(B+fn,B+fn.replace('.csv',f'.prev_{TS}.csv'))
  w=csv.DictWriter(open(B+fn,'w',newline=''),fieldnames=fields); w.writeheader(); w.writerows(rows)
FIELDS=['post_id','url','date_utc','author_handle','member_bioguide','member_name','member_party','person_id','lobbyist','person_party_lean','match','edge_type','has_photo','caption_review','member_status_at_post','lobbying_era','conversation_id','query_id','weight_raw','source_layer','built_at']
edges=[]
gop_posts=set()
for e in csv.DictReader(open(F+'x/x_edges_handreviewed.csv')):
  e=dict(e); gop_posts.add((e['post_id'],e['person_id']))
  e.update(member_party=(MH.get(e['member_bioguide']) or {}).get('party','R'),person_party_lean=(P.get(e['person_id']) or {}).get('party_lean',''),source_layer='gop_x_layer',built_at=NOWS)
  edges.append({k:e.get(k,'') for k in FIELDS})
T={r['post_id']:r for r in csv.DictReader(open(B+'review_triage.csv'))}
def pick(r,default):
  ms=[s.lower() for s in r['matched'].split('|')]
  for pid,nm in zip(r['person_ids'].split('|'),r['person_names'].split('|')):
    f=nm.split()[0].lower() if nm else ''
    if any(s.split()[0][:3]==f[:3] and s.split()[-1]==nm.split()[-1].lower() for s in ms): return pid
  return default
rej=[]
for d in csv.DictReader(open(B+'review_decisions.csv')):
  r=T.get(d['post_id'])
  if not r: continue
  pid=d['person_id'] if d['person_id'] in r['person_ids'].split('|') and len(r['person_ids'].split('|'))==1 else pick(r,d['person_id'])
  if d['decision']=='reject':
    rej.append(dict(post_id=r['post_id'],url=r['url'],date_utc=r['date_utc'],author_handle=r['author_handle'],matched_string=r['matched'],reason_rejected=d['reason'],query_id=r['query_id'],decided_at=d['decided_at_ET'])); continue
  if (r['post_id'],pid) in gop_posts: continue
  p=P.get(pid,{}); m=MH.get(r['member_bioguide'],{})
  edges.append(dict(post_id=r['post_id'],url=r['url'],date_utc=r['date_utc'],author_handle=r['author_handle'],member_bioguide=r['member_bioguide'],member_name=r['member_name'],member_party=r['member_party'],
    person_id=pid,lobbyist=p.get('name',''),person_party_lean=p.get('party_lean',''),match=f'name "{r["matched"]}" in text',edge_type=d['edge_type'],has_photo=int('photo' in r['has_media']),
    caption_review=d['reason'],member_status_at_post='member (current-member handle; pre-member status not checked)',lobbying_era=era(pid,r['date_utc']),conversation_id=r['conversation_id'],query_id=r['query_id'],
    weight_raw=W[d['edge_type']],source_layer='x_all',built_at=NOWS))
save('x_edges_all_party.csv',edges,FIELDS)
save('x_hits_rejected_all.csv',rej,['post_id','url','date_utc','author_handle','matched_string','reason_rejected','query_id','decided_at'])
agg=collections.defaultdict(lambda:dict(w=0.0,mem=set(),R=set(),D=set(),posts=set(),photos=0,rows=0)); seen=set()
for e in edges:
  a=agg[e['person_id']]; a['rows']+=1
  if not e['lobbying_era'].startswith('in_era') or float(e['weight_raw'] or 0)<=0: continue
  k=(e['conversation_id'] or e['post_id'],e['person_id'],e['member_bioguide'])
  k2=(re.sub(r'https?://\S+','',T.get(e['post_id'],{}).get('text',''))[:120],e['person_id'],e['member_bioguide']) if e['source_layer']=='x_all' else None
  if k in seen or (k2 and k2 in seen): continue  # also collapse re-posted identical text
  seen.add(k); seen.add(k2); w=float(e['weight_raw'])*(0.5 if e['member_status_at_post'].startswith('pre_member') else 1)
  a['w']+=w; a['mem'].add(e['member_bioguide']); a['posts'].add(e['post_id']); a['photos']+=e['edge_type']=='photo_together'
  (a['R'] if e['member_party']=='R' else a['D'] if e['member_party']=='D' else set()).add(e['member_bioguide'])
rows=[]
for pid,a in agg.items():
  p=P.get(pid,{}); i=INFO.get(pid,{})
  mix='R-only' if a['R'] and not a['D'] else 'D-only' if a['D'] and not a['R'] else 'bipartisan' if a['R'] and a['D'] else ''
  rows.append(dict(person_id=pid,lobbyist=p.get('name',''),main_registrant=i.get('main_registrant',''),kind=p.get('kind',''),attrib_income_usd=p.get('usd',''),party_lean=p.get('party_lean',''),
    x_weighted_degree=round(a['w'],2),x_distinct_members=len(a['mem']),x_R_members=len(a['R']),x_D_members=len(a['D']),x_member_party_mix=mix,x_member_authored_posts=len(a['posts']),x_photo_together=a['photos'],x_rows_incl_out_of_era=a['rows'],built_at=NOWS))
rows.sort(key=lambda r:(-r['x_weighted_degree'],-r['x_distinct_members'],-(float(r['attrib_income_usd'] or 0))))
for i,r in enumerate(rows,1): r['x_rank']=i if r['x_weighted_degree']>0 else ''
save('ranking_x_all_party.csv',rows,list(rows[0]))
import networkx as nx, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
G=nx.Graph(); col={'R':'#d62728','D':'#1f77b4','mixed':'#9467bd','unknown':'#7f7f7f','':'#7f7f7f'}
for e in edges:
  if not e['lobbying_era'].startswith('in_era') or float(e['weight_raw'] or 0)<=0: continue
  l='L:'+e['lobbyist'].title(); m='M:'+e['member_name']
  G.add_node(l,kind='L',c=col.get(e['person_party_lean'],'#7f7f7f')); G.add_node(m,kind='M',c=col.get(e['member_party'],'#7f7f7f'))
  G.add_edge(l,m,weight=G.get_edge_data(l,m,{}).get('weight',0)+float(e['weight_raw']))
if os.path.exists(B+'network_all_party.png'): shutil.copy(B+'network_all_party.png',B+f'network_all_party.prev_{TS}.png')
plt.figure(figsize=(16,12)); pos=nx.spring_layout(G,k=0.6,seed=7,weight=None)
nx.draw_networkx_edges(G,pos,width=[0.6*G[u][v]['weight'] for u,v in G.edges()],alpha=0.4)
for kind,shape in (('L','o'),('M','s')):
  ns=[n for n in G if G.nodes[n]['kind']==kind]; nx.draw_networkx_nodes(G,pos,nodelist=ns,node_shape=shape,node_color=[G.nodes[n]['c'] for n in ns],node_size=[60+40*G.degree(n,weight='weight') for n in ns],alpha=0.85)
nx.draw_networkx_labels(G,pos,{n:n[2:] for n in G},font_size=6)
plt.title(f'All-party lobbyist–Congress X graph (in-era, hand-reviewed edges) — {G.number_of_nodes()} nodes, {G.number_of_edges()} pairs. Circles = lobbyists (colour = party lean), squares = members (colour = party). Built {NOWS}',fontsize=9)
plt.axis('off'); plt.tight_layout(); plt.savefig(B+'network_all_party.png',dpi=110); plt.close()
print('edges',len(edges),'(x_all',sum(e['source_layer']=='x_all' for e in edges),') in-era scored lobbyists',sum(1 for r in rows if r['x_weighted_degree']>0),'rejected',len(rej),'graph',G.number_of_nodes(),G.number_of_edges())
