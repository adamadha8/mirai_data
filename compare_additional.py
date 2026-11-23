from pathlib import Path
import csv
R=Path(__file__).resolve().parent
with (R/'05_Statistical_Analysis/targeted_bootstrap.csv').open(encoding='utf-8',newline='') as f:b={x['metric']:x for x in csv.DictReader(f) if x['configuration']=='Full MIRAI'}
rows=[]
def add(loc,metric,reported,calc='',source='',note=''):
 diff='' if calc=='' else float(calc)-float(reported);rows.append(dict(location=loc,metric=metric,reported=reported,reconstructed=calc,difference=diff,status='reported only' if calc=='' else ('exact' if abs(diff)<1e-12 else 'different'),source=source,assumptions=note))
for metric,lo,hi in [('no_evidence',.863,.920),('identity_update',.863,.938),('source_attribution',.932,.963),('style_rule',.912,.926)]:
 add('Table 4',metric+' CI low',lo,b[metric]['ci_low'],'05_Statistical_Analysis/targeted_bootstrap.csv','Synthetic assignment and assumed seed');add('Table 4',metric+' CI high',hi,b[metric]['ci_high'],'05_Statistical_Analysis/targeted_bootstrap.csv','Synthetic assignment and assumed seed')
for metric,val in [('item micro-F1 CI low',.896),('item micro-F1 CI high',.923),('audit claim agreement',.89),('audit style agreement',.92),('parser accuracy',.94),('parser recall',.92),('parser F1',.93),('style accuracy',.95)]:add('Table 4 / Section 5',metric,val,'','06_Evaluator_Audit/calculate_audit_metrics.py','See audit script; item CI not yet reconstructed')
for metric,val in [('LoCoMo QA F1',.640),('LongMemEval accuracy',.610),('GPT-4.1 mini primary micro-F1',.918),('GPT-4.1 mini held-out micro-F1',.889)]:add('Table 7',metric,val,'','07_Public_Benchmarks/benchmark_information.csv','No actual model run')
for c,mean,p95,it,ot in [('Full MIRAI',2.74,5.21,2480,118),('Flat RAG',1.86,3.34,2120,126),('Tiered memory',2.08,3.72,2260,121),('Extract/consolidate',2.21,4.03,2330,119)]:
 for m,v in [('mean seconds',mean),('p95 seconds',p95),('input tokens',it),('output tokens',ot)]:add('Table 9',c+' '+m,v,'','08_Failure_and_Overhead_Logs/reported_overhead.csv','Original per-response measurements unavailable; synthetic logs separate')
with (R/'09_Validation_and_Comparison/additional_results.csv').open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
print('Additional comparison rows:',len(rows))
