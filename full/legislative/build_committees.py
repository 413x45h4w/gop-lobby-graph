import yaml,dclib,os
cm=yaml.safe_load(open(os.path.join(dclib.TMP,'cm.yaml'))); cc=yaml.safe_load(open(os.path.join(dclib.TMP,'cc.yaml')))
names={}
for c in cc:
  code=c['thomas_id']; names[code]=(c['name'],c['type'],'',code)
  for s in c.get('subcommittees',[]) or []: names[code+s['thomas_id']]=(c['name']+' — '+s['name'],c['type'],code,code+s['thomas_id'])
M=dclib.members(); now=dclib.NOW(); rows=[]
for code,L in cm.items():
  nm,typ,parent,_=names.get(code,('', '', '', code))
  for m in L:
    b=m.get('bioguide'); mm=M.get(b,{})
    rows.append([b,m.get('name'),mm.get('party',m.get('party','')),code,nm,typ,parent or code,'subcommittee' if parent else 'committee',m.get('party'),m.get('rank',''),m.get('title',''),'unitedstates/congress-legislators committee-membership-current.yaml','high',now])
n=dclib.wcsv('member_committee_edges.csv',['bioguide','member','party','committee_code','committee_name','chamber_type','parent_committee_code','level','side','rank','title','source','confidence','built_at'],rows)
crow=[[k,v[0],v[1],v[2] or k,'subcommittee' if v[2] else 'committee'] for k,v in sorted(names.items())]
dclib.wcsv('committees.csv',['committee_code','committee_name','chamber_type','parent_committee_code','level'],crow)
print(n,len(crow),len({r[0] for r in rows}))
