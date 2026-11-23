import json,sys,re
src=open(sys.argv[1]).read()
# canvas read may wrap source; find import line
i=src.find('import {'); src=src[i:]
d=json.load(open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'map_v2.json')))
rows=d['rows']
def lit(name):
    m=re.search(r'const '+name+r' = `(.*?)`;',src,re.S)
    return [l for l in m.group(1).split('\n') if l] if m else None
got=[]
for n in ['RSA','RSB','RSC','RSD']:
    v=lit(n); print(n,len(v) if v is not None else None); got+=v or []
bad=[(i,a,b) for i,(a,b) in enumerate(zip(got,rows)) if a!=b]
print('rows got',len(got),'mismatch',len(bad))
for b in bad[:20]: print(b)
def es(name):
    m=re.search(r'const '+name+r' = (\[.*?\]\.join\(" "\)|".*?");',src,re.S)
    if not m: return None
    s=m.group(1)
    if s.startswith('['): s=' '.join(re.findall(r'"([^"]*)"',s))
    else: s=s[1:-1]
    return [t for t in s.split(' ') if t]
et=[]
for n in ['EA0','EA1','EA2','EA3','EA4','EB0','EB1','EB2','EB3','EB4']: v=es(n); print(n,len(v) if v else v); et+=v or []
ref=d['es'].split(' ')
print('edges got',len(et),'of',len(ref),'mismatch',sum(1 for a,b in zip(et,ref) if a!=b))
for k,(a,b) in enumerate(zip(et,ref)):
    if a!=b: print(k,a,b); break
