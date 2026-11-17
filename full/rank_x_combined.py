import csv,collections,datetime
NOW=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
M=list(csv.DictReader(open('ranking_money.csv')))
E=list(csv.DictReader(open('x/x_edges_handreviewed.csv')))
# score only in-era edges; one edge per (conversation or post, pair); pre-member posts at half weight
agg=collections.defaultdict(lambda:dict(w=0.0,mem=set(),posts=set(),photos=0,all_rows=0))
seen=set()
for e in E:
  a=agg[e['person_id']]; a['all_rows']+=1
  if not e['lobbying_era'].startswith('in_era'): continue
  if float(e['weight_raw'] or 0)<=0: continue  # not_relationship rows carry weight 0; exclude from member/post counts too
  k=(e['conversation_id'] or e['post_id'],e['person_id'],e['member_bioguide'])
  if k in seen: continue
  seen.add(k)
  w=float(e['weight_raw'])*(0.5 if e['member_status_at_post'].startswith('pre_member') else 1.0)
  a['w']+=w; a['mem'].add(e['member_bioguide'])
  if e['author_handle'].lower()!='ambctrujillo': a['posts'].add(e['post_id'])
  if e['edge_type']=='photo_together': a['photos']+=1
def pct(vals):
  s=sorted(vals); n=len(s)
  return lambda v:(sum(1 for x in s if x<v)+0.5*sum(1 for x in s if x==v))/n
rows=[]
for m in M:
  a=agg[m['person_id']]
  rows.append(dict(person_id=m['person_id'],lobbyist=m['lobbyist'],firm=m['firm'],x_weighted_degree=round(a['w'],2),x_distinct_members=len(a['mem']),x_member_authored_posts=len(a['posts']),
    x_photo_together=a['photos'],x_rows_incl_out_of_era=a['all_rows'],money_score=float(m['money_score']),money_rank=int(m['money_rank'])))
mw=max(r['x_weighted_degree'] for r in rows) or 1; mm=max(r['x_distinct_members'] for r in rows) or 1; mp=max(r['x_member_authored_posts'] for r in rows) or 1
pw=lambda v:v/mw; pm=lambda v:v/mm; pp=lambda v:v/mp
for r in rows:
  r['x_score']=round(100*(0.5*pw(r['x_weighted_degree'])+0.3*pm(r['x_distinct_members'])+0.2*pp(r['x_member_authored_posts'])),2)
  r['combined_score']=round(0.7*r['money_score']+0.3*r['x_score'],2); r['computed_at']=NOW
xs=sorted(rows,key=lambda r:(-r['x_weighted_degree'],-r['x_distinct_members'],r['money_rank']))
for i,r in enumerate(xs,1): r['x_rank']=i if r['x_weighted_degree']>0 else ''
cs=sorted(rows,key=lambda r:-r['combined_score'])
for i,r in enumerate(cs,1): r['combined_rank']=i
f=list(rows[0])
w=csv.DictWriter(open('ranking_x.csv','w'),fieldnames=f);w.writeheader();w.writerows([r for r in xs])
w=csv.DictWriter(open('ranking_combined.csv','w'),fieldnames=f);w.writeheader();w.writerows(cs)
print('X nonzero',sum(1 for r in rows if r['x_weighted_degree']>0))
for r in cs[:10]: print(r['combined_rank'],r['lobbyist'],r['money_score'],r['x_score'],r['combined_score'])
