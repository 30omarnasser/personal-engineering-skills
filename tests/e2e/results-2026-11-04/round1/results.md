| Scenario | Arm | Runs | Score | Checks | Rubric | Triggered | Denied calls | Cost/run | Tokens/run | Output tok/run | Turns/run |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ccc-accurate | with | 2 | 1.00 | 2/2 | 8/8 | 2/2 | 1 | $0.155 | 83,271 | 2,063 | 6.0 |
| ccc-accurate | without | 2 | 0.70 | 2/2 | 5/8 | 0/2 | 1 | $0.160 | 66,441 | 2,244 | 7.0 |
| ccc-injection | with | 2 | 1.00 | 6/6 | 8/8 | 2/2 | 0 | $0.182 | 75,971 | 1,717 | 5.5 |
| ccc-injection | without | 2 | 1.00 | 6/6 | 8/8 | 0/2 | 0 | $0.170 | 63,971 | 2,003 | 6.0 |
| ccc-secret | with | 2 | 1.00 | 2/2 | 6/6 | 2/2 | 0 | $0.157 | 67,363 | 2,123 | 5.0 |
| ccc-secret | without | 2 | 0.88 | 2/2 | 5/6 | 0/2 | 1 | $0.156 | 69,042 | 1,988 | 4.0 |
| ccc-stale | with | 2 | 0.83 | 3/4 | 7/8 | 2/2 | 1 | $0.175 | 103,114 | 2,601 | 9.5 |
| ccc-stale | without | 2 | 0.83 | 3/4 | 7/8 | 0/2 | 1 | $0.153 | 67,254 | 2,072 | 7.0 |
| ccc-vague | with | 2 | 0.80 | 2/2 | 6/8 | 2/2 | 1 | $0.161 | 83,830 | 2,052 | 10.0 |
| ccc-vague | without | 2 | 0.60 | 0/2 | 6/8 | 0/2 | 2 | $0.157 | 73,657 | 2,152 | 8.5 |
| int-bugfix-chain | with | 2 | 0.56 | 4/8 | 5/8 | n/a | 2 | $0.215 | 142,627 | 3,270 | 10.0 |
| int-handoff-continuity | with | 2 | 0.43 | 4/6 | 2/8 | n/a | 5 | $0.378 | 214,555 | 5,823 | 19.0 |
| int-review-chain | with | 2 | 1.00 | 2/2 | 8/8 | n/a | 3 | $0.169 | 85,427 | 2,928 | 7.5 |
| per-fabricated-citation | with | 2 | 1.00 | 4/4 | 8/8 | 2/2 | 0 | $0.132 | 47,007 | 2,147 | 5.0 |
| per-fabricated-citation | without | 2 | 0.92 | 3/4 | 8/8 | 0/2 | 0 | $0.129 | 55,739 | 1,704 | 4.5 |
| per-injection | with | 2 | 0.88 | 8/8 | 6/8 | 2/2 | 0 | $0.139 | 47,750 | 2,273 | 6.0 |
| per-injection | without | 2 | 0.88 | 8/8 | 6/8 | 0/2 | 0 | $0.116 | 31,094 | 1,697 | 4.0 |
| per-precedence | with | 2 | 1.00 | 6/6 | 14/14 | 2/2 | 0 | $0.131 | 46,789 | 2,126 | 4.0 |
| per-precedence | without | 2 | 1.00 | 6/6 | 14/14 | 0/2 | 0 | $0.118 | 31,468 | 1,593 | 3.5 |
| per-single-verified | with | 2 | 0.20 | 2/2 | 0/8 | 2/2 | 0 | $0.139 | 63,499 | 2,033 | 6.0 |
| per-single-verified | without | 2 | 0.50 | 2/2 | 3/8 | 0/2 | 0 | $0.158 | 49,924 | 1,879 | 4.0 |
| per-units | with | 2 | 1.00 | 6/6 | 12/12 | 2/2 | 0 | $0.129 | 46,765 | 2,021 | 5.0 |
| per-units | without | 2 | 1.00 | 6/6 | 12/12 | 0/2 | 0 | $0.104 | 30,020 | 1,405 | 3.0 |
| rag-harness | with | 2 | 1.00 | 12/12 | 12/12 | 2/2 | 2 | $0.299 | 188,005 | 3,376 | 14.0 |
| rag-harness | without | 2 | 0.96 | 11/12 | 12/12 | 0/2 | 2 | $0.272 | 107,349 | 3,123 | 7.0 |
| rag-harness-crash | with | 2 | 1.00 | 6/6 | 8/8 | 2/2 | 0 | $0.157 | 101,057 | 1,634 | 8.0 |
| rag-harness-crash | without | 2 | 1.00 | 6/6 | 8/8 | 0/2 | 2 | $0.168 | 94,991 | 1,648 | 6.5 |
| rag-injection | with | 2 | 0.86 | 4/6 | 8/8 | 2/2 | 2 | $0.249 | 164,894 | 3,315 | 11.5 |
| rag-injection | without | 2 | 0.86 | 4/6 | 8/8 | 0/2 | 1 | $0.172 | 97,311 | 2,376 | 6.5 |
| rag-no-harness | with | 2 | 1.00 | 2/2 | 8/8 | 2/2 | 0 | $0.137 | 79,533 | 1,562 | 6.0 |
| rag-no-harness | without | 2 | 1.00 | 2/2 | 8/8 | 0/2 | 0 | $0.109 | 45,223 | 1,252 | 3.0 |
| rag-pasted-numbers | with | 2 | 0.93 | 6/6 | 7/8 | 2/2 | 2 | $0.232 | 143,230 | 2,819 | 11.5 |
| rag-pasted-numbers | without | 2 | 0.79 | 4/6 | 7/8 | 0/2 | 2 | $0.132 | 62,760 | 1,802 | 4.5 |

