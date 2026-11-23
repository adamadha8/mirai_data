from pathlib import Path
import csv,collections,math,importlib.util
R=Path(__file__).resolve().parents[1]
def rd(s):
 with (R/s).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
items=rd('02_Benchmark_and_Personas/identity_items.csv'); mem=rd('02_Benchmark_and_Personas/memory_records.csv'); turns=rd('02_Benchmark_and_Personas/dialogue_turns.csv'); sessions=rd('02_Benchmark_and_Personas/conversations.csv'); trials=rd('02_Benchmark_and_Personas/source_attribution_trials.csv'); updates=rd('02_Benchmark_and_Personas/identity_update_trials.csv'); preds=rd('04_Item_Level_Results/item_predictions.csv'); audit=rd('06_Evaluator_Audit/audit_sample.csv'); mm={x['record_id']:x for x in mem}; im={x['item_id']:x for x in items}; sid={x['conversation_id'] for x in sessions}; pairs={(x['configuration'],x['item_id']):x for x in preds}; checks=[]
def ck(label,ok):checks.append((label,bool(ok)));print(('PASS ' if ok else 'FAIL ')+label)
ck('session and evidence-turn links',all(x['conversation_id'] in sid for x in turns) and all(any(t['record_id']==i['evidence_id'] for t in turns) for i in items))
ck('expected identity values match authorized active record',all(mm[x['evidence_id']]['value']==x['expected_value'] and mm[x['evidence_id']]['persona_id']==x['persona_id'] and mm[x['evidence_id']]['consent']=='granted' and mm[x['evidence_id']]['authority']=='authorized' for x in items))
ck('attribution distractor genuinely belongs to another actor',all(mm[x['distractor_record_id']]['persona_id']==x['distractor_owner']!=x['persona_id'] and mm[x['distractor_record_id']]['attribute']==mm[x['evidence_id']]['attribute'] for x in trials))
ck('update old and current values and supersession match',all(mm[x['old_evidence_id']]['value']==x['old_value'] and mm[x['evidence_id']]['value']==x['expected_value'] and mm[x['evidence_id']]['supersedes']==x['old_evidence_id'] and mm[x['old_evidence_id']]['valid_to']==mm[x['evidence_id']]['valid_from'] for x in updates))
ck('responses agree with expected value and scoring',all(x['expected_value']==im[x['item_id']]['expected_value'] and (x['predicted_value']==x['expected_value'])==(x['outcome']=='correct') and (x['outcome']!='omitted' or 'I do not know' in x['response']) for x in preds))
ck('audit references correct response',all((x['configuration'],x['item_id']) in pairs and pairs[x['configuration'],x['item_id']]['response']==x['response'] for x in audit))
ck('audit claim adjudication agrees with scenario',all(int(x['adjudicated_claim'])==int(pairs[x['configuration'],x['item_id']]['outcome']=='correct') for x in audit))
# These checks do not assert constructed style labels are measured from text.
texts=[x['text'] for x in turns]; dup=len(texts)-len(set(texts)); counts=collections.Counter(texts)
report='# Semantic validation\n\n'+''.join(('- PASS ' if ok else '- FAIL ')+name+'\n' for name,ok in checks)+f'\nDialogue: {len(texts)} turns, {len(set(texts))} unique exact texts, {dup} exact duplicates; most repeated text occurs {max(counts.values())} times. Text is template-generated; exact diversity does not establish naturalness.\n\nStyle verdicts are checked against constructed response text with a limited deterministic rule set. Configuration demos are simplified, and attribution errors are scenario-based allocations rather than outputs of those demos. This validation cannot establish original-study reproducibility.\n'
(R/'09_Validation_and_Comparison/semantic_validation.md').write_text(report,encoding='utf-8');print(report)
if not all(ok for _,ok in checks):raise SystemExit(1)

