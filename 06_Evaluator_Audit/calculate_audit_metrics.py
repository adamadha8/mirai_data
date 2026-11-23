from pathlib import Path
import csv
root=Path(__file__).resolve().parents[1]
with (root/'06_Evaluator_Audit/audit_sample.csv').open(encoding='utf-8',newline='') as f:r=list(csv.DictReader(f))
n=len(r); agree=sum(x['evaluator_a']==x['evaluator_b'] for x in r); acc=sum(x['parser']==x['adjudicated'] for x in r); tp=sum(x['parser']=='1' and x['adjudicated']=='1' for x in r); fp=sum(x['parser']=='1' and x['adjudicated']=='0' for x in r); fn=sum(x['parser']=='0' and x['adjudicated']=='1' for x in r)
print('Illustrative audit only:',n,'agreement',agree/n,'accuracy',acc/n,'recall',tp/(tp+fn),'F1',2*tp/(2*tp+fp+fn))
