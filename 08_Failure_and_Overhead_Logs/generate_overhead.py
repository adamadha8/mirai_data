from pathlib import Path
import csv,random,math,statistics
R=Path(__file__).resolve().parent;path=R;rng=random.Random(20260619)
rows=[]
for conf,avg in [('Full MIRAI',2.74),('Flat RAG',1.86),('Tiered memory',2.08),('Extract/consolidate',2.21)]:
 for i in range(50):rows.append(dict(response_id=f'SYN-{conf[:3]}-{i+1:03}',configuration=conf,duration_seconds=round(avg*rng.uniform(.6,1.8),3),input_tokens=rng.randint(1700,3000),output_tokens=rng.randint(75,160),provenance='reconstructed_reference',note='illustrative synthetic values; not measurements'))
with (path/'reference_response_logs.csv').open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
out=[]
for c in sorted({r['configuration'] for r in rows}):
 rs=[r for r in rows if r['configuration']==c];v=sorted(x['duration_seconds'] for x in rs);out.append(dict(configuration=c,n=len(rs),mean_seconds=statistics.mean(v),p95_seconds=v[math.ceil(.95*len(v))-1],mean_input_tokens=statistics.mean(x['input_tokens'] for x in rs),mean_output_tokens=statistics.mean(x['output_tokens'] for x in rs),provenance='calculated_from_reconstructed_reference'))
with (path/'reference_overhead_summary.csv').open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=out[0]);w.writeheader();w.writerows(out)
print('Generated',len(rows),'synthetic overhead rows, seed 20260619.')

