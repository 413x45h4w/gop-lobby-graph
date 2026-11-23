from common import *
s1=load('s1_lob'); s2=load('s2'); s3=load('s3'); s4=load('s4')
LM=s1['LM']; T=s1['T']; FM=s1['FM']; MM=s2['MM']; OM=s2['OM']; ON=s2['ON']; E2=s2['E2']
LS,MS,OS=s3['LS'],s3['MS'],s3['OS']
R={}; key2pid={}
for r in rd('money_all/ranking_money_all_with_pac.csv'):
    R[r['person_id']]=r
    for k in r['person_key'].split('|'): key2pid[k]=r['person_id']
P=lambda p: key2pid.get(p,p)
MEM={r['bioguide']:r for r in rd('money_all/member_totals_all_with_pac.csv')}
Ldraw=set(s4['Ldraw']); Mdraw=set(s4['Mdraw']); Kdraw=set(s4['Kdraw'])
NODE={}
def node(i,kind,name,lean='U',sub='',score=0,draw=True,**kw):
    if i in NODE:
        if draw: NODE[i]['draw']=True
        return i
    NODE[i]=dict(kind=kind,name=name,lean=lean,sub=sub,score=score,draw=draw,**kw); return i
EDG=collections.defaultdict(lambda:[0.0,9])
def edge(s,t,ty,v,conf=0):
    e=EDG[(s,t,ty)]; e[0]+=v; e[1]=min(e[1],conf)
CONF={'high':0,'medium':1,'low':2}
lean=lambda s:{'R':'R','D':'D','mixed':'M','Republican':'R','Democrat':'D','Democratic':'D'}.get(s,'U')
for p in s4['Lidx']:
    r=R[p]; node('L'+p,'L',r['lobbyist'],lean(r['party_lean']),r['firm'],LS[p],draw=p in Ldraw)
for b,r in MEM.items():
    node('M'+b,'M',r['member'],r['party'],r['chamber'][0]+'-'+r['state']+('' if r['chamber']=='Senate' else '-'+r['district']),MS[b],draw=b in Mdraw)
for k in s4['Kidx']:
    node('K'+k,'K',ON.get(k,k),'U','',OS[k],draw=k in Kdraw)
D=lambda i: i in NODE and NODE[i]['draw']
def topk(items,k,minv=0):
    return [x for x in sorted(items,key=lambda t:-t[-1]) if x[-1]>=minv][:k]
dp=collections.defaultdict(list)
for r in rd('money_all/edges_money_pairs_all.csv'):
    p=r['person_id']
    if p in Ldraw and D('M'+r['bioguide']): dp[p].append(('M'+r['bioguide'],f(r['total_usd'])))
for p,it in dp.items():
    for m,v in topk(it,3,2000): edge('L'+p,m,'direct',v)
ip=collections.defaultdict(list); jp=collections.defaultdict(list)
with open(B+'money_all/edges_indirect_lobbyist_pac_member.csv') as fh:
    for r in csv.DictReader(fh):
        p=r['person_id']
        if p not in Ldraw or not D('M'+r['bioguide']): continue
        a=f(r['indirect_pac_direct_usd']); j=f(r['jfc_split_usd'])
        if a>0: ip[p].append(('M'+r['bioguide'],a))
        if j>0: jp[p].append(('M'+r['bioguide'],j))
for p,it in ip.items():
    for m,v in topk(it,2,250): edge('L'+p,m,'pacind',v)
for p,it in jp.items():
    for m,v in topk(it,1,1000): edge('L'+p,m,'jfc',v)
print('indirect done',flush=True)
TOP=list(rd('money_all/pac/top_pacs_by_lobbyist_money.csv')); TOPD={x['fec_committee_id']:x for x in TOP}
CM={r['committee_id']:r for r in rd('money_all/pac/committees_classified.csv')}
SPS={r['fec_committee_id']:r for r in rd('outside_money/outside_spenders_summary.csv')}
def cname(cid,fallback=''):
    t=TOPD.get(cid)
    n=(t and t.get('name')) or CM.get(cid,{}).get('name') or SPS.get(cid,{}).get('committee_name') or fallback or cid
    return n.replace('POLITICAL ACTION COMMITTEE','PAC').split(' (AKA')[0].split('; AKA')[0]
