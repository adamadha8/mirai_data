import json,sys,hashlib
from pathlib import Path
if len(sys.argv)!=3 or sys.argv[1] not in ('inspect-locomo','inspect-longmem'):
 print('Usage: python integrate.py inspect-locomo|inspect-longmem DATA.json');sys.exit(2)
p=Path(sys.argv[2]); data=json.loads(p.read_text(encoding='utf-8')); print('SHA256',hashlib.sha256(p.read_bytes()).hexdigest()); print('instances',len(data))
if sys.argv[1]=='inspect-locomo':
 print('question count',sum(len(x['qa']) for x in data));print('first sample fields',sorted(data[0]));print('first QA fields',sorted(data[0]['qa'][0]))
else:
 required={'question_id','question_type','question','answer','haystack_sessions'}; missing=[i for i,x in enumerate(data) if not required<=x.keys()];print('missing required rows',len(missing));print('first instance fields',sorted(data[0]));
 if missing:sys.exit(1)
