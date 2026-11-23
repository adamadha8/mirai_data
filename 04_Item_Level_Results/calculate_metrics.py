from pathlib import Path
import csv
from collections import defaultdict
root=Path(__file__).resolve().parents[1]
def rows(p):
 with (root/p).open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
a=defaultdict(lambda:[0,0,0])
for x in rows('04_Item_Level_Results/item_predictions.csv'):
 z=a[(x['split'],x['configuration'])]
 for i,k in enumerate(('tp','fp','fn')):z[i]+=int(x[k])
for key,(tp,fp,fn) in a.items():print(*key, 'TP/FP/FN',tp,fp,fn,'micro-F1',round(2*tp/(2*tp+fp+fn),6))
for typ,col in [('no_evidence','correct'),('identity_update','correct'),('source_attribution','correct'),('style_rule','passed')]:
 d=defaultdict(lambda:[0,0])
 for x in rows('04_Item_Level_Results/'+typ+'_results.csv'):
  z=d[(x['split'],x['configuration'])];z[0]+=int(x[col]);z[1]+=1
 for k,v in d.items():print(typ,*k,f'{v[0]}/{v[1]}',round(v[0]/v[1],6))
