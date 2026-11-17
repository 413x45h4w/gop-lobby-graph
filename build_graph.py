import json,csv,re,collections,datetime
NOW=datetime.datetime.now().astimezone().isoformat()
P=json.load(open('pilot_lobbyists.json'))
M=list(csv.DictReader(open('nodes_gop_members.csv')))
L=json.load(open('raw/legislators-current.json'))
byb={l['id']['bioguide']:l for l in L}
# member handle map
mh={}
for m in M:
  for h in [m['x_handle']]+[x for x in m['x_handles_alt_wikidata'].split(';') if x]:
    if h and h.lower()!='wvgovernor': mh[h.lower()]=m['bioguide']
mh['speakerjohnson']=[m['bioguide'] for m in M if m['name'].startswith('Mike Johnson')][0] if any(m['name'].startswith('Mike Johnson') for m in M) else None
mname={m['bioguide']:m['name'] for m in M}
# member full-name patterns for lobbyist-authored captions (conservative: first/nickname + last)
lastcount=collections.Counter()
pats=[]
for m in M:
  l=byb[m['bioguide']]; n=l['name']; last=n['last']
  firsts={n['first']}
  if n.get('nickname'): firsts.add(n['nickname'])
  of=n.get('official_full','')
  if of: firsts.add(of.split()[0])
  for f in firsts:
    pats.append((re.compile(r'\b'+re.escape(f)+r'\s+(?:[A-Z]\.\s+)?'+re.escape(last)+r'\b'),m['bioguide']))
  ch='Senator|Sen\\.' if m['chamber']=='Senate' else 'Congressman|Congresswoman|Rep\\.|Representative'
  lastcount[(m['chamber'],last)]+=1
  pats.append((re.compile(r'\b(?:'+ch+r')\s+'+re.escape(last)+r'\b(?!\s+[A-Z][a-z])'),m['bioguide'],(m['chamber'],last)))
