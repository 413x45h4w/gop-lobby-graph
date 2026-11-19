# ALL-PARTY universe: every LDA lobbyist ID on any LD-2 quarterly report 2023Q1-2026Q3 (outside firms AND in-house registrants),
# plus lobbyist IDs that filed an LD-203 (2023 mid-year .. 2026 mid-year) but appear on no 2023+ LD-2. Same person-merge rule as full/merge_people.py.
import json,glob,collections,re,datetime,csv,gzip,sys
sys.path.insert(0,'..'); import partylex as P
NOW=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
OUTLIER_INC=5_000_000  # single LD-2 income >= $5M is implausible (only LOC COMMUNITY ASSOCIATION filings, $20M/quarter); excluded from attributable dollars, listed in income_outliers_excluded.csv
GOP_FIRMS=['BALLARD PARTNERS','MILLER STRATEGIES','CONTINENTAL STRATEGY','CGCN','CHECKMATE GOVERNMENT RELATIONS','MICHAEL BEST STRATEGIES','COVE STRATEGIES']
QSTART={'Q1':'-01-01','Q2':'-04-01','Q3':'-07-01','Q4':'-10-01'}
L=collections.defaultdict(lambda:{'names':collections.Counter(),'regs':collections.Counter(),'rids':set(),'inc':0.0,'exp':0.0,'inc_by_year':collections.Counter(),'filings':0,'f_out':0,'f_inh':0,'clients':set(),'issues':collections.Counter(),'cov':set(),'first_q':'9999','last_q':'0000','filing_ids':[]})
seen=set(); outl=[]
for fn in sorted(glob.glob('../../lda/ld2_universe/ld2_*.jsonl.gz')):
  for line in gzip.open(fn,'rt'):
    d=json.loads(line)
    if d['uuid'] in seen or d['y']<2023: continue
    seen.add(d['uuid'])
    q=f"{d['y']}{QSTART[d['t'][:2]]}"
    lobs={}
    for a in d['acts']:
      for lid,fi,la,cp in a['lob']: lobs.setdefault(lid,(fi,la,set()))[2].add(cp or '')
    inc=float(d['inc'] or 0); exp=float(d['exp'] or 0)
    if inc>=OUTLIER_INC: outl.append(dict(filing_uuid=d['uuid'],registrant=d['rn'],client=d['cn'],year=d['y'],quarter=d['t'],income=inc,n_lobbyists=len(lobs),url=f"https://lda.gov/filings/public/filing/{d['uuid']}/print/")); inc=0
    kind='outside' if d['inc'] is not None else ('in_house' if d['exp'] is not None else 'unreported_under_threshold')
    n=len(lobs) or 1
    for lid,(fi,la,cps) in lobs.items():
      x=L[lid]; x['names'][f"{(fi or '').strip()} {(la or '').strip()}".upper().strip()]+=1; x['regs'][d['rn']]+=1; x['rids'].add(d['rid'])
      x['first_q']=min(x['first_q'],q); x['last_q']=max(x['last_q'],q)
      x['inc']+=inc/n; x['exp']+=exp/n; x['inc_by_year'][d['y']]+=(inc+exp)/n; x['filings']+=1; x['clients'].add(d['cn'])
      if kind=='outside': x['f_out']+=1
      elif kind=='in_house': x['f_inh']+=1
      if len(x['filing_ids'])<5: x['filing_ids'].append(d['uuid'])
      for a in d['acts']:
        if any(l[0]==lid for l in a['lob']): x['issues'][a['issue']]+=1
      x['cov'].update(c for c in cps if c)
