| Scenario | Arm | Runs | Score | Checks | Rubric | Triggered | Denied calls | Cost/run | Tokens/run | Output tok/run | Turns/run |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ccc-accurate | with | 2 | 1.00 | 2/2 | 8/8 | 2/2 | 0 | $0.183 | 91,716 | 2,263 | 13.5 |
| ccc-injection | with | 2 | 1.00 | 6/6 | 8/8 | 2/2 | 0 | $0.180 | 92,498 | 2,228 | 12.0 |
| ccc-secret | with | 2 | 1.00 | 2/2 | 6/6 | 2/2 | 0 | $0.186 | 93,171 | 2,436 | 14.0 |
| ccc-stale | with | 2 | 1.00 | 4/4 | 8/8 | 2/2 | 0 | $0.179 | 92,606 | 2,178 | 12.5 |
| ccc-vague | with | 2 | 1.00 | 2/2 | 8/8 | 2/2 | 0 | $0.183 | 93,093 | 2,259 | 13.0 |
| int-bugfix-chain | with | 2 | 1.00 | 8/8 | 8/8 | n/a | 0 | $0.253 | 162,348 | 4,335 | 13.0 |
| int-handoff-continuity | with | 2 | 1.00 | 6/6 | 8/8 | n/a | 3 | $0.394 | 218,151 | 5,824 | 27.0 |
| int-review-chain | with | 2 | 1.00 | 2/2 | 8/8 | n/a | 2 | $0.187 | 103,569 | 2,629 | 10.5 |
| per-fabricated-citation | with | 2 | 1.00 | 4/4 | 8/8 | 2/2 | 0 | $0.130 | 47,636 | 1,910 | 5.0 |
| per-injection | with | 2 | 1.00 | 8/8 | 8/8 | 2/2 | 1 | $0.143 | 48,748 | 2,346 | 6.0 |
| per-precedence | with | 2 | 1.00 | 6/6 | 14/14 | 2/2 | 0 | $0.128 | 47,611 | 1,816 | 6.0 |
| per-single-verified | with | 2 | 0.80 | 2/2 | 6/8 | 2/2 | 0 | $0.110 | 30,888 | 1,504 | 3.0 |
| per-units | with | 2 | 1.00 | 6/6 | 12/12 | 2/2 | 0 | $0.128 | 47,601 | 1,823 | 5.0 |
| rag-harness | with | 2 | 0.96 | 12/12 | 11/12 | 2/2 | 0 | $0.231 | 148,275 | 2,656 | 13.0 |
| rag-harness-crash | with | 2 | 1.00 | 6/6 | 8/8 | 2/2 | 0 | $0.152 | 93,294 | 1,477 | 8.0 |
| rag-injection | with | 2 | 1.00 | 6/6 | 8/8 | 2/2 | 0 | $0.216 | 128,851 | 2,956 | 12.5 |
| rag-no-harness | with | 2 | 1.00 | 2/2 | 8/8 | 2/2 | 0 | $0.117 | 61,685 | 1,259 | 6.5 |
| rag-pasted-numbers | with | 2 | 0.93 | 6/6 | 7/8 | 2/2 | 0 | $0.144 | 74,897 | 1,557 | 5.5 |

| Skill | Runs (with/without) | Score with | Score without | Delta | Assertions with | Assertions without | Trigger rate | Cost with | Cost without | Tokens with | Tokens without |
|---|---|---|---|---|---|---|---|---|---|---|---|

| Interop run | Score | Skills invoked (in order) | Failed checks / rubric |
|---|---|---|---|
| int-bugfix-chain #1 | 1.00 | (none) | none |
| int-bugfix-chain #2 | 1.00 | systematic-debugging | none |
| int-handoff-continuity #1 | 1.00 | context-continuity-check | none |
| int-handoff-continuity #2 | 1.00 | context-continuity-check | none |
| int-review-chain #1 | 1.00 | (none) | none |
| int-review-chain #2 | 1.00 | (none) | none |

Runs: 36. Total agent cost: $6.49 (judge calls not included).
