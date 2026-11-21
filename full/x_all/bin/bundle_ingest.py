"""bundle_ingest.py <bundle.json>: split a TS-SDK batch [{qid,result,est_left}] into req/r/<qid>.txt and ingest them in order.
(Run 2026-11-20 onward: X calls are made from the TS SDK; the reads-left note is not machine-readable there,
so est_left is the run's own call-count estimate and is written to the call log note, not as X-reported reads.)"""
import sys,json,os,subprocess
B='/workspace/gop-lobby-graph/full/x_all/'
bun=json.load(open(sys.argv[1])); args=[]
for it in bun:
  p=B+'req/r/'+it['qid']+'.txt'; open(p,'w').write(json.dumps(it['result'])); args+=[it['qid'],p]
if args: subprocess.run([sys.executable,B+'bin/ingest.py']+args,check=True)
