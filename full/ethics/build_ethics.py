# Ethics layer: House PTRs, Senate eFD PTRs + annual-report holdings/gifts/travel, House privately funded (gift) travel.
import sys,os,re,json,csv,collections,xml.etree.ElementTree as ET
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','legislative')); import dclib
now=dclib.NOW(); M=dclib.members(); OI=dclib.org_index()
OIkeys=sorted(OI)
import bisect
def org_match(name):
  """company/sponsor name -> (lda_org_key, method). exact normalized; else unique-prefix on >=2-token keys."""
  n=re.sub(r'\s+-\s+(Common Stock|Class [A-Z].*|Ordinary Shares.*|American Depositary.*|ADR.*|Common Shares.*|Units.*)$','',name or '',flags=re.I)
  n=re.sub(r'\[[A-Z]{2}\]|\([A-Z0-9.\-/]{1,8}\)','',n)
  k=dclib.norm_org(n)
  if len(k)<3: return '',''
  if k in OI: return k,'exact_norm'
  if False:  # prefix matching disabled 2026-11-22: produced false positives (e.g. 'Commercial Real Estate', 'Blackstone Energy')
    i=bisect.bisect_left(OIkeys,k+' '); C=[]
    while i<len(OIkeys) and OIkeys[i].startswith(k+' '): C.append(OIkeys[i]); i+=1
    if C: return max(C,key=lambda c:OI[c]['n_filings']),'prefix_norm'
  return '',''
def amt(s):
  v=[int(x.replace(',','')) for x in re.findall(r'\$([\d,]+)',s or '')]
  if not v: return '',''
  if 'Over' in (s or ''): return v[0],''
  return v[0],(v[1] if len(v)>1 else '')
def house_bioguide(last,first,sd):
  st=sd[:2]; fk=(dclib.norm_person((first or '')+' XX') or ('',))[0]
  c=dclib.member_by_name(fk,dclib.last_key(last),st)
  c=[b for b in c if M[b]['state']==st and 'House' in M[b]['chambers']]
  if len(c)!=1:
    c2=[b for b in dclib.member_by_name('*',dclib.last_key(last)) if M[b]['state']==st and 'House' in M[b]['chambers']]
    if len(c2)==1: return c2[0],'last+state'
    if len(c)>1 and sd[2:]:
      c3=[b for b in (c or c2) if sd[2:].lstrip('0') in [d.lstrip('0') or '0' for d in M[b]['districts']]]
      if len(c3)==1: return c3[0],'name+district'
    return '','unmatched'
  return c[0],'first+last+state'
tx=[];stat=collections.Counter()
for l in open('raw/house_ptr_transactions.jsonl'):
  t=json.loads(l); b,mm=house_bioguide(t['filer_last'],t['filer_first'],t['state_dst'])
  a=t['asset']; extra=re.search(r'\s(\$[\d,]+)$',a)
  if extra: a=a[:extra.start()]; t['amount']=t['amount'].rstrip(' -')+' - '+extra.group(1) if t['amount'].endswith('-') else t['amount']
  lo,hi=amt(t['amount']); ok,om=org_match(a)
  stat['house_tx']+=1; stat['house_tx_bioguide']+=bool(b); stat['house_tx_org']+=bool(ok)
  y=t['filing_date'][-4:]
  tx.append([b,M.get(b,{}).get('name',t['filer_first']+' '+t['filer_last']),M.get(b,{}).get('party',''),'House',t['doc_id'],t['filing_date'],t['owner'],a,t['ticker'],t['asset_type'],t['tx_type'],t['tx_date'],t['notification_date'],t['amount'],lo,hi,ok,om,f"https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/{y}/{t['doc_id']}.pdf",mm])
# Senate eFD
sen_hold=[];sen_gift=[];sen_trav=[]
def sen_bioguide(first,last):
  L=dclib.last_key(last)
  c=[b for b in dclib.member_by_name('*',L) if 'Senate' in M[b]['chambers']]
  if len(c)>1:
    f=(first or '').upper().split()
    c2=[b for b in c if M[b]['first'].upper() in f or (M[b]['nick'] or '').upper() in f]
    c=c2 or c
  return (c[0],'last(+first)') if len(c)==1 else ('','unmatched')
