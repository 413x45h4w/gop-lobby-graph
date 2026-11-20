"""ingest a round: ir.py <hash1> <hash2> ... (asset hashes or paths, in the same order as the last `next.py` output saved to req/last_round.txt)"""
import sys,subprocess,os
A='/cursor/stores/user/grok-bot/agents/541d1ad4-458c-449f-a6ec-f1b5f02d3dfe/assets/'
B='/workspace/gop-lobby-graph/full/x_all/'
q=[l.split('\t')[0].strip() for l in open(B+'req/last_round.txt') if l.strip()]
h=sys.argv[1:]; assert len(h)<=len(q),(len(h),len(q))
args=[]
for qi,hh in zip(q,h): args+= [qi, hh if hh.startswith('/') else A+hh+('' if hh.endswith('.txt') else '.txt')]
subprocess.run([sys.executable,B+'bin/ingest.py']+args,check=True)