ISSPAC=lambda cid: SPS.get(cid,{}).get('committee_type','').startswith(('super_pac','hybrid'))
for t in TOP[:22]:
    cid=t['fec_committee_id']; kind='S' if ISSPAC(cid) else 'C'
    node(kind+cid,kind,cname(cid),lean(t.get('party_lean')),(t.get('committee_class') or '').replace('_',' '),f(t['usd_from_universe_lobbyists']),usd=f(t['usd_from_universe_lobbyists']),nlob=int(f(t['n_lobbyists'])))
cid2n=lambda cid: ('S'+cid) if ('S'+cid) in NODE else ('C'+cid)
lp=collections.defaultdict(lambda: collections.defaultdict(float))
for r in rd('money_all/edges_lobbyist_to_pac_all.csv'):
    if r['person_id'] in Ldraw: lp[r['person_id']][r['fec_committee_id']]+=f(r['usd'])
for p,d in lp.items():
    it=[(cid2n(c),v) for c,v in d.items() if D(cid2n(c))]
    for c,v in topk(it,1,500): edge('L'+p,c,'topac',v)
cm=collections.defaultdict(lambda: collections.defaultdict(float))
cset=set(i[1:] for i in NODE if i[0] in 'CS')
for r in rd('money_all/edges_pac_to_member_all.csv'):
    if r['committee_id'] in cset and r['category'] in ('direct_contribution','direct_inkind') and D('M'+r['bioguide']): cm[r['committee_id']][r['bioguide']]+=f(r['usd'])
for c,d in cm.items():
    for b,v in sorted(d.items(),key=lambda t:-t[1])[:4]: edge(cid2n(c),'M'+b,'pac2mem',v)
for r in rd('money_all/edges_lobbyist_pac_officer.csv'):
    if r['person_id'] in Ldraw and D(cid2n(r['fec_committee_id'])): edge('L'+r['person_id'],cid2n(r['fec_committee_id']),'officer',1)
bund=collections.defaultdict(float); bl=set()
for r in rd('money_all/edges_bundling_all.csv'):
    if r['scored']!='True': continue
    nm=(r['matched_registrant'] or r['bundler']); k='B'+okey(nm)
    node(k,'B',nm,'U','Form 3L bundler',0)
    if D('M'+r['member_bioguide']): bund[(k,'M'+r['member_bioguide'])]+=f(r['bundled_usd'])
    NODE[k]['score']+=f(r['bundled_usd'])
    for p in r['matched_person_ids'].split('|'):
        if p in Ldraw: bl.add(('L'+p,k))
bb=collections.defaultdict(list)
for (k,m),v in bund.items(): bb[k].append((m,v))
for k,it in bb.items():
    for m,v in topk(it,3): edge(k,m,'bundling',v)
for s,t in bl: edge(s,t,'bundlink',1)
print('money done',len(EDG),flush=True)
for p in Ldraw:
    agg=collections.defaultdict(float)
    for (k,nm,v,n) in T.get(p,{}).get('client',[]):
        if D('K'+k): agg['K'+k]+=v
    for k,v in topk(list(agg.items()),2,1): edge('L'+p,k,'client',v)
cb=collections.defaultdict(list); billclients=collections.Counter(); billtitle={}
for r in rd('ld2/edges_client_bill.csv.gz'):
    if r['bill_in_billstatus']!='True': continue
    k=okey(r['client']); billclients[r['bill_id']]+=1; billtitle[r['bill_id']]=r['bill_title']
    if D('K'+k): cb[r['bill_id']].append(('K'+k,int(r['n_filings'])))
