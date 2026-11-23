# Hearings + witnesses from docs.house.gov Committee Repository (House, 118th-119th) and GovInfo CHRG MODS (House+Senate+Joint, published transcripts).
import json,re,collections,dclib
now=dclib.NOW(); OI=dclib.org_index(); byname,byid=dclib.people_index()
GOVRX=re.compile(r'\b(DEPARTMENT|DEPT|AGENCY|BUREAU|ADMINISTRATION|OFFICE OF|COMMISSION|U S |UNITED STATES|SECRETARY|INSPECTOR GENERAL|GOVERNMENT ACCOUNTABILITY|ARMY|NAVY|AIR FORCE|MARINE CORPS|SPACE FORCE|COMMAND)\b')
GENERIC={'PRESIDENT','DIRECTOR','CEO','FOUNDER','CHAIRMAN','CHAIR','PROFESSOR','PARTNER','OWNER','MEMBER','SENIOR FELLOW','FELLOW','PH D','PHD','MD','JD','ESQ','WASHINGTON','DC','WASHINGTON DC','INDEPENDENT','RETIRED','PRIVATE CITIZEN','STATE','CITY','COUNTY','SENATE','HOUSE'}
LEG=r'\b(INC|INCORPORATED|LLC|L L C|LLP|LP|CORP|CORPORATION|CO|LTD|PLC|PC|PLLC|THE)\b'
def legal(x): return re.sub(r'\s+',' ',re.sub(LEG,' ',re.sub(r'[^A-Z0-9 ]',' ',re.sub(r'\(.*?\)',' ',(x or '').upper().replace('&',' AND '))))).strip()
def segs(s): return [x.strip(' .;') for x in re.split(r',\s*|\s+-\s+|\s*;\s*',s or '') if x.strip(' .;')]
def find_org(parts):
  best=None
  for i in range(len(parts)):
    for j in range(min(len(parts),i+3),i,-1):
      cand=', '.join(parts[i:j]); k=dclib.norm_org(cand)
      if len(k)<5 or k in GENERIC: continue
      if k in OI and (best is None or len(k)>len(best[0])):
        if len(k.split())==1 and legal(cand)!=legal(OI[k]['name']): continue  # single-token keys must match the full LDA name
        best=(k,cand)
  # also try "on behalf of X" / text in parentheses as alias
  return best
def guess_org_text(parts):
  # last non-location segment, for display when no LDA match
  P=[p for p in parts if not re.fullmatch(r'[A-Z][a-z]+(?: [A-Z][a-z]+)?|[A-Z]{2}|D\.?C\.?|Washington|Ph\.?D|M\.?D|J\.?D|Esq|Jr|Sr|II|III',p)]
  return P[-1] if P else ''
def person(name,org_key):
  k=dclib.norm_person(re.sub(r'\(.*?\)','',name)); 
  if not k or k not in byname: return [],'' 
  C=byname[k]
  if org_key:
    o=OI[org_key]; lob={byid.get(str(i)) for i in o['lob']}
    hit=[c for c in C if c[0] in lob or dclib.norm_org(c[2])==org_key or org_key in [dclib.norm_org(x) for x in c[3].split('; ')]]
    if hit: return hit,'name+org_in_lda'
  if len({c[0] for c in C})==1: return C[:1],'name_only_unique'
  return C,'name_only_ambiguous'
def ccode_house(rc):
  return 'HS'+rc[:2] if rc[2:]=='00' else 'HS'+rc
def ccode_auth(a):
  a=(a or '').upper(); return a[:4] if a[4:]=='00' else a
hearings=[];wit=[]
for l in open('raw/house_events.jsonl'):
  h=json.loads(l)
  if h['status']!='ok': continue
  m=re.search(r'(\w+), (\w+ \d+, \d{4})',h['date_text']); 
  import datetime
  try: d=datetime.datetime.strptime(m.group(2),'%B %d, %Y').date().isoformat() if m else ''
  except Exception: d=''
  cong='119' if d>='2025-01-03' else ('118' if d>='2023-01-03' else ('117' if d else ''))
  codes='|'.join(dict.fromkeys(ccode_house(c) for c in h['repo_codes']))
  hid=f"house:{h['event_id']}"
  hearings.append([hid,'docs.house.gov',cong,'House',d,h.get('kind',''),h['title'][:300],codes,h['committee_text'],len(h['witnesses']),f"https://docs.house.gov/Committee/Calendar/ByEvent.aspx?EventID={h['event_id']}"])
  for w in h['witnesses']: wit.append((hid,d,codes,'House',w['name'],w['title_org']))
