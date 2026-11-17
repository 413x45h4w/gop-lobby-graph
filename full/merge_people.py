# Merge LDA lobbyist ids that are the same person (same name AND (covered-position token Jaccard>=0.4 OR registrants share a first word, e.g. POLARIS / POLARIS-HUTTON)).
# Then re-derive eligibility on the merged person and take top 300 by attributable income.
import csv,re,collections,shutil,datetime
NOW=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
U=list(csv.DictReader(open('lobbyist_universe_scored.csv')))
STOP={'OF','THE','AND','TO','FOR','ON','REP','SEN','SENATOR','US','U','S','HOUSE','SENATE','COMMITTEE','STAFF','CHIEF','LEGISLATIVE'}
def toks(s): return {t for t in re.findall(r'[A-Z]{3,}',s.upper()) if t not in STOP}
def fw(s): return re.findall(r'[A-Z0-9]+',s.upper())[0] if s else ''
by=collections.defaultdict(list)
for r in U: by[r['name']].append(r)
groups=[]
for nm,g in by.items():
  clusters=[]
  for r in sorted(g,key=lambda r:-int(r['attrib_income_2023_26'])):
    for c in clusters:
      ok=False
      for o in c:
        a,b=toks(r['covered_positions']),toks(o['covered_positions'])
        if a and b and len(a&b)/len(a|b)>=0.4: ok=True
        if fw(r['main_registrant'])==fw(o['main_registrant']) and fw(r['main_registrant']) not in ('THE','LAW','CAPITOL'): ok=True
      if ok: c.append(r); break
    else: clusters.append([r])
  groups+=clusters
out=[]
for c in groups:
  h=c[0]; m=dict(h)
  m['person_key']='|'.join(x['lda_lobbyist_id'] for x in c)
  m['merged_ids_n']=len(c)
  for k in ('attrib_income_2023_26','inc_2023','inc_2024','inc_2025','inc_2026','n_filings_2023_26','ld203_R_usd','ld203_D_usd','ld203_unclassified_usd'):
    m[k]=sum(int(x[k] or 0) for x in c)
  m['registrants']='; '.join(dict.fromkeys(x['main_registrant'] for x in c))
  m['first_quarter_seen']=min(x['first_quarter_seen'] for x in c); m['last_quarter_seen']=max(x['last_quarter_seen'] for x in c)
  m['covered_positions']=' || '.join(dict.fromkeys(x['covered_positions'] for x in c if x['covered_positions']))[:600]
  sig={s for x in c for s in x['gop_signals'].split('|') if s and s!='S3_gop_heavy_ld203'}
  dsig={s for x in c for s in x['dem_signals'].split('|') if s and s!='D_heavy_ld203'}
  R,D=m['ld203_R_usd'],m['ld203_D_usd']; sh=R/(R+D) if R+D else None
  m['ld203_R_share']='' if sh is None else round(sh,3)
  if sh is not None and sh>=0.67 and R>=2000: sig.add('S3_gop_heavy_ld203')
  if sh is not None and sh<=0.33 and D>=2000: dsig.add('D_heavy_ld203')
  m['gop_signals']='|'.join(sorted(sig)); m['dem_signals']='|'.join(sorted(dsig)); m['eligible']=bool(sig) and not dsig
  m['sample_filing_ids']='|'.join(x['sample_filing_ids'] for x in c)[:400]
  m['computed_at']=NOW
  out.append(m)
out.sort(key=lambda r:-r['attrib_income_2023_26'])
el=[r for r in out if r['eligible']]
for r in out: r['rank_income_eligible']=''
for i,r in enumerate(el,1): r['rank_income_eligible']=i
f=['person_key','merged_ids_n']+[k for k in U[0].keys()]
shutil.copy('selected_top300.csv','selected_top300_by_lda_id.csv')
w=csv.DictWriter(open('people_universe_scored.csv','w'),fieldnames=f);w.writeheader();w.writerows(out)
w=csv.DictWriter(open('selected_top300.csv','w'),fieldnames=f);w.writeheader();w.writerows(el[:300])
print('ids',len(U),'people',len(out),'merged groups',sum(1 for r in out if r['merged_ids_n']>1),'eligible',len(el),'cutoff',el[299]['attrib_income_2023_26'])
for r in el[:300]:
  if r['merged_ids_n']>1: print(r['rank_income_eligible'],r['name'],r['registrants'][:70],r['attrib_income_2023_26'])
