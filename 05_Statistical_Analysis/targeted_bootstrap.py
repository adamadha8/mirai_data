from pathlib import Path
import csv,random
from collections import defaultdict
R=Path(__file__).resolve().parents[1];rng=random.Random(20260619)
def rd(p):
 with (R/p).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
results=[]
for metric,col in [('no_evidence','correct'),('identity_update','correct'),('source_attribution','correct'),('style_rule','passed')]:
 d=defaultdict(lambda:[0,0])
 for x in rd('04_Item_Level_Results/'+metric+'_results.csv'):
  if x['split']=='primary':z=d[x['configuration'],x['persona_id']];z[0]+=int(x[col]);z[1]+=1
 for c in sorted({k[0] for k in d}):
  pairs=[v for (conf,p),v in sorted(d.items()) if conf==c]; vals=[]
  for i in range(10000):
   sample=rng.choices(pairs,k=len(pairs));vals.append(sum(x[0] for x in sample)/sum(x[1] for x in sample))
  vals.sort();results.append(dict(metric=metric,configuration=c,observed=sum(x[0] for x in pairs)/sum(x[1] for x in pairs),ci_low=vals[249],ci_high=vals[9749],resamples=10000,seed=20260619,provenance='calculated_from_reconstructed_reference'))
with (R/'05_Statistical_Analysis/targeted_bootstrap.csv').open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=results[0]);w.writeheader();w.writerows(results)
print('Wrote',len(results),'persona cluster bootstrap intervals.')
