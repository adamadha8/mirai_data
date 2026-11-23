from pathlib import Path
import csv,random,collections
R=Path(__file__).resolve().parent; rng=random.Random(20260619)
def rd(p):
 with (R/p).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def wr(p,rows):
 with (R/p).open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
pred=rd('04_Item_Level_Results/item_predictions.csv');rules=rd('04_Item_Level_Results/style_rule_results.csv');rulemap={(r['configuration'],r['item_id'],r['rule_id']):r['passed'] for r in rules}; configs=list(dict.fromkeys(x['configuration'] for x in pred));out=[]
for ci,c in enumerate(configs):
 pool=[x for x in pred if x['configuration']==c and x['split']=='primary']; groups={s:[x for x in pool if x['outcome']==s] for s in ('correct','incorrect','omitted')}
 # balanced audit designed to enrich difficult cases, not empirical prevalence.
 chosen=[]
 for typ,n in [('correct',15+(ci==7)),('incorrect',17-(ci==7)),('omitted',8)]:chosen.extend(rng.sample(groups[typ],n))
 for j,x in enumerate(chosen):
  label=int(x['outcome']=='correct'); A=1-label if j in (0,1) else label;B=1-label if j in (2,3) else label; check=1-label if j in (4,5) else label
  rid=f'AUD-{ci*40+j+1:03d}'; rule=['length','formality','greeting','language'][j%4]; truth=int(rulemap[c,x['item_id'],rule]); sa=1-truth if j in (6,7) else truth;sb=1-truth if j in (8,9) else truth;sc=1-truth if j in (10,11) else truth
  out.append(dict(response_id=rid,persona_id=x['persona_id'],configuration=c,sampling_stratum=x['outcome'],item_id=x['item_id'],query=x['query'],evidence_id=x['evidence_id'],response=x['response'],rule_id=rule,adjudicated_claim=label,evaluator_a_claim=A,evaluator_b_claim=B,parser_claim=check,claim_rationale=('Value agrees with active evidence' if label else 'Value missing or differs from expected evidence'),adjudicated_style=truth,evaluator_a_style=sa,evaluator_b_style=sb,checker_style=sc,style_rationale='Synthetic assigned verdict for '+rule,provenance='reconstructed_reference'))
wr('06_Evaluator_Audit/audit_sample.csv',out)
for name,key in [('evaluator_a_labels','evaluator_a'),('evaluator_b_labels','evaluator_b')]:wr('06_Evaluator_Audit/'+name+'.csv',[dict(response_id=x['response_id'],claim=x[key+'_claim'],style=x[key+'_style'],rationale=x['claim_rationale']+'; '+x['style_rationale'],provenance=x['provenance']) for x in out])
d=[dict(response_id=x['response_id'],claim_a=x['evaluator_a_claim'],claim_b=x['evaluator_b_claim'],style_a=x['evaluator_a_style'],style_b=x['evaluator_b_style'],adjudicated_claim=x['adjudicated_claim'],adjudicated_style=x['adjudicated_style'],reason=x['claim_rationale']+'; '+x['style_rationale'],provenance=x['provenance']) for x in out if x['evaluator_a_claim']!=x['evaluator_b_claim'] or x['evaluator_a_style']!=x['evaluator_b_style']]
wr('06_Evaluator_Audit/disagreements_and_adjudication.csv',d)
print('Audit constructed:',len(out),'disagreements:',len(d))


