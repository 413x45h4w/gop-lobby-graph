import csv, gzip, re, collections, json, math, pickle, os, sys
csv.field_size_limit(10**9)
B='/workspace/gop-lobby-graph/full/'
OUT='/workspace/mapbuild/v2/'
def rd(p):
    p=B+p
    fh=gzip.open(p,'rt',newline='') if p.endswith('.gz') else open(p,newline='')
    return csv.DictReader(fh)
f=lambda x: float(x) if x not in ('',None,'nan') else 0.0
STOP={'INC','LLC','LLP','LP','L','P','CORP','CORPORATION','CO','COMPANY','GROUP','HOLDINGS','HOLDING','THE','AND','OF','LTD','PLC','INCORPORATED','LIMITED','VARIOUS','SUBSIDIARIES','AFFILIATES','ITS','SERVICES','NA','N','A'}
def okey(s):
    s=(s or '').upper().replace('&',' AND ').replace("'",'')
    s=re.sub(r'\(.*?\)',' ',s)
    t=re.sub(r'[^A-Z0-9]+',' ',s).split()
    # join runs of single letters (U S A -> USA)
    o=[];run=''
    for w in t:
        if len(w)==1 and w not in('A',): run+=w; continue
        if run: o.append(run); run=''
        o.append(w)
    if run: o.append(run)
    k=' '.join(w for w in o if w not in STOP)
    return k or ' '.join(o)
def save(name,obj): pickle.dump(obj,open(OUT+name+'.pkl','wb'))
def load(name): return pickle.load(open(OUT+name+'.pkl','rb'))
def pctile(d):
    """d: key->value; returns key->percentile in (0,1] for value>0, 0 otherwise (ties averaged)"""
    pos=sorted((v,k) for k,v in d.items() if v>0)
    n=len(pos); out={k:0.0 for k in d}
    i=0
    while i<n:
        j=i
        while j+1<n and pos[j+1][0]==pos[i][0]: j+=1
        p=((i+j)/2+1)/n
        for t in range(i,j+1): out[pos[t][1]]=p
        i=j+1
    return out
