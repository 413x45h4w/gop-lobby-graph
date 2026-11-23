import re,unicodedata
SUFX={'THE','INC','INCORPORATED','LLC','L','C','LLP','LP','CORP','CORPORATION','CO','COMPANY','LTD','LIMITED','PLC','NA','N','A','SA','AG','NV','SE','HOLDINGS','HOLDING','GROUP','AND','OF','USA','US','AMERICA','AMERICAS','NORTH','DBA','FKA','FORMERLY','ON','BEHALF'}
GENERIC={'SELF','NONE','RETIRED','NOT EMPLOYED','INFORMATION REQUESTED','UNEMPLOYED','HOMEMAKER','N A','REQUESTED','SELF EMPLOYED','ENTREPRENEUR','STUDENT','INVESTOR','PHYSICIAN','ATTORNEY','CONSULTANT','REAL ESTATE','FARMER','OWNER','BUSINESS OWNER','PRIVATE','INFORMATION REQUESTED PER BEST EFFORTS'}
def norm(s):
  s=unicodedata.normalize('NFKD',s or '').encode('ascii','ignore').decode().upper()
  s=re.sub(r'\(.*?\)','',s).replace('&',' AND ').replace("'",'').replace('\u2019','')
  s=re.split(r'\b(?:ON BEHALF OF|OBO|F/K/A|FKA|D/B/A|DBA|FORMERLY)\b',s)[0]
  return re.sub(r'[^A-Z0-9 ]',' ',s).split()
def key(s):
  t=[w for w in norm(s) if w not in SUFX]
  k=' '.join(t)
  return '' if (k in GENERIC or len(k)<3) else k
