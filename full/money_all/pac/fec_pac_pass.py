# PAC layer, step 1: filter FEC bulk individual contributions (indiv24/26, local copies dated 2026-11-15) to NON-candidate committees
# (PACs, super PACs, hybrids, party committees, JFCs, non-member leadership PACs) and to donor names in the LDA lobbyist name pool (incl. nicknames).
# Excluded: candidate committees (type H/S/P); member committees already in the direct layer (except party committees type X/Y/Z that FEC ccl links
# to a member, e.g. NRSC->Sullivan, which the direct layer dropped); ActBlue/WinRed conduit receipts (counted, not kept: the earmarked recipient files its own row).
import json,glob,sys,subprocess,datetime,re,csv,gzip,collections
sys.path.insert(0,'../..'); from nicks import NICK
cyc=sys.argv[1]
CM={}
for yy in ('24','26'):
  for line in open(f'../raw/fec_bulk/cm{yy}.txt',encoding='latin-1'):
    q=line.rstrip('\n').split('|'); CM[q[0]]=q[9]
MEMC={r['committee_id'] for r in csv.DictReader(open('../bundling/member_committees_all.csv'))}
CONDUIT={'C00401224','C00694323'}
def keep(c):
  t=CM.get(c,'')
  if c in CONDUIT or t in ('H','S','P'): return False
  if c in MEMC and t not in ('X','Y','Z'): return False
  return True
SUF={'JR','SR','II','III','IV'}
def cl(s): return ' '.join(x for x in re.split(r'[\s\.]+',s.upper().strip()) if x and x not in SUF)
pool=set()
def add(fi,la):
  if not (fi and la): return
  f=fi.upper().split()[0].strip('.'); l=cl(la)
  for v in {f}|set(NICK.get(f,[]))|{k for k,vs in NICK.items() if f in vs}: pool.add((l,v))
for fn in glob.glob('../../../lda/ld2_universe/*.jsonl.gz'):
  for line in gzip.open(fn,'rt'):
    for a in json.loads(line)['acts']:
      for _,fi,la,_ in a['lob']: add(fi,la)
for fn in glob.glob('../../../lda/ld203_universe/*.jsonl.gz'):
  for line in gzip.open(fn,'rt'):
    d=json.loads(line); add(d.get('fn'),d.get('ln'))
lasts={p[0] for p in pool}
now=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
out=gzip.open(f'../raw/fec_indiv{cyc}_pac_poolname.jsonl.gz','wt'); n=0; k=0; st=collections.Counter()
p=subprocess.Popen(['unzip','-p',f'../raw/fec_bulk/indiv{cyc}.zip','itcont.txt'],stdout=subprocess.PIPE,bufsize=1<<22)
for raw in p.stdout:
  n+=1
  if n%10_000_000==0: print(n,k,dict(st),file=sys.stderr,flush=True)
  c=raw[:9].decode('latin-1')
  if c in CONDUIT: st['conduit_rows_skipped']+=1; continue
  if not keep(c): continue
  f=raw.decode('latin-1').rstrip('\n').split('|')
  if f[6]!='IND': continue
  nm=f[7].upper()
  if ',' not in nm: continue
  last,rest=nm.split(',',1); last=cl(last)
  if last not in lasts: continue
  toks=[t for t in re.split(r'[\s\.]+',rest) if t and t not in ('MR','MS','MRS','DR','HON')]
  if not toks or (last,toks[0]) not in pool: continue
  out.write(json.dumps({'f':now,'cyc':cyc,'cmte':c,'name':nm,'city':f[8],'st':f[9],'emp':f[11],'occ':f[12],'dt':f[13],'amt':f[14],'tp':f[5],'memo':f[18],'memo_text':f[19][:80],'sub_id':f[20],'image':f[4]},separators=(',',':'))+'\n'); k+=1
out.close()
print('lines',n,'kept',k,dict(st),file=sys.stderr)