topbills=[b for b,_ in billclients.most_common(30)]
TB=set(topbills)
BILLS={r['bill_id']:r for r in rd('legislative/bills.csv') if r['bill_id'] in TB}
for b in topbills:
    br=BILLS.get(b,{})
    node('W'+b,'W',billtitle.get(b,b),lean(br.get('sponsor_party','')),b,billclients[b],nclients=billclients[b],law=br.get('laws',''),sponsor=br.get('sponsor_bioguide',''))
    for k,n in topk(cb[b],4): edge(k,'W'+b,'clientbill',n)
    if br.get('sponsor_bioguide') and D('M'+br['sponsor_bioguide']): edge('W'+b,'M'+br['sponsor_bioguide'],'sponsor',1)
for r in rd('ld2/edges_bill_committee.csv'):
    if ('W'+r['bill_id']) in NODE and r['is_subcommittee']=='False':
        node('H'+r['committee_id'],'H',r['committee_name'],'U',r['committee_id'],0); edge('W'+r['bill_id'],'H'+r['committee_id'],'billcomm',1)
sr=collections.defaultdict(list)
for (k,b,ns,nc) in E2['sponsreach']:
    if D('K'+k) and D('M'+b): sr[k].append(('M'+b,ns))
for k,it in sr.items():
    for m,n in topk(it,1): edge('K'+k,m,'sponsreach',n)
RULES=[('WHITE HOUSE','White House and EOP'),('EXECUTIVE OFFICE OF THE PRESIDENT','White House and EOP'),('(OMB)','White House and EOP'),('MANAGEMENT & BUDGET','White House and EOP'),('NATL ECONOMIC COUNCIL','White House and EOP'),('NATL SECURITY COUNCIL','White House and EOP'),('SCIENCE & TECHNOLOGY POLICY','White House and EOP'),('VICE PRESIDENT','White House and EOP'),('CEQ','White House and EOP'),('ENVIRONMENTAL QUALITY','White House and EOP'),
  ('TRADE REPRESENTATIVE','USTR'),('USTR','USTR'),
  ('HHS','HHS'),('HEALTH & HUMAN','HHS'),('MEDICARE','HHS'),('CMS','HHS'),('FOOD & DRUG','HHS'),('FDA','HHS'),('DISEASE CONTROL','HHS'),('INSTITUTES OF HEALTH','HHS'),('HRSA','HHS'),
  ('TREAS','Treasury'),('INTERNAL REVENUE','Treasury'),('IRS','Treasury'),('OCC','Treasury'),
  ('COMMERCE, DEPT','Commerce'),('(DOC)','Commerce'),('DOC/','Commerce'),('NOAA','Commerce'),('OCEANIC','Commerce'),('PATENT','Commerce'),
  ('TRANSPORTATION','Transportation'),('DOT/','Transportation'),('(DOT)','Transportation'),('AVIATION','Transportation'),('FAA','Transportation'),('NHTSA','Transportation'),('PHMSA','Transportation'),
  ('FEDERAL ENERGY REG','FERC'),('ENERGY, DEPT','Energy'),('DOE/','Energy'),
  ('DEFENSE','Defense'),('(DOD)','Defense'),('DOD/','Defense'),('ARMY','Defense'),('NAVY','Defense'),('AIR FORCE','Defense'),
  ('ENVIRONMENTAL PROTECTION','EPA'),('EPA','EPA'),
  ('AGRICULTURE','USDA'),('USDA','USDA'),
  ('STATE, DEPT','State'),('INTERIOR','Interior'),('DOI/','Interior'),
  ('HOMELAND','Homeland Security'),('DHS','Homeland Security'),('FEMA','Homeland Security'),('CUSTOMS','Homeland Security'),
  ('LABOR, DEPT','Labor'),('(DOL)','Labor'),('DOL/','Labor'),('JUSTICE','Justice'),('DOJ','Justice'),('EDUCATION, DEPT','Education'),('ED/','Education'),
  ('HOUSING & URBAN','HUD'),('(HUD)','HUD'),('VETERANS','Veterans Affairs'),('FEDERAL TRADE','FTC'),('FEDERAL COMMUNICATIONS','FCC'),
  ('SECURITIES & EXCHANGE','SEC'),('SMALL BUSINESS','SBA'),('CONSUMER FINANCIAL','CFPB'),('NUCLEAR REGULATORY','NRC'),('NRC','NRC'),('FEDERAL RESERVE','Federal Reserve')]
