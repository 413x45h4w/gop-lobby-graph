import json,glob,collections,re,datetime,csv
import partylex as P
NOW=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
GOP_FIRMS={  # documented: firms described in LDA-based press analyses (POLITICO Influence, NOTUS, Sludge 2025-26) as Republican-only or Trump-tied, or founded/led by GOP operatives
 'BALLARD PARTNERS':'Trump-tied (Brian Ballard); NOTUS/Sludge',
 'MILLER STRATEGIES':'Trump-tied (Jeff Miller); NOTUS/Sludge',
 'CONTINENTAL STRATEGY':'Trump-tied (Carlos Trujillo); NOTUS/Sludge',
 'CGCN':'Republican-only firm; NOTUS',
 'CHECKMATE GOVERNMENT RELATIONS':'Trump-tied (Ches McDowell); NOTUS/Sludge',
 'MICHAEL BEST STRATEGIES':'Trump-tied (Reince Priebus); Sludge',
 'COVE STRATEGIES':'Matt Schlapp (CPAC chair)',
}
def gopfirm(n):
  N=n.upper()
  for k in GOP_FIRMS:
    if k in N: return k
  return ''
QSTART={'Q1':'-01-01','Q2':'-04-01','Q3':'-07-01','Q4':'-10-01'}
L=collections.defaultdict(lambda:{'names':collections.Counter(),'regs':collections.Counter(),'inc':0.0,'inc_by_year':collections.Counter(),'filings':0,'clients':set(),'issues':collections.Counter(),'ents':collections.Counter(),'cov':set(),'first_q':'9999','last_q':'0000','filing_ids':[]})
seen=set()
for fn in sorted(glob.glob('../lda/ld2_universe/ld2_*.jsonl.gz')):
  for line in __import__('gzip').open(fn,'rt'):
    d=json.loads(line)
    if d['uuid'] in seen: continue
    seen.add(d['uuid'])
    q=f"{d['y']}{QSTART[d['t'][:2]]}"
    lobs={}
    for a in d['acts']:
      for lid,fi,la,cp in a['lob']:
        lobs.setdefault(lid,(fi,la,set()))[2].add(cp or '')
    inc=float(d['inc'] or 0); share=inc/len(lobs) if lobs else 0
    for lid,(fi,la,cps) in lobs.items():
      x=L[lid]; x['names'][f"{(fi or '').strip()} {(la or '').strip()}".upper()]+=1; x['regs'][d['rn']]+=1
      x['first_q']=min(x['first_q'],q); x['last_q']=max(x['last_q'],q)
      if d['y']>=2023:
        x['inc']+=share; x['inc_by_year'][d['y']]+=share; x['filings']+=1; x['clients'].add(d['cn'])
        if len(x['filing_ids'])<400: x['filing_ids'].append(d['uuid'])
        for a in d['acts']:
          if any(l[0]==lid for l in a['lob']):
            x['issues'][a['issue']]+=1
            for e in a['ents']: x['ents'][e]+=1
      x['cov'].update(c for c in cps if c)
# LD-203 by lobbyist id
G=collections.defaultdict(lambda:{'R':0.0,'D':0.0,'other':0.0,'items':0,'reports':set()})
seen203=set()
PARTYCMTE_R=re.compile(r"\b(NRCC|NRSC|RNC|REPUBLICAN|WINRED|GOP)\b"); PARTYCMTE_D=re.compile(r"\b(DCCC|DSCC|DNC|DEMOCRAT\w*|ACTBLUE)\b")
for fn in glob.glob('../lda/ld203_universe/*.jsonl.gz'):
  for line in __import__('gzip').open(fn,'rt'):
    d=json.loads(line)
    if d['uuid'] in seen203 or d['ft']!='lobbyist' or not d['lid']: continue
    seen203.add(d['uuid'])
    g=G[d['lid']]; g['reports'].add(d['uuid'])
    for tp,cn,payee,hon,amt,dt in d['items']:
      if tp!='feca': continue
      t=f"{payee or ''} | {hon or ''}"; T=t.upper()
      r,dd=P.party_of_text(t)
      if PARTYCMTE_R.search(T): r+=1
      if PARTYCMTE_D.search(T): dd+=1
      a=float(amt or 0); g['items']+=1
      if r>dd: g['R']+=a
      elif dd>r: g['D']+=a
      else: g['other']+=a
