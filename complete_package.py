from pathlib import Path
import csv, json
from collections import defaultdict
root=Path(__file__).resolve().parent
def read(p):
 with (root/p).open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
def write(p,rows):
 with (root/p).open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
configs=['Full MIRAI','No owner/consent gate','No version ledger','No relationship style','No claim check','Flat RAG','Tiered memory','Extract/consolidate']
primary=[(.909,357,216,758,5883),(.858,297,194,539,5774),(.873,325,162,721,5807),(.891,349,214,741,4519),(.893,243,211,726,5824),(.819,269,144,578,4894),(.853,299,172,614,5066),(.867,335,169,651,5311)]
held=[(.879,160,105,345,2790),(.841,139,105,250,2747),(.828,162,69,316,2758),(.883,170,106,328,2070),(.850,128,97,326,2770),(.789,124,70,260,2273),(.815,148,76,271,2370),(.826,141,84,290,2490)]
agg=defaultdict(lambda:[0,0,0])
for x in read('04_Item_Level_Results/item_predictions.csv'):
 for i,k in enumerate(('tp','fp','fn')):agg[x['split'],x['configuration']][i]+=int(x[k])
target={}
for typ,col in [('no_evidence','correct'),('identity_update','correct'),('source_attribution','correct'),('style_rule','passed')]:
 d=defaultdict(lambda:[0,0])
 for x in read('04_Item_Level_Results/'+typ+'_results.csv'):
  v=d[x['split'],x['configuration']];v[0]+=int(x[col]);v[1]+=1
 target[typ]=d
out=[]
for split,table in [('primary',primary),('held-out',held)]:
 for idx,c in enumerate(configs):
  tp,fp,fn=agg[split,c]; calc=2*tp/(2*tp+fp+fn)
  vals=[('micro-F1',table[idx][0],calc,'item_predictions.csv'),*[(typ,table[idx][j+1],target[typ][split,c][0],typ+'_results.csv') for j,typ in enumerate(target)]]
  for metric,reported,actual,file in vals:
   delta=actual-reported;out.append(dict(split=split,configuration=c,metric=metric,manuscript_reported=reported,reconstructed=actual,difference=delta,match='exact' if abs(delta)<1e-12 else ('within rounding' if metric=='micro-F1' and abs(delta)<.0005 else 'different'),source='04_Item_Level_Results/'+file,limitation='Individual outcomes assigned artificially; held-out F1 counts are assumed' if split=='held-out' else 'Individual outcomes assigned artificially'))
write('09_Validation_and_Comparison/manuscript_vs_reference_results.csv',out)
columns=[]
for f in sorted((root/'02_Benchmark_and_Personas').glob('*.csv')):
 rows=read(str(f.relative_to(root)))
 for col in rows[0]:columns.append(dict(file=f.name,column=col,definition={'provenance':'Source classification; reconstructed rows are synthetic','persona_id':'Synthetic unique persona key','split':'Development, primary or held-out','evidence_id':'Synthetic record identifier','active_identity_version':'Assumed identity version','supersedes':'Prior record ID replaced by this record','valid_from':'Start of validity (inclusive)','valid_to':'End of validity (exclusive); blank means open','expected_value':'Constructed reference answer','trial_id':'Synthetic trial key','item_id':'Synthetic item key','query':'Constructed query','source_actor':'Actor supplying the record','source_role':'Actor role','consent':'Assumed permission state','authority':'Assumed source authorization','evidence_hash':'SHA-256 of ID and value, synthetic integrity marker'}.get(col,col.replace('_',' ').capitalize()+' (synthetic reference)')))
write('02_Benchmark_and_Personas/data_dictionary.csv',columns)
(root/'09_Validation_and_Comparison/reproducibility_gaps.md').write_text('''# Reproducibility gaps\n\nThis package is a partial reference reconstruction. It does not supply the original persona fields, prompt text, model responses, evidence retrieval scores, checker outputs, audit rationales, response timings, or public benchmark predictions. The synthetic content is schematic and repetitive, not a realistic recovery of natural dialogue. The source-attribution trials do not yet include independent third-party distractor records; the audit style verdicts, meaningful strata, and documented evaluator decision rubrics are not reconstructed. The local demonstration does not implement all baselines, source authority updates, semantic embeddings, recipient style, claim extraction, rewrite, or full ablation behavior. It should not be used to claim an implementation replication.\n\nThe comparison CSV covers Tables 3 and 5; Tables 4, 6, 7 and 9 are not comprehensively compared observation-by-observation. Held-out F1 is approximate. Bootstrap and randomization seeds are assumptions; reconstructed confidence intervals and p-values cannot verify Table 6. Audit labels were generated mechanically and do not reproduce reported audit accuracy or agreement. No public dataset or official scoring version was verified or run. Aggregate timings are transcribed but no fabricated per-response timings are asserted.\n''',encoding='utf-8')
(root/'06_Evaluator_Audit/README.md').write_text('''# Illustrative audit\n320 synthetic records, 40 per configuration. Evaluator snapshots reported in manuscript: A gpt-5.4-mini-2026-03-17; B gpt-5.2-2025-12-11; adjudicator gpt-5.5-pro-2026-04-23. No model calls were made. Decisions here are synthetic binary labels; style decisions are not reconstructed. The sample selection and disagreements are artificial; calculated performance must not be compared as if it reproduced the reported audit.\n''',encoding='utf-8')
(root/'05_Statistical_Analysis/README.md').write_text('''# Statistics\nRun `python 05_Statistical_Analysis/analyze.py`. The analysis calculates mean paired persona F1 differences, percentile intervals from 10,000 paired persona resamples and two-sided sign flips with (b+1)/10001, followed by Holm correction over seven contrasts. Seed 20260619 is a reconstruction assumption; manuscript only specifies the generation seed. Results derive from synthetic allocations and do not verify Table 6.\n''',encoding='utf-8')
(root/'requirements.txt').write_text('# Python 3.11+; standard library only\n',encoding='utf-8')
print('Comparison and documentation generated.')
