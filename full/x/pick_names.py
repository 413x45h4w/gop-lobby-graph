import csv,json,re,sys
sys.path.insert(0,'..'); import partylex as P; from nicks import NICK as NK
COMMON_LAST=set('SMITH JOHNSON WILLIAMS BROWN JONES GARCIA MILLER DAVIS RODRIGUEZ MARTINEZ HERNANDEZ LOPEZ WILSON ANDERSON THOMAS TAYLOR MOORE JACKSON MARTIN LEE THOMPSON WHITE HARRIS CLARK LEWIS ROBINSON WALKER YOUNG ALLEN KING WRIGHT SCOTT HILL GREEN ADAMS BAKER NELSON CARTER MITCHELL ROBERTS TURNER PHILLIPS CAMPBELL PARKER EVANS EDWARDS COLLINS STEWART MURPHY COOK ROGERS MORGAN COOPER PETERSON REED BAILEY BELL KELLY HOWARD WARD COX RICHARDSON WOOD WATSON BROOKS BENNETT GRAY JAMES PRICE HUGHES SANDERS LONG FOSTER POWELL PERRY RUSSELL SULLIVAN BUTLER STONE RICHARDS PALMER FORBES MARSHALL OWEN FRENCH WELLS'.split())
COMMON_FIRST=set('JAMES JOHN ROBERT MICHAEL WILLIAM DAVID RICHARD JOSEPH THOMAS CHARLES CHRISTOPHER DANIEL MATTHEW ANTHONY MARK DONALD STEVEN PAUL ANDREW JOSHUA KENNETH KEVIN BRIAN GEORGE EDWARD RONALD TIMOTHY JASON JEFFREY JEFFERY RYAN JACOB GARY NICHOLAS ERIC JONATHAN STEPHEN LARRY JUSTIN SCOTT BRANDON BENJAMIN SAMUEL FRANK GREGORY RAYMOND PATRICK JACK DENNIS JERRY TYLER AARON ADAM BILL CHRIS DAN JEFF MIKE BOB TOM JIM JOE MARY JENNIFER ELIZABETH SARAH JESSICA SUSAN KAREN LISA NANCY EMILY ASHLEY KATE KATHERINE JULIE AMY LAURA'.split())
M=list(csv.DictReader(open('../ranking_money.csv')))
S={r['lda_lobbyist_id']:r for r in csv.DictReader(open('../selected_top300.csv'))}
inc=sorted(S.values(),key=lambda r:int(r['rank_income_eligible']))
N=int(sys.argv[1]) if len(sys.argv)>1 else 70
pick=list(dict.fromkeys([m['person_id'] for m in M[:N]]+[r['lda_lobbyist_id'] for r in inc[:40]]))
NICK=json.load(open('lda_nicknames.json'))
names=[];amb=[]
disp=lambda s:s.title()
for pid in pick:
  r=S[pid]; p=r['name'].split(); first=p[0]; last=p[-1] if p[-1] not in('JR','JR.','II','III','IV') else p[-2]
  legis=[x for x in P.BYLAST.get(last,[]) if first in x['firsts']]
  isformer='S4_former_gop_member' in r['gop_signals']
  if (legis and not isformer) or (last in COMMON_LAST and first in COMMON_FIRST):
    amb.append((pid,r['name'],'legislator_namesake' if legis else 'common_name')); continue
  vs=[disp(first)+' '+disp(last)]+[disp(n)+' '+disp(last) for n in NK.get(first,[])[:1]]+[disp(NICK[i])+' '+disp(last) for i in r['person_key'].split('|') if i in NICK]
  names.append((pid,r['name'],list(dict.fromkeys(vs))))
json.dump(dict(names=names,ambiguous_excluded=amb),open('xA_names.json','w'),indent=0)
print(len(pick),'picked',len(names),'queryable',len(amb),'ambiguous');print(amb)
