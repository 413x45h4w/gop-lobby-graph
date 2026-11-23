# FARA layer from efile.fara.gov bulk CSVs + text of Supplemental Statements (2023-01-01+).
import zipfile,csv,io,re,gzip,json,glob,collections,datetime,sys,os,unicodedata
sys.path.insert(0,'../revolving'); import memberlex as ML
NOW=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
P=ML.P
def bulk(n):
  zf=zipfile.ZipFile(f'raw/{n}.csv.zip'); return list(csv.DictReader(io.TextIOWrapper(zf.open(zf.namelist()[0]),encoding='latin-1')))
REG=bulk('FARA_All_Registrants'); FP=bulk('FARA_All_ForeignPrincipals'); SF=bulk('FARA_All_ShortForms'); DOCS=bulk('FARA_All_RegistrantDocs')
def d(s):
  m=re.match(r'(\d\d)/(\d\d)/(\d{4})',s or ''); return f'{m.group(3)}-{m.group(1)}-{m.group(2)}' if m else ''
UA=lambda s:unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode()
norm=lambda s:re.sub(r'\b(LLC|L L C|INC|LLP|LP|PLLC|CORP|CORPORATION|CO|COMPANY|THE|GROUP|PC|LTD|AND)\b','',re.sub(r'[^A-Z0-9 ]',' ',UA(s).upper().replace('&',' AND '))).split()
nkey=lambda s:' '.join(norm(s))
# active in window: registration not terminated before 2023
ACT=lambda term:(not term) or d(term)>='2023-01-01'
# ----- LDA linkage: registrants and lobbyists -----
pid_of={}; prow={}
for r in csv.DictReader(open('../money_all/people_all.csv')):
  for lid in r['person_key'].split('|'): pid_of[int(lid)]=r['person_id']
  prow[r['person_id']]=r
scored={r['lda_lobbyist_id'] for r in csv.DictReader(open('../lobbyist_universe_scored.csv'))}
LDAREG=collections.defaultdict(set); LOBREG=collections.defaultdict(set); LOBNAME=collections.defaultdict(set)
NICK={'BOB':'ROBERT','BILL':'WILLIAM','JIM':'JAMES','MIKE':'MICHAEL','TOM':'THOMAS','JOE':'JOSEPH','DAN':'DANIEL','DAVE':'DAVID','STEVE':'STEVEN','CHRIS':'CHRISTOPHER','MATT':'MATTHEW','JEFF':'JEFFREY','TONY':'ANTHONY','NICK':'NICHOLAS','ALEX':'ALEXANDER','SAM':'SAMUEL','BEN':'BENJAMIN','TIM':'TIMOTHY','GREG':'GREGORY','DOUG':'DOUGLAS','ANDY':'ANDREW','RICK':'RICHARD','DICK':'RICHARD','ED':'EDWARD','TED':'EDWARD','JON':'JONATHAN','PAT':'PATRICK','KEN':'KENNETH','RON':'RONALD','DON':'DONALD','LARRY':'LAWRENCE','JOSH':'JOSHUA','ZACH':'ZACHARY','KATIE':'KATHERINE','KATE':'KATHERINE','LIZ':'ELIZABETH','BETH':'ELIZABETH','JOHNNY':'JOHN','WILL':'WILLIAM'}
cn=lambda f:NICK.get(f,f)
cl=lambda s:re.sub(r"[^A-Z\- ]",'',UA(s).upper().replace('.',' ')).split()
for fn in sorted(glob.glob('../ld2/raw/ld2full_*.jsonl.gz')):
  for line in gzip.open(fn,'rt'):
    try: x=json.loads(line)
    except: continue
    LDAREG[nkey(x['rn'])].add((x['rid'],x['rn']))
    for a in x['acts']:
      for lid,fi,la,cp,new in a['l']:
        f=cl(fi or ''); l=cl(la or '')
        if f and l:
          LOBNAME[(l[-1],cn(f[0]))].add(lid); LOBREG[lid].add(nkey(x['rn']))