print('LD-2 filings 2023+',len(seen),'lobbyist ids',len(L),file=sys.stderr)
G=collections.defaultdict(lambda:{'R':0.0,'D':0.0,'other':0.0,'items':0,'reports':set(),'name':'','rn':''})
seen203=set(); SIG=collections.defaultdict(set)
PR=re.compile(r"\b(NRCC|NRSC|RNC|REPUBLICAN|WINRED|GOP)\b"); PD=re.compile(r"\b(DCCC|DSCC|DNC|DEMOCRAT\w*|ACTBLUE)\b")
for fn in sorted(glob.glob('../../lda/ld203_universe/*.jsonl.gz')):
  for line in gzip.open(fn,'rt'):
    d=json.loads(line)
    if d['uuid'] in seen203 or d['ft']!='lobbyist' or not d['lid']: continue
    seen203.add(d['uuid'])
    g=G[d['lid']]; g['reports'].add(d['uuid']); g['name']=f"{(d['fn'] or '').strip()} {(d['ln'] or '').strip()}".upper().strip(); g['rn']=d['rn'] or ''
    for tp,cn,payee,hon,amt,dt in d['items']:
      if amt and dt: SIG[d['lid']].add((re.sub(r'[^A-Z]','',(payee or '').upper())[:20],str(amt),str(dt)[:10]))
      if tp!='feca': continue
      t=f"{payee or ''} | {hon or ''}"; T=t.upper(); r,dd=P.party_of_text(t)
      if PR.search(T): r+=1
      if PD.search(T): dd+=1
      a=float(amt or 0); g['items']+=1
      if r>dd: g['R']+=a
      elif dd>r: g['D']+=a
      else: g['other']+=a
only203=[lid for lid in G if lid not in L]
print('LD-203 lobbyist reports',len(seen203),'ids',len(G),'ids not on 2023+ LD-2',len(only203),file=sys.stderr)
MEMBER_SELF=re.compile(r"\b(MEMBER OF CONGRESS|MEMBER,? U\.?S\.? HOUSE|U\.?S\.? REPRESENTATIVE|U\.?S\.? CONGRESSMAN|CONGRESSMAN|CONGRESSWOMAN|U\.?S\.? SENATOR|UNITED STATES SENATOR|MEMBER OF THE HOUSE|FORMER MEMBER|REPRESENTATIVE \()",re.I)
rows=[]
for lid in list(L)+only203:
  x=L.get(lid); g=G.get(lid,{'R':0,'D':0,'other':0,'items':0,'reports':set(),'name':'','rn':''})
  if x:
    name=x['names'].most_common(1)[0][0]; reg=x['regs'].most_common(1)[0][0]; cov=' ; '.join(sorted(x['cov']))
  else:
    name=g['name']; reg=g['rn']; cov=''
  if not name: continue
  r,d=P.party_of_text(cov) if cov else (0,0)
  fi,la=name.split(' ',1)[0],name.split(' ')[-1]
  sm=[p for p in P.BYLAST.get(la,[]) if fi in p['firsts']]
  fm=sm[0]['party'] if sm and MEMBER_SELF.search(cov) else ''
  tot=g['R']+g['D']
  kind='ld203_only' if not x else ('outside_and_in_house' if x['f_out'] and x['f_inh'] else ('outside' if x['f_out'] else ('in_house' if x['f_inh'] else 'no_amount_reported')))
  regs=x['regs'] if x else collections.Counter({reg:1})
  rows.append({'lda_lobbyist_id':lid,'name':name,'main_registrant':reg,'registrants':'; '.join(k for k,_ in regs.most_common(4)),'lobbyist_kind':kind,
    'attrib_income_2023_26':round(x['inc']) if x else 0,'attrib_inhouse_expense_2023_26':round(x['exp']) if x else 0,
    'attrib_lobbying_usd_2023_26':round(x['inc']+x['exp']) if x else 0,
    **{f'lob_usd_{y}':round(x['inc_by_year'][y]) if x else 0 for y in (2023,2024,2025,2026)},
    'n_filings_2023_26':x['filings'] if x else 0,'n_outside_filings':x['f_out'] if x else 0,'n_inhouse_filings':x['f_inh'] if x else 0,'n_clients':len(x['clients']) if x else 0,
    'first_quarter_seen':x['first_q'] if x else '','last_quarter_seen':x['last_q'] if x else '',
    'covered_positions':cov[:500],'cov_R_hits':r,'cov_D_hits':d,'former_member_party':fm,'gop_firm':'|'.join(k for k in GOP_FIRMS if any(k in rg.upper() for rg in regs)),
    'ld203_R_usd':round(g['R']),'ld203_D_usd':round(g['D']),'ld203_unclassified_usd':round(g['other']),'ld203_R_share':'' if not tot else round(g['R']/tot,3),'ld203_reports':len(g['reports']),
    'top_issues':'|'.join(k for k,_ in x['issues'].most_common(8)) if x else '','sample_filing_ids':'|'.join(x['filing_ids']) if x else '|'.join(sorted(g['reports'])[:3]),'computed_at':NOW})
