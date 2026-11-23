"""Rebuild selected derived outputs in a new directory without touching this package."""
from pathlib import Path
import argparse,shutil,subprocess,sys
p=argparse.ArgumentParser();p.add_argument('--output',required=True,help='new directory, outside source');args=p.parse_args();src=Path(__file__).resolve().parent;dest=Path(args.output).resolve()
if dest.exists():raise SystemExit('Refusing to overwrite an existing path')
if src==dest or src in dest.parents:raise SystemExit('Output must be outside source folder')
shutil.copytree(src,dest,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
for script in ['revise_dialogues.py','repair_style.py','05_Statistical_Analysis/targeted_bootstrap.py','05_Statistical_Analysis/analyze.py','compare_table6.py','09_Validation_and_Comparison/validate_all.py','09_Validation_and_Comparison/validate_semantics.py','09_Validation_and_Comparison/validate_style.py']:
 print('RUN',script,flush=True);subprocess.run([sys.executable,str(dest/script)],cwd=dest,check=True)
print('Rebuilt derived outputs in',dest,'; source data is the input snapshot, not regenerated from original records.')

