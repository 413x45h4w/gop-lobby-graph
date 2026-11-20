"""triage.py: classify unique member-authored hits with a matched lobbyist name string into review tiers.
Writes review_triage.csv (derived; .prev_ copy kept). Tiers:
  T1_former   person's LDA covered-position text names the posting member (former staffer cue)
  T2_cue      post text has a relationship/lobbying cue word
  T3_plain    name match only (needs hand review; common-name namesakes likely)
  X_member    matched string is the name of a member of Congress (auto-reject candidate)"""
import json,csv,re,os,shutil,datetime
B='/workspace/gop-lobby-graph/full/x_all/'
P=json.load(open(B+'persons_index.json')); Q=json.load(open(B+'queue.json')); BL={b['id']:b for b in Q['blocks']}
MH={r['handle'].lower():r for r in csv.DictReader(open(B+'member_handles_all_party.csv'))}
csv.field_size_limit(10**8)
COV={}
for fn,key in (('../people_universe_scored.csv','person_key'),('../lobbyist_universe_scored.csv','lda_lobbyist_id')):
  for r in csv.DictReader(open(B+fn)):
    COV.setdefault(r[key],(r.get('covered_positions') or '',r.get('main_registrant') or ''))
MEMBER_NAMES={r['member'].lower() for r in MH.values()}
cue=re.compile(r'lobby|former (chief|staff|legislative|deputy|counsel|colleague)|my former|alum|chief of staff|staffer|worked (for|with)|our team|friend|thank(s| you)|great to (see|meet|catch)|met with|meeting with|joined by',re.I)
seen=set(); rows=[]
for l in open(B+'hits_raw.jsonl'):
  h=json.loads(l)
  if not (h['member_author'] and h['matched']): continue
  if h['post_id'] in seen: continue
  seen.add(h['post_id'])
  m=MH[h['author'].lower()]; mlast=m['member'].split()[-1].lower()
  b=BL[h['qid'].split('.')[0]]
  cands=[]
  for pid in b['persons']:
    p=P.get(str(pid),{}); nm=p.get('name','').split()
    if nm and any(s.lower().split()[-1]==nm[-1].lower() for s in h['matched']): cands.append((str(pid),p))
  former=any(re.search(r'\b'+re.escape(mlast)+r'\b',COV.get(pid,('',''))[0].lower()) for pid,_ in cands)
  regcue=any(len(COV.get(pid,('',''))[1].split())>0 and len(COV[pid][1].split()[0])>3 and COV[pid][1].split()[0].lower() in h['text'].lower() for pid,_ in cands)
  ismem=all(s.lower() in MEMBER_NAMES for s in h['matched'])
  tier='X_member' if ismem else 'T1_former' if former else 'T1_firm' if regcue else 'T2_cue' if cue.search(h['text']+' '.join(h.get('alt_text',[]))) else 'T3_plain'
  rows.append(dict(tier=tier,post_id=h['post_id'],url=h['url'],date_utc=h['created_at'],author_handle=h['author'],member_bioguide=m['bioguide'],member_name=m['member'],member_party=m['party'],
    matched='|'.join(h['matched']),person_ids='|'.join(c[0] for c in cands),person_names='|'.join(c[1].get('name','') for c in cands),
    person_registrant=' || '.join(COV.get(c[0],('',''))[1] for c in cands),person_covered=' || '.join(COV.get(c[0],('',''))[0][:200] for c in cands),person_lean='|'.join(c[1].get('party_lean','') for c in cands),has_media='|'.join(h.get('media') or []),alt_text=' | '.join(h.get('alt_text') or []),
    query_id=h['qid'],conversation_id=h.get('conversation_id',''),text=h['text'].replace('\n',' ')))
out=B+'review_triage.csv'
if os.path.exists(out): shutil.copy(out,B+'review_triage.prev_'+datetime.datetime.now().strftime('%Y%m%d_%H%M')+'.csv')
w=csv.DictWriter(open(out,'w',newline=''),fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
import collections; print(collections.Counter(r['tier'] for r in rows))
