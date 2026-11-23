"""Deterministic demonstration, not the original model or experimental predictions."""
from datetime import date

def eligible(r, persona, at):
 return r['persona']==persona and r['consent'] and r['authorized'] and r['from']<=at and (r['to'] is None or at<r['to'])
def score(r):return .45*r['semantic']+.20*r['lexical']+.15*r['recency']+.20*r['trust']
def respond(records,persona,at,attribute):
 records=sorted((r for r in records if eligible(r,persona,at)),key=score,reverse=True)[:8]
 matches=[r for r in records if r['attribute']==attribute]
 if not matches:return 'I do not have enough evidence.',[]
 r=matches[0];draft=r['value']; supported=any(x['value']==draft and x['attribute']==attribute for x in records)
 return (draft if supported else 'I do not have enough evidence.'),[x['id'] for x in records]
r=[dict(id='old',persona='P001',consent=True,authorized=True,attribute='drink',value='tea',**{'from':date(2025,2,4),'to':date(2025,6,12)},semantic=1,lexical=1,recency=.3,trust=1),dict(id='new',persona='P001',consent=True,authorized=True,attribute='drink',value='coffee',**{'from':date(2025,6,12),'to':None},semantic=1,lexical=1,recency=1,trust=1)]
if __name__=='__main__':print('DEMO only:',respond(r,'P001',date(2025,7,1),'drink'));print('Missing:',respond(r,'P001',date(2025,7,1),'pet'))
