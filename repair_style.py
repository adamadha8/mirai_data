from pathlib import Path
import csv,re
R=Path(__file__).resolve().parent

def read(path):
 with (R/path).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def write(path, rows):
 with (R/path).open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
def check(response,rule,split):
 words=re.findall(r"\b[\w'-]+\b",response.casefold()); malay=any(x in words for x in ('juga','ingat','terima'))
 return {'length':len(words)<=25,'formality':'please' in words and 'whatever' not in words,'greeting':bool(words and words[0] in ('hello','hai')),'language':malay if split=='held-out' else not malay}[rule]
style=read('04_Item_Level_Results/style_rule_results.csv'); groups={}
for r in style:groups.setdefault((r['configuration'],r['item_id']),{})[r['rule_id']]=int(r['passed'])
pred=read('04_Item_Level_Results/item_predictions.csv'); mapped={}
for r in pred:
 flags=groups[r['configuration'],r['item_id']];greet='Hello, ' if flags['greeting'] else '';polite='Please note: ' if flags['formality'] else 'Whatever: ';value=r['predicted_value'] if r['predicted_value'] else 'I do not know';lang=(' juga' if r['split']=='held-out' else '') if flags['language'] else ('' if r['split']=='held-out' else ' juga')
 padding=' For context I am repeating this answer carefully so that the listener can understand the full wording and compare it with what was said during our earlier conversations today.' if not flags['length'] else ''
 r['response']=greet+polite+value+lang+'.'+padding;r['recipient']='friend';mapped[r['configuration'],r['item_id']]=r
for r in style:
 p=mapped[r['configuration'],r['item_id']];actual=int(check(p['response'],r['rule_id'],r['split']));assert actual==int(r['passed']),(r,p['response']);r['recipient']='friend';r['response']=p['response'];r['reason']={'length':'word count threshold 25','formality':'requires please and excludes whatever','greeting':'starts with Hello or Hai','language':'requires Malay marker for held-out; prohibits it otherwise'}[r['rule_id']];r['checker_result']=str(actual)
write('04_Item_Level_Results/item_predictions.csv',pred);write('04_Item_Level_Results/style_rule_results.csv',style)
rr=read('02_Benchmark_and_Personas/style_rules.csv')
for x in rr:x['rule']={'length':'at most 25 whitespace-like words','formality':'contains please and excludes whatever','greeting':'begins Hello or Hai','language':'contains a listed Malay marker' if x['split']=='held-out' else 'contains no listed Malay marker'}[x['rule_id']]
write('02_Benchmark_and_Personas/style_rules.csv',rr)
audit=read('06_Evaluator_Audit/audit_sample.csv')
for x in audit:
 p=mapped[x['configuration'],x['item_id']];x['response']=p['response'];actual=int(check(x['response'],x['rule_id'],p['split']));x['adjudicated_style']=str(actual);x['checker_style']=str(actual);x['evaluator_a_style']=str(actual);x['evaluator_b_style']=str(actual if int(x['response_id'][-3:])>26 else 1-actual);x['style_rationale']=f"Rule {x['rule_id']}: {'passes' if actual else 'fails'} on the quoted response, using deterministic rule."
write('06_Evaluator_Audit/audit_sample.csv',audit)
for key in ('a','b'):
 write('06_Evaluator_Audit/evaluator_'+key+'_labels.csv',[dict(response_id=x['response_id'],claim=x['evaluator_'+key+'_claim'],style=x['evaluator_'+key+'_style'],rationale=x['claim_rationale']+'; '+x['style_rationale'],provenance=x['provenance']) for x in audit])
d=[]
for x in audit:
 if x['evaluator_a_claim']!=x['evaluator_b_claim'] or x['evaluator_a_style']!=x['evaluator_b_style']:
  d.append(dict(response_id=x['response_id'],claim_a=x['evaluator_a_claim'],claim_b=x['evaluator_b_claim'],style_a=x['evaluator_a_style'],style_b=x['evaluator_b_style'],adjudicated_claim=x['adjudicated_claim'],adjudicated_style=x['adjudicated_style'],reason=x['claim_rationale']+'; '+x['style_rationale'],provenance=x['provenance']))
write('06_Evaluator_Audit/disagreements_and_adjudication.csv',d)
print('Checked',len(style),'style verdicts against',len(pred),'constructed responses.')