def agency(g):
    G=(g or '').upper()
    for a,b in RULES:
        if a in G: return b
    return None
AGV=collections.Counter()
ca=collections.defaultdict(lambda: collections.defaultdict(float))
for (k,g,n,v) in E2['clientagency']:
    a=agency(g)
    if a:
        AGV[a]+=n
        if D('K'+k): ca[k][a]+=n
for (k,ag,n,c) in E2['orgoira']:
    a=agency(ag.split('-',1)[-1])
    if a: AGV[a]+=n
topag=[a for a,_ in AGV.most_common(22)]
for a in topag: node('A'+a,'A',a,'U','Executive agency',AGV[a])
for k,d in ca.items():
    for a,n in topk([(a,n) for a,n in d.items() if ('A'+a) in NODE],1): edge('K'+k,'A'+a,'clientagency',n)
print('lobbying done',len(EDG),flush=True)
for p in Ldraw:
    st=[x for x in T.get(p,{}).get('staff',[]) if D('M'+x[0])]
    st.sort(key=lambda t:(CONF[t[3]],-len(t[4])))
    for (b,nm,cur,c,src) in st[:3]: edge('L'+p,'M'+b,'staff',1,CONF[c])
    for (cids,c) in T.get(p,{}).get('staffcomm',[])[:2]:
        for cid in cids.split('|'):
            cid=cid.rstrip('?')
            if ('H'+cid) in NODE: edge('L'+p,'H'+cid,'staffcomm',1,CONF.get(c,1))
    for (ag,) in T.get(p,{}).get('formeragency',[]):
        a=agency(ag)
        if a and ('A'+a) in NODE: edge('L'+p,'A'+a,'formeragency',1,0)
GOVRE=re.compile(r'EMBASSY|GOVERNMENT|MINISTRY|REPUBLIC|KINGDOM|STATE OF|EMIRATE|PRESIDENT|PRIME MINISTER|CONSULATE|ROYAL',re.I)
fpm=collections.defaultdict(set); fpc={}; fpreg=collections.defaultdict(set)
for (fp,cty,reg,regn,b,att,nd) in E2['fprm']:
    if att in ('context_match','single_active_principal'): fpm[fp].add(b); fpc[fp]=cty; fpreg[fp].add((reg,regn))
topfp=sorted(fpm,key=lambda k:-len(fpm[k]))[:24]
regm=collections.defaultdict(lambda: collections.defaultdict(lambda:[0,9])); regname={}
for (reg,regn,b,c,fp,att,dt) in E2['faracontact']:
    x=regm[reg][b]; x[0]+=1; x[1]=min(x[1],CONF.get(c,2)); regname[reg]=regn
topreg=sorted(regm,key=lambda r:-len(regm[r]))[:16]
for fp in topfp:
    node('F'+fp,'F',fp,'U',fpc.get(fp,''),len(fpm[fp]),gov=bool(GOVRE.search(fp)),nmem=len(fpm[fp]))
    for reg,regn in fpreg[fp]:
        if reg in topreg or len(fpreg[fp])==1:
            node('R'+reg,'R',regn,'U','FARA registrant',len(regm.get(reg,{}))); edge('F'+fp,'R'+reg,'fprincipal',1,1)
for reg in topreg: node('R'+reg,'R',regname[reg],'U','FARA registrant',len(regm[reg]))
for reg in [i[1:] for i in NODE if i[0]=='R']:
    it=[(b,x[0],x[1]) for b,x in regm.get(reg,{}).items() if D('M'+b)]
    it.sort(key=lambda t:(t[2],-t[1]))
    for b,n,c in it[:6]: edge('R'+reg,'M'+b,'faracontact',n,c)
