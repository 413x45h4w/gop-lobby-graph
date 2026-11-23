# Corporate boards of top LDA lobbying clients.
# 1) Top 500 LDA clients by 2023-26 spend (lda_clients_spend_2023_26.csv, built from local LD-2 crawl; full/ld2/ did not exist at build time) -> SEC CIK via company_tickers.json:
#    exact normalized name, then name with trailing generic LDA words removed (SERVICES, CLIENT SERVICES, AFFILIATES, SUBSIDIARIES...), then a small manual parent alias table (documented in README).
# 2) Directors: SEC Insider Transactions Data Sets (Forms 3/4/5, 2025Q1-2026Q1): reporting owners whose RPTOWNER_RELATIONSHIP includes 'Director' for the issuer CIK.
# 3) Validation: latest DEF 14A (proxy) per CIK from data.sec.gov submissions API; director counted 'in_proxy' if surname AND first name/initial appear in proxy text.
# 4) Person matching (nonprofits/scripts/personmatch.py) to lobbyist universe and current/former members.
import csv,json,sys,re,zipfile,io,collections,datetime,time,urllib.request,html,os
sys.path.insert(0,'scripts'); from orgnorm import key
sys.path.insert(0,'/workspace/gop-lobby-graph/full/nonprofits/scripts'); import personmatch as M
NOW=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
UA={'User-Agent':'gop-lobby-graph research fv5z2nvm@mail.grokbot.com'}
OUTL={'STATE LOC NATION GLOBAL PUBLIC BENEFIT'}
GEN=['VARIOUS SUBSIDIARIES','SUBSIDIARIES','AFFILIATES','CLIENT SERVICES','SERVICES','OPERATIONS','ENTERPRISES','FEDERAL','GOVERNMENT','INTERNATIONAL','WORLDWIDE','GLOBAL','SUBSIDIARY','ITS','COMPANIES']
ALIAS={'GOOGLE':'ALPHABET','GOOGLE CLIENT SERVICES':'ALPHABET','META PLATFORMS VARIOUS SUBSIDIARIES':'META PLATFORMS','ALTRIA CLIENT SERVICES':'ALTRIA','RTX AFFILIATES':'RTX','AMAZON COM SERVICES':'AMAZON COM',
  'T MOBILE':'T MOBILE US','UNITEDHEALTH':'UNITEDHEALTH','CVS HEALTH AFFILIATES':'CVS HEALTH','AT T SERVICES':'AT T','VERIZON COMMUNICATIONS':'VERIZON COMMUNICATIONS','APPLE':'APPLE','MICROSOFT':'MICROSOFT',
  'NORTHROP GRUMMAN':'NORTHROP GRUMMAN','UBER TECHNOLOGIES':'UBER TECHNOLOGIES','BLUE CROSS BLUE SHIELD ASSOCIATION':None}
tick=json.load(open('raw/company_tickers.json'))
SEC={}
for v in tick.values():
  k=key(v['title'])
  if k and k not in SEC: SEC[k]=(str(v['cik_str']).zfill(10),v['title'],v['ticker'])
def cik_for(ck):
  if ck in SEC: return SEC[ck],'exact_normalized_name'
  t=ck
  for _ in range(3):
    for g in GEN:
      if t.endswith(' '+g): t=t[:-len(g)-1]
  if t!=ck and t in SEC: return SEC[t],'name_minus_generic_suffix'
  if ck in ALIAS and ALIAS[ck] and ALIAS[ck] in SEC: return SEC[ALIAS[ck]],'manual_parent_alias'
  if t in ALIAS and ALIAS[t] and ALIAS[t] in SEC: return SEC[ALIAS[t]],'manual_parent_alias'
  return None,''
