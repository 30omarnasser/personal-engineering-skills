# Supply Chain Risk Report — `library-deps`

**Scanned:** `<HOME>\AppData\Local\Temp\claude\5d6096a35e425d74\016e5144-fb6d-4528-97f3-d474144c2932\scratchpad\audit\library-deps`  
**Manifests read:** `requirements.txt`  
**Scanned at:** 2026-11-04T18:57:03+00:00  
**Direct dependencies:** 10 (PyPI 10)

## Summary

- **No known advisory affects any of the 10 direct dependencies** — but 10 of them were not checked at a project-resolved version (latest-release fallback or go.mod minimum; see Method and caveats).
- Transitive dependencies were **not examined**: no lockfile resolves the transitive tree (package-lock.json, uv.lock, or a go 1.17+ go.mod).
- 1 of 10 dependencies carry at least one finding, 1 of which reaches production.
- Weakest coverage: **Install-time script execution**, established for 0 of 10; the Coverage section lists every criterion.

## Production dependencies

10 dependencies are declared as runtime dependencies and ship in the built artifact. Advisory status is given for every one, clean or not.

| Dependency | Version | Advisories | Other findings |
|---|---|---|---|
| `accelerate` | 1.15.0 (latest, not the project's pin) | none known | — |
| `inspect-ai` | 0.3.287 (latest, not the project's pin) | none known | — |
| `inspect-evals` | 0.27.0 (latest, not the project's pin) | none known | — |
| `lighteval` | 0.13.0 (latest, not the project's pin) | none known | — |
| `openai` | 3.45.0 (latest, not the project's pin) | none known | — |
| `pytest` | 9.2.0 (latest, not the project's pin) | none known | — |
| `pyyaml` | 6.0.3 (latest, not the project's pin) | none known | — |
| `torch` | 2.15.0 (latest, not the project's pin) | none known | — |
| `transformers` | 5.22.1 (latest, not the project's pin) | none known | — |
| `vllm` | 0.33.0 (latest, not the project's pin) | none known | — |

## Findings

No dependency was flagged on these criteria.

## Upstream repository and CI hygiene — OpenSSF Scorecard

These criteria describe each dependency's own repository, not the audited
project. Remediation, where any exists, is upstream.

### Reaches production

| Dependency | Version | Weekly downloads | Findings |
|---|---|---|---|
| `torch` | 2.15.0 (latest, not the project's pin) | — | Binary-Artifacts scores 9/10 (below 10) |

## Transitive advisories

Not examined: no lockfile resolves the transitive tree (package-lock.json, uv.lock, or a go 1.17+ go.mod). Commit a lockfile to close this gap.

## Informational

Measured, not flagged.

- **CI token permissions**: median 0/10 across 5 scored dependencies; 3 score below 6. Not flagged — this measures whether CI workflows declare least-privilege tokens, which tracks project maturity rather than the likelihood of malicious code being published.
- **Changes reviewed by a second person**: median 9/10 across 6 scored dependencies; 1 score below 6. Not flagged — this measures the share of recent commits reviewed by a second person, which is low for most small single-maintainer projects and largely restates publisher concentration.
- **Publish provenance**: not determinable for any dependency in this project.
- **Security policy published**: 8 of 10 publish a security policy.
  Without: `inspect-evals`, `lighteval`
- **Download volume**: not determinable for any dependency in this project.

## Coverage

What was and was not measured, per criterion.

| Criterion | Tier | Assessed | Flagged | Not assessable |
|---|---|---|---|---|
| Known advisories | A | 10/10 | 0 | 0 |
| Deprecated or yanked | A | 10/10 | 0 | 0 |
| Repository archived | A | 10/10 | 0 | 0 |
| Maintenance activity | A | 10/10 | 0 | 0 |
| Publisher concentration | B | 0/10 | 0 | 10 |
| Install-time script execution | B | 0/10 | 0 | 10 |
| Dangerous CI workflow | scorecard | 6/10 | 0 | 4 |
| CI token permissions | scorecard | 5/10 | 0 | 5 |
| Checked-in binaries | scorecard | 6/10 | 1 | 4 |
| Changes reviewed by a second person | scorecard | 6/10 | 0 | 4 |
| Publish provenance | info | 0/10 | 0 | 10 |
| Security policy published | info | 10/10 | 0 | 0 |
| Download volume | info | 0/10 | 0 | 10 |

## Not assessable

**Checked-in binaries**

- 4 dependencies — OpenSSF Scorecard has no report for this repository: `inspect-ai`, `inspect-evals`, `lighteval`, `vllm`

**Changes reviewed by a second person**

- 4 dependencies — OpenSSF Scorecard has no report for this repository: `inspect-ai`, `inspect-evals`, `lighteval`, `vllm`

**Dangerous CI workflow**

- 4 dependencies — OpenSSF Scorecard has no report for this repository: `inspect-ai`, `inspect-evals`, `lighteval`, `vllm`

**Download volume**

- 10 dependencies — PyPI's download counters are disabled and return -1: `accelerate`, `inspect-ai`, `inspect-evals`, `lighteval`, `openai`, `pytest` and 4 more

**Install-time script execution**

- 10 dependencies — install-time execution depends on whether a wheel or an sdist is installed, which this collector does not determine: `accelerate`, `inspect-ai`, `inspect-evals`, `lighteval`, `openai`, `pytest` and 4 more

**Publish provenance**

- 10 dependencies — PyPI publish attestations are not read by this collector: `accelerate`, `inspect-ai`, `inspect-evals`, `lighteval`, `openai`, `pytest` and 4 more

**Publisher concentration**

- 10 dependencies — PyPI publishes no upload ACL, so who can publish this package is not observable: `accelerate`, `inspect-ai`, `inspect-evals`, `lighteval`, `openai`, `pytest` and 4 more

**CI token permissions**

- 4 dependencies — OpenSSF Scorecard has no report for this repository: `inspect-ai`, `inspect-evals`, `lighteval`, `vllm`
- 1 dependency — Scorecard could not evaluate Token-Permissions (score -1): `torch`

## Method and caveats

- cache directory ownership was not verified: os.getuid is POSIX-only, so a cache at <HOME>\AppData\Local\Temp\claude\5d6096a35e425d74\016e5144-fb6d-4528-97f3-d474144c2932\scratchpad\audit\cache owned by another user would not be detected on this platform. Keep the cache under your own user profile, or pass --cache with a private path.
- 10 dependencies are specified as a version range with no lockfile, so their advisories were matched against the current latest release rather than against what this project installs — commit a lockfile for an exact answer: accelerate, inspect-ai, inspect-evals, lighteval, openai, pytest, pyyaml, torch ...
- Optional tooling detected: npm. Not installed, so not used: bundler-audit, cargo-audit, osv-scanner, pip-audit.
- Direct dependencies only. Advisories attach to the package that ships the affected code, so an umbrella package can look clean while its components are not — rails 5.0.0 reports 0 advisories where actionpack 5.0.0 reports 10. Transitive dependencies were not examined: no lockfile resolves the transitive tree (package-lock.json, uv.lock, or a go 1.17+ go.mod).
- HTTP sources: 31 fetched, 15 served from cache (oldest 0.0h old), 0 refetched as stale, 0 unavailable offline, 0 errors.
