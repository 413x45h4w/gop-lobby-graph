import json,sys
q=json.load(open('pending_queries_rest.json'))['queries']+json.load(open('pending_queries_rest_supp.json'))['queries']
b=[x for x in q if x['block']==int(sys.argv[1])]
print('NAMES: ('+b[0]['q'].split(') (',1)[1])
for x in b: print(x['id'],'|',x['q'].split(') (',1)[0]+')')
