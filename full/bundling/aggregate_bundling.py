# Aggregate Form 3L SA3L lines: most_recent filings only; per (committee, bundler, half-year) total = max(max semi-annual cumulative, sum of period amounts).
import csv,collections,datetime,json
NOW=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
S={r['lda_lobbyist_id']:r for r in csv.DictReader(open('../selected_top300.csv'))}
O=[o for o in csv.DictReader(open('f3l_sa3l_all_2024_2026.csv')) if o['most_recent']=='True' and '2023-01-01'<=o['coverage_end']<='2026-12-31']
def half(d): return d[:4]+('H1' if d[5:7]<='06' else 'H2')
def key(o): return (o['committee_id'],o['bundler_entity'],(o['bundler_last']+','+o['bundler_first']).upper() if o['bundler_entity']=='IND' else o['bundler_org'].upper(),half(o['coverage_end']))
g=collections.defaultdict(list)
for o in O: g[key(o)].append(o)
agg=[]
for k,rows in g.items():
  per=sum(float(r['period_bundled_usd']) for r in rows); semi=max(float(r['semiannual_bundled_usd']) for r in rows)
  r0=rows[0]
  agg.append(dict(committee_id=k[0],committee_name=r0['committee_name'],gop_member_bioguide=r0['gop_member_bioguide'],gop_member=r0['gop_member'],committee_link=r0['committee_link'],
    half_year=k[3],bundler_entity=k[1],bundler=k[2],bundler_employer=r0['bundler_employer'],bundler_city=r0['bundler_city'],bundler_state=r0['bundler_state'],
    bundled_usd=round(max(per,semi),2),sum_period_usd=round(per,2),max_semiannual_usd=round(semi,2),n_lines=len(rows),
    matched_person_ids=r0['matched_top300_ids'],matched_lobbyists='|'.join(S[i]['name'] for i in r0['matched_top300_ids'].split('|') if i),matched_firm='|'.join(S[i]['main_registrant'] for i in r0['matched_top300_ids'].split('|') if i),match_confidence=r0['match_confidence'],
    fec_file_numbers='|'.join(sorted({r['file_number'] for r in rows})),pdf_urls='|'.join(sorted({r['pdf_url'] for r in rows})),fec_urls='|'.join(sorted({r['fec_url'] for r in rows})),computed_at=NOW))
F=list(agg[0])
inscope=[a for a in agg if a['gop_member_bioguide']]
w=csv.DictWriter(open('../edges_money_bundling.csv','w'),fieldnames=['scope']+F);w.writeheader()
for a in inscope: w.writerow(dict(scope='gop_member_pcc_or_lpac',**a))
ctx=[a for a in agg if a['matched_person_ids'] and not a['gop_member_bioguide']]
w=csv.DictWriter(open('bundling_top300_to_nonmember_committees.csv','w'),fieldnames=['scope']+F);w.writeheader()
for a in sorted(ctx,key=lambda a:-a['bundled_usd']): w.writerow(dict(scope='context_not_scored_nonmember_committee',**a))
tot_in=sum(a['bundled_usd'] for a in inscope); tot_in_matched=sum(a['bundled_usd'] for a in inscope if a['matched_person_ids'])
print('agg rows',len(agg),'in-scope rows',len(inscope),'in-scope $',tot_in,'in-scope matched $',tot_in_matched)
per=collections.defaultdict(lambda:collections.Counter())
for a in ctx: per[a['matched_lobbyists']][a['committee_name']]+=a['bundled_usd']
for p,c in sorted(per.items(),key=lambda x:-sum(x[1].values())): print(p,round(sum(c.values()),2),dict(c))
json.dump(dict(computed_at=NOW,filings_cycles_2024_2026=len({o['file_number'] for o in csv.DictReader(open('f3l_sa3l_all_2024_2026.csv'))}),lines=len(O),inscope_usd=tot_in,inscope_matched_usd=tot_in_matched,context_matched_usd=sum(a['bundled_usd'] for a in ctx)),open('bundling_summary.json','w'),indent=1)
