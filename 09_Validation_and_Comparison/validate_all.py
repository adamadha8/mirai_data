from pathlib import Path
import csv, subprocess, sys
from collections import Counter
root=Path(__file__).resolve().parents[1]
def read(path):
 with (root/path).open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
checks=[]
def check(name,condition):
 checks.append((name,bool(condition)));print(('PASS ' if condition else 'FAIL ')+name)
p=read('02_Benchmark_and_Personas/personas.csv'); items=read('02_Benchmark_and_Personas/identity_items.csv'); mem=read('02_Benchmark_and_Personas/memory_records.csv');pred=read('04_Item_Level_Results/item_predictions.csv'); audit=read('06_Evaluator_Audit/audit_sample.csv'); lookup={x['persona_id']:x['split'] for x in p}; ids={x['record_id'] for x in mem}; byid={x['record_id']:x for x in mem}
check('persona counts and unique IDs',len(lookup)==68 and Counter(lookup.values())=={'development':8,'primary':40,'held-out':20})
check('item counts',Counter(x['split'] for x in items)=={'development':320,'primary':1600,'held-out':800})
check('item links',all(lookup.get(x['persona_id'])==x['split'] and x['evidence_id'] in ids for x in items))
for typ,counts in [('identity_update',(240,120)),('no_evidence',(400,200)),('source_attribution',(800,400))]:
 r=read('02_Benchmark_and_Personas/'+typ+'_trials.csv');counts_actual=Counter(x['split'] for x in r);check(typ+' counts', (counts_actual['primary'],counts_actual['held-out'])==counts);check(typ+' persona links',all(lookup.get(x['persona_id'])==x['split'] for x in r))
check('supersession dates',all(not x['supersedes'] or (x['supersedes'] in ids and byid[x['supersedes']]['valid_to']==x['valid_from'] and byid[x['supersedes']]['persona_id']==x['persona_id']) for x in mem))
check('prediction labels',all(int(x['tp'])==int(x['outcome']=='correct') and int(x['fp'])==int(x['outcome']=='incorrect') and int(x['fn'])==int(x['outcome']!='correct') and ((x['predicted_value']==x['expected_value'])==(x['outcome']=='correct')) for x in pred))
check('matched items',all(len({x['configuration'] for x in pred if x['item_id']==i['item_id']})==8 for i in items if i['split']!='development'))
check('audit counts and ids',len(audit)==320 and len({x['response_id'] for x in audit})==320 and all(x['evidence_id'] in ids for x in audit))
check('data provenance',all(x['provenance']=='reconstructed_reference' for x in pred+mem+audit))
for script in ['04_Item_Level_Results/calculate_metrics.py','05_Statistical_Analysis/analyze.py','06_Evaluator_Audit/calculate_audit_metrics.py','03_Configurations_and_Implementation/run_local_demo.py']:
 run=subprocess.run([sys.executable,str(root/script)],capture_output=True,text=True);check(script+' runs',run.returncode==0)
report='# Validation report\n\n'+''.join(('- PASS ' if ok else '- FAIL ')+name+'\n' for name,ok in checks)+'\nThese checks establish internal consistency only, not fidelity to the original records. Timing rows and original evaluator records were not provided. See reproducibility gaps.\n'
(root/'09_Validation_and_Comparison/validation_report.md').write_text(report,encoding='utf-8')
if not all(ok for _,ok in checks):sys.exit(1)