hm=[]
for l in open('raw/chrg_mods.jsonl'):
  c=json.loads(l)
  if c['status']!='ok': continue
  hid=f"chrg:{c['package']}"; codes='|'.join(dict.fromkeys(ccode_auth(x['id']) for x in c['committees'] if x.get('id')))
  d=(c['held'] or [''])[0]; ch={'HOUSE':'House','SENATE':'Senate'}.get((c['chamber'] or '').upper(),c['chamber'])
  hearings.append([hid,'govinfo CHRG',c['congress'],ch,d,'Hearing (published transcript)',(c['title'] or '')[:300],codes,'|'.join(x['name'] or '' for x in c['committees']),len(c['witness_text']),f"https://www.govinfo.gov/app/details/{c['package']}"])
  senate='shrg' in c['package'] or 'jhrg' in c['package']
  for wt in c['witness_text']:
    P=segs(wt)
    if senate and len(P)>=2 and ' ' not in P[0] and re.fullmatch(r"[A-Z][\w'.\-]+(?: [A-Z][\w'.\-]*)*",P[1] or ''):
      name=P[1]+' '+P[0]; rest=', '.join(P[2:])
    else: name=P[0] if P else wt; rest=', '.join(P[1:])
    wit.append((hid,d,codes,ch,name,rest))
  for m in c['members']: hm.append([hid,m['bioguide'],m['role'],m['party'],m['state'],d,codes])
nh=dclib.wcsv('hearings.csv',['hearing_id','source','congress','chamber','date','kind','title','committee_codes','committee_names','n_witnesses','url'],hearings)
seen=set();rows=[];stats=collections.Counter();agg=collections.defaultdict(lambda:{'n':0,'h':set(),'d':[], 'w':set()});lobagg=[]
for hid,d,codes,ch,name,to in wit:
  P=segs(to); o=find_org(P); ok=o[0] if o else ''
  gov=bool(GOVRX.search(dclib.norm_org(to)+' ')) and not ok
  C,mt=person(name,ok); od=OI.get(ok,{})
  conf='high' if mt=='name+org_in_lda' else ('medium' if ok else '')
  stats['witness']+=1; stats['org_match']+=bool(ok); stats[mt or 'no_person_match']+=1
  pid='|'.join(c[0] for c in C) if mt in ('name+org_in_lda','name_only_unique') else ''
  rows.append([hid,d,ch,codes,name,to[:300],guess_org_text(P)[:150],ok,od.get('name',''),'|'.join(od.get('kinds',[])),'|'.join(map(str,od.get('client_ids',[])[:5])),'|'.join(map(str,od.get('registrant_ids',[])[:5])),int(gov),pid,mt,('high' if mt=='name+org_in_lda' else 'low' if mt=='name_only_unique' else ''),conf,'org_match=exact normalized name vs LD-2 client/registrant 2022Q4-2026Q3'])
  dk=(d,codes,dclib.norm_person(name))
  if ok and dk not in seen:
    seen.add(dk)
    for cc in (codes.split('|') if codes else ['']):
      a=agg[(ok,cc)]; a['n']+=1; a['h'].add((d,cc)); a['d'].append(d); a['w'].add(name)
  if pid and (d,codes,dclib.norm_person(name),'L') not in seen:
    seen.add((d,codes,dclib.norm_person(name),'L'))
    for cc in (codes.split('|') if codes else ['']): lobagg.append([pid,C[0][1],name,ok,hid,d,cc,mt,'high' if mt=='name+org_in_lda' else 'low'])
nw=dclib.wcsv('hearing_witnesses.csv',['hearing_id','date','chamber','committee_codes','witness_name','witness_title_org','org_text_guess','lda_org_key','lda_org_name','lda_org_kinds','lda_client_ids','lda_registrant_ids','is_government_witness','lobbyist_person_ids','person_match_type','person_match_confidence','org_match_confidence','method'],rows)
ag=[[k[0],OI[k[0]]['name'],'|'.join(OI[k[0]]['kinds']),k[1],v['n'],len(v['h']),min(x for x in v['d'] if x) if any(v['d']) else '',max(v['d']),'|'.join(sorted(v['w']))[:300],len(OI[k[0]]['lob']),'medium',now] for k,v in sorted(agg.items(),key=lambda x:-x[1]['n'])]
na=dclib.wcsv('edges_witness_org_to_committee.csv',['lda_org_key','lda_org_name','lda_org_kinds','committee_code','n_witness_appearances_dedup','n_hearing_days','first_date','last_date','witnesses','n_lda_lobbyists_for_org','confidence','built_at'],ag)
nl=dclib.wcsv('edges_lobbyist_witness_to_committee.csv',['lobbyist_person_ids','lobbyist','witness_name_as_listed','lda_org_key','hearing_id','date','committee_code','match_type','confidence'],lobagg)
nm=dclib.wcsv('hearing_members_listed.csv',['hearing_id','bioguide','role','party','state','date','committee_codes'],hm)
json.dump({'hearings':nh,'witness_rows':nw,'org_committee_edges':na,'lobbyist_witness_rows':nl,'hearing_member_rows':nm,**stats,'built_at':now},open('hearings_stats.json','w'),indent=1)
print(nh,nw,na,nl,nm,dict(stats))
