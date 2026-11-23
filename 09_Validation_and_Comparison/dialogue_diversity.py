from pathlib import Path
import csv,random,difflib,collections
R=Path(__file__).resolve().parents[1]
with (R/'02_Benchmark_and_Personas/dialogue_turns.csv').open(encoding='utf-8',newline='') as f:r=list(csv.DictReader(f))
rng=random.Random(20260619);pairs=[(rng.choice(r)['text'],rng.choice(r)['text']) for _ in range(1000)];ratios=[difflib.SequenceMatcher(None,a,b).ratio() for a,b in pairs];c=collections.Counter(x['text'] for x in r);examples=[r[i]['text'] for i in (0,25,100,500,1200,2500)]
s='# Dialogue diversity check\n\n'+f'Turns: {len(r)}; exact unique: {len(c)}; duplicate occurrences: {len(r)-len(c)}; maximum frequency: {max(c.values())}. Random seed 20260619; 1,000 randomly sampled pairs; mean character similarity {sum(ratios)/len(ratios):.3f}; fraction with similarity >= 0.8: {sum(x>=.8 for x in ratios)/len(ratios):.3f}. Pair sampling includes any self-pairs. Similarity is a heuristic, not a language-quality score.\n\nRepresentative examples for inspection:\n\n'+''.join('- '+x+'\n' for x in examples)+'\nManual review: generated connectors and attribute/value combinations are often mechanical, including unnatural category-value matches; low exact duplication does not make these natural conversations. These examples are not human transcripts.\n'
(R/'09_Validation_and_Comparison/dialogue_diversity.md').write_text(s,encoding='utf-8');print(s)
