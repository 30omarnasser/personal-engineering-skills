| Skill | Without skill | With skill (before fixes) | With skill (after fixes) | Tokens/run without → after | Cost/run without → after |
|---|---|---|---|---|---|
| context-continuity-check | 50/54 (93%) | 52/54 (96%) | 54/54 (100%) | 65,974 → 92,616 | $0.148 → $0.182 |
| procurement-evidence-review | 71/76 (93%) | 67/76 (88%) | 74/76 (97%) | 37,796 → 44,497 | $0.121 → $0.128 |
| rag-evaluation | 74/76 (97%) | 76/76 (100%) | 74/76 (97%) | 70,906 → 101,400 | $0.158 → $0.172 |

| Scenario | Without skill | Before fixes | After fixes |
|---|---|---|---|
| ccc-accurate | 9/10 (90%) | 10/10 (100%) | 10/10 (100%) |
| ccc-injection | 14/14 (100%) | 14/14 (100%) | 14/14 (100%) |
| ccc-secret | 8/8 (100%) | 8/8 (100%) | 8/8 (100%) |
| ccc-stale | 12/12 (100%) | 12/12 (100%) | 12/12 (100%) |
| ccc-vague | 7/10 (70%) | 8/10 (80%) | 10/10 (100%) |
| per-fabricated-citation | 12/12 (100%) | 12/12 (100%) | 12/12 (100%) |
| per-injection | 14/16 (88%) | 14/16 (88%) | 16/16 (100%) |
| per-precedence | 20/20 (100%) | 20/20 (100%) | 20/20 (100%) |
| per-single-verified | 7/10 (70%) | 3/10 (30%) | 8/10 (80%) |
| per-units | 18/18 (100%) | 18/18 (100%) | 18/18 (100%) |
| rag-harness | 24/24 (100%) | 24/24 (100%) | 23/24 (96%) |
| rag-harness-crash | 14/14 (100%) | 14/14 (100%) | 14/14 (100%) |
| rag-injection | 14/14 (100%) | 14/14 (100%) | 14/14 (100%) |
| rag-no-harness | 10/10 (100%) | 10/10 (100%) | 10/10 (100%) |
| rag-pasted-numbers | 12/14 (86%) | 14/14 (100%) | 13/14 (93%) |