for r in rd('fara/edges_registrant_agent.csv'):
    c=r['lda_match_confidence']
    if c in('high','medium') and ('R'+r['registration_number']) in NODE:
        for p0 in r['lda_person_ids'].split('|'):
            if P(p0) in Ldraw: edge('R'+r['registration_number'],'L'+P(p0),'faraagent',1,CONF[c])
fc=collections.defaultdict(lambda: collections.defaultdict(lambda:[0,9]))
for (reg,regn,b,c,v) in E2['faracontrib']:
    if ('R'+reg) in NODE and D('M'+b): x=fc[reg][b]; x[0]+=v; x[1]=min(x[1],CONF.get(c,2))
for reg,d in fc.items():
    for b,(v,c) in sorted(d.items(),key=lambda t:-t[1][0])[:4]: edge('R'+reg,'M'+b,'faracontrib',v,c)
print('foreign done',len(EDG),flush=True)
ies=collections.defaultdict(float); iesn={}; iest={}
for (sid,sn,st,b,so,v,cy) in E2['ie']: ies[sid]+=v; iesn[sid]=sn; iest[sid]=st
for sid in sorted(ies,key=lambda k:-ies[k])[:30]:
    sp=SPS.get(sid,{})
    node('S'+sid,'S',iesn[sid] or sid,lean(sp.get('ie_lean','')),iest[sid].replace('_',' '),ies[sid],ie=ies[sid])
    NODE['S'+sid]['ie']=ies[sid]; NODE['S'+sid]['sub']=iest[sid].replace('_',' ')
agg=collections.defaultdict(float)
for (sid,sn,st,b,so,v,cy) in E2['ie']:
    if ('S'+sid) in NODE and D('M'+b): agg[(sid,so,b)]+=v
iem2=collections.defaultdict(list)
for (sid,so,b),v in agg.items(): iem2[sid].append((so,b,v))
for sid,it in iem2.items():
    for so,b,v in topk(it,5): edge('S'+sid,'M'+b,'iesup' if so=='support' else 'ieopp',v)
for p in Ldraw:
    for (cid,cn,v,c,ln) in T.get(p,{}).get('spac',[]):
        if ('S'+cid) not in NODE and v>=25000: node('S'+cid,'S',cn,lean(ln),'super PAC',0)
        if ('S'+cid) in NODE:
            edge('L'+p,'S'+cid,'lobspac',v,CONF.get(c,2)); NODE['S'+cid]['usd']=NODE['S'+cid].get('usd',0)+v
cs=collections.defaultdict(float)
for (k,cid,cn,v,ln,cy) in E2['clientspac']:
    if D('K'+k):
        if ('S'+cid) not in NODE and v>=1e6: node('S'+cid,'S',cn,lean(ln),'super PAC',0)
        if ('S'+cid) in NODE: cs[(k,cid)]+=v; NODE['S'+cid]['usd']=NODE['S'+cid].get('usd',0)+v
for (k,cid),v in cs.items(): edge('K'+k,'S'+cid,'clientspac',v)
O990={r['ein']:r for r in rd('nonprofits/orgs_990.csv')}
npv=collections.defaultdict(float)
nps=list(rd('nonprofits/edges_nonprofit_to_superpac_fec.csv'))
for r in nps: npv[r['org_ein']]+=f(r['usd'])
gr=[]
for r in rd('nonprofits/edges_org_to_org_grants.csv.gz'):
    if r['quality_flag']!='ok': continue
    v=f(r['usd'])
    if v>=1e6: gr.append((r['grantor_ein'],r['grantor'],r['grantee_ein'],r['grantee_name'],r['grantee_bmf_subsection'],v))
