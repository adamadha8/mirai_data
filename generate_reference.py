from pathlib import Path
import csv, random, json, math, statistics, hashlib
from collections import Counter, defaultdict
ROOT=Path(__file__).resolve().parent
random.seed(20260619)
D=['01_Manuscript_Audit','02_Benchmark_and_Personas','03_Configurations_and_Implementation','04_Item_Level_Results','05_Statistical_Analysis','06_Evaluator_Audit','07_Public_Benchmarks','08_Failure_and_Overhead_Logs','09_Validation_and_Comparison']
for d in D:(ROOT/d).mkdir(exist_ok=True)
def write(path, rows):
 p=ROOT/path; p.parent.mkdir(parents=True,exist_ok=True); rows=list(rows)
 if not rows:return
 with p.open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def md(path,s):(ROOT/path).write_text(s,encoding='utf-8')
def tag(r):return dict(r, provenance='reconstructed_reference')
configs=['Full MIRAI','No owner/consent gate','No version ledger','No relationship style','No claim check','Flat RAG','Tiered memory','Extract/consolidate']
primary=[(1417,99,183,357,216,758,5883),(1325,162,275,297,194,539,5774),(1339,128,261,325,162,721,5807),(1376,114,224,349,214,741,4519),(1426,166,174,243,211,726,5824),(1253,207,347,269,144,578,4894),(1317,172,283,299,172,614,5066),(1344,156,256,335,169,651,5311)]
held=[(.879,160,105,345,2790),(.841,139,105,250,2747),(.828,162,69,316,2758),(.883,170,106,328,2070),(.850,128,97,326,2770),(.789,124,70,260,2273),(.815,148,76,271,2370),(.826,141,84,290,2490)]
personas=[]; items=[]; memories=[]; updates=[]; noev=[]; sources=[]; rules=[]
categories=[('fact',10),('preference',8),('event',10),('relationship',6),('value',6)]
values={'fact':['Bangi','Kuala Lumpur','Johor Bahru','Penang','Kuching','Ipoh','Alor Setar','Kuantan','Melaka','Seremban'],'preference':['tea','coffee','noodles','rice','cycling','reading','blue','green'],'event':['joined a club in 2021','visited Penang in 2022','started a course in 2023','moved in 2024','completed a project in 2022','attended a workshop in 2023','learned cooking in 2020','started cycling in 2021','visited family in 2024','joined a group in 2023'],'relationship':['sibling','friend','colleague','cousin','mentor','neighbour'],'value':['honesty','kindness','learning','patience','fairness','reliability']}
for prefix,n,split in [('D',8,'development'),('P',40,'primary'),('H',20,'held-out')]:
 for pi in range(1,n+1):
  pid=f'{prefix}{pi:03d}'; personas.append(tag(dict(persona_id=pid,split=split,display_name=f'Persona {pid}',language='Malay-English' if split=='held-out' else 'English',identity_version='v2')))
  ix=0
  for cat,num in categories:
   for j in range(num):
    ix+=1;iid=f'{pid}-I{ix:02d}';rid=f'{pid}-R{ix:02d}';v=values[cat][(j+pi)%len(values[cat])]
    q=(f'Apa {cat} saya number {j+1}?' if split=='held-out' else f'What is my {cat} number {j+1}?')
    items.append(tag(dict(item_id=iid,persona_id=pid,split=split,category=cat,query=q,expected_value=v,evidence_id=rid,active_identity_version='v2')))
    memories.append(tag(dict(record_id=rid,persona_id=pid,attribute=f'{cat}_{j+1}',value=v,source_actor=pid,source_role='self',consent='granted',authority='authorized',observed_at='2025-06-12',valid_from='2025-06-12',valid_to='',supersedes='',status='active',confidence=1.0,evidence_hash=hashlib.sha256((rid+v).encode()).hexdigest())))
  for j in range(1,7):
   active=next(x for x in items if x['persona_id']==pid and x['category']=='preference' and x['item_id'].endswith(f'{10+j:02d}'))
   old=f'previous preference {j}'; oldid=f'{pid}-OLD{j:02d}'
   memories.append(tag(dict(record_id=oldid,persona_id=pid,attribute=f'preference_{j}',value=old,source_actor=pid,source_role='self',consent='granted',authority='authorized',observed_at='2025-02-04',valid_from='2025-02-04',valid_to='2025-06-12',supersedes='',status='superseded',confidence=1.0,evidence_hash=hashlib.sha256((oldid+old).encode()).hexdigest())))
   next(x for x in memories if x['record_id']==active['evidence_id'])['supersedes']=oldid
   updates.append(tag(dict(trial_id=f'{pid}-U{j:02d}',persona_id=pid,split=split,query=active['query'],old_value=old,expected_value=active['expected_value'],old_evidence_id=oldid,evidence_id=active['evidence_id'],active_identity_version='v2')))
  for j in range(1,11):noev.append(tag(dict(trial_id=f'{pid}-N{j:02d}',persona_id=pid,split=split,query=f'What is my unrecorded detail {j}?',expected_value='ABSTAIN',evidence_id='',active_identity_version='v2')))
  for j in range(1,21):
   item=next(x for x in items if x['persona_id']==pid and x['item_id'].endswith(f'{j:02d}'))
   sources.append(tag(dict(trial_id=f'{pid}-S{j:02d}',persona_id=pid,split=split,query=item['query'],expected_value=pid,evidence_id=item['evidence_id'],active_identity_version='v2')))
  for k,desc in [('length','at most 25 words'),('formality','polite wording'),('greeting','include a greeting'),('language','use English' if split!='held-out' else 'include Malay and English')]: rules.append(tag(dict(persona_id=pid,split=split,recipient='friend',rule_id=k,rule=desc)))
