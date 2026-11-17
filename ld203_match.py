import json,csv,re,collections,datetime
L=json.load(open('raw/legislators-current.json'))
R=[l for l in L if l['terms'][-1]['party']=='Republican']
def keyset(l):
  n=l['name']; firsts={n['first'].upper()}
  if n.get('nickname'): firsts.add(n['nickname'].upper())
  if n.get('official_full'): firsts.add(n['official_full'].split()[0].upper())
  return firsts,n['last'].upper()
mem=[(l['id']['bioguide'],l['name'].get('official_full'),)+keyset(l) for l in R]
seen=set(); rows=[]
for line in open('lda/ld203_pilot_contributions.jsonl'):
  d=json.loads(line)
  for it in d['items']:
    k=(d['lid'],it.get('payee_name'),it.get('honoree_name'),it.get('amount'),it.get('date'))
    if k in seen: continue
    seen.add(k)
    txt=((it.get('honoree_name') or '')+' | '+(it.get('payee_name') or '')).upper()
    hits=[]
    for b,full,firsts,last in mem:
      if re.search(r'\b'+re.escape(last)+r'\b',txt) and any(re.search(r'\b'+re.escape(f)+r'\b',txt) for f in firsts): hits.append((b,full))
    rows.append({'lobbyist_id':d['lid'],'year':d['year'],'period':d['period'],'filing_uuid':d['filing_uuid'],'type':it.get('contribution_type'),'payee':it.get('payee_name'),'honoree':it.get('honoree_name'),'amount':it.get('amount'),'date':it.get('date'),
      'matched_gop_member_bioguide':';'.join(h[0] for h in hits),'matched_gop_member':';'.join(h[1] for h in hits),'match_rule':'first+last name in honoree/payee text','computed_at':datetime.datetime.now().astimezone().isoformat(timespec='seconds')})
with open('pilot_ld203_contributions.csv','w') as f:
  w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
agg=collections.defaultdict(lambda:[0,0.0,set(),0.0])
for r in rows:
  a=agg[r['lobbyist_id']]; a[1]+=float(r['amount'] or 0)
  if r['matched_gop_member_bioguide']: a[0]+=1; a[3]+=float(r['amount'] or 0); a[2].update(r['matched_gop_member_bioguide'].split(';'))
for k,v in sorted(agg.items()): print(k,'items_to_gop_members',v[0],'usd_to_gop_members',round(v[3]),'distinct',len(v[2]),'all_usd',round(v[1]))
json.dump({k:{'items_to_current_gop_members':v[0],'usd_to_current_gop_members':v[3],'distinct_gop_members_funded':len(v[2]),'all_ld203_usd':v[1],'members':sorted(v[2])} for k,v in agg.items()},open('ld203_summary.json','w'),indent=1)