SR=[json.loads(l) for l in open('raw/senate_efd_reports.jsonl')] if os.path.exists('raw/senate_efd_reports.jsonl') else []
for r in SR:
  if r['status']!='ok': continue
  b,mm=sen_bioguide(r['first'],r['last']); nm=M.get(b,{}).get('name',r['filer'])
  for T in r['tables']:
    H=T['rows'][0]; Hl=[h.lower() for h in H]; sec=T['section'].lower()
    for row in T['rows'][1:]:
      if len(row)!=len(H): continue
      d=dict(zip(Hl,row))
      if r['kind']=='ptr' and 'transaction date' in d:
        lo,hi=amt(d.get('amount','')); ok,om=org_match(d.get('asset name',''))
        stat['senate_tx']+=1; stat['senate_tx_bioguide']+=bool(b); stat['senate_tx_org']+=bool(ok)
        tk=d.get('ticker','');tk='' if tk=='--' else tk
        tx.append([b,nm,M.get(b,{}).get('party',''),'Senate',r['report_id'],r['filed'],d.get('owner',''),d.get('asset name',''),tk,d.get('asset type',''),d.get('type',''),d.get('transaction date',''),'',d.get('amount',''),lo,hi,ok,om,r['url'],mm])
      elif r['kind']=='annual':
        if 'asset' in ' '.join(Hl) and ('value' in ' '.join(Hl)):
          an=d.get('asset') or d.get('asset name') or ''; ok,om=org_match(re.split(r'\s+(?:Company|Description|Location|Filer comment|Rate/Coupon|Matures|Underlying assets):',an)[0])
          sen_hold.append([b,nm,M.get(b,{}).get('party',''),r['report_id'],r['title'],r['filed'],T['section'],an[:250],d.get('asset type',''),d.get('owner',''),d.get('value',''),d.get('income type',''),d.get('income amount',''),ok,om,r['url']])
        elif 'gift' in sec or ('source' in ' '.join(Hl) and 'description' in ' '.join(Hl) and 'value' in ' '.join(Hl)):
          src=d.get('source',''); ok,om=org_match(src); sen_gift.append([b,nm,r['report_id'],r['filed'],T['section'],src,d.get('description',''),d.get('value',''),ok,om,r['url']])
        elif 'travel' in sec or 'itinerary' in ' '.join(Hl):
          src=d.get('source','') or d.get('sponsor',''); ok,om=org_match(src); sen_trav.append([b,nm,r['report_id'],r['filed'],T['section'],src,json.dumps(d)[:400],ok,om,r['url']])
H=['bioguide','member','party','chamber','doc_id','filing_date','owner','asset','ticker','asset_type','tx_type','tx_date','notification_date','amount_range','amount_min','amount_max','lda_org_key','lda_org_match','source_url','member_match']
ntx=dclib.wcsv('stock_transactions.csv',H,tx)
agg=collections.defaultdict(lambda:[0,0,0,0,0,set(),'',''])
for r in tx:
  if not r[0]: continue
  key=(r[0],r[8] or dclib.norm_org(r[7])[:60])
  a=agg[key]; a[0]+=1; t=r[10].lower(); a[1]+=t.startswith('p'); a[2]+=t.startswith('s'); a[3]+=int(r[14] or 0); a[4]+=int(r[15] or r[14] or 0); a[5].add(r[11][-4:]); a[6]=a[6] or r[16]; a[7]=a[7] or r[7]
rows=[[b,M.get(b,{}).get('name',''),M.get(b,{}).get('party',''),M.get(b,{}).get('chamber',''),k,v[7][:150],v[0],v[1],v[2],v[3],v[4],'|'.join(sorted(v[5])),v[6],OI.get(v[6],{}).get('name',''),len(OI.get(v[6],{}).get('lob',[])),'high' if v[6] else '',now] for (b,k),v in sorted(agg.items(),key=lambda x:-x[1][4])]
nag=dclib.wcsv('edges_member_company_trades.csv',['bioguide','member','party','chamber','asset_key','asset_example','n_tx','n_purchases','n_sales','sum_amount_min','sum_amount_max','tx_years','lda_org_key','lda_org_name','n_lda_lobbyists_for_org','member_match_confidence','built_at'],rows)
nh=dclib.wcsv('senate_annual_holdings.csv',['bioguide','member','party','report_id','report_title','filed','section','asset','asset_type','owner','value','income_type','income_amount','lda_org_key','lda_org_match','source_url'],sen_hold)
ng=dclib.wcsv('senate_annual_gifts.csv',['bioguide','member','report_id','filed','section','source','description','value','lda_org_key','lda_org_match','source_url'],sen_gift)
nt=dclib.wcsv('senate_annual_travel_reimbursements.csv',['bioguide','member','report_id','filed','section','source','raw_row','lda_org_key','lda_org_match','source_url'],sen_trav)
# House privately funded travel (gift travel filings)
trav=[]
for y in (2023,2024,2025,2026):
  for t in ET.parse(f'/workspace/tmp_dcgraph/htravel/{y}Travel.xml').getroot():
    g={c.tag:(c.text or '').strip() for c in t}
    mn=g.get('MemberName',''); last,_,first=mn.partition(', ')
    b,mm=house_bioguide(last,first,g.get('State','')+g.get('District',''))
    filer=g.get('FilerName',''); is_member=dclib.norm_person(filer)==dclib.norm_person(first+' '+last) if first else False
    ok,om=org_match(g.get('TravelSponsor',''))
    stat['house_travel']+=1; stat['house_travel_bioguide']+=bool(b); stat['house_travel_org']+=bool(ok)
    trav.append([g.get('DocID'),y,b,M.get(b,{}).get('name',mn),M.get(b,{}).get('party',''),filer,'member' if is_member else 'staff',g.get('Destination'),g.get('DepartureDate'),g.get('ReturnDate'),g.get('TravelSponsor'),g.get('FilingType'),ok,om,OI.get(ok,{}).get('name',''),f"https://disclosures-clerk.house.gov/public_disc/gift-pdfs/{g.get('DocID')}.pdf",mm])
