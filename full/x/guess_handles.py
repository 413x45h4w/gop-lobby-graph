# Build username guesses for selected 300 (first/nick + last variants). Output batches of <=100.
import csv,json,re
import sys; sys.path.insert(0,'..'); from nicks import NICK
rows=list(csv.DictReader(open('../selected_top300.csv')))
nick=json.load(open('lda_nicknames.json')) if __import__('os').path.exists('lda_nicknames.json') else {}
out={}
for r in rows:
  parts=r['name'].split(); first=parts[0]; last=re.sub(r'[^A-Z]','',parts[-1] if parts[-1] not in('JR','JR.','III','II','IV','SR') else parts[-2])
  firsts=[first]+NICK.get(first,[])+([nick[r['lda_lobbyist_id']].upper()] if nick.get(r['lda_lobbyist_id']) else [])
  g=[]
  for f in dict.fromkeys(re.sub(r'[^A-Z]','',x) for x in firsts):
    for u in (f+last, f+'_'+last, f[0]+last, f+last+'DC'):
      if 1<=len(u)<=15 and u not in g: g.append(u)
  out[r['lda_lobbyist_id']]=g[:8]
allu=sorted({u for g in out.values() for u in g})
json.dump(out,open('guesses.json','w'))
b=[allu[i:i+100] for i in range(0,len(allu),100)]
json.dump(b,open('guess_batches.json','w'))
print(len(allu),'usernames',len(b),'batches')
