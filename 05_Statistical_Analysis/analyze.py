from pathlib import Path
import csv, random, statistics
root=Path(__file__).resolve().parents[1]; p=root/'05_Statistical_Analysis'
with (p/'persona_level_scores.csv').open(encoding='utf-8',newline='') as f: rows=list(csv.DictReader(f))
lookup={(r['configuration'],r['persona_id']):float(r['f1']) for r in rows}; personas=sorted({r['persona_id'] for r in rows}); configs=sorted({r['configuration'] for r in rows}-{'Full MIRAI'}); rng=random.Random(20260619); output=[]
for c in configs:
 diffs=[lookup['Full MIRAI',pid]-lookup[c,pid] for pid in personas]; obs=statistics.mean(diffs)
 boot=sorted(statistics.mean(rng.choices(diffs,k=len(diffs))) for _ in range(10000)); b=sum(abs(sum(x*(1 if rng.getrandbits(1) else -1) for x in diffs)/len(diffs))>=abs(obs)-1e-15 for _ in range(10000)); output.append(dict(comparison=c,mean_difference=obs,ci_low=boot[249],ci_high=boot[9749],raw_p=(b+1)/10001))
order=sorted(range(len(output)),key=lambda i:output[i]['raw_p']); prev=0
for rank,i in enumerate(order):
 prev=max(prev,min(1,(len(order)-rank)*output[i]['raw_p']));output[i]['holm_p']=prev
for x in output:x['provenance']='calculated_from_reconstructed_reference';print(x)
with (p/'paired_comparisons.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=output[0]);w.writeheader();w.writerows(output)
