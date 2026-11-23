from pathlib import Path
import csv,re,collections
R=Path(__file__).resolve().parents[1]
def rd(p):
 with (R/p).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
pred=rd('04_Item_Level_Results/item_predictions.csv');style=rd('04_Item_Level_Results/style_rule_results.csv');audit=rd('06_Evaluator_Audit/audit_sample.csv');responses={(r['configuration'],r['item_id']):r for r in pred}; bad=[]
for r in style:
 p=responses[r['configuration'],r['item_id']];words=re.findall(r"\b[\w'-]+\b",p['response'].casefold());malay=any(x in words for x in ('juga','ingat','terima'));rule=r['rule_id'];actual={'length':len(words)<=25,'formality':'please' in words and 'whatever' not in words,'greeting':bool(words and words[0] in ('hello','hai')),'language':malay if p['split']=='held-out' else not malay}[rule]
 if int(actual)!=int(r['passed']) or r['response']!=p['response']:bad.append((r['item_id'],rule))
assert not bad,bad[:10]
assert len(audit)==320 and collections.Counter(x['configuration'] for x in audit)=={c:40 for c in {x['configuration'] for x in audit}}
print('PASS',len(style),'rule verdicts match full response text; audit is 40 per configuration')
