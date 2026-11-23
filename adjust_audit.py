from pathlib import Path
import csv, random
p=Path(__file__).resolve().parent/'06_Evaluator_Audit';f=p/'audit_sample.csv'
with f.open(encoding='utf-8',newline='') as h:r=list(csv.DictReader(h))
# Keep ground truth from sampled response; 160 positive. With this prevalence the three rounded claim targets cannot be reached together.
# Agreement and style accuracy can nevertheless be illustrated exactly to published rounding.
for i,x in enumerate(r):
 truth=int(x['adjudicated_claim']);x['evaluator_a_claim']=str(truth);x['evaluator_b_claim']=str(1-truth if i<35 else truth)
 st=int(x['adjudicated_style']);x['evaluator_a_style']=str(st);x['evaluator_b_style']=str(1-st if i<26 else st);x['checker_style']=str(1-st if i<16 else st)
with f.open('w',encoding='utf-8',newline='') as h:
 w=csv.DictWriter(h,fieldnames=r[0]);w.writeheader();w.writerows(r)
for label in ('a','b'):
 with (p/f'evaluator_{label}_labels.csv').open('w',encoding='utf-8',newline='') as h:
  w=csv.DictWriter(h,fieldnames=['response_id','claim','style','rationale','provenance']);w.writeheader();w.writerows(dict(response_id=x['response_id'],claim=x[f'evaluator_{label}_claim'],style=x[f'evaluator_{label}_style'],rationale=x['claim_rationale']+'; '+x['style_rationale'],provenance=x['provenance']) for x in r)
d=[dict(response_id=x['response_id'],claim_a=x['evaluator_a_claim'],claim_b=x['evaluator_b_claim'],style_a=x['evaluator_a_style'],style_b=x['evaluator_b_style'],adjudicated_claim=x['adjudicated_claim'],adjudicated_style=x['adjudicated_style'],reason=x['claim_rationale']+'; '+x['style_rationale'],provenance=x['provenance']) for x in r if x['evaluator_a_claim']!=x['evaluator_b_claim'] or x['evaluator_a_style']!=x['evaluator_b_style']]
with (p/'disagreements_and_adjudication.csv').open('w',encoding='utf-8',newline='') as h:
 w=csv.DictWriter(h,fieldnames=d[0]);w.writeheader();w.writerows(d)
