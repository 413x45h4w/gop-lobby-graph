"""emit.py N: write the next N queries (same order/logic as next.py) to req/q/<qid>.txt (no newline) and print qid [NT]."""
import os,sys,subprocess
B='/workspace/gop-lobby-graph/full/x_all/'
os.makedirs(B+'req/q',exist_ok=True)
out=subprocess.run([sys.executable,B+'bin/next.py',sys.argv[1]],env=dict(os.environ,FULL='1'),capture_output=True,text=True,check=True).stdout
for l in out.splitlines():
  p=l.split('\t'); open(B+'req/q/'+p[0]+'.txt','w').write(p[1]); print(p[0],p[2] if len(p)>2 else '')
