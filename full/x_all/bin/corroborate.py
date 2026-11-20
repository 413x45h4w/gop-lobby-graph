"""corroborate.py: for unreviewed T1/T2 hits, look up each candidate person's LD-2 registrants and clients (2023-2026)
and report distinctive word overlap with the post text. Writes corroboration.csv (derived)."""
import gzip,json,glob,csv,re,collections,os,shutil,datetime
B='/workspace/gop-lobby-graph/full/x_all/'; L='/workspace/gop-lobby-graph/lda/ld2_universe/'
R=[r for r in csv.DictReader(open(B+'review_triage.csv'))]
done={r['post_id'] for r in csv.DictReader(open(B+'review_decisions.csv'))}
R=[r for r in R if r['post_id'] not in done and r['tier']!='X_member' and r['tier']!='T3_plain']
need=set()
for r in R:
  for pk in r['person_ids'].split('|'):
    for i in pk.split('|'): need.add(i)
need={int(x) for r in R for pk in r['person_ids'].split('|') for x in re.split(r'\D+',pk) if x}
orgs=collections.defaultdict(set)
for f in sorted(glob.glob(L+'ld2_202[3-6]_Q*.jsonl.gz')):
  for l in gzip.open(f,'rt'):
    j=json.loads(l)
    for a in j.get('acts') or []:
      for lb in a.get('lob') or []:
        if lb and lb[0] in need: orgs[lb[0]].add(j.get('rn') or ''); orgs[lb[0]].add(j.get('cn') or '')
STOP=set('the of and for inc llc co corp company association national american group partners strategies government affairs public policy council america united states international services consulting firm law llp pc ltd a an on in to at by'.split())
def toks(s): return {w for w in re.findall(r'[a-z]{4,}',s.lower()) if w not in STOP}
out=[]
for r in R:
  ids=[int(x) for x in re.split(r'\D+',r['person_ids']) if x]
  O=set().union(*[orgs.get(i,set()) for i in ids]) if ids else set()
  T=toks(r['text'].replace('@',' '))
  hits=sorted({o for o in O if toks(o)&T and o})
  out.append(dict(post_id=r['post_id'],author=r['author_handle'],matched=r['matched'],person_ids=r['person_ids'],n_orgs=len(O),overlap_orgs=' || '.join(h[:60] for h in hits[:4]),overlap_words=' '.join(sorted(set().union(*[toks(h)&T for h in hits]))) if hits else ''))
fn=B+'corroboration.csv'
if os.path.exists(fn): shutil.copy(fn,B+'corroboration.prev_'+datetime.datetime.now().strftime('%Y%m%d_%H%M')+'.csv')
w=csv.DictWriter(open(fn,'w',newline=''),fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
print(len(out),'with overlap',sum(1 for o in out if o['overlap_orgs']))
