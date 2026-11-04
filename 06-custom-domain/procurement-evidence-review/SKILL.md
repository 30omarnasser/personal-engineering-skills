---
name: procurement-evidence-review
description: Use when reviewing tender, RFQ, datasheet or procurement-analysis output before it reaches a customer or quote — checks every finding is traced to a source, applicability is explicit, and nothing is concluded without evidence.
---

# Procurement Evidence Review

**Status: DRAFT — refine with skill-creator against real tender outputs before trusting it.**

## When to use
- An agent or pipeline has extracted requirements from a tender / RFQ / spec sheet
- A product match, compliance table or technical offer is about to be sent
- NOT for: general code review, free-form research questions

## Procedure
1. **Inventory findings.** List every requirement, match or conclusion in the output as a numbered table.
2. **Trace each to source.** For each finding record: document, page/section/clause, exact quoted text (short). No source → mark `UNSUPPORTED`.
3. **Set applicability state** — exactly one of: `APPLIES`, `DOES NOT APPLY`, `CONDITIONAL (state condition)`, `UNKNOWN`.
4. **Check exceptions and precedence.** Look for clauses that override the cited one (special conditions, addenda, later revisions, "unless otherwise stated"). Precedence order must be stated, not assumed.
5. **Check units, tolerances, standards.** Unit conversions, IEC/IP/ATEX ratings, voltage/frequency, standard editions. Recompute any derived number.
6. **Flag gaps.** Requirements in the source that the output missed.
7. **Report.**

## Output format
| # | Finding | Source (doc / clause) | Applicability | Exceptions checked | Result |
|---|---------|-----------------------|---------------|--------------------|--------|

Result ∈ `VERIFIED`, `UNSUPPORTED`, `CONTRADICTED`, `NEEDS HUMAN`.
End with: counts per result, missed requirements, and a single go / no-go line.

## Success condition
Every finding has a source reference, an explicit applicability state and a validation result. Zero findings left as "looks right".
