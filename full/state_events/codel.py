# House official foreign travel (CODELs/STAFFDELs) from the Clerk's text copies of Congressional Record expenditure reports
# (disclosures-clerk.house.gov/ForeignTravel, 2023-2026 releases). Produces traveler legs and member<->member co-travel edges.
import sys,os,re,glob,json,collections,itertools
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','legislative')); import dclib
M=dclib.members(); now=dclib.NOW()
ROW=re.compile(r'^(?P<name>\S.*?)\.{2,}\s+(?P<arr>\d{1,2}/\d{1,2})\s+(?P<dep>\d{1,2}/\d{1,2})\s+(?P<country>[A-Za-z].*?)(?:\.{2,}|\s{2,})(?P<rest>.*)$')
CONT=re.compile(r'^\s{8,}(?P<arr>\d{1,2}/\d{1,2})\s+(?P<dep>\d{1,2}/\d{1,2})\s+(?P<country>[A-Za-z].*?)(?:\.{2,}|\s{2,})(?P<rest>.*)$')
def mem(name):
  hon=name.startswith('Hon.'); k=dclib.norm_person(name.replace('Hon.',''))
  if not k: return '',hon
  c=[b for b in dclib.member_by_name(k[0],k[1]) if 'House' in M[b]['chambers']]
  if len(c)!=1 and hon:
    c2=[b for b in dclib.member_by_name('*',k[1]) if 'House' in M[b]['chambers']]
    if len(c2)==1: c=c2
  return (c[0] if len(c)==1 else ''),hon
legs=[]
for fn in sorted(glob.glob('/workspace/tmp_dcgraph/ftr/*.txt')):
  T=open(fn,encoding='utf-8',errors='ignore').read().split('\n')
  cr=re.search(r'\[Congressional Record Volume (\d+), Number (\d+) \(([^)]+)\)\]',T[0]); pages=''
  for l in T[:4]:
    if l.startswith('[Pages') or l.startswith('[Page'): pages=l.strip('[]')
  title='';year='';cur=None
  for l in T:
    if 'REPORT OF EXPENDITURES FOR OFFICIAL FOREIGN TRAVEL' in l:
      title=re.sub(r'\s+',' ',l).strip(); y=re.findall(r'(\d{4})',title); year=y[-1] if y else ''; cur=None; continue
    m=ROW.match(l)
    if m:
      cur=m.group('name').strip(); 
    else:
      m=CONT.match(l)
      if not m or not cur: 
        if l.strip()=='' or l.startswith('---') or 'Total' in l: cur=None if ('Committee total' in l or 'Total' in l) else cur
        continue
    nums=re.findall(r'[\d,]+\.\d\d',m.group('rest')); tot=nums[-1].replace(',','') if nums else ''
    b,hon=mem(cur)
    legs.append([os.path.basename(fn),f"{cr.group(3)} vol {cr.group(1)} no {cr.group(2)} {pages}" if cr else pages,title[:250],year,cur,int(hon),b,M.get(b,{}).get('name',''),M.get(b,{}).get('party',''),m.group('arr'),m.group('dep'),re.sub(r'\.+$','',m.group('country')).strip(),tot])
n=dclib.wcsv('house_foreign_travel_legs.csv',['source_file','congressional_record','report_title','report_year','traveler_as_listed','is_member_hon','bioguide','member','party','arrival','departure','country','total_usd_leg'],legs)
# co-travel: two members in the same report with the same (country, arrival, departure)
G=collections.defaultdict(set)
for r in legs:
  if r[6]: G[(r[0],r[2],r[3],r[11].lower()[:20],r[9],r[10])].add(r[6])
E2=collections.defaultdict(lambda:[0,set(),set()])
for (f,t,y,c,a,d),S in G.items():
  for x,z in itertools.combinations(sorted(S),2):
    e=E2[(x,z)]; e[0]+=1; e[1].add(c); e[2].add(y)
rows=[[x,M[x]['name'],M[x]['party'],z,M[z]['name'],M[z]['party'],v[0],'|'.join(sorted(v[1]))[:200],'|'.join(sorted(v[2])),int(M[x]['party']!=M[z]['party']),'high',now] for (x,z),v in sorted(E2.items(),key=lambda q:-q[1][0])]
n2=dclib.wcsv('edges_member_codel_cotravel.csv',['bioguide_a','member_a','party_a','bioguide_b','member_b','party_b','n_shared_legs','countries','years','cross_party','confidence','built_at'],rows)
print(n,n2,sum(1 for r in legs if r[5]),sum(1 for r in legs if r[6]),sum(1 for r in legs if r[5] and not r[6]))
print([r[4] for r in legs if r[5] and not r[6]][:15])
