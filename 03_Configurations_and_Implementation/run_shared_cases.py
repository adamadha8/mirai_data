from pathlib import Path
import sys,csv
sys.path.insert(0,str(Path(__file__).resolve().parent))
from reference_pipeline import Record,execute,CONFIGS
cases=[('ownership','P','drink',[Record('valid','P','drink','coffee',2024,semantic=.7),Record('other','Q','drink','tea',2024,semantic=1,lexical=1,recency=1,trust=1)],None),('consent','P','snack',[Record('denied','P','snack','nuts',2024,consent=False)],None),('update','P','drink',[Record('old','P','drink','tea',2022,2024,semantic=1,lexical=1,recency=1,trust=1),Record('current','P','drink','coffee',2024,semantic=.6)],None),('no_evidence','P','pet',[],'Milo'),('recipient','P','drink',[Record('current','P','drink','coffee',2024)],None)]
rows=[]
for case,p,attr,records,draft in cases:
 for config in CONFIGS:
  r=execute(config,records,p,attr,injected_draft=draft);rows.append(dict(case=case,configuration=config,input_dialogue='Synthetic memory statements for '+attr,records='; '.join(f'{x.id}:owner={x.owner},value={x.value},valid={x.date}-{x.end},consent={x.consent}' for x in records),retrieved=';'.join(r['retrieved']),draft=r['draft'],claims=';'.join(r['claims']),checker=r['check'],rewrite=r['rewrite'],final=r['final'],style=r['style'],provenance='executed_local_demo_on_synthetic_cases'))
out=Path(__file__).resolve().parent/'demo_results.csv'
with out.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
print('Executed',len(rows),'configuration-case pairs; see',out)
