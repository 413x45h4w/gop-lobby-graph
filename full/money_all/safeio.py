# Before overwriting an output, keep a timestamped .prev_ copy (append-only data rule).
import os,shutil,datetime
TS=datetime.datetime.now().astimezone().strftime('%Y%m%d_%H%M')
def keep_prev(fn):
  if os.path.exists(fn):
    b,e=os.path.splitext(fn); dst=f'{b}.prev_{TS}{e}'
    if not os.path.exists(dst): shutil.copy2(fn,dst)
  return fn