gout=collections.defaultdict(float)
for g in gr: gout[g[0]]+=g[5]
sc=list(rd('nonprofits/edges_org_to_527_or_committee_schedC.csv'))
scv=collections.defaultdict(float)
for r in sc: scv[r['org_ein']]+=f(r['paid_internal_funds'])+f(r['contributions_received_delivered'])
cand=collections.defaultdict(float)
for e,v in npv.items(): cand[e]+=v
for e,v in gout.items():
    if O990.get(e,{}).get('subsection','') in ('501(c)(4)','501(c)(6)','501(c)(5)'): cand[e]+=v
for e,v in scv.items(): cand[e]+=v
def nkey(ein,name):
    k=okey(name)
    return ('K'+k) if ('K'+k) in NODE else ('N'+ein)
for e in sorted(cand,key=lambda k:-cand[k])[:24]:
    o=O990.get(e,{}); nm=o.get('name') or next((g[1] for g in gr if g[0]==e),e)
    i=nkey(e,nm)
    if i[0]=='K': NODE[i]['sub']=o.get('subsection',''); NODE[i]['draw']=True
    else: node(i,'N',nm,'U',o.get('subsection',''),cand[e],rev=f(o.get('total_revenue')))
for r in nps:
    i=nkey(r['org_ein'],r['org'])
    if i in NODE:
        cid=r['fec_committee_id']
        if ('S'+cid) not in NODE and f(r['usd'])>=5e6: node('S'+cid,'S',r['committee_name'],'U','super PAC',0)
        if ('S'+cid) in NODE: edge(i,'S'+cid,'npspac',f(r['usd'])); NODE['S'+cid]['usd']=NODE['S'+cid].get('usd',0)+f(r['usd'])
for g in gr:
    a=nkey(g[0],g[1]); b=nkey(g[2],g[3]) if g[2] else None
    if a in NODE and b and b in NODE and a!=b: edge(a,b,'grant',g[5])
for r in rd('nonprofits/edges_person_org_officer.csv'):
    if r['lobbyist_person_id'] and P(r['lobbyist_person_id']) in Ldraw:
        i=nkey(r['ein'],r['org']); c=r['lobbyist_confidence'].split('_')[0]
        if i not in NODE and c=='high': node(i,'N',r['org'],'U',r['subsection'],0)
        if i in NODE: edge('L'+P(r['lobbyist_person_id']),i,'off990',1,CONF.get(c,2))
tv=collections.defaultdict(int); tvn={}
for (k,sn,b,n,nm,ns,isorg) in E2['travel']: tv[k]+=n; tvn[k]=sn
for k in sorted(tv,key=lambda k:-tv[k])[:10]:
    i=('K'+k) if ('K'+k) in NODE else ('N'+k)
    if i not in NODE: node(i,'N',tvn[k],'U','Travel sponsor',tv[k])
    else: NODE[i]['draw']=True
tvm=collections.defaultdict(list)
for (k,sn,b,n,nm,ns,isorg) in E2['travel']:
    i=('K'+k) if ('K'+k) in NODE else ('N'+k)
    if i in NODE and D('M'+b): tvm[i].append(('M'+b,n))
for i,it in tvm.items():
    for m,n in topk(it,5): edge(i,m,'travel',n)
print('outside done',len(EDG),flush=True)
# grants: biggest grants from drawn nonprofit/client orgs; add grantee nodes
gsel=[g for g in gr if nkey(g[0],g[1]) in NODE and D(nkey(g[0],g[1]))]
gsel.sort(key=lambda g:-g[5])
for g in gsel[:24]:
    a=nkey(g[0],g[1]); b=nkey(g[2],g[3]) if g[2] else 'N'+okey(g[3])
    if b not in NODE: node(b,'N',g[3],'U',g[4] or 'grantee',g[5])
    else: NODE[b]['draw']=True
    if a!=b: edge(a,b,'grant',g[5])
