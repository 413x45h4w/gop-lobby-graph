# Caucus memberships: member links inside the "members" sections of English Wikipedia caucus articles (revision id recorded),
# resolved title -> Wikidata -> bioguide (P1157). Plus Wikidata P463 (member of) caucus statements. Confidence: medium (crowd-sourced).
import sys,os,re,json,urllib.request,urllib.parse,collections
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','legislative')); import dclib
UA={'User-Agent':'gop-lobby-graph research (fv5z2nvm@mail.grokbot.com)'}
def api(params,host='en.wikipedia.org'):
  u=f'https://{host}/w/api.php?'+urllib.parse.urlencode({**params,'format':'json','formatversion':'2'})
  return json.load(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=60))
PAGES=['Freedom Caucus','Congressional Progressive Caucus','New Democrat Coalition','Blue Dog Coalition','Republican Study Committee','Problem Solvers Caucus',
 'Congressional Black Caucus','Congressional Hispanic Caucus','Congressional Asian Pacific American Caucus','Republican Main Street Caucus','Congressional Hispanic Conference',
 'Republican Governance Group','Congressional Western Caucus','Congressional LGBTQ+ Equality Caucus','Congressional Bitcoin Caucus','Congressional Taiwan Caucus','Second Amendment Caucus',
 'Congressional Pro-Life Caucus','Climate Solutions Caucus','Senate Climate Change Task Force','Congressional Blockchain Caucus','Congressional Shipbuilding Caucus']
rows=[];log=[]
title2qid={}
for p in PAGES:
  try:
    j=api({'action':'parse','page':p,'prop':'sections|revid','redirects':1})
  except Exception as e: log.append({'page':p,'error':str(e)[:100]}); continue
  if 'error' in j: log.append({'page':p,'error':j['error'].get('info')}); continue
  rev=j['parse']['revid']; secs=[s for s in j['parse']['sections'] if re.search(r'member',s['line'],re.I) and not re.search(r'former|notable former|past|chair|leader',s['line'],re.I)]
  links=set()
  for s in secs:
    w=api({'action':'parse','page':j['parse']['title'],'prop':'wikitext','section':s['index']})['parse']['wikitext']
    for m in re.finditer(r'\[\[([^\]|#]+)',w): links.add(m.group(1).strip())
  log.append({'page':p,'resolved_title':j['parse']['title'],'revid':rev,'sections':[s['line'] for s in secs],'n_links':len(links)})
  for t in links: rows.append((j['parse']['title'],rev,t,','.join(s['line'] for s in secs)))
titles=sorted({r[2] for r in rows})
for i in range(0,len(titles),50):
  j=api({'action':'query','titles':'|'.join(titles[i:i+50]),'prop':'pageprops','ppprop':'wikibase_item','redirects':1})
  red={r['from']:r['to'] for r in j['query'].get('redirects',[])}; norm={r['from']:r['to'] for r in j['query'].get('normalized',[])}
  q={pg['title']:pg.get('pageprops',{}).get('wikibase_item') for pg in j['query']['pages']}
  for t in titles[i:i+50]:
    tt=norm.get(t,t); tt=red.get(tt,tt); title2qid[t]=q.get(tt)
qids=sorted({v for v in title2qid.values() if v}); q2b={}
for i in range(0,len(qids),50):
  j=api({'action':'wbgetentities','ids':'|'.join(qids[i:i+50]),'props':'claims'},host='www.wikidata.org')
  for k,e in j.get('entities',{}).items():
    c=e.get('claims',{}).get('P1157')
    if c: q2b[k]=c[0]['mainsnak']['datavalue']['value']
M=dclib.members(); now=dclib.NOW(); out=[]
for cau,rev,t,secs in rows:
  b=q2b.get(title2qid.get(t))
  if b and b in M: out.append([b,M[b]['name'],M[b]['party'],M[b]['chamber'],cau,'wikipedia_members_section',f'https://en.wikipedia.org/w/index.php?oldid={rev}',secs,'medium',now])
import csv
for r in csv.DictReader(open('/workspace/tmp_dcgraph/wd_caucus.csv')):
  b=r['bioguide']
  if b in M: out.append([b,M[b]['name'],M[b]['party'],M[b]['chamber'],r['orgLabel'],'wikidata_P463',r['org'],f"start={r['start'][:10]} end={r['end'][:10]}",'medium',now])
seen=set(); ded=[]
for r in out:
  k=(r[0],r[4].lower(),r[5])
  if k not in seen: seen.add(k); ded.append(r)
n=dclib.wcsv('member_caucus_edges.csv',['bioguide','member','party','chamber','caucus','source','source_ref','section_or_dates','confidence','built_at'],ded)
json.dump(log,open('raw/caucus_pages_log.json','w'),indent=1)
print(n,collections.Counter(r[4] for r in ded).most_common(30))
