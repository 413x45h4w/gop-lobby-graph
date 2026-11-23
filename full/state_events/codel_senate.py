# Senate "FOREIGN TRAVEL FINANCIAL REPORTS" (Congressional Record, Senate section, via GovInfo CREC granules found by crec_foreign_travel_scan.py).
# Senate tables list traveler then countries (no dates). Co-travel edge = two senators in the same report section sharing >=2 foreign countries (medium).
import sys,os,re,glob,html,json,collections,itertools
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','legislative')); import dclib
M=dclib.members(); now=dclib.NOW(); legs=[]
for fn in sorted(glob.glob('/workspace/tmp_dcgraph/sftr/*.htm')):
  T=html.unescape(re.sub(r'<[^>]+>','',open(fn,encoding='utf-8',errors='ignore').read())).split('\n')
  g=os.path.basename(fn)[:-4]; title='';buf='';cur=None
  for i,l in enumerate(T):
    if 'CONSOLIDATED REPORT OF EXPENDITURE' in l:
      buf=l.strip(); j=i+1
      while j<len(T) and T[j].strip() and not T[j].startswith('---'): buf+=' '+T[j].strip(); j+=1
      title=re.sub(r'\s+',' ',buf); cur=None; continue
    m=re.match(r'^(\S[^:]{2,60}):\s*$',l)
    if m and title: cur=m.group(1).strip(); continue
    m=re.match(r'^\s{2,8}([A-Z][A-Za-z .,\'()\-]+?)\.{2,}\s+(\S.*?)\.{2,}(.*)$',l)
    if m and cur:
      nums=re.findall(r'[\d,]+\.\d\d',m.group(3)); 
      hon=cur.startswith('Senator'); k=dclib.norm_person(cur.replace('Senator',''))
      b=''
      if hon and k:
        c=[x for x in dclib.member_by_name(k[0],k[1]) if 'Senate' in M[x]['chambers']] or [x for x in dclib.member_by_name('*',k[1]) if 'Senate' in M[x]['chambers']]
        b=c[0] if len(c)==1 else ''
      legs.append([g,title[:300],(re.findall(r'(\d{4})',title) or [''])[-1],cur,int(hon),b,M.get(b,{}).get('name',''),M.get(b,{}).get('party',''),m.group(1).strip(),m.group(2).strip(),nums[-1].replace(',','') if nums else ''])
    elif l.strip().startswith('Total') or l.strip().startswith('Delegation expenses') : cur=None
n=dclib.wcsv('senate_foreign_travel_legs.csv',['granule','report_title','report_year','traveler_as_listed','is_senator','bioguide','member','party','country','currency','total_usd_leg'],legs)
S=collections.defaultdict(set)
for r in legs:
  if r[5] and r[8].lower()!='united states': S[(r[0],r[1],r[5])].add(r[8].lower())
by=collections.defaultdict(dict)
for (g,t,b),cs in S.items(): by[(g,t)][b]=cs
E2=collections.defaultdict(lambda:[0,set(),set()])
for (g,t),D in by.items():
  for x,z in itertools.combinations(sorted(D),2):
    sh=D[x]&D[z]
    if len(sh)>=2: e=E2[(x,z)]; e[0]+=1; e[1]|=sh; e[2].add((re.findall(r'(\d{4})',t) or [''])[-1])
rows=[[x,M[x]['name'],M[x]['party'],z,M[z]['name'],M[z]['party'],v[0],'|'.join(sorted(v[1]))[:200],'|'.join(sorted(v[2])),int(M[x]['party']!=M[z]['party']),'medium',now] for (x,z),v in sorted(E2.items(),key=lambda q:-q[1][0])]
n2=dclib.wcsv('edges_senator_codel_cotravel.csv',['bioguide_a','member_a','party_a','bioguide_b','member_b','party_b','n_shared_report_sections','shared_countries','years','cross_party','confidence','built_at'],rows)
print(n,n2,sum(r[4] for r in legs),sum(1 for r in legs if r[5]),[r[3] for r in legs if r[4] and not r[5]][:10])
