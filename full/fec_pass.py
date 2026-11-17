import json,glob,sys,subprocess,datetime,re
cyc=sys.argv[1]  # 24 or 26
L=json.load(open('../raw/legislators-current.json'))
gop={}
for l in L:
  if l['terms'][-1]['party']!='Republican': continue
  for c in l['id'].get('fec',[]): gop[c]=l['id']['bioguide']
cm2b={}
for yy in ('24','26'):
  for line in open(f'../fec/tmp/ccl{yy}.txt'):
    f=line.rstrip('\n').split('|')
    if f[0] in gop: cm2b[f[3]]=gop[f[0]]
# pool names from LD-2 universe
pool=set()
for fn in glob.glob('../lda/ld2_universe/*.jsonl.gz'):
  for line in __import__('gzip').open(fn,'rt'):
    d=json.loads(line)
    for a in d['acts']:
      for _,fi,la,_ in a['lob']:
        if fi and la: pool.add((la.upper().strip(), fi.upper().split()[0].strip('.')))
lasts={p[0] for p in pool}
print('gop cmtes',len(cm2b),'pool',len(pool),file=sys.stderr,flush=True)
out=open(f'fec_indiv{cyc}_gopmember_poolname.jsonl','a'); n=0; k=0
now=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
p=subprocess.Popen(['unzip','-p',f'../fec/tmp/indiv{cyc}.zip','itcont.txt'],stdout=subprocess.PIPE,bufsize=1<<22)
for raw in p.stdout:
  n+=1
  c=raw[:9].decode()
  if c not in cm2b: continue
  f=raw.decode('latin-1').rstrip('\n').split('|')
  if f[6]!='IND': continue
  nm=f[7].upper()
  if ',' not in nm: continue
  last,rest=nm.split(',',1); last=last.strip()
  if last not in lasts: continue
  toks=[t for t in re.split(r'[\s\.]+',rest) if t and t not in ('MR','MS','MRS','DR','HON')]
  if not toks or (last,toks[0]) not in pool: continue
  out.write(json.dumps({'f':now,'cyc':cyc,'cmte':c,'bio':cm2b[c],'name':nm,'city':f[8],'st':f[9],'emp':f[11],'occ':f[12],'dt':f[13],'amt':f[14],'tp':f[5],'memo':f[18],'memo_text':f[19][:80],'sub_id':f[20],'image':f[4]},separators=(',',':'))+'\n'); k+=1
print('lines',n,'kept',k,file=sys.stderr)
