# Build GOP member committee map: principal/authorized (bulk ccl24/26) + leadership PACs (OpenFEC sponsor_candidate_id)
import fecapi,json,csv,os,datetime
NOW=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
L=json.load(open('../../raw/legislators-current.json'))
gop={}
for l in L:
  if l['terms'][-1]['party']!='Republican': continue
  for c in l['id'].get('fec',[]): gop[c]=(l['id']['bioguide'],l['name'].get('official_full') or l['name']['first']+' '+l['name']['last'])
rows={}
for yy in ('24','26'):
  for line in open(f'../../fec/tmp/ccl{yy}.txt'):
    f=line.rstrip('\n').split('|')
    if f[0] in gop: rows[f[3]]=dict(committee_id=f[3],bioguide=gop[f[0]][0],member=gop[f[0]][1],cand_id=f[0],link_type='principal_or_authorized(ccl'+yy+')',committee_name='',designation=f[6] if len(f)>6 else '')
cands=sorted(gop)
lp=[]
cache='lpac_raw.jsonl'
if not os.path.exists(cache):
  with open(cache,'w') as out:
    for i in range(0,len(cands),40):
      page=1
      while True:
        d=fecapi.get('/committees/',{'sponsor_candidate_id':cands[i:i+40],'per_page':100,'page':page})
        for r in d['results']: out.write(json.dumps(r)+'\n')
        if page>=d['pagination']['pages']: break
        page+=1
      print(i,fecapi.STATE['remaining'],flush=True)
for r in map(json.loads,open(cache)):
  for s in r.get('sponsor_candidate_ids') or []:
    if s in gop and r['committee_id'] not in rows:
      rows[r['committee_id']]=dict(committee_id=r['committee_id'],bioguide=gop[s][0],member=gop[s][1],cand_id=s,link_type='leadership_pac_sponsor(designation '+str(r.get('designation'))+')',committee_name=r['name'],designation=r.get('designation'))
w=csv.DictWriter(open('gop_member_committees.csv','w'),fieldnames=list(next(iter(rows.values())))+['computed_at']);w.writeheader()
for r in rows.values(): r['computed_at']=NOW; w.writerow(r)
print('committees',len(rows),'lpac',sum(1 for r in rows.values() if r['link_type'].startswith('lead')),'members covered',len({r['bioguide'] for r in rows.values()}))
