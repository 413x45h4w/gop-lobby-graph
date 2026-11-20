# Build all-party member handle candidate list (539 current members) from local sources.
import json,csv,collections,datetime,os
R='/workspace/gop-lobby-graph/'
NOW=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
sm=json.load(open(R+'raw/legislators-social-media.json'))
smb={s['id']['bioguide']:s.get('social',{}) for s in sm}
wd=collections.defaultdict(list)
for r in csv.DictReader(open(R+'raw/wikidata_bioguide_x.csv')): wd[r['bio']].append(r['handle'])
ex=collections.defaultdict(list)
for h,b in json.load(open(R+'full/x/member_handles_all.json')): ex[b].append(h)
mem=list(csv.DictReader(open(R+'full/money_all/member_totals_all.csv')))
rows=[]
for m in mem:
  b=m['bioguide'];seen=set()
  srcs=[(smb.get(b,{}).get('twitter'),'congress-legislators official')]+[(h,'gop_x_layer member_handles_all.json') for h in ex[b]]+[(h,'wikidata P2002') for h in wd[b]]
  for h,s in srcs:
    if not h or h.lower() in seen: continue
    seen.add(h.lower())
    rows.append(dict(bioguide=b,member=m['member'],party=m['party'],chamber=m['chamber'],state=m['state'],handle=h,source=s,
      in_gop_layer=int(any(h.lower()==x.lower() for x in ex[b]))))
with open('member_handle_candidates.csv','w',newline='') as f:
  w=csv.DictWriter(f,list(rows[0].keys())+['built_at']); w.writeheader()
  for r in rows: w.writerow({**r,'built_at':NOW})
hs=[r['handle'] for r in rows]
os.makedirs('req',exist_ok=True)
for i in range(0,len(hs),100):
  open(f'req/verify_{i//100}.txt','w').write(','.join(hs[i:i+100]))
print(len(rows),'candidates',len(hs)//100+1,'batches')
