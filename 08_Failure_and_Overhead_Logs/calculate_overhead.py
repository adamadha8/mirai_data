import csv,sys,math,statistics
if len(sys.argv)!=2:raise SystemExit('Usage: python calculate_overhead.py response_log.csv')
with open(sys.argv[1],encoding='utf-8',newline='') as f:r=list(csv.DictReader(f))
if not r:raise SystemExit('No records')
v=sorted(float(x['duration_seconds']) for x in r)
print('n',len(v),'mean_seconds',statistics.mean(v),'p95_nearest_rank',v[math.ceil(.95*len(v))-1],'mean_input_tokens',statistics.mean(float(x['input_tokens']) for x in r),'mean_output_tokens',statistics.mean(float(x['output_tokens']) for x in r))