ntr=dclib.wcsv('house_privately_funded_travel.csv',['doc_id','filing_year','bioguide','member_office','party','traveler','traveler_type','destination','departure','return','sponsor','filing_type','lda_org_key','lda_org_match','lda_org_name','source_url','member_match'],trav)
ag=collections.defaultdict(lambda:[0,0,set(),set()])
for r in trav:
  if not r[2]: continue
  k=(r[10],r[2]); a=ag[k]; a[0]+=1; a[1]+=r[6]=='member'; a[2].add(r[8][-4:]); a[3].add(r[7])
sp=[[s,dclib.norm_org(s),org_match(s)[0],b,M[b]['name'],M[b]['party'],v[0],v[1],v[0]-v[1],'|'.join(sorted(v[2])),'|'.join(sorted(v[3]))[:200],now] for (s,b),v in sorted(ag.items(),key=lambda x:-x[1][0])]
nsp=dclib.wcsv('edges_travel_sponsor_to_member.csv',['sponsor','sponsor_key','lda_org_key','bioguide','member','party','n_trips','n_member_trips','n_staff_trips','years','destinations','built_at'],sp)

# House annual FD (Schedule A holdings, G gifts, H travel reimbursements)
hh=[];hgt=[]
if os.path.exists('raw/house_fd_annual_items.jsonl'):
  for l in open('raw/house_fd_annual_items.jsonl'):
    x=json.loads(l); b,mm=house_bioguide(x['filer_last'],x['filer_first'],x['state_dst']); nm=M.get(b,{}).get('name',x['filer_first']+' '+x['filer_last'])
    u=f"https://disclosures-clerk.house.gov/public_disc/financial-pdfs/{x['filing_year']}/{x['doc_id']}.pdf"
    if x['sched']=='A':
      tk=re.findall(r'\(([A-Z][A-Z0-9.\-/]{0,7})\)',x['asset']); ok,om=org_match(x['asset'])
      lo,hi=amt(x['value']); stat['house_fd_assets']+=1; stat['house_fd_assets_org']+=bool(ok)
      hh.append([b,nm,M.get(b,{}).get('party',''),x['doc_id'],x['filing_year'],x['asset'][:250],tk[-1] if tk else '',x['asset_code'],x['value'],lo,hi,ok,om,u,mm])
    else:
      c=x['cols']; txt=' '.join(c)
      if x['sched']=='H' and not re.search(r'\d\d/\d\d/\d{4}',txt): continue
      if x['sched']=='G' and not re.search(r'\$[\d,]+',txt): continue
      src=c[0]; ok,om=org_match(src); stat['house_fd_'+x['sched']]+=1
      hgt.append([b,nm,x['doc_id'],x['filing_year'],{'G':'gift','H':'travel_reimbursement'}[x['sched']],src,txt[:300],ok,om,u])
nhh=dclib.wcsv('house_annual_holdings.csv',['bioguide','member','party','doc_id','filing_year','asset','ticker','asset_code','value_range','value_min','value_max','lda_org_key','lda_org_match','source_url','member_match'],hh)
nhg=dclib.wcsv('house_annual_gifts_travel.csv',['bioguide','member','doc_id','filing_year','kind','source','raw_text','lda_org_key','lda_org_match','source_url'],hgt)
HA=collections.defaultdict(lambda:[0,0,0,'',set()])
for r in hh:
  if r[0] and r[11]:
    a=HA[(r[0],r[11])]; a[0]+=1; a[1]+=int(r[9] or 0); a[2]+=int(r[10] or r[9] or 0); a[3]=r[5]; a[4].add(r[4])
for r in sen_hold:
  if r[0] and r[13]:
    a=HA[(r[0],r[13])]; a[0]+=1; lo,hi=amt(r[10]); a[1]+=int(lo or 0); a[2]+=int(hi or lo or 0); a[3]=r[7]; a[4].add(r[5][-4:])
nha=dclib.wcsv('edges_member_company_holdings.csv',['bioguide','member','party','chamber','lda_org_key','lda_org_name','n_holding_rows','sum_value_min','sum_value_max','asset_example','report_years','built_at'],
  [[b,M.get(b,{}).get('name',''),M.get(b,{}).get('party',''),M.get(b,{}).get('chamber',''),k,OI[k]['name'],v[0],v[1],v[2],v[3][:150],'|'.join(sorted(v[4])),now] for (b,k),v in sorted(HA.items(),key=lambda q:-q[1][2])])
stat.update({'house_annual_holdings_rows':nhh,'house_annual_gift_travel_rows':nhg,'member_company_holding_edges':nha})

json.dump({**stat,'stock_tx_rows':ntx,'member_company_edges':nag,'senate_holdings':nh,'senate_gifts':ng,'senate_travel':nt,'house_travel':ntr,'travel_sponsor_edges':nsp,'built_at':now},open('ethics_stats.json','w'),indent=1)
print(json.load(open('ethics_stats.json')))