w=csv.DictWriter(open('lobbyist_ids_all.csv','w'),fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
w=csv.DictWriter(open('income_outliers_excluded.csv','w'),fieldnames=list(outl[0])+['computed_at']);w.writeheader();[w.writerow(dict(o,computed_at=NOW)) for o in outl]
# ---- person merge (same rule as full/merge_people.py) ----
STOP={'OF','THE','AND','TO','FOR','ON','REP','SEN','SENATOR','US','U','S','HOUSE','SENATE','COMMITTEE','STAFF','CHIEF','LEGISLATIVE'}
def toks(s): return {t for t in re.findall(r'[A-Z]{3,}',s.upper()) if t not in STOP}
def fw(s):
  m=re.findall(r'[A-Z0-9]+',s.upper()); return m[0] if m else ''
# v2 merge key (all-party build): canonical first name (nickname -> formal, e.g. DAN->DANIEL, ED->EDWARD) + last token, middle names/initials and JR/SR/II/III ignored.
# Link rule within a key: covered-position Jaccard>=0.4 OR registrants share first word OR registrants share a DISTINCTIVE word (in <=25 of all registrant names)
# OR the two IDs' LD-203 reports list the same contribution items (>=3 identical payee+amount+date, >=50% of the smaller set).
from nicks import NICK
CANON={}
for formal,ns in NICK.items():
  for n in ns: CANON.setdefault(n,formal)
SUFX={'JR','SR','II','III','IV'}
def nkey(nm):
  t=[x for x in re.split(r'[\s\.,]+',nm.upper()) if x and x not in SUFX and not re.fullmatch(r'\(.*\)',x)]
  if not t: return nm
  return (CANON.get(t[0],t[0]),t[-1])
RW=lambda s:set(re.findall(r"[A-Z0-9']{3,}",s.upper()))-{'THE','LLC','LLP','INC','AND','GROUP','GOVERNMENT','RELATIONS','STRATEGIES','PARTNERS','AFFAIRS','PUBLIC','CONSULTING','ASSOCIATES','COMPANY','LAW','POLICY','ADVISORS','STRATEGY','SOLUTIONS','FIRM','PLLC','CORP','CORPORATION','FOR','USA'}
_df=collections.Counter(w for rg in {rg for r in rows for rg in r['registrants'].split('; ')} for w in RW(rg))
def distw(r): return {w for rg in r['registrants'].split('; ') for w in RW(rg) if _df[w]<=25}
by=collections.defaultdict(list)
for r in rows: by[nkey(r['name'])].append(r)
groups=[]
for nm,g in by.items():
  clusters=[]
  for r in sorted(g,key=lambda r:-r['attrib_lobbying_usd_2023_26']):
    for c in clusters:
      ok=False
      for o in c:
        a,b=toks(r['covered_positions']),toks(o['covered_positions'])
        if a and b and len(a&b)/len(a|b)>=0.4: ok=True
        if fw(r['main_registrant'])==fw(o['main_registrant']) and fw(r['main_registrant']) not in ('THE','LAW','CAPITOL',''): ok=True
        if distw(r)&distw(o): ok=True
        a_,b_=SIG.get(r['lda_lobbyist_id'],set()),SIG.get(o['lda_lobbyist_id'],set())
        if a_ and b_ and len(a_&b_)>=3 and len(a_&b_)>=0.5*min(len(a_),len(b_)): ok=True  # same person filing the same LD-203 items under two registrant IDs
      if ok: c.append(r); break
    else: clusters.append([r])
  groups+=clusters
SUM=['attrib_income_2023_26','attrib_inhouse_expense_2023_26','attrib_lobbying_usd_2023_26','lob_usd_2023','lob_usd_2024','lob_usd_2025','lob_usd_2026','n_filings_2023_26','n_outside_filings','n_inhouse_filings','n_clients','ld203_R_usd','ld203_D_usd','ld203_unclassified_usd','ld203_reports','cov_R_hits','cov_D_hits']
out=[]
for c in groups:
  m=dict(c[0]); m['merged_names']='|'.join(dict.fromkeys(x['name'] for x in c)); m['person_id']=c[0]['lda_lobbyist_id']; m['person_key']='|'.join(str(x['lda_lobbyist_id']) for x in c); m['merged_ids_n']=len(c)
  for k in SUM: m[k]=sum(int(x[k] or 0) for x in c)
  m['registrants']='; '.join(dict.fromkeys(rg for x in c for rg in x['registrants'].split('; ')))[:400]
  kinds={x['lobbyist_kind'] for x in c}
  m['lobbyist_kind']=('outside_and_in_house' if ('outside_and_in_house' in kinds or {'outside','in_house'}<=kinds) else sorted(kinds,key=['outside','in_house','no_amount_reported','ld203_only'].index)[0])
  fq=[x['first_quarter_seen'] for x in c if x['first_quarter_seen']]; lq=[x['last_quarter_seen'] for x in c if x['last_quarter_seen']]
  m['first_quarter_seen']=min(fq) if fq else ''; m['last_quarter_seen']=max(lq) if lq else ''
  m['covered_positions']=' || '.join(dict.fromkeys(x['covered_positions'] for x in c if x['covered_positions']))[:600]
  m['former_member_party']=next((x['former_member_party'] for x in c if x['former_member_party']),'')
  m['gop_firm']='|'.join(sorted({g for x in c for g in x['gop_firm'].split('|') if g}))
  R,D=m['ld203_R_usd'],m['ld203_D_usd']; m['ld203_R_share']='' if not R+D else round(R/(R+D),3)
  cr,cd=m['cov_R_hits'],m['cov_D_hits']
  m['covered_position_lean']='none' if not (cr or cd) else ('R' if cr>cd else ('D' if cd>cr else 'mixed'))
  m['sample_filing_ids']='|'.join(x['sample_filing_ids'] for x in c)[:400]; m['computed_at']=NOW
  out.append(m)
out.sort(key=lambda r:-r['attrib_lobbying_usd_2023_26'])
F=['person_id','person_key','merged_ids_n','name','merged_names','main_registrant','registrants','lobbyist_kind']+SUM[:11]+['first_quarter_seen','last_quarter_seen','covered_positions','cov_R_hits','cov_D_hits','covered_position_lean','former_member_party','gop_firm','ld203_R_usd','ld203_D_usd','ld203_unclassified_usd','ld203_R_share','ld203_reports','top_issues','sample_filing_ids','computed_at']
F=list(dict.fromkeys(F))
w=csv.DictWriter(open('people_all.csv','w'),fieldnames=F,extrasaction='ignore');w.writeheader();w.writerows(out)
print('ids',len(rows),'people',len(out),'merged groups',sum(1 for r in out if r['merged_ids_n']>1),collections.Counter(r['lobbyist_kind'] for r in out),'outlier filings',len(outl))
