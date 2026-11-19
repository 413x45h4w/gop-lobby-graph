# ALL current members' committees: principal/authorized/JFC from FEC bulk ccl24+ccl26 (fetched 2026-11-18) + leadership PACs from OpenFEC sponsor_candidate_id.
import fecapi,json,csv,os,datetime
NOW=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
L=json.load(open('../../../raw/legislators-current.json'))
mem={}
for l in L:
  for c in l['id'].get('fec',[]): mem[c]=(l['id']['bioguide'],l['name'].get('official_full') or l['name']['first']+' '+l['name']['last'],l['terms'][-1]['party'],l['terms'][-1]['type'])
# manual: Sen. Darline Graham (G000608, appointed 2026-07-14) has no FEC id in legislators-current; cn26 has exactly one SC Senate REP candidate GRAHAM, DARLINE (S6SC04437)
EXTRA={'S6SC04437':'G000608'}
for c,b in EXTRA.items():
  l=[x for x in L if x['id']['bioguide']==b][0]; mem[c]=(b,l['name'].get('official_full'),l['terms'][-1]['party'],l['terms'][-1]['type'])
CMT={}
for yy in ('24','26'):
  for line in open(f'../raw/fec_bulk/cm{yy}.txt',encoding='latin-1'):
    f=line.split('|'); CMT[f[0]]=(f[1],f[9],f[8])
rows={}
for yy in ('24','26'):
  for line in open(f'../raw/fec_bulk/ccl{yy}.txt'):
    f=line.rstrip('\n').split('|')
    if f[0] in mem: rows.setdefault(f[3],dict(committee_id=f[3],bioguide=mem[f[0]][0],member=mem[f[0]][1],party=mem[f[0]][2],cand_id=f[0],link_type='principal_or_authorized(ccl'+yy+')',committee_name=CMT.get(f[3],('',))[0],committee_type=CMT.get(f[3],('',''))[1],designation=f[5]))
cands=sorted(mem)
cache='lpac_raw_all.jsonl'
done=set()
if os.path.exists(cache):
  for l in open(cache): done.add(json.loads(l).get('_batch'))
with open(cache,'a') as out:
  for i in range(0,len(cands),40):
    if i in done: continue
    page=1
    while True:
      d=fecapi.get('/committees/',{'sponsor_candidate_id':cands[i:i+40],'per_page':100,'page':page})
      for r in d['results']: r['_batch']=i; r['_fetched']=NOW; out.write(json.dumps(r)+'\n')
      if not d['results']: out.write(json.dumps({'_batch':i,'_empty':True,'_fetched':NOW})+'\n')
      if page>=d['pagination']['pages']: break
      page+=1
    print(i,fecapi.STATE['remaining'],flush=True)
for r in map(json.loads,open(cache)):
  if r.get('_empty'): continue
  for s in r.get('sponsor_candidate_ids') or []:
    if s in mem and r['committee_id'] not in rows:
      rows[r['committee_id']]=dict(committee_id=r['committee_id'],bioguide=mem[s][0],member=mem[s][1],party=mem[s][2],cand_id=s,link_type='leadership_pac_sponsor(designation '+str(r.get('designation'))+')',committee_name=r['name'],committee_type=r.get('committee_type'),designation=r.get('designation'))
w=csv.DictWriter(open('member_committees_all.csv','w'),fieldnames=list(next(iter(rows.values())))+['computed_at']);w.writeheader()
for r in rows.values(): r['computed_at']=NOW; w.writerow(r)
import collections
print('committees',len(rows),collections.Counter(r['link_type'][:10] for r in rows.values()),'members covered',len({r['bioguide'] for r in rows.values()}),'of',len(L))
print('members with no committee:',[ (l['id']['bioguide'],l['name'].get('official_full')) for l in L if l['id']['bioguide'] not in {r['bioguide'] for r in rows.values()}])
