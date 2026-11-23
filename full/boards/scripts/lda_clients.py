# Aggregate LDA client lobbying spend 2023-2026 from local LD-2 crawl (lda/ld2_universe). Spend = income reported by outside registrants + expenses of in-house (self-filing) registrants.
import gzip,json,glob,collections,csv,datetime,sys
sys.path.insert(0,'scripts'); from orgnorm import key
NOW=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
A=collections.defaultdict(lambda: dict(usd=0.0,names=collections.Counter(),cids=set(),regs=set(),n=0,years=set()))
seen=set()
for fn in sorted(glob.glob('/workspace/gop-lobby-graph/lda/ld2_universe/*.jsonl.gz')):
  for line in gzip.open(fn,'rt'):
    d=json.loads(line)
    if d['uuid'] in seen or d['y']<2023: continue
    seen.add(d['uuid']); k=key(d['cn'])
    if not k: continue
    a=A[k]; v=float(d.get('inc') or 0)+float(d.get('exp') or 0)
    a['usd']+=v; a['names'][d['cn']]+=1; a['cids'].add(str(d['cid'])); a['regs'].add(d['rn']); a['n']+=1; a['years'].add(d['y'])
R=[dict(client_key=k,client_name=a['names'].most_common(1)[0][0],lda_spend_2023_26=round(a['usd']),n_filings=a['n'],n_registrants=len(a['regs']),lda_client_ids='|'.join(sorted(a['cids'])[:50]),
  years='|'.join(map(str,sorted(a['years']))),registrants_sample='|'.join(sorted(a['regs'])[:8]),computed_at=NOW) for k,a in A.items()]
R.sort(key=lambda r:-r['lda_spend_2023_26'])
for i,r in enumerate(R,1): r['rank']=i
w=csv.DictWriter(open('lda_clients_spend_2023_26.csv','w'),fieldnames=['rank']+[k for k in R[0] if k!='rank']); w.writeheader(); w.writerows(R)
print(len(R),'clients; filings',len(seen)); print(R[:5])
