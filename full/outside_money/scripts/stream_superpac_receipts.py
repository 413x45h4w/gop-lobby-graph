# Stream FEC indiv{cyc}.zip (itcont.txt only) and keep receipts of IE-only (O), single-candidate IE (U) and hybrid (V,W) committees,
# plus any committee that appears as a spender in the FEC independent_expenditure_{year}.csv file. Output: gzip pipe-delimited raw lines.
import zipfile,gzip,io,sys,csv,os,json,datetime
cyc=sys.argv[1]; B='/workspace/gop-lobby-graph/full/money_all/raw/fec_bulk'
S={}; CT={}
for c in ('24','26'):
  for l in open(f'{B}/cm{c}.txt',encoding='latin-1'):
    f=l.rstrip('\n').split('|')
    CT[f[0]]=f[9]
    if f[9] in ('O','U','V','W'): S[f[0]]=f[9]
for y in ('2024','2026'):
  for r in csv.DictReader(open(f'raw/independent_expenditure_{y}.csv',encoding='latin-1')):
    # IE spenders that are not super PACs: keep only non-committee filers (type I) and ids missing from the committee master.
    # Party committees (X,Y), candidate committees (H,S,P), conduits (ActBlue/WinRed) and ordinary PACs (N,Q) are excluded: their receipts are not super-PAC money.
    if r['spe_id'].startswith('C') and r['spe_id'] not in S and CT.get(r['spe_id'],'') in ('I',''): S[r['spe_id']]='ie_spender_type_'+(CT.get(r['spe_id']) or 'not_in_master')
json.dump(S,open(f'raw/superpac_committee_set_{cyc}.json','w'))
out=f'raw/superpac_receipts{cyc}.txt.gz'; tmp=out+'.part'
n=k=0
with zipfile.ZipFile(f'{B}/indiv{cyc}.zip') as z, z.open('itcont.txt') as fh, gzip.open(tmp,'wt') as o:
  for line in io.TextIOWrapper(fh,encoding='latin-1'):
    n+=1
    if line[:9] in S: o.write(line); k+=1
    if n%20000000==0: print(datetime.datetime.now().isoformat(timespec='seconds'),n,k,flush=True)
os.rename(tmp,out); print('DONE',n,k,flush=True)
