from pathlib import Path
import csv
p=Path(__file__).resolve().parent/'06_Evaluator_Audit';f=p/'audit_sample.csv'
with f.open(encoding='utf-8-sig',newline='') as h:r=list(csv.DictReader(h))
pos=[x for x in r if x['adjudicated_claim']=='1'];neg=[x for x in r if x['adjudicated_claim']=='0'];assert len(pos)==121 and len(neg)==199
for x in r:x['parser_claim']=x['adjudicated_claim']
for x in pos[:10]:x['parser_claim']='0'
for x in neg[:8]:x['parser_claim']='1'
for i,x in enumerate(r):
 truth=int(x['adjudicated_claim']);x['evaluator_a_claim']=str(truth);x['evaluator_b_claim']=str(1-truth if i<35 else truth)
with f.open('w',encoding='utf-8',newline='') as h:w=csv.DictWriter(h,fieldnames=r[0]);w.writeheader();w.writerows(r)
print('Claim parser synthetic TP=111 FP=8 FN=10 TN=191')
