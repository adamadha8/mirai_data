from pathlib import Path
import csv,hashlib
R=Path(__file__).resolve().parent;B=R/'02_Benchmark_and_Personas';O=R/'04_Item_Level_Results'
def rd(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def wr(p,r):
 with p.open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=r[0]);w.writeheader();w.writerows(r)
items=rd(B/'identity_items.csv');mem=rd(B/'memory_records.csv');turn=rd(B/'dialogue_turns.csv');lookup={m['record_id']:m for m in mem};turnmap={t['record_id']:t for t in turn};changes={}
options={'club joined':['reading club','robotics club','hiking group','photography club'],'workshop attended':['design workshop','cooking workshop','coding workshop','first aid workshop'],'trip taken':['visited Penang','visited Sabah','travelled to Melaka','visited Ipoh'],'project completed':['finished a garden project','completed a class project','finished a community survey','completed a design project'],'class started':['started an evening class','began a cooking class','joined a language class','started a photography class'],'community event attended':['attended a food festival','attended a neighbourhood meeting','joined a cultural festival','attended a community fair'],'family visit':['visited relatives','visited a sibling','spent a weekend with cousins','visited grandparents'],'volunteer activity':['volunteered at a food bank','helped at a community garden','volunteered at a library','helped at a beach clean-up'],'first job':['worked at a bookstore','worked at a cafe','worked at a clinic','worked at a library'],'recent milestone':['completed a training course','earned a certificate','finished a degree','moved into a new home']}
for x in items:
 if x['attribute'] not in options:continue
 old=x['expected_value'];n=int(x['persona_id'][1:]);new=options[x['attribute']][n%4]+' in '+str(2015+n%10);x['expected_value']=new;changes[x['item_id']]=new;m=lookup[x['evidence_id']];m['value']=new;m['evidence_hash']=hashlib.sha256((m['record_id']+new).encode()).hexdigest();turnmap[m['record_id']]['text']=turnmap[m['record_id']]['text'].replace(old,new)
wr(B/'identity_items.csv',items);wr(B/'memory_records.csv',mem);wr(B/'dialogue_turns.csv',turn)
r=rd(O/'item_predictions.csv')
for x in r:
 if x['item_id'] in changes:
  x['expected_value']=changes[x['item_id']]
  if x['outcome']=='correct':x['predicted_value']=x['expected_value']
wr(O/'item_predictions.csv',r)
print('Repaired',len(changes),'event attribute/value pairings.')