def lda_reg(name):
  k=nkey(name)
  if k in LDAREG: return LDAREG[k],'exact_normalized'
  # prefix match on first 2 significant tokens
  t=k.split()[:2]
  if len(t)==2:
    c=set().union(*[v for kk,v in LDAREG.items() if kk.split()[:2]==t]) if any(kk.split()[:2]==t for kk in LDAREG) else set()
    if 0<len({r for r,_ in c})<=2: return c,'first_two_tokens'
  return set(),''
regs={}
for r in REG:
  rid,how=lda_reg(r['Name']); 
  regs[r['Registration Number']]=dict(registration_number=r['Registration Number'],registrant=r['Name'],business_name=r['Business Name'],registration_date=d(r['Registration Date']),termination_date=d(r['Termination Date']),
    city=r['City'],state=r['State'],active_2023_plus=ACT(r['Termination Date']),lda_registrant_ids='|'.join(sorted({str(a) for a,_ in rid})),lda_registrant_names='|'.join(sorted({b for _,b in rid}))[:200],lda_match_how=how)
fps=[]; FPBY=collections.defaultdict(list)
for r in FP:
  e=dict(registration_number=r['Registration Number'],registrant=r['Registrant Name'],foreign_principal=r['Foreign Principal'],country=r['Country/Location Represented'],
    fp_registration_date=d(r['Foreign Principal Registration Date']),fp_termination_date=d(r['Foreign Principal Termination Date']),active_2023_plus=ACT(r['Foreign Principal Termination Date']))
  fps.append(e); FPBY[e['registration_number']].append(e)
ags=[]
for r in SF:
  f=cl(r['Short Form First Name']); l=cl(r['Short Form Last Name'])
  lids=LOBNAME.get((l[-1],cn(f[0])),set()) if f and l else set()
  regk=regs.get(r['Registration Number'],{}).get('lda_registrant_names','')
  regk_n={nkey(x) for x in regk.split('|') if x}
  pids={pid_of.get(x,f'lda{x}') for x in lids}
  same_firm=[x for x in lids if LOBREG[x]&regk_n]
  if same_firm: conf='high'; pids={pid_of.get(x,f'lda{x}') for x in same_firm}
  elif len(pids)==1: conf='medium'
  elif pids: conf='low_multiple_people'
  else: conf=''
  ags.append(dict(registration_number=r['Registration Number'],registrant=r['Registrant Name'],agent_first=r['Short Form First Name'],agent_last=r['Short Form Last Name'],
    short_form_date=d(r['Short Form Date']),short_form_termination_date=d(r['Short Form Termination Date']),active_2023_plus=ACT(r['Short Form Termination Date']),
    lda_person_ids='|'.join(sorted(pids)) if conf in('high','medium') else '',lda_candidate_person_ids='|'.join(sorted(pids))[:200] if conf=='low_multiple_people' else '',
    in_lobbyist_universe_scored=any(str(x) in scored for x in (same_firm or lids)) if conf in('high','medium') else False,lda_match_confidence=conf))
# ----- supplemental statements: contacts & contributions -----
COUNTRIES={e['country'].upper() for e in fps if e['country']}
CONTRIB=re.compile(r'^\s*(\d{1,2}/\d{1,2}/\d{2,4})\s{2,}(\S.*?)\s{2,}(\S.*?)(?:\s{2,}(\S.*?))?\s{2,}[\$£S,\s]*\s*([\d,]+\.\d\d)\s*$')
CAMP=re.compile(r'(FOR (?:CONGRESS|SENATE|US SENATE|U\.S\. SENATE|AMERICA|[A-Z]+)|FRIENDS (?:OF|FOR) |VICTORY|COMMITTEE TO ELECT|PEOPLE FOR|LEADERSHIP|\bPAC\b|\bFUND\b|CAMPAIGN|4 CONGRESS|COMITE)',re.I)
docmeta={}
for x in DOCS:
  if x['Document Type']=='Supplemental Statement': docmeta[x['URL'].split('/')[-1][:-4]]=x