base='02_Benchmark_and_Personas/'
for name,data in [('personas',personas),('persona_splits',[{k:r[k] for k in ('persona_id','split','provenance')} for r in personas]),('memory_records',memories),('identity_items',items),('identity_update_trials',updates),('no_evidence_trials',noev),('source_attribution_trials',sources),('style_rules',rules)]:write(base+name+'.csv',data)
# Reconstructed outcomes are assigned reproducibly and independently, not generated by the local demo.
result=[]; targeted={'no_evidence':[],'identity_update':[],'source_attribution':[],'style_rule':[]}
for ci,c in enumerate(configs):
 for split in ('primary','held-out'):
  ii=[x for x in items if x['split']==split]; rng=random.Random(20260619+ci*91+(0 if split=='primary' else 1000)); order=list(range(len(ii)));rng.shuffle(order)
  if split=='primary':tp,fp,fn,*counts=primary[ci]
  else:
   score,*counts=held[ci];tp=round(score*len(ii));fn=len(ii)-tp;fp=fn # approximation, not reported
  correct=set(order[:tp]); wrong=set(order[tp:tp+fp])
  for k,x in enumerate(ii):
   status='correct' if k in correct else ('incorrect' if k in wrong else 'omitted'); pred=x['expected_value'] if status=='correct' else ('unsupported reconstructed value' if status=='incorrect' else '')
   result.append(tag(dict(configuration=c,**{key:x[key] for key in ('persona_id','split','item_id','query','expected_value','evidence_id','active_identity_version')},predicted_value=pred,response=(pred or 'I do not know.'),outcome=status,tp=int(status=='correct'),fp=int(status=='incorrect'),fn=int(status!='correct'))))
  for typ,arr,count in [('no_evidence',noev,counts[0]),('identity_update',updates,counts[1]),('source_attribution',sources,counts[2])]:
   rows=[x for x in arr if x['split']==split]; inds=list(range(len(rows)));rng.shuffle(inds); success=set(inds[:count])
   for k,x in enumerate(rows):
    good=k in success; pred=x['expected_value'] if good else ('invented detail' if typ=='no_evidence' else x.get('old_value','other speaker'))
    targeted[typ].append(tag(dict(configuration=c,trial_id=x['trial_id'],persona_id=x['persona_id'],split=split,query=x['query'],expected_value=x['expected_value'],predicted_value=pred,evidence_id=x['evidence_id'],active_identity_version=x['active_identity_version'],correct=int(good))))
  total=len(ii)*4; inds=list(range(total));rng.shuffle(inds); success=set(inds[:counts[3]])
  for k in range(total):
   x=ii[k//4]; rule=['length','formality','greeting','language'][k%4]
   targeted['style_rule'].append(tag(dict(configuration=c,persona_id=x['persona_id'],split=split,item_id=x['item_id'],rule_id=rule,passed=int(k in success))))
write('04_Item_Level_Results/item_predictions.csv',result)
for typ,rows in targeted.items():write('04_Item_Level_Results/'+typ+'_results.csv',rows)
write('03_Configurations_and_Implementation/configuration_comparison.csv',[tag(dict(configuration=c,change=change)) for c,change in zip(configs,['all controls active','owner and consent filters removed','latest write wins; prior versions unavailable','persona-wide style','no claim verification','untyped index','hierarchical memory','extract and consolidate'])])
(ROOT/'03_Configurations_and_Implementation/experiment_settings.json').write_text(json.dumps(dict(provenance='manuscript_reported',generation_seed=20260619,temperature=0.2,top_p=1,max_output_tokens=512,top_k=8,weights=dict(semantic=.45,lexical=.2,recency=.15,trust=.2),response_model='gpt-4o-mini-2024-07-18',embedding_model='text-embedding-3-small',bootstrap_resamples=10000,sign_flips=10000),indent=2))
# audit sample: explicitly illustrative, not fitted to published checker performance
sample=[]
for ci,c in enumerate(configs):
 rr=[x for x in result if x['configuration']==c and x['split']=='primary'][:40]
 for j,x in enumerate(rr):
  truth=int(x['outcome']=='correct'); a=truth if j%13 else 1-truth; b=truth if j%17 else 1-truth; checker=truth if j%11 else 1-truth
  sample.append(tag(dict(response_id=f'AUD-{ci*40+j+1:03d}',persona_id=x['persona_id'],configuration=c,sampling_stratum='illustrative_first_40',item_id=x['item_id'],query=x['query'],evidence_id=x['evidence_id'],response=x['response'],style_rules='length; formality; greeting; language',parser=checker,evaluator_a=a,evaluator_b=b,adjudicated=truth,reason='Illustrative disagreement' if a!=b else 'Agreement; illustrative labels')))
write('06_Evaluator_Audit/audit_sample.csv',sample)
for name,field in [('evaluator_a_labels','evaluator_a'),('evaluator_b_labels','evaluator_b')]:write('06_Evaluator_Audit/'+name+'.csv',[tag(dict(response_id=x['response_id'],decision=x[field])) for x in sample])
write('06_Evaluator_Audit/disagreements_and_adjudication.csv',[tag(dict(response_id=x['response_id'],evaluator_a=x['evaluator_a'],evaluator_b=x['evaluator_b'],adjudicated=x['adjudicated'],reason=x['reason'])) for x in sample if x['evaluator_a']!=x['evaluator_b']])
# persona scores
agg=defaultdict(lambda:[0,0,0])
for x in result:
 if x['split']=='primary':
  a=agg[(x['configuration'],x['persona_id'])]
  for i,k in enumerate(('tp','fp','fn')):a[i]+=x[k]
pr=[]
for (c,p),(tp,fp,fn) in agg.items():pr.append(tag(dict(configuration=c,persona_id=p,tp=tp,fp=fp,fn=fn,f1=2*tp/(2*tp+fp+fn))))
write('05_Statistical_Analysis/persona_level_scores.csv',pr)
md('PROVENANCE.md','''# Provenance\n\nAll persona, memory, prompt, trial, response, evaluator and timing rows are constructed reference material, not recovered study records or model outputs. Aggregate targets and settings come only from the supplied manuscript. Individual assignments are arbitrary, generated with seed 20260619; other assignments fit the same aggregate. Executing local scripts calculates results from these constructed rows; it does not reproduce the original experiment. The local demo is deterministic and uses no API. Public benchmark releases and official scoring were not downloaded or verified.\n''')
md('README.md','''# MIRAI reference data package\n\nThis is a synthetic comparison reference, not the original study data. Read PROVENANCE.md and the audit first. Python 3.11 or later, standard library only; no API or network required.\n\nFrom this folder run `python generate_reference.py`, `python 04_Item_Level_Results/calculate_metrics.py`, `python 05_Statistical_Analysis/analyze.py`, `python 09_Validation_and_Comparison/validate_all.py`, and `python 03_Configurations_and_Implementation/run_local_demo.py`. The generator overwrites generated CSVs.\n\nFolders 01–09 contain the manuscript audit, benchmark and personas, configurations/demo, item and trial outcomes, paired statistical analysis, illustrative evaluator audit, public benchmark notes, illustrative overhead, and validation. Compare your files by joining on your own persona/item mapping, checking counts, fields, split membership and formulas; synthetic IDs and values have no identity correspondence to your originals. Reported figures and constructed results are identified separately. Original logs, exact prompts, actual evaluator outputs, and benchmark predictions are needed for independent reproduction.\n''')
md('01_Manuscript_Audit/manuscript_audit.md','''# Manuscript audit\n\nSource: MIRAI: Evidence-Scoped Identity Continuity for Long-Term Conversational Agents, Adam Adha Bin Kamarul Zaman and Ibrahim Bin Mohamed, 16 pages. Table 1 compares related work; Figure 1 is the enforcement flow; Table 2 defines eight configurations; Tables 3–4 primary outcomes and confidence intervals; Table 5 held-out; Table 6 paired tests; Table 7 public benchmarks and cross-model; Table 8 errors; Table 9 overhead. Equations 1–6 specify record contract, retrieval score, micro-F1, accuracy, style rate, permutation p. Sections 7–8 and declarations describe limitations and funding, ethics, competing interests, and data.\n\nDevelopment: 8, primary: 40 personas × 40 items (10 facts, 8 preferences, 10 events, 6 relationships, 6 values); per persona 10 no-evidence, 6 updates, 20 attribution trials. Held-out: 20 personas, same counts per persona. Four style decisions per item. Audit: 320 responses, 40 per system. The original values, item-level outcomes, evaluation rationales, style definitions, and bootstrap seed are not provided.\n\nImportant: benchmark generation seed 20260619 is reported, while main development and response runs are described as conducted in 2025; the chronology is ambiguous. A wrong item generates FP and FN and an omission FN; all table-3 counts are consistent with that rule. Values rounded to three decimals can differ from arithmetic rounded separately; e.g. 357/400 is 0.8925. Table 6 uses mean persona F1 differences, unlike pooled micro-F1; confidence intervals and p-values cannot be reconstructed uniquely from aggregates. No human evaluation.\n''')
write('01_Manuscript_Audit/assumptions_and_ambiguities.csv',[dict(topic='Seed chronology',reported='20260619; main runs 2025',assumption='reused as reference seed',limitation='chronology unexplained'),dict(topic='Held-out TP FP FN',reported='F1 only',assumption='FP equals FN and TP rounded to target rate',limitation='one artificial realization'),dict(topic='Audit sampling',reported='40 per configuration, stratified',assumption='first 40 reconstructed responses',limitation='strata unspecified; not true original sample'),dict(topic='Timing',reported='Table 9 aggregate statistics',assumption='none generated',limitation='individual recorded values unavailable')])
write('01_Manuscript_Audit/manuscript_evidence_map.csv',[dict(location='Table 3',result='primary TP FP FN and targeted rates',reference='04_Item_Level_Results/*.csv',fields='tp;fp;fn;correct;passed'),dict(location='Table 5',result='held-out rates',reference='04_Item_Level_Results/*.csv',fields='tp;fp;fn;correct;passed'),dict(location='Table 6',result='persona paired differences and tests',reference='05_Statistical_Analysis/persona_level_scores.csv',fields='persona_id;configuration;f1'),dict(location='Table 7',result='independent benchmarks and cross model',reference='07_Public_Benchmarks/benchmark_information.csv',fields='reported_score;actual_run'),dict(location='Table 8',result='three representative failure types',reference='08_Failure_and_Overhead_Logs/failure_cases.csv',fields='case;cause'),dict(location='Table 9',result='latency and token aggregates',reference='08_Failure_and_Overhead_Logs/reported_overhead.csv',fields='mean_seconds;p95_seconds;input_tokens;output_tokens')])
write('07_Public_Benchmarks/benchmark_information.csv',[dict(benchmark='LoCoMo',coverage=1986,metric='normalized partial-match F1',reported_score=.640,actual_run='not run',official_source='not independently verified'),dict(benchmark='LongMemEval-S',coverage=500,metric='binary correctness',reported_score=.610,actual_run='not run',official_source='not independently verified'),dict(benchmark='MIRAI primary GPT-4.1 mini',coverage=1600,metric='micro-F1',reported_score=.918,actual_run='not run',official_source='manuscript Table 7'),dict(benchmark='MIRAI held-out GPT-4.1 mini',coverage=800,metric='micro-F1',reported_score=.889,actual_run='not run',official_source='manuscript Table 7')])
md('07_Public_Benchmarks/scoring_instructions.md','''# Public benchmarks\n\nThe manuscript describes 1,986 LoCoMo QA items and 500 LongMemEval-S questions. Its LoCoMo measure is normalized partial-match F1 and LongMemEval-S uses post-hoc binary correctness. Exact release identifiers, official scripts, prediction formats and judging prompts were not verified; do not treat the synthetic examples here as official formats. Obtain the official releases and pin their commit and evaluation instructions before running. No public benchmark was executed and no official question ID is asserted.\n''')
write('07_Public_Benchmarks/reference_prediction_example.csv',[tag(dict(benchmark='LoCoMo',example_id='SYNTHETIC-EXAMPLE-1',question='What drink?',prediction='tea',note='illustrative only; not official format or model output'))])
write('08_Failure_and_Overhead_Logs/failure_cases.csv',[dict(case='U-017',query='What drink do I usually order?',evidence='R114 tea; R287 correction coffee; identity v4',draft='tea',final='tea',expected='coffee',cause='supersession link not resolved',provenance='manuscript_reported_example'),dict(case='S-031',query='When did I join the robotics club?',evidence='R442: Amir joined in 2023; third speaker; identity v6',draft='2023',final='2023',expected='abstain',cause='speaker-reference resolution failure',provenance='manuscript_reported_example'),dict(case='A-009',query='What was the name of my first cat?',evidence='No cat record; identity v2',draft='Milo',final='Milo',expected='abstain',cause='claim parser did not detect unsupported claim',provenance='manuscript_reported_example')])
write('08_Failure_and_Overhead_Logs/reported_overhead.csv',[dict(configuration=c,mean_seconds=a,p95_seconds=b,input_tokens=i,output_tokens=o,provenance='manuscript_reported') for c,a,b,i,o in [('Full MIRAI',2.74,5.21,2480,118),('Flat RAG',1.86,3.34,2120,126),('Tiered memory',2.08,3.72,2260,121),('Extract/consolidate',2.21,4.03,2330,119)]])
print('Generated synthetic package tables.')