# Sched C transfers to 527s / committees from drawn orgs
scs=[r for r in sc if nkey(r['org_ein'],r['org']) in NODE and D(nkey(r['org_ein'],r['org']))]
scs.sort(key=lambda r:-(f(r['paid_internal_funds'])+f(r['contributions_received_delivered'])))
for r in scs[:12]:
    v=f(r['paid_internal_funds'])+f(r['contributions_received_delivered'])
    if v<=0: continue
    a=nkey(r['org_ein'],r['org']); b=('S'+r['fec_committee_id']) if ('S'+r['fec_committee_id']) in NODE else ('C'+r['fec_committee_id']) if ('C'+r['fec_committee_id']) in NODE else 'N'+(r['recipient_ein'] or okey(r['recipient_527']))
    if b not in NODE: node(b,'N',r['recipient_527'].split(' (')[0],'U','527 / political org',v)
    edge(a,b,'schedc',v)
# biggest 527s (ActBlue conduits excluded) and LDA-client orgs giving to them
T527={r['org_527_ein']:r for r in rd('nonprofits/irs527_orgs_totals_2023_26.csv')}
top527=[e for e in sorted(T527,key=lambda e:-f(T527[e]['sched_a_usd_2023_26'])) if 'ACTBLUE' not in T527[e]['org_527'].upper()][:8]
for e in top527: node('N'+e,'N',T527[e]['org_527'],'U','527 political org',f(T527[e]['sched_a_usd_2023_26']),rcpt=f(T527[e]['sched_a_usd_2023_26']))
c527=collections.defaultdict(float)
for r in rd('nonprofits/irs527_contributions_2023_26.csv'):
    if r['org_527_ein'] in top527 and r['contributor_kind']=='org_lda_client':
        k='K'+okey(r['lda_client_name'] or r['lda_client_key'])
        if D(k): c527[(k,'N'+r['org_527_ein'])]+=f(r['amount'])
for (a,b),v in sorted(c527.items(),key=lambda t:-t[1])[:40]: edge(a,b,'c527',v)
print('dark money extras',len(EDG),flush=True)
dirs=collections.defaultdict(set)
for r in rd('boards/edges_person_company_board.csv'):
    k=okey(r['lda_client_names'].split(' | ')[0]) if r['lda_client_names'] else okey(r['company'])
    if D('K'+k): dirs[r['director_sec_cik']].add('K'+k)
pairs=collections.Counter()
for d,s in dirs.items():
    s=sorted(s)
    for i in range(len(s)):
        for j in range(i+1,len(s)): pairs[(s[i],s[j])]+=1
for (a,b),n in pairs.items(): edge(a,b,'interlock',n)
for r in rd('legislative/member_committee_edges.csv'):
    if r['level']=='committee':
        node('H'+r['committee_code'],'H',r['committee_name'],'U',r['committee_code'],0)
        NODE['H'+r['committee_code']]['score']+=1
        if D('M'+r['bioguide']) and (r['rank']=='1' or r['title']): edge('M'+r['bioguide'],'H'+r['committee_code'],'roster',1)
cos=[(a,b,n,x) for (a,b,n,x) in E2['cospon'] if D('M'+a) and D('M'+b) and a!=b]
cross=sorted([c for c in cos if c[3]],key=lambda t:-t[2])[:50]; same=sorted([c for c in cos if not c[3]],key=lambda t:-t[2])[:50]
for a,b,n,x in cross+same: edge('M'+b,'M'+a,'cospon',n)
for p in Ldraw:
    for (cc,dt,c,h) in T.get(p,{}).get('wit',[]):
        if ('H'+cc) in NODE: edge('L'+p,'H'+cc,'witness',1,CONF.get(c,2))
ow=collections.defaultdict(list)
for (k,cc,n,nd,c) in E2['orgwit']:
    if D('K'+k) and ('H'+cc) in NODE: ow[k].append(('H'+cc,n))
for k,it in ow.items():
    for h,n in topk(it,1): edge('K'+k,h,'orgwitness',n,1)