contacts=[]; contribs=[]; scan_stats=collections.Counter(); amb=[]
def member_from_recipient(rec,yr):
  R=re.sub(r'\s+',' ',UA(rec)).upper(); R2=re.sub(r"[^A-Z' \-]",' ',R)
  toks=[t for t in R2.split() if t not in {'FOR','CONGRESS','SENATE','US','FRIENDS','OF','THE','COMMITTEE','TO','ELECT','INC','VICTORY','FUND','PAC','AMERICA','PEOPLE','RE','CAMPAIGN','DR','COMITE','LEADERSHIP','HOUSE','LLC','SENATOR','REP','CONGRESSMAN','CONGRESSWOMAN','GOVERNOR'}]
  best=None
  for i in range(len(toks)):
    for j in (2,1):
      sur=' '.join(toks[i:i+j])
      if sur not in ML.BYLAST: continue
      first=toks[i-1] if i>0 else None
      b,n,how=ML.resolve(sur,first,None,yr)
      if not b or how=='last_only_first_mismatch': continue
      if how=='first+last': return (b,how)
      # surname-only: require campaign-committee framing right around the surname ('X for Congress', 'Friends of X', 'X Victory/Leadership')
      if best is None and re.search(r"(FRIENDS (?:OF|FOR)|ELECT|^)\s*"+re.escape(sur)+r"\b|\b"+re.escape(sur)+r"\s+(FOR|VICTORY|LEADERSHIP|4|2026|2024|PAC)\b",R2.strip()): best=(b,how)
  return best
for fn in sorted(glob.glob('raw/ss_text/*.txt.gz')):
  name=os.path.basename(fn)[:-7]; meta=docmeta.get(name,{})
  reg=meta.get('Registration Number') or name.split('-')[0]; ds=d(meta.get('Date Stamped','')); yr=int(ds[:4]) if ds else None
  lines=gzip.open(fn,'rt').read().split('\n'); scan_stats['docs']+=1
  if sum(len(l) for l in lines)<2000: scan_stats['docs_no_text_layer']+=1; continue
  fpn=[(e['foreign_principal'],[w for w in norm(e['foreign_principal']) if len(w)>3][:3],e['country'].upper()) for e in FPBY.get(reg,[]) if e['active_2023_plus']]
  seen=set(); cons=0
  for i,l in enumerate(lines):
    m=CONTRIB.match(l)
    if m:
      dt,donor,rec,method,amt=m.groups()
      nxt=lines[i+1] if i+1<len(lines) else ''
      if nxt.strip() and not CONTRIB.match(nxt) and re.match(r'^\s{20,}\S',nxt) and len(nxt.strip())<40: rec=rec+' '+nxt.strip()
      if not (CAMP.search(rec) or member_from_recipient(rec,yr)): continue
      mb=member_from_recipient(rec,yr)
      contribs.append(dict(registration_number=reg,registrant=meta.get('Registrant Name',''),doc=name,doc_url=meta.get('URL',''),date_stamped=ds,contribution_date=dt,donor=donor.strip()[:80],recipient=rec.strip()[:100],
        amount_usd=float(amt.replace(',','')),bioguide=mb[0] if mb else '',member=P[mb[0]]['name'] if mb else '',member_party=P[mb[0]]['party'] if mb else '',member_current=P[mb[0]]['current'] if mb else '',
        match_how=mb[1] if mb else '',confidence=('high' if mb and mb[1]=='first+last' else ('medium' if mb else 'unmatched_recipient')),computed_at=NOW))
      continue
    if not re.search(r'SENATOR|SEN\.|REP\.|REPRESENTATIVE|CONGRESSM|CONGRESSW|OFFICE OF|HON\.',l,re.I): continue
    if re.search(r'is required to|registrant|reporting period|Item \d|Exhibit|pursuant',l,re.I): continue
    txt=l+' '+(lines[i+1] if i+1<len(lines) else '')
    for b,n,how,mt in ML.find(txt,yr):
      if not b: amb.append([reg,name,mt,n]); continue
      if b in seen: continue
      seen.add(b); cons+=1
      ctx=' '.join(lines[max(0,i-4):i+5]).upper()
      hit=[fp for fp,w,c in fpn if (w and all(x in ctx for x in w[:2])) or (c and c in ctx)]
      contacts.append(dict(registration_number=reg,registrant=meta.get('Registrant Name',''),doc=name,doc_url=meta.get('URL',''),date_stamped=ds,bioguide=b,member=P[b]['name'],member_party=P[b]['party'],
        member_current=P[b]['current'],mention=mt,match_how=how,foreign_principal_attributed='|'.join(hit[:3]) if hit else '',principal_attribution=('context_match' if hit else ('single_active_principal' if len(fpn)==1 else 'registrant_level_only')),
        foreign_principal_if_single=fpn[0][0] if len(fpn)==1 and not hit else '',confidence='high' if how=='first+last' else 'medium',line_excerpt=re.sub(r'\s+',' ',l.strip())[:160],computed_at=NOW))
  scan_stats['docs_with_member_mentions']+=bool(cons)
