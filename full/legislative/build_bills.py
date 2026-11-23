# Parse GovInfo BILLSTATUS bulk zips (118th+119th) -> bills, cosponsors, referrals, member->member cosponsor edges.
import zipfile,glob,os,collections,dclib
import xml.etree.ElementTree as ET
M=dclib.members(); now=dclib.NOW()
def tx(e,p,d=''):
  x=e.find(p); return (x.text or '').strip() if x is not None and x.text else d
def cc(code):
  c=code.upper(); return c[:4] if c[4:]=='00' else c
bills=[];cos=[];refs=[];zips=sorted(glob.glob(os.path.join(dclib.TMP,'billstatus/BILLSTATUS-*.zip')))
stats=collections.Counter()
for z in zips:
  with zipfile.ZipFile(z) as Z:
    for nm in Z.namelist():
      if not nm.endswith('.xml'): continue
      b=ET.fromstring(Z.read(nm)).find('bill')
      typ=tx(b,'type').lower(); num=tx(b,'number'); cong=tx(b,'congress')
      bid=f'{typ}{num}-{cong}'
      sp=b.find('sponsors/item'); spb=tx(sp,'bioguideId') if sp is not None else ''
      pa=tx(b,'policyArea/name'); subj=[tx(i,'name') for i in b.findall('subjects/legislativeSubjects/item')]
      la_d=tx(b,'latestAction/actionDate'); la_t=tx(b,'latestAction/text')
      laws=[tx(l,'type')+' '+tx(l,'number') for l in b.findall('laws/item')]
      cl=b.findall('cosponsors/item')
      committees=[]
      for c in b.findall('committees/item'):
        code=tx(c,'systemCode'); committees.append(cc(code))
        acts='|'.join(sorted({tx(a,'name') for a in c.findall('activities/item')}))
        refs.append([bid,cc(code),tx(c,'name'),tx(c,'chamber'),acts,'',now])
        for s in c.findall('subcommittees/item'):
          refs.append([bid,cc(tx(s,'systemCode')),tx(s,'name'),tx(c,'chamber'),'|'.join(sorted({tx(a,'name') for a in s.findall('activities/item')})),cc(code),now])
      active=0
      for c in cl:
        wd=tx(c,'sponsorshipWithdrawnDate'); active+= (wd=='')
        cos.append([bid,cong,spb,tx(c,'bioguideId'),tx(c,'party'),tx(c,'sponsorshipDate'),tx(c,'isOriginalCosponsor'),wd])
      bills.append([bid,cong,typ,num,tx(b,'title'),tx(b,'introducedDate'),pa,spb,tx(sp,'fullName') if sp is not None else '',tx(sp,'party') if sp is not None else '',active,len(cl),'|'.join(dict.fromkeys(committees)),la_d,la_t[:300],'|'.join(laws),'|'.join(subj[:15]),now])
      stats[cong]+=1
n1=dclib.wcsv('bills.csv',['bill_id','congress','bill_type','number','title','introduced','policy_area','sponsor_bioguide','sponsor_name','sponsor_party','n_cosponsors_active','n_cosponsors_incl_withdrawn','committee_codes','latest_action_date','latest_action','laws','subjects_top15','built_at'],bills)
n2=dclib.wcsv('bill_cosponsors.csv',['bill_id','congress','sponsor_bioguide','cosponsor_bioguide','cosponsor_party','sponsorship_date','is_original','withdrawn_date'],cos)
n3=dclib.wcsv('bill_committee_referrals.csv',['bill_id','committee_code','committee_name','chamber','activities','parent_committee_code','built_at'],refs)
E=collections.defaultdict(lambda:[0,0,set()])
for bid,cong,s,c,p,d,o,wd in cos:
  if wd or not s or not c: continue
  k=(s,c); E[k][0]+=1; E[k][1]+=(o=='True'); E[k][2].add(cong)
rows=[]
for (s,c),(n,o,cg) in sorted(E.items(),key=lambda x:-x[1][0]):
  ps=M.get(s,{}).get('party',''); pc=M.get(c,{}).get('party','')
  rows.append([s,M.get(s,{}).get('name',''),ps,c,M.get(c,{}).get('name',''),pc,n,o,'|'.join(sorted(cg)),int(bool(ps and pc and ps!=pc)),'govinfo BILLSTATUS bulk','high',now])
n4=dclib.wcsv('member_cosponsor_edges.csv',['sponsor_bioguide','sponsor','sponsor_party','cosponsor_bioguide','cosponsor','cosponsor_party','n_bills','n_original','congresses','cross_party','source','confidence','built_at'],rows)
print(dict(stats),n1,n2,n3,n4)
