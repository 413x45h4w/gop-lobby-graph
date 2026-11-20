"""usage: ingest.py <qid> <result_path> [<qid> <result_path> ...]
Logs each call (x_calls_all.csv, raw/), marks qid done in state.json, appends candidate hits to hits_raw.jsonl
(for hand review), queues page-2 follow-ups when next_token is present, then prints a compact summary."""
import sys,os,json,re,shutil
sys.path.insert(0,os.path.dirname(__file__)); import xlog
B=xlog.BASE
Q=json.load(open(B+'queue.json')); BL={b['id']:b for b in Q['blocks']}
S=json.load(open(B+'state.json'))
import csv
MH={r['handle'].lower():r for r in csv.DictReader(open(B+'member_handles_all_party.csv'))}
QUIET=os.environ.get('QUIET','1')=='1'
a=sys.argv[1:]; last=None
for k in range(0,len(a),2):
  qid,path=a[k],a[k+1]
  parts=qid.split('.'); bid,cid=parts[0],parts[1]
  j,rlm,reset,rlt,raw=xlog.parse(path)
  err=None
  if 'data' not in j and 'meta' not in j:
    err=(j.get('title') or j.get('detail') or str(j)[:200])
  b=BL[bid]; cid0=cid.split(':')[0]; ch=Q['chunks'][cid0]['handles']
  if Q['chunks'][cid0].get('type')=='list': summ=f'search {qid}: list:{Q["chunks"][cid0]["list_id"]} ({len(ch)} probed on-list member handles) x {len(b["names"])} name strings ({len(b["persons"])} persons)'
  else: summ=f'search {qid}: {len(ch)} member handles x {len(b["names"])} name strings ({len(b["persons"])} persons)'
  n=xlog.log_call('search_posts_all',qid,summ,j,rlm,reset,rlt,('ERROR '+err) if err else '')
  if rlt is not None: S['last_reads_left_today']=rlt; S['last_reads_left_minute']=rlm; S['last_reset_minute_utc']=reset
  if err:
    print('ERR',qid,err,rlm,rlt); S.setdefault('errors',[]).append({'qid':qid,'at':xlog.now(),'err':err}); continue
  U={u['id']:u.get('username','') for u in (j.get('includes') or {}).get('users',[])}
  MD={m['media_key']:m for m in (j.get('includes') or {}).get('media',[])}
  nh=0
  for p in j.get('data',[]) or []:
    txt=p.get('text','')+' '+((p.get('note_post') or {}).get('text','') if isinstance(p.get('note_post'),dict) else '')
    alts=[MD.get(mk,{}).get('alt_text') or '' for mk in (p.get('attachments') or {}).get('media_keys',[])]
    types=[MD.get(mk,{}).get('type','') for mk in (p.get('attachments') or {}).get('media_keys',[])]
    hay=(txt+' '+' '.join(alts)).lower()
    matched=[s for s in b['names'] if s.lower() in hay]
    au=U.get(p.get('author_id'),'')
    mrow=MH.get(au.lower())
    rec=dict(found_at=xlog.now(),qid=qid,member_author=bool(mrow),member_bioguide=(mrow or {}).get('bioguide',''),post_id=p['id'],url=f"https://x.com/{au or 'i'}/status/{p['id']}",author=au,created_at=p.get('created_at'),
             conversation_id=p.get('conversation_id'),media=types,alt_text=[x for x in alts if x],matched=matched,text=txt.strip())
    with open(B+'hits_raw.jsonl','a') as f: f.write(json.dumps(rec)+'\n')
    nh+=1
    if QUIET and not (mrow and matched): continue
    if os.environ.get('SHOWHITS')!='1': continue
    print(f"HIT {qid} @{au} {p.get('created_at','')[:10]} {rec['url']} m={matched} media={types} :: {txt.strip()[:220]!r}"+(f" ALT={alts}" if any(alts) else ''))
  nt=(j.get('meta') or {}).get('next_token')
  rc=len(j.get('data',[]) or [])
  pg=int(qid.split('.p')[1]) if '.p' in qid else 1
  if nt and ((rc<15 and rc>0) or (rc==0 and pg>=3)):
    S.setdefault('skipped_next_tokens',[]).append({'qid':qid,'result_count':rc,'next_token':nt,'at':xlog.now()})
  elif nt:
    S.setdefault('followups',[]).append({'qid':qid.split('.p')[0]+f'.p{len([f for f in S.get("followups",[]) if f["qid"].startswith(qid.split(".p")[0])])+2}','block':bid,'chunk':cid,'next_token':nt,'added_at':xlog.now()})
    print('NEXT_TOKEN queued for',qid)
  S['done'][qid]={'at':xlog.now(),'n':len(j.get('data',[]) or []),'call_seq':n}
  last=(rlm,rlt)
S['updated_at']=xlog.now()
tmp=B+'state.json.tmp'; json.dump(S,open(tmp,'w')); os.replace(tmp,B+'state.json')
nq=sum(len(b['need']) for b in Q['blocks']); nd=sum(1 for d in S['done'] if '.p' not in d)
nmh=sum(1 for l in open(B+'hits_raw.jsonl') if '"member_author": true' in l)
print(f'member-author hits total {nmh}; done {nd}/{nq} queries; reads left minute/today: {last}')