lh={p['x_handle'].lower():p['lid'] for p in P if p['x_handle']}
lnames=[(re.compile(r'\b'+re.escape(t)+r'\b',re.I),p['lid']) for p in P for t in p['name_terms']]
lp={p['lid']:p for p in P}
start={'L12':'2025-01-04','L14':'2025-01-01'}  # first date counted as lobbying era (left Congress Jan 2025 / first LDA filing year 2025)  # left Congress; earlier posts = colleague era
AMBIG_NAME={'L10'}  # "Connie Mack" also refers to Connie Mack III (former senator) / baseball
COPRES=re.compile(r"\b(with|w/|join(ed|ing)? (me|us)|great to (see|be|catch|meet|welcome)|good to (see|be)|catch(ing)? up|met with|meeting with|pictured|alongside|hosted|welcom(e|ed|ing)|stopped by|sat down|thanks? (you )?(\S+ )?for (joining|stopping|coming|having|hosting)|enjoyed|dinner|lunch|breakfast|reception|together|visited|presented me)\b",re.I)
AWARD=re.compile(r"\b(award|honou?red|presented|presenting|recogni[sz]ed|receive[d]?)\b",re.I)
POS=re.compile(r"\b(thank|thanks|congrat|proud|great|honou?r|friend|grateful|happy birthday|good luck|well done|go get|endorse|welcome)\w*",re.I)
seen=set(); edges=[]
for line in open('x_posts_raw.jsonl'):
  p=json.loads(line)
  if p['id'] in seen: continue
  seen.add(p['id'])
  au=(p.get('_author_username') or '').lower(); txt=p['text']; date=p['created_at'][:10]
  ments=[x['username'].lower() for x in (p.get('entities') or {}).get('mentions',[])] or [h[1:].lower() for h in re.findall(r'@\w{1,15}',txt)]
  media=[x.get('type') for x in p.get('_media',[])]
  alts=' | '.join(x.get('alt_text','') for x in p.get('_media',[]) if x.get('alt_text'))
  is_reply='in_reply_to_user_id' in p
  lead=re.match(r'^((?:@\w+\s*)+)',txt); lead_set=set(h[1:].lower() for h in re.findall(r'@\w+',lead.group(1))) if lead else set()
  pairs=[]  # (member_bioguide, lobbyist lid, direction, match_method)
  if au in mh:   # member-authored
    for h in ments:
      if h in lh: pairs.append((mh[au],lh[h],'member->lobbyist','@mention',h in lead_set))
    for rx,lid in lnames:
      if rx.search(txt) and not any(pp[1]==lid for pp in pairs):
        amb = lid in AMBIG_NAME and not re.search(r'Connie Mack IV\b',txt)
        pairs.append((mh[au],lid,'member->lobbyist','name_in_text_AMBIGUOUS' if amb else 'name_in_text',False))
  elif au in lh:
    lid=lh[au]
    for h in ments:
      if h in mh: pairs.append((mh[h],lid,'lobbyist->member','@mention',h in lead_set))
    for item in pats:
      rx,b=item[0],item[1]
      if len(item)==3 and lastcount[item[2]]>1: continue
      if rx.search(txt) and not any(pp[0]==b for pp in pairs):
        pairs.append((b,lid,'lobbyist->member','name_in_text',False))
  else:
    continue
  # dedupe
  uniq={}
  for pr in pairs: uniq.setdefault((pr[0],pr[1]),pr)
  nm=len(set(ments))
  for (b,lid),pr in uniq.items():
    has_photo='photo' in media
    if pr[4] and is_reply: t='reply'
    elif has_photo and (COPRES.search(txt) or COPRES.search(alts)): t='photo_together'
    elif has_photo and AWARD.search(txt): t='photo_probable_award'
    elif has_photo: t='photo_mention_unclear'
    elif nm>=8: t='list_mention'
    elif any(x in ('video','animated_gif') for x in media): t='video_or_gif_mention'
    elif POS.search(txt): t='shoutout'
    else: t='mention_other'
    era='colleague_era' if lid in start and date<start[lid] else 'lobbying_era'
    if 'AMBIGUOUS' in pr[3]: era='ambiguous_identity_excluded'
    first_start=min(t['start'] for t in byb[b]['terms'])
    member_status='in_congress' if date>=first_start else 'pre_congress (member not yet in Congress)'
    edges.append({'post_id':p['id'],'url':p.get('url') or f"https://x.com/{p.get('_author_username')}/status/{p['id']}",'date':date,'author':p.get('_author_username'),
      'direction':pr[2],'member_bioguide':b,'member_name':mname.get(b),'lobbyist_id':lid,'lobbyist_name':lp[lid]['name'],'firm':lp[lid]['firm'],
      'match_method':pr[3],'edge_type':t,'n_media':len(media),'media_types':';'.join(media),'alt_text':alts[:200],'n_mentions':nm,'era':era,'member_status_at_post':member_status,
      'text_snippet':re.sub(r'\s+',' ',txt)[:240],'query_set':p['_query_set'],'classified_at':NOW,'needs_review':t.startswith('photo'),'classifier':'rules_v2 (caption/tag/alt-text only; no image analysis)'})
W={'photo_together':3,'photo_probable_award':2,'photo_mention_unclear':1.5,'shoutout':1,'video_or_gif_mention':1,'mention_other':0.5,'reply':0.5,'list_mention':0.25}
for e in edges: e['weight']=W[e['edge_type']]
with open('pilot_edges_posts.csv','w') as f:
  w=csv.DictWriter(f,fieldnames=list(edges[0].keys())); w.writeheader(); w.writerows(sorted(edges,key=lambda e:(e['lobbyist_id'],e['date'])))
print(len(edges)); print(collections.Counter(e['edge_type'] for e in edges)); print(collections.Counter((e['lobbyist_name'],e['era']) for e in edges))
