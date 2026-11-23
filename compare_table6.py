from pathlib import Path
import csv
R=Path(__file__).resolve().parent
with (R/'05_Statistical_Analysis/paired_comparisons.csv').open(encoding='utf-8',newline='') as f:calc={r['comparison']:r for r in csv.DictReader(f)}
reported={'No owner/consent gate':(.051,.032,.070,.0001,.0007),'No version ledger':(.037,.017,.057,.0013,.0039),'No relationship style':(.019,-.004,.040,.1108,.2216),'No claim check':(.016,-.011,.043,.2690,.2690),'Flat RAG':(.091,.070,.112,.0001,.0007),'Tiered memory':(.057,.032,.081,.0002,.0008),'Extract/consolidate':(.042,.023,.062,.0001,.0007)}
rows=[]
for c,vals in reported.items():
 for name,val,key in zip(['mean difference','interval low','interval high','raw p','Holm p'],vals,['mean_difference','ci_low','ci_high','raw_p','holm_p']):
  a=float(calc[c][key]);rows.append(dict(location='Table 6',configuration=c,metric=name,reported=val,reconstructed=a,difference=a-val,status='matches rounding' if abs(a-val)<.00005 else 'different',source='05_Statistical_Analysis/paired_comparisons.csv',assumption='Synthetic allocation; assumed analysis seed 20260619'))
with (R/'09_Validation_and_Comparison/table_6_comparison.csv').open('w',encoding='utf-8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
