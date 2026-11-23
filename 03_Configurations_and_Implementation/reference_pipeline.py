"""Toy deterministic architecture; fixed inputs, synthetic scores, no LLM/API."""
from dataclasses import dataclass
@dataclass
class Record:
 id:str; owner:str; attr:str; value:str; date:int; end:int=9999; consent:bool=True; authorized:bool=True; kind:str='profile'; semantic:float=.8; lexical:float=.8; recency:float=.8; trust:float=.8
CONFIGS=['Full MIRAI','No owner/consent gate','No version ledger','No relationship style','No claim check','Flat RAG','Tiered memory','Extract/consolidate']
def execute(configuration, records, owner, attribute, time=2025, recipient='colleague', injected_draft=None):
 if configuration not in CONFIGS:raise ValueError(configuration)
 source_gate=configuration not in ('No owner/consent gate','Flat RAG','Tiered memory','Extract/consolidate')
 ledger=configuration not in ('No version ledger','Flat RAG','Tiered memory','Extract/consolidate')
 claim_check=configuration not in ('No claim check','Flat RAG','Tiered memory','Extract/consolidate')
 candidates=[r for r in records if r.attr==attribute]
 if source_gate:candidates=[r for r in candidates if r.owner==owner and r.consent and r.authorized]
 if ledger:candidates=[r for r in candidates if r.date<=time<r.end]
 elif configuration=='No version ledger':
  # Latest observed write wins, including a late-entered historical value; date is the stand-in.
  candidates=sorted(candidates,key=lambda r:r.date,reverse=True)[:1]
 elif configuration=='Tiered memory':candidates=sorted(candidates,key=lambda r:(r.kind=='profile',r.date),reverse=True)
 elif configuration=='Extract/consolidate':candidates=sorted(candidates,key=lambda r:r.trust,reverse=True)[:1]
 candidates=sorted(candidates,key=lambda r:.45*r.semantic+.20*r.lexical+.15*r.recency+.20*r.trust,reverse=True)[:8]
 draft=injected_draft if injected_draft is not None else (candidates[0].value if candidates else 'ABSTAIN')
 # Claim extraction is an exact-value toy; it cannot parse arbitrary natural language.
 extracted=[] if draft=='ABSTAIN' else [draft]
 eligible=[r for r in records if r.owner==owner and r.consent and r.authorized and r.attr==attribute and r.date<=time<r.end]
 supported=not extracted or any(r.value==draft for r in eligible)
 rewritten='';final=draft
 if claim_check and not supported:
  rewritten=eligible[0].value if eligible else 'ABSTAIN';final=rewritten
 style='formal' if recipient=='colleague' and configuration!='No relationship style' else 'casual'
 return dict(configuration=configuration,retrieved=[r.id for r in candidates],draft=draft,claims=extracted,check=('pass' if supported else 'fail') if claim_check else 'disabled',rewrite=rewritten,final=final,style=style)
if __name__=='__main__':
 records=[Record('old','P','drink','tea',2023,2024,semantic=1),Record('new','P','drink','coffee',2024,semantic=.8),Record('third','OTHER','drink','juice',2025,semantic=1,lexical=1,recency=1,trust=1)]
 for c in CONFIGS:print(execute(c,records,'P','drink'))
 print('unsupported claim:',execute('Full MIRAI',records,'P','pet',injected_draft='Milo'))