MEMBER_SELF=re.compile(r"\b(MEMBER OF CONGRESS|MEMBER,? U\.?S\.? HOUSE|U\.?S\.? REPRESENTATIVE|U\.?S\.? CONGRESSMAN|CONGRESSMAN|CONGRESSWOMAN|U\.?S\.? SENATOR|UNITED STATES SENATOR|MEMBER OF THE HOUSE|FORMER MEMBER|REPRESENTATIVE \()",re.I)
rows=[]
for lid,x in L.items():
  if x['inc']<=0: continue
  name=x['names'].most_common(1)[0][0]; reg=x['regs'].most_common(1)[0][0]
  cov=' ; '.join(sorted(x['cov']))
  r,d=P.party_of_text(cov) if cov else (0,0)
  fi,la=name.split(' ',1)[0], name.split(' ')[-1]
  selfmatch=[p for p in P.BYLAST.get(la,[]) if fi in p['firsts']]
  former_member=''
  if selfmatch and MEMBER_SELF.search(cov):
    former_member=selfmatch[0]['party']
  g=G.get(lid,{'R':0,'D':0,'other':0,'items':0,'reports':set()})
  tot=g['R']+g['D']; rshare=g['R']/tot if tot else None
  firm=''.join(gopfirm(rg) for rg in x['regs'])[:60]
  sig=[]
  if firm: sig.append('S1_gop_firm')
  if r>d: sig.append('S2_gop_covered_position')
  if former_member=='R': sig.append('S4_former_gop_member')
  if rshare is not None and rshare>=0.67 and g['R']>=2000: sig.append('S3_gop_heavy_ld203')
  dsig=[]
  if d>r and former_member!='R': dsig.append('D_covered_position')
  if former_member=='D': dsig.append('D_former_member')
  if rshare is not None and rshare<=0.33 and g['D']>=2000: dsig.append('D_heavy_ld203')
  eligible= bool(sig) and not dsig
  rows.append({'lda_lobbyist_id':lid,'name':name,'main_registrant':reg,'registrants':'; '.join(k for k,_ in x['regs'].most_common(4)),'attrib_income_2023_26':round(x['inc']),
    'inc_2023':round(x['inc_by_year'][2023]),'inc_2024':round(x['inc_by_year'][2024]),'inc_2025':round(x['inc_by_year'][2025]),'inc_2026':round(x['inc_by_year'][2026]),
    'n_filings_2023_26':x['filings'],'n_clients':len(x['clients']),'first_quarter_seen':x['first_q'],'last_quarter_seen':x['last_q'],
    'covered_positions':cov[:500],'cov_R_hits':r,'cov_D_hits':d,'former_member_party':former_member,'gop_firm':firm,
    'ld203_R_usd':round(g['R']),'ld203_D_usd':round(g['D']),'ld203_unclassified_usd':round(g['other']),'ld203_R_share':'' if rshare is None else round(rshare,3),
    'gop_signals':'|'.join(sig),'dem_signals':'|'.join(dsig),'eligible':eligible,
    'top_issues':'|'.join(k for k,_ in x['issues'].most_common(8)),'sample_filing_ids':'|'.join(x['filing_ids'][:5]),'computed_at':NOW})
rows.sort(key=lambda r:-r['attrib_income_2023_26'])
el=[r for r in rows if r['eligible']]
for i,r in enumerate(el,1): r['rank_income_eligible']=i
for r in rows: r.setdefault('rank_income_eligible','')
fields=list(rows[0].keys())
with open('lobbyist_universe_scored.csv','w') as f:
  w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
with open('selected_top300.csv','w') as f:
  w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(el[:300])
print('universe with income',len(rows),'eligible',len(el))
print(collections.Counter(s for r in el[:300] for s in r['gop_signals'].split('|')))
for r in el[:40]: print(r['rank_income_eligible'],r['name'],r['main_registrant'][:30],r['attrib_income_2023_26'],r['gop_signals'],r['ld203_R_share'])
print('cutoff income #300:', el[299]['attrib_income_2023_26'] if len(el)>=300 else None)
