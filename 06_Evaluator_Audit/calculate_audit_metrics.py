from pathlib import Path
import csv
p=Path(__file__).resolve().parent
with (p/'audit_sample.csv').open(encoding='utf-8',newline='') as f:r=list(csv.DictReader(f))
n=len(r)
for dim in ('claim','style'):
 a='evaluator_a_'+dim;b='evaluator_b_'+dim;t='adjudicated_'+dim;checker='parser_claim' if dim=='claim' else 'checker_style'
 tp=sum(x[checker]=='1' and x[t]=='1' for x in r);fp=sum(x[checker]=='1' and x[t]=='0' for x in r);fn=sum(x[checker]=='0' and x[t]=='1' for x in r)
 print(dim,'N',n,'agreement',sum(x[a]==x[b] for x in r)/n,'accuracy',sum(x[checker]==x[t] for x in r)/n,'recall',tp/(tp+fn) if tp+fn else None,'F1',2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else None,'TP FP FN',tp,fp,fn)
