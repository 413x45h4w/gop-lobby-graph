import csv,json,requests,concurrent.futures as cf,time
rows=list(csv.DictReader(open('../selected_top300.csv')))
def get(i):
  for k in range(5):
    r=requests.get(f'https://lda.gov/api/v1/lobbyists/?id={i}',timeout=30)
    if r.status_code==200:
      x=r.json()['results']; return i,(x[0].get('nickname') if x else None),(x[0].get('middle_name') if x else None)
    time.sleep(3*(k+1))
  return i,None,None
with cf.ThreadPoolExecutor(6) as ex: res=list(ex.map(get,[i for r in rows for i in r['person_key'].split('|')]))
json.dump({i:n for i,n,m in res if n},open('lda_nicknames.json','w'))
print(sum(1 for _,n,_ in res if n),'nicknames')
