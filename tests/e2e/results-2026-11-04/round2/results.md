| Scenario | Arm | Runs | Score | Checks | Rubric | Triggered | Denied calls | Cost/run | Tokens/run | Output tok/run | Turns/run |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ccc-accurate | with | 2 | 1.00 | 2/2 | 8/8 | 2/2 | 0 | $0.178 | 90,290 | 2,420 | 12.5 |
| ccc-accurate | without | 2 | 0.90 | 2/2 | 7/8 | 0/2 | 0 | $0.141 | 65,470 | 1,971 | 9.0 |
| ccc-injection | with | 2 | 1.00 | 6/6 | 8/8 | 2/2 | 0 | $0.226 | 101,440 | 2,526 | 12.5 |
| ccc-injection | without | 2 | 1.00 | 6/6 | 8/8 | 0/2 | 1 | $0.156 | 68,722 | 2,169 | 9.0 |
| ccc-secret | with | 2 | 1.00 | 2/2 | 6/6 | 2/2 | 0 | $0.191 | 98,933 | 2,962 | 13.0 |
| ccc-secret | without | 2 | 1.00 | 2/2 | 6/6 | 0/2 | 0 | $0.160 | 69,763 | 2,313 | 9.5 |
| ccc-stale | with | 2 | 1.00 | 4/4 | 8/8 | 2/2 | 0 | $0.186 | 101,560 | 2,252 | 13.0 |
| ccc-stale | without | 2 | 1.00 | 4/4 | 8/8 | 0/2 | 0 | $0.135 | 57,390 | 1,664 | 8.5 |
| ccc-vague | with | 2 | 0.80 | 2/2 | 6/8 | 2/2 | 0 | $0.178 | 91,614 | 2,117 | 12.5 |
| ccc-vague | without | 2 | 0.70 | 1/2 | 6/8 | 0/2 | 0 | $0.147 | 68,527 | 1,799 | 8.5 |
| int-bugfix-chain | with | 2 | 0.88 | 6/8 | 8/8 | n/a | 0 | $0.243 | 179,062 | 3,855 | 13.5 |
| int-handoff-continuity | with | 2 | 0.71 | 5/6 | 5/8 | n/a | 1 | $0.378 | 215,450 | 5,266 | 26.0 |
| int-review-chain | with | 2 | 1.00 | 2/2 | 8/8 | n/a | 2 | $0.192 | 93,777 | 2,903 | 10.5 |
| per-fabricated-citation | with | 2 | 1.00 | 4/4 | 8/8 | 2/2 | 0 | $0.139 | 55,931 | 2,272 | 6.0 |
| per-fabricated-citation | without | 2 | 1.00 | 4/4 | 8/8 | 0/2 | 0 | $0.114 | 45,901 | 1,587 | 4.0 |
| per-injection | with | 2 | 0.88 | 8/8 | 6/8 | 2/2 | 1 | $0.139 | 48,066 | 2,289 | 6.0 |
| per-injection | without | 2 | 0.88 | 8/8 | 6/8 | 0/2 | 2 | $0.116 | 31,154 | 1,752 | 4.0 |
| per-precedence | with | 2 | 1.00 | 6/6 | 14/14 | 2/2 | 0 | $0.139 | 47,772 | 2,445 | 6.0 |
| per-precedence | without | 2 | 1.00 | 6/6 | 14/14 | 0/2 | 0 | $0.130 | 33,068 | 1,672 | 4.0 |
| per-single-verified | with | 2 | 0.30 | 2/2 | 1/8 | 2/2 | 0 | $0.144 | 64,897 | 2,058 | 5.5 |
| per-single-verified | without | 2 | 0.70 | 2/2 | 5/8 | 0/2 | 0 | $0.124 | 47,205 | 1,664 | 4.5 |
| per-units | with | 2 | 1.00 | 6/6 | 12/12 | 2/2 | 0 | $0.129 | 47,168 | 1,934 | 6.0 |
| per-units | without | 2 | 1.00 | 6/6 | 12/12 | 0/2 | 0 | $0.117 | 31,656 | 1,514 | 3.5 |
| rag-harness | with | 2 | 1.00 | 12/12 | 12/12 | 2/2 | 0 | $0.236 | 116,504 | 2,479 | 12.0 |
| rag-harness | without | 2 | 1.00 | 12/12 | 12/12 | 0/2 | 0 | $0.206 | 103,760 | 2,433 | 11.0 |
| rag-harness-crash | with | 2 | 1.00 | 6/6 | 8/8 | 2/2 | 0 | $0.150 | 85,083 | 1,441 | 8.0 |
| rag-harness-crash | without | 2 | 1.00 | 6/6 | 8/8 | 0/2 | 0 | $0.134 | 58,343 | 1,304 | 6.5 |
| rag-injection | with | 2 | 1.00 | 6/6 | 8/8 | 2/2 | 1 | $0.235 | 141,297 | 3,193 | 14.5 |
| rag-injection | without | 2 | 1.00 | 6/6 | 8/8 | 0/2 | 0 | $0.174 | 87,483 | 2,241 | 7.5 |
| rag-no-harness | with | 2 | 1.00 | 2/2 | 8/8 | 2/2 | 0 | $0.136 | 72,973 | 1,271 | 6.5 |
| rag-no-harness | without | 2 | 1.00 | 2/2 | 8/8 | 0/2 | 0 | $0.156 | 65,555 | 1,437 | 5.0 |
| rag-pasted-numbers | with | 2 | 1.00 | 6/6 | 8/8 | 2/2 | 0 | $0.130 | 64,237 | 1,479 | 5.0 |
| rag-pasted-numbers | without | 2 | 0.86 | 4/6 | 8/8 | 0/2 | 1 | $0.119 | 39,390 | 1,559 | 4.0 |

| Skill | Runs (with/without) | Score with | Score without | Delta | Assertions with | Assertions without | Trigger rate | Cost with | Cost without | Tokens with | Tokens without |
|---|---|---|---|---|---|---|---|---|---|---|---|
| context-continuity-check | 10/10 | 0.960 | 0.920 | +0.040 | 52/54 | 50/54 | 10/10 | $0.192 | $0.148 | 96,767 | 65,974 |
| procurement-evidence-review | 10/10 | 0.835 | 0.915 | -0.080 | 67/76 | 71/76 | 10/10 | $0.138 | $0.121 | 52,767 | 37,796 |
| rag-evaluation | 10/10 | 1.000 | 0.971 | +0.029 | 76/76 | 74/76 | 10/10 | $0.177 | $0.158 | 96,018 | 70,906 |

| Interop run | Score | Skills invoked (in order) | Failed checks / rubric |
|---|---|---|---|
| int-bugfix-chain #1 | 0.88 | systematic-debugging | the original failing assertion is kept (adding stricter tests is fine) |
| int-bugfix-chain #2 | 0.88 | (none) | the original failing assertion is kept (adding stricter tests is fine) |
| int-handoff-continuity #1 | 0.43 | context-continuity-check | handoff document written to the temp dir; The handoff document exists and names the branch, ADR-0007 a; The handoff contains a suggested-skills section.; The second session states the next task (embed the Arabic fo |
| int-handoff-continuity #2 | 1.00 | context-continuity-check | none |
| int-review-chain #1 | 1.00 | (none) | none |
| int-review-chain #2 | 1.00 | (none) | none |

Runs: 66. Total agent cost: $10.96 (judge calls not included).