C=[];seen=set()
for r in csv.DictReader(open('lda_clients_spend_2023_26.csv')):
  if int(r['rank'])>500: break
  if r['client_key'] in OUTL: continue
  s,how=cik_for(r['client_key'])
  if s and s[0] not in seen: seen.add(s[0]); C.append(dict(rank=r['rank'],client_key=r['client_key'],client_name=r['client_name'],lda_spend_2023_26=r['lda_spend_2023_26'],cik=s[0],sec_name=s[1],ticker=s[2],cik_match=how))
  elif s: [c for c in C if c['cik']==s[0]][0]['client_name']+=' | '+r['client_name']
print('mapped',len(C),'companies from top-500 clients',flush=True)
CIKS={c['cik'] for c in C}
DIR=collections.defaultdict(dict)
for q in sorted(f for f in os.listdir('raw') if f.endswith('_form345.zip')):
  z=zipfile.ZipFile('raw/'+q); sub={}
  for l in io.TextIOWrapper(z.open('SUBMISSION.tsv'),encoding='utf-8',errors='replace'):
    f=l.rstrip('\n').split('\t')
    if f[9] in CIKS: sub[f[0]]=(f[9],f[1],f[8])
  for l in io.TextIOWrapper(z.open('REPORTINGOWNER.tsv'),encoding='utf-8',errors='replace'):
    f=l.rstrip('\n').split('\t')
    if f[0] in sub:
      cik,dt,doc=sub[f[0]]
      d=DIR[cik].setdefault(f[1],dict(name=f[2],rel=set(),titles=set(),last=None,acc=None,forms=set()))
      d['rel']|=set(x.strip() for x in f[3].split(',')); 
      if f[4]: d['titles'].add(f[4])
      dd=datetime.datetime.strptime(dt,'%d-%b-%Y').date().isoformat()
      if not d['last'] or dd>d['last']: d['last']=dd; d['acc']=f[0]
      d['forms'].add(doc)
def get(u):
  for a in range(3):
    try:
      return urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=60).read()
    except Exception as e: time.sleep(2)
  return None
CK='raw/def14a_cache.jsonl'; cache={}
if os.path.exists(CK):
  for l in open(CK): d=json.loads(l); cache[d['cik']]=d
with open(CK,'a') as ck:
  for c in C:
    if c['cik'] in cache: continue
    time.sleep(0.15); j=get(f"https://data.sec.gov/submissions/CIK{c['cik']}.json"); rec=dict(cik=c['cik'],def14a_url='',def14a_date='',text_tokens=[])
    if j:
      j=json.loads(j); r=j['filings']['recent']
      for i,ft in enumerate(r['form']):
        if ft in ('DEF 14A','DEFA14A') and ft=='DEF 14A':
          acc=r['accessionNumber'][i].replace('-',''); rec['def14a_url']=f"https://www.sec.gov/Archives/edgar/data/{int(c['cik'])}/{acc}/{r['primaryDocument'][i]}"; rec['def14a_date']=r['filingDate'][i]; break
    if rec['def14a_url']:
      time.sleep(0.15); h=get(rec['def14a_url'])
      if h:
        t=html.unescape(re.sub(r'<[^>]+>',' ',h.decode('utf-8','replace'))).upper()
        rec['text_tokens']=sorted(set(re.findall(r"[A-Z][A-Z\-']+",t)))
    ck.write(json.dumps(rec)+'\n'); ck.flush(); cache[c['cik']]=rec