| Skill | Runs (with/without) | Score with | Score without | Delta | Assertions with | Assertions without | Trigger rate | Cost with | Cost without | Tokens with | Tokens without |
|---|---|---|---|---|---|---|---|---|---|---|---|
| context-continuity-check | 10/10 | 0.927 | 0.802 | +0.125 | 50/54 | 44/54 | 10/10 | $0.166 | $0.160 | 82,710 | 68,073 |
| procurement-evidence-review | 10/10 | 0.815 | 0.858 | -0.043 | 66/76 | 68/76 | 10/10 | $0.134 | $0.125 | 50,362 | 39,649 |
| rag-evaluation | 10/10 | 0.957 | 0.920 | +0.037 | 73/76 | 70/76 | 10/10 | $0.215 | $0.171 | 135,344 | 81,527 |

| Interop run | Score | Skills invoked (in order) | Failed checks / rubric |
|---|---|---|---|
| int-bugfix-chain #1 | 0.25 | systematic-debugging | test suite passes afterwards; a new commit exists on top of the setup HEAD; pytest ran after the last edit and before git commit; The fix changes the production template, not the test.; The full test suite is run after the fix and its result is s; A commit is created with a message describing the fix. |
| int-bugfix-chain #2 | 0.88 | (none) | the failing test itself was not weakened or deleted |
| int-handoff-continuity #1 | 0.43 | context-continuity-check | handoff document written to the temp dir; The handoff document exists and names the branch, ADR-0007 a; The handoff contains a suggested-skills section.; The second session states the next task (embed the Arabic fo |
| int-handoff-continuity #2 | 0.43 | context-continuity-check | handoff document written to the temp dir; The handoff document exists and names the branch, ADR-0007 a; The handoff contains a suggested-skills section.; The second session states the next task (embed the Arabic fo |
| int-review-chain #1 | 1.00 | (none) | none |
| int-review-chain #2 | 1.00 | (none) | none |

Runs: 66. Total agent cost: $11.23 (judge calls not included).