def W(fn,rows):
  if not rows: print('EMPTY',fn); return 0
  op=gzip.open(fn,'wt',newline='') if fn.endswith('.gz') else open(fn,'w',newline='')
  with op as f: w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
  print(fn,len(rows),file=sys.stderr); return len(rows)
cnt={}
cnt['fara_registrants']=W('fara_registrants.csv',list(regs.values()))
cnt['edges_principal_registrant']=W('edges_principal_registrant.csv',fps)
cnt['edges_registrant_agent']=W('edges_registrant_agent.csv',ags)
cnt['edges_fara_contact_member']=W('edges_fara_contact_member.csv',contacts)
_s=set(); _d=[]
for c in contribs:
  k=(c['registration_number'],c['contribution_date'],re.sub(r'\W','',c['donor'].upper())[:12],re.sub(r'\W','',c['recipient'].upper())[:15],c['amount_usd'])
  if k in _s: continue
  _s.add(k); _d.append(c)
print('contrib dedup',len(contribs),'->',len(_d),file=sys.stderr); contribs=_d
cnt['edges_fara_contribution_member']=W('edges_fara_contribution_member.csv',contribs)
with open('fara_ambiguous_member_mentions.csv','w',newline='') as f: w=csv.writer(f); w.writerow(['registration_number','doc','mention','n_candidates']); w.writerows(amb)
# chained edge: principal -> registrant -> agent(lobbyist) -> member (contacts by that registrant)
CH=collections.defaultdict(lambda:{'docs':set(),'n':0})
for c in contacts:
  pr=c['foreign_principal_attributed'] or c['foreign_principal_if_single'] or '(registrant-level)'
  for p in pr.split('|'):
    k=(p,c['registration_number'],c['registrant'],c['bioguide'],c['member'],c['member_party'],c['member_current'],c['principal_attribution']); CH[k]['docs'].add(c['doc']); CH[k]['n']+=1
country={(e['registration_number'],e['foreign_principal']):e['country'] for e in fps}
chain=[dict(foreign_principal=k[0],country=country.get((k[1],k[0]),''),registration_number=k[1],registrant=k[2],bioguide=k[3],member=k[4],member_party=k[5],member_current=k[6],principal_attribution=k[7],n_docs=len(v['docs']),docs='|'.join(sorted(v['docs']))[:300],
  agents_lda_matched='|'.join(sorted({a['lda_person_ids'] for a in ags if a['registration_number']==k[1] and a['lda_person_ids'] and a['active_2023_plus']}))[:300],computed_at=NOW) for k,v in CH.items()]
cnt['edges_principal_registrant_member']=W('edges_principal_registrant_member.csv',chain)
json.dump(dict(counts=cnt,scan=scan_stats,agent_match=collections.Counter(a['lda_match_confidence'] for a in ags if a['active_2023_plus']),
  registrant_lda_match=collections.Counter(bool(r['lda_registrant_ids']) for r in regs.values() if r['active_2023_plus']),computed_at=NOW,bulk_pulled_at=open('raw/PULLED_AT.txt').read().strip()),open('build_stats_fara.json','w'),indent=1,default=str)