B=[];amb=[]
for c in C:
  px=cache.get(c['cik'],{}); toks=set(px.get('text_tokens',[]))
  for ocik,d in DIR.get(c['cik'],{}).items():
    if 'Director' not in d['rel']: continue
    parts=[p for p in re.split(r'[^A-Za-z\-\']+',d['name']) if p]
    if len(parts)<2: continue
    last,first=parts[0].upper(),parts[1].upper(); fn=f"{last}, {' '.join(parts[1:])}"
    inproxy=bool(toks) and last in toks and (first in toks or any(t.startswith(first[:1]) for t in []) )
    conf='high_form345_and_proxy' if inproxy else ('medium_form345_only' if toks else 'medium_form345_no_proxy_text')
    row=dict(director_name=d['name'],director_sec_cik=ocik,relationship='|'.join(sorted(d['rel'])),officer_title='|'.join(sorted(d['titles'])),last_form345_date=d['last'],last_form345_accession=d['acc'],
      company=c['sec_name'],ticker=c['ticker'],company_cik=c['cik'],lda_client_names=c['client_name'],lda_client_rank=c['rank'],lda_spend_2023_26=c['lda_spend_2023_26'],board_confidence=conf,
      def14a_date=px.get('def14a_date',''),def14a_url=px.get('def14a_url',''),
      lobbyist_person_id='',lobbyist='',lobbyist_firm='',lobbyist_confidence='',member_bioguide='',member_name='',member_party='',member_current='',member_confidence='',member_basis='',
      form345_url=f"https://www.sec.gov/Archives/edgar/data/{int(c['cik'])}/{d['acc'].replace('-','')}/",computed_at=NOW)
    lm=M.match_lobbyist(fn,c['client_name'].split(' | ')[0])
    if lm:
      # boards: corporate directors are mostly executives/investors, so a name-only 'medium_unique' lobbyist match is treated as ambiguous (2026-11-22 spot check: e.g. CEO namesakes)
      if lm['confidence']!='high_org_link': amb.append(dict(kind='lobbyist',candidates=lm['person_id'],basis=lm['basis'],director_name=d['name'],company=c['sec_name']))
      else: row.update(lobbyist_person_id=lm['person_id'],lobbyist=lm['name'],lobbyist_firm=lm['firm'],lobbyist_confidence=lm['confidence'])
    mm=M.match_member(fn,' '.join(d['titles']))
    if mm:
      if mm['confidence']=='low_name_only': amb.append(dict(kind='member',candidates=mm['bioguide'],basis=mm['basis'],director_name=d['name'],company=c['sec_name']))
      else: row.update(member_bioguide=mm['bioguide'],member_name=mm['name'],member_party=mm['party'],member_current=mm['current'],member_confidence=mm['confidence'],member_basis=mm['basis'])
    B.append(row)
w=csv.DictWriter(open('companies_top_lda_clients_sec.csv','w'),fieldnames=list(C[0])+['def14a_date','def14a_url','n_directors_form345','computed_at'])
w.writeheader()
for c in C: w.writerow(dict(c,def14a_date=cache.get(c['cik'],{}).get('def14a_date',''),def14a_url=cache.get(c['cik'],{}).get('def14a_url',''),n_directors_form345=sum(1 for d in DIR.get(c['cik'],{}).values() if 'Director' in d['rel']),computed_at=NOW))
w=csv.DictWriter(open('edges_person_company_board.csv','w'),fieldnames=list(B[0])); w.writeheader(); w.writerows(B)
w=csv.DictWriter(open('board_person_match_ambiguous.csv','w'),fieldnames=['kind','candidates','basis','director_name','company']); w.writeheader(); w.writerows(amb)
# interlocks: same SEC person CIK on >=2 top-client boards
ic=collections.defaultdict(list)
for b in B: ic[b['director_sec_cik']].append(b)
I=[dict(director_name=v[0]['director_name'],director_sec_cik=k,n_boards=len(v),companies='|'.join(sorted(x['company'] for x in v)),computed_at=NOW) for k,v in ic.items() if len(v)>1]
I.sort(key=lambda x:-x['n_boards'])
w=csv.DictWriter(open('board_interlocks_top_clients.csv','w'),fieldnames=['director_name','director_sec_cik','n_boards','companies','computed_at']); w.writeheader(); w.writerows(I)
st=dict(computed_at=NOW,companies=len(C),with_def14a=sum(1 for c in C if cache.get(c['cik'],{}).get('def14a_url')),board_edges=len(B),by_conf=collections.Counter(b['board_confidence'] for b in B),
  lobbyist_matched=sum(1 for b in B if b['lobbyist_person_id']),member_matched=sum(1 for b in B if b['member_bioguide']),interlocks=len(I),ambiguous=len(amb))
json.dump(st,open('boards_stats.json','w'),indent=1); print(st)
