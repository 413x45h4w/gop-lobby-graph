# Full LD-2 crawl incl. specific-issue descriptions (bills), gov entities, foreign entities, affiliated orgs.
# Resumable: state in raw/<yr>_<q>.next ; output gz appended (multi-member gzip). Pull timestamp per record ('f').
import json,sys,time,urllib.request,urllib.parse,datetime,os,gzip
year,ftype=sys.argv[1],sys.argv[2]
base=f'raw/ld2full_{year}_{ftype}'; state=base+'.next'; donef=base+'.done'
if os.path.exists(donef): sys.exit(0)
u=open(state).read().strip() if os.path.exists(state) else ''
if not u: u="https://lda.gov/api/v1/filings/?"+urllib.parse.urlencode({'filing_year':year,'filing_type':ftype,'page_size':25,'ordering':'dt_posted'})
while u:
  for i in range(10):
    try:
      req=urllib.request.Request(u,headers={'Accept':'application/json','User-Agent':'gop-lobby-graph research (public data)'})
      d=json.load(urllib.request.urlopen(req,timeout=90)); break
    except Exception as e:
      print('err',year,ftype,e,file=sys.stderr,flush=True); time.sleep(20*(i+1))
  else: sys.exit(1)
  now=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
  buf=[]
  for r in d['results']:
    acts=[]
    for la in r['lobbying_activities'] or []:
      acts.append({'i':la['general_issue_code'],'d':la.get('description') or '','fe':la.get('foreign_entity_issues') or '',
        'e':[g.get('name') for g in (la.get('government_entities') or [])],
        'l':[[l['lobbyist']['id'],l['lobbyist']['first_name'],l['lobbyist']['last_name'],l['covered_position'],l.get('new')] for l in la['lobbyists']]})
    c=r['client']; g=r['registrant']
    buf.append(json.dumps({'f':now,'uuid':r['filing_uuid'],'y':r['filing_year'],'t':r['filing_type'],'p':r['filing_period'],'posted':r.get('dt_posted'),
      'term':r.get('termination_date'),'rid':g['id'],'rn':g['name'],'cid':c['id'],'cn':c['name'],'cdesc':c.get('general_description'),
      'cst':c.get('state'),'cco':c.get('country'),'cgov':c.get('client_government_entity'),'inc':r['income'],'exp':r['expenses'],'acts':acts,
      'fe':[[x.get('name'),x.get('country'),x.get('contribution'),x.get('ownership_percentage')] for x in (r.get('foreign_entities') or [])],
      'ao':[[x.get('name'),x.get('country')] for x in (r.get('affiliated_organizations') or [])]},separators=(',',':')))
  with gzip.open(base+'.jsonl.gz','at') as out: out.write('\n'.join(buf)+('\n' if buf else ''))
  u=d['next'] or ''; open(state,'w').write(u)
  time.sleep(0.5)
open(donef,'w').write(datetime.datetime.now().astimezone().isoformat(timespec='seconds'))
print('done',year,ftype,file=sys.stderr,flush=True)
