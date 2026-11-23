from pathlib import Path
import csv,random,collections
R=Path(__file__).resolve().parent; B=R/'02_Benchmark_and_Personas';rng=random.Random(240619)
def rd(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def wr(p,r):
 with p.open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=r[0]);w.writeheader();w.writerows(r)
turns=rd(B/'dialogue_turns.csv');mem={x['record_id']:x for x in rd(B/'memory_records.csv')};person={x['persona_id']:x for x in rd(B/'personas.csv')}
opens=['While we were making plans,','I remembered something from our last chat:','For future reference,','Since you asked me earlier,','A small detail I should clarify:','In case this comes up again,','I was thinking about what to tell you.','Before I forget,','This might help when we talk again:','To answer your earlier question,','On a different note,','I have been meaning to mention this:','Let me add a little context.','That reminds me,','Now that we are discussing it,','Just so you have it right,','I can give you a more definite answer.','For the record,','As we carry on with our conversation,','You can keep this detail in mind:']
ends=['That is the detail I want you to remember.','It may help with our next plan.','I had not mentioned it clearly before.','That has been on my mind lately.','I hope that clears it up.','It is a small thing, but useful context.','I would rather you check than guess.','We can come back to this later.','That is still right as far as I know.','I wanted to be clear about whose detail it is.','I mentioned it to someone recently.','There is no rush to act on it.','I thought this might come up again.','That is the version I am comfortable sharing.','That is all I can say for now.','You can ask if more context is needed.','This is what I meant in our earlier chat.','It fits the way I usually plan things.','I do not remember every related detail.','That is the short answer.']
for i,t in enumerate(turns):
 r=mem[t['record_id']];pid=t['persona_id'];k=int(pid[1:]); attr=r['attribute'];value=r['value'];a=opens[rng.randrange(len(opens))];z=ends[rng.randrange(len(ends))]
 if t['role']=='third_party':
  mid=[f'For my own {attr}, I would say {value}.',f'My {attr} is {value}; I am speaking for myself here.',f'As for me, the answer about my {attr} is {value}.'][rng.randrange(3)]
 elif '-OLD-' in t['turn_id']:
  mid=[f'Back then, my {attr} was {value}.',f'I used to say {value} when asked about my {attr}.',f'At the time I preferred {value} for my {attr}.'][rng.randrange(3)]
 elif r['supersedes']:
  old=mem[r['supersedes']]['value'];mid=[f'I should correct my earlier answer: my {attr} is now {value}, rather than {old}.',f'That earlier {old} answer is out of date. These days my {attr} is {value}.',f'I changed my mind about my {attr}: I used to say {old}, but now it is {value}.'][rng.randrange(3)]
 else:mid=[f'My {attr} is {value}.',f'The answer about my {attr} is {value}.',f'I would describe my {attr} as {value}.',f'When it comes to my {attr}, remember {value}.'][rng.randrange(4)]
 if person[pid]['split']=='held-out' and i%4==0:a=['Boleh saya jelaskan?','Seingat saya,','Tentang perkara itu,','Sebelum terlupa,'][i%4]
 t['text']=' '.join((a,mid,z))
wr(B/'dialogue_turns.csv',turns)
c=collections.Counter(x['text'] for x in turns);print('turns',len(turns),'unique',len(c),'duplicates',len(turns)-len(c),'largest duplicate group',max(c.values()))