cau=collections.Counter(c for (b,c,cf) in E2['caucus'] if b in MEM)
CAU=[c for c,_ in cau.most_common(8)]
for c in CAU: node('U'+c,'U',c,'U','Caucus',cau[c])
cm2=collections.defaultdict(list)
for (b,c,cf) in E2['caucus']:
    if c in CAU and D('M'+b): cm2[c].append(('M'+b,MS.get(b,0)))
for c,it in cm2.items():
    for m,s in topk(it,10): edge(m,'U'+c,'caucus',1,1)
oa=collections.defaultdict(lambda: collections.defaultdict(int))
for (k,ag,n,c) in E2['orgoira']:
    a=agency(ag.split('-',1)[-1])
    if a and D('K'+k) and ('A'+a) in NODE: oa[k][a]+=n
for k,d in oa.items():
    for a,n in topk(list(d.items()),1): edge('K'+k,'A'+a,'oira',n)
for p in Ldraw:
    agg=collections.defaultdict(lambda:[0,9])
    for (ag,mid,c,dt) in T.get(p,{}).get('oira',[]):
        a=agency(ag.split('-',1)[-1])
        if a and ('A'+a) in NODE: x=agg[a]; x[0]+=1; x[1]=min(x[1],CONF.get(c,2))
    for a,(n,c) in agg.items(): edge('L'+p,'A'+a,'oiral',n,c)
    w=LM.get(p,{}).get('wh_low',0)
    if w: edge('L'+p,'AWhite House and EOP','whvisit',w,2)
dk=collections.defaultdict(lambda: collections.defaultdict(int))
for (k,ag,dock,n,c) in E2['docket']:
    a=agency(ag)
    if a and D('K'+k) and ('A'+a) in NODE: dk[k][a]+=n
for k,d in dk.items():
    for a,n in topk(list(d.items()),1): edge('K'+k,'A'+a,'docket',n)
tr=collections.defaultdict(list)
for (b,k,n,lo,hi,tk) in E2['trade']:
    if D('M'+b) and D('K'+k): tr[b].append(('K'+k,n))
for b,it in tr.items():
    for k,n in topk(it,2): edge('M'+b,k,'trade',n)
ho=collections.defaultdict(list)
for (b,k,lo,hi) in E2['hold']:
    if D('M'+b) and D('K'+k): ho[b].append(('K'+k,hi))
for b,it in ho.items():
    for k,v in topk(it,1): edge('M'+b,k,'holding',v)
cod=[(a,b,n,x,c) for (a,b,n,x,c) in E2['codel'] if D('M'+a) and D('M'+b)]
for a,b,n,x,c in sorted(cod,key=lambda t:-t[2])[:50]: edge('M'+a,'M'+b,'codel',n,CONF[c])
for (p,b),w in s1['xe'].items():
    if p in Ldraw and D('M'+b): edge('L'+p,'M'+b,'x',w)
MEMn={r['member'].lower():b for b,r in MEM.items()}
for r in rd('instagram/edges_instagram.csv'):
    for nm in r['members_named'].split(';'):
        b=MEMn.get(nm.strip().lower())
        if not b:
            t=nm.strip().lower().split(); c=[bb for n,bb in MEMn.items() if n.split()[0]==t[0] and n.split()[-1]==t[-1]]; b=c[0] if len(c)==1 else None
        if b and s4['miller']: edge('L'+s4['miller'][0],'M'+b,'ig',1)
E=[(s,t,ty,v,c) for (s,t,ty),(v,c) in EDG.items() if D(s) and D(t)]
used=set([e[0] for e in E]+[e[1] for e in E])
for i,n in NODE.items():
    if n['draw'] and i not in used and n['kind'] not in 'LMK': n['draw']=False
print('nodes drawn',collections.Counter(n['kind'] for n in NODE.values() if n['draw']))
print('nodes total',collections.Counter(n['kind'] for n in NODE.values()))
print('edges',len(E),collections.Counter(e[2] for e in E))
save('s5',{'NODE':NODE,'E':E,'topag':topag,'CAU':CAU})
