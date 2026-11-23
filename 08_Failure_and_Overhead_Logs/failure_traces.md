# Reconstructed failure traces and overhead

Table 8 cases are transcribed in failure_cases.csv; they are manuscript examples, not recovered logs. The following possible traces illustrate mechanisms; retrieval order and intermediate checker results are assumptions.

- U-017: eligible R114 (old tea, superseded) and R287 (current coffee). Faulty order R114 then R287; draft claim tea; checker incorrectly treats tea as supported due to unresolved supersession; no rewrite; final tea; expected coffee; identity v4. The exact retrieved ranking is not published.
- S-031: R442 belongs to Amir, not the target. A speaker-resolution fault admits it and yields a 2023 claim; checker erroneously accepts it; final 2023; expected abstention; identity v6. Exact intermediate steps are inferred.
- A-009: inventory contains no cat record. Draft Milo; extractor misses the possessive pet-name claim; checker sees no extracted personal claim and passes; final Milo; expected abstention; identity v2.

Table 9 summary is in reported_overhead.csv. No per-response timings are available; logging schema below is a suggestion, not a claim of measurement. Mean latency = sum(duration_seconds)/n; nearest-rank P95 = sorted durations[ceil(.95*n)-1]; input/output means = sums/n. Other quantile definitions may differ. Logs should contain response_id, configuration, start/end, stage, duration_seconds, input_tokens, output_tokens, provenance, model and timestamp. Include conditional rewrites and embedding operations separately to avoid misrepresenting total cost.
