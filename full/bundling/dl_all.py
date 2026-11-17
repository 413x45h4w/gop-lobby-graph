import json,os,time,subprocess
R=[json.loads(l) for l in open('f3l_filings_raw.jsonl') if '_empty' not in l]
for r in R:
  u=r.get('fec_url'); n=r['file_number']
  if not u: continue
  p=f'fecfiles/{n}.fec'
  if os.path.exists(p) and os.path.getsize(p)>0: continue
  subprocess.run(['curl','-sS','-m','60','-A','Mozilla/5.0 research','-o',p,u])
  time.sleep(0.4)
print('done')
