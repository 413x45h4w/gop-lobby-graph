import json,csv,re,sys,datetime,collections
sys.path.insert(0,'..')
from nicks import NICK
NOW=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
R={}
for r in (json.loads(l) for l in open('f3l_filings_raw.jsonl') if '_empty' not in l): R[r['file_number']]=r
G={r['committee_id']:r for r in csv.DictReader(open('gop_member_committees.csv'))}
S=list(csv.DictReader(open('../selected_top300.csv')))
STOPW={'THE','LLC','LLP','INC','GROUP','GOVERNMENT','RELATIONS','STRATEGIES','PARTNERS','AFFAIRS','PUBLIC','CONSULTING','ASSOCIATES','AND','COMPANY','LAW','CAPITOL','POLICY','ADVISORS','STRATEGY','STRATEGIC','SOLUTIONS','FIRM','OF','PLLC','LTD'}
idx=collections.defaultdict(list); firmidx=collections.defaultdict(set)
for r in S:
  p=r['name'].replace('.','').split(); last=p[-1] if p[-1] not in ('JR','II','III','IV','SR') else p[-2]
  fs={p[0]}|set(NICK.get(p[0],[]))|{k for k,v in NICK.items() if p[0] in v}
  for f in fs: idx[(last,f)].append(r)
  for reg in r['registrants'].split(';'):
    k=' '.join(w for w in re.findall(r"[A-Z0-9&']+",reg.upper()) if w not in STOPW)
    if k: firmidx[k].add(r['lda_lobbyist_id'])
def norm_org(s): return ' '.join(w for w in re.findall(r"[A-Z0-9&']+",s.upper()) if w not in STOPW)
out=[]
for fn,rec in R.items():
  try: txt=open(f'fecfiles/{fn}.fec','rb').read().decode('latin-1')
  except FileNotFoundError: continue
  for line in txt.replace('\r','').split('\n'):
    f=line.split('\x1c')
    if f[0]!='SA3L': continue
    f+=['']*40
    ent=f[5]; org=f[6]; last=f[7].upper().replace('.','').strip(); first=f[8].upper().replace('.','').strip()
    emp,occ=f[23],f[24]
    try: amt=float(f[20] or 0)
    except: amt=0.0
    try: semi=float(f[21] or 0)
    except: semi=0.0
    match=[];conf=''
    if ent=='IND':
      fk=first.split()[0] if first else ''
      cand=[]
      for r in idx.get((last,fk),[]):
        regs=set(' '.join(norm_org(x) for x in r['registrants'].split(';')).split())-set(r['name'].replace('.','').split())-{fk}
        ew=set(norm_org(emp).split())
        empraw=' '.join(re.findall(r"[A-Z0-9&']+",emp.upper()))
        phr={' '.join(re.findall(r"[A-Z0-9&']+",x.upper())[:2]) for x in r['registrants'].split(';')}
        if (ew & regs) or any(p and len(p.split())==2 and p in empraw for p in phr): c='1_high_employer_matches_registrant'
        elif f[15] in ('DC','VA','MD'): c='2_medium_name_dc_area'
        else: c='3_low_name_only'
        cand.append((c,r['lda_lobbyist_id']))
      if cand:
        best=min(c for c,_ in cand); match=sorted({i for c,i in cand if c==best}); conf=best[2:]
    else:
      k=norm_org(org)
      ids=set()
      for fk,v in firmidx.items():
        if k and (k==fk): ids|=v
      if ids: match=sorted(ids); conf='firm_registrant_exact(org)'
    g=G.get(rec['committee_id'])
    out.append(dict(file_number=fn,committee_id=rec['committee_id'],committee_name=rec['committee_name'],gop_member_bioguide=g['bioguide'] if g else '',gop_member=g['member'] if g else '',committee_link=g['link_type'] if g else '',
      cycle=rec['cycle'],report_type=rec['report_type'],coverage_start=(rec.get('coverage_start_date') or '')[:10],coverage_end=(rec.get('coverage_end_date') or '')[:10],receipt_date=rec['receipt_date'][:10],
      amendment_indicator=rec['amendment_indicator'],most_recent=rec.get('most_recent'),bundler_entity=ent,bundler_org=org,bundler_last=f[7],bundler_first=f[8],bundler_city=f[14],bundler_state=f[15],
      bundler_employer=emp,bundler_occupation=occ,bundler_pac_id=f[25] if ent!='IND' else '',period_bundled_usd=amt,semiannual_bundled_usd=semi,report_amount_used=(amt if amt>0 else semi),
      matched_top300_ids='|'.join(match),match_confidence=conf,pdf_url=rec['pdf_url'],fec_url=rec['fec_url'],computed_at=NOW))
w=csv.DictWriter(open('f3l_sa3l_all_2024_2026.csv','w'),fieldnames=list(out[0]));w.writeheader();w.writerows(out)
print('lines',len(out),'gop-member lines',sum(1 for o in out if o['gop_member']),'top300 matched lines',sum(1 for o in out if o['matched_top300_ids']))
