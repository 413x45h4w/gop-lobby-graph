# Filter FEC bulk individual contributions (indiv24 / indiv26, FEC files dated 2026-11-15) to committees of ALL current members
# (principal/authorized/JFC via ccl + leadership PACs) and to donor names whose (LAST, FIRST) matches any LDA lobbyist name (LD-2 2022Q4-2026Q3 or LD-203), incl. nickname variants.
import json,glob,sys,subprocess,datetime,re,csv,gzip
sys.path.insert(0,'..'); from nicks import NICK
cyc=sys.argv[1]
cm2b={r['committee_id']:(r['bioguide'],r['link_type']) for r in csv.DictReader(open('bundling/member_committees_all.csv'))}
SUF={'JR','SR','II','III','IV'}
def cl(s): 
  t=[x for x in re.split(r'[\s\.]+',s.upper().strip()) if x and x not in SUF]; return ' '.join(t)
pool=set()
def add(fi,la):
  if not (fi and la): return
  f=fi.upper().split()[0].strip('.'); l=cl(la)
  for v in {f}|set(NICK.get(f,[]))|{k for k,vs in NICK.items() if f in vs}: pool.add((l,v))
for fn in glob.glob('../../lda/ld2_universe/*.jsonl.gz'):
  for line in gzip.open(fn,'rt'):
    for a in json.loads(line)['acts']:
      for _,fi,la,_ in a['lob']: add(fi,la)
for fn in glob.glob('../../lda/ld203_universe/*.jsonl.gz'):
  for line in gzip.open(fn,'rt'):
    d=json.loads(line); add(d.get('fn'),d.get('ln'))
lasts={p[0] for p in pool}
print('member cmtes',len(cm2b),'pool',len(pool),file=sys.stderr,flush=True)
now=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
out=gzip.open(f'raw/fec_indiv{cyc}_allmember_poolname.jsonl.gz','wt'); n=0; k=0
p=subprocess.Popen(['unzip','-p',f'raw/fec_bulk/indiv{cyc}.zip','itcont.txt'],stdout=subprocess.PIPE,bufsize=1<<22)
for raw in p.stdout:
  n+=1
  if n%10_000_000==0: print(n,k,file=sys.stderr,flush=True)
  c=raw[:9].decode('latin-1')
  if c not in cm2b: continue
  f=raw.decode('latin-1').rstrip('\n').split('|')
  if f[6]!='IND': continue
  nm=f[7].upper()
  if ',' not in nm: continue
  last,rest=nm.split(',',1); last=cl(last)
  if last not in lasts: continue
  toks=[t for t in re.split(r'[\s\.]+',rest) if t and t not in ('MR','MS','MRS','DR','HON')]
  if not toks or (last,toks[0]) not in pool: continue
  out.write(json.dumps({'f':now,'cyc':cyc,'cmte':c,'bio':cm2b[c][0],'link':cm2b[c][1],'name':nm,'city':f[8],'st':f[9],'emp':f[11],'occ':f[12],'dt':f[13],'amt':f[14],'tp':f[5],'memo':f[18],'memo_text':f[19][:80],'sub_id':f[20],'image':f[4]},separators=(',',':'))+'\n'); k+=1
out.close()
print('lines',n,'kept',k,file=sys.stderr)
