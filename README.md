# MIRAI reference data package

This is a synthetic comparison reference, not the original study data. Read PROVENANCE.md and the audit first. Python 3.11 or later, standard library only; no API or network required.

From this folder run `python generate_reference.py`, `python 04_Item_Level_Results/calculate_metrics.py`, `python 05_Statistical_Analysis/analyze.py`, `python 09_Validation_and_Comparison/validate_all.py`, and `python 03_Configurations_and_Implementation/run_local_demo.py`. The generator overwrites generated CSVs.

Folders 01–09 contain the manuscript audit, benchmark and personas, configurations/demo, item and trial outcomes, paired statistical analysis, illustrative evaluator audit, public benchmark notes, illustrative overhead, and validation. Compare your files by joining on your own persona/item mapping, checking counts, fields, split membership and formulas; synthetic IDs and values have no identity correspondence to your originals. Reported figures and constructed results are identified separately. Original logs, exact prompts, actual evaluator outputs, and benchmark predictions are needed for independent reproduction.
