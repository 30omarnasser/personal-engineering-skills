# Supply Chain Risk Report — `synthetic`

**Scanned:** `<HOME>\AppData\Local\Temp\claude\5d6096a35e425d74\016e5144-fb6d-4528-97f3-d474144c2932\scratchpad\audit\synthetic`  
**Manifests read:** `requirements.txt`  
**Scanned at:** 2026-11-04T18:56:08+00:00  
**Direct dependencies:** 6 (PyPI 6)

## Summary

- **4 of 6 dependencies have known advisories.** See the findings below.
- Transitive dependencies were **not examined**: no lockfile resolves the transitive tree (package-lock.json, uv.lock, or a go 1.17+ go.mod).
- 4 of 6 dependencies carry at least one finding, 4 of which reach production.
- Weakest coverage: **Install-time script execution**, established for 0 of 6; the Coverage section lists every criterion.

## Production dependencies

6 dependencies are declared as runtime dependencies and ship in the built artifact. Advisory status is given for every one, clean or not.

| Dependency | Version | Advisories | Other findings |
|---|---|---|---|
| `fastapi` | 0.162.0 (latest, not the project's pin) | none known | — |
| `jinja2` | 2.10 | **12 advisories affect the pinned 2.10** | — |
| `nose` | 1.3.7 | none known | — |
| `pyyaml` | 5.3 | **4 advisories affect the pinned 5.3** | — |
| `requests` | 2.19.0 | **10 advisories affect the pinned 2.19.0** | — |
| `urllib3` | 1.24.1 | **26 advisories affect the pinned 1.24.1** | — |

## Findings

### Reaches production

| Dependency | Version | Weekly downloads | Findings |
|---|---|---|---|
| `jinja2` | 2.10 | — | 12 advisories affect the pinned 2.10 |
| `pyyaml` | 5.3 | — | 4 advisories affect the pinned 5.3 |
| `requests` | 2.19.0 | — | 10 advisories affect the pinned 2.19.0 |
| `urllib3` | 1.24.1 | — | 26 advisories affect the pinned 1.24.1 |

## Upstream repository and CI hygiene — OpenSSF Scorecard

These criteria describe each dependency's own repository, not the audited
project. Remediation, where any exists, is upstream.

No dependency was flagged on these criteria.

## Transitive advisories

Not examined: no lockfile resolves the transitive tree (package-lock.json, uv.lock, or a go 1.17+ go.mod). Commit a lockfile to close this gap.

## Informational

Measured, not flagged.

- **CI token permissions**: median 10/10 across 4 scored dependencies; 2 score below 6. Not flagged — this measures whether CI workflows declare least-privilege tokens, which tracks project maturity rather than the likelihood of malicious code being published.
- **Changes reviewed by a second person**: median 8/10 across 4 scored dependencies; 2 score below 6. Not flagged — this measures the share of recent commits reviewed by a second person, which is low for most small single-maintainer projects and largely restates publisher concentration.
- **Publish provenance**: not determinable for any dependency in this project.
- **Security policy published**: 5 of 5 publish a security policy.
- **Download volume**: not determinable for any dependency in this project.

## Coverage

What was and was not measured, per criterion.

| Criterion | Tier | Assessed | Flagged | Not assessable |
|---|---|---|---|---|
| Known advisories | A | 6/6 | 4 | 0 |
| Deprecated or yanked | A | 6/6 | 0 | 0 |
| Repository archived | A | 5/6 | 0 | 1 |
| Maintenance activity | A | 5/6 | 0 | 1 |
| Publisher concentration | B | 0/6 | 0 | 6 |
| Install-time script execution | B | 0/6 | 0 | 6 |
| Dangerous CI workflow | scorecard | 4/6 | 0 | 2 |
| CI token permissions | scorecard | 4/6 | 0 | 2 |
| Checked-in binaries | scorecard | 4/6 | 0 | 2 |
| Changes reviewed by a second person | scorecard | 4/6 | 0 | 2 |
| Publish provenance | info | 0/6 | 0 | 6 |
| Security policy published | info | 5/6 | 0 | 1 |
| Download volume | info | 0/6 | 0 | 6 |

## Not assessable

**Repository archived**

- 1 dependency — no source repository could be resolved for this package: `nose`

**Checked-in binaries**

- 1 dependency — OpenSSF Scorecard has no report for this repository: `fastapi`
- 1 dependency — no source repository to score: `nose`

**Changes reviewed by a second person**

- 1 dependency — OpenSSF Scorecard has no report for this repository: `fastapi`
- 1 dependency — no source repository to score: `nose`

**Dangerous CI workflow**

- 1 dependency — OpenSSF Scorecard has no report for this repository: `fastapi`
- 1 dependency — no source repository to score: `nose`

**Download volume**

- 6 dependencies — PyPI's download counters are disabled and return -1: `fastapi`, `jinja2`, `nose`, `pyyaml`, `requests`, `urllib3`

**Install-time script execution**

- 6 dependencies — install-time execution depends on whether a wheel or an sdist is installed, which this collector does not determine: `fastapi`, `jinja2`, `nose`, `pyyaml`, `requests`, `urllib3`

**Publish provenance**

- 6 dependencies — PyPI publish attestations are not read by this collector: `fastapi`, `jinja2`, `nose`, `pyyaml`, `requests`, `urllib3`

**Publisher concentration**

- 6 dependencies — PyPI publishes no upload ACL, so who can publish this package is not observable: `fastapi`, `jinja2`, `nose`, `pyyaml`, `requests`, `urllib3`

**Security policy published**

- 1 dependency — no source repository could be resolved for this package: `nose`

**Maintenance activity**

- 1 dependency — no source repository could be resolved for this package: `nose`

**CI token permissions**

- 1 dependency — OpenSSF Scorecard has no report for this repository: `fastapi`
- 1 dependency — no source repository to score: `nose`

## Method and caveats

- cache directory ownership was not verified: os.getuid is POSIX-only, so a cache at <HOME>\AppData\Local\Temp\claude\5d6096a35e425d74\016e5144-fb6d-4528-97f3-d474144c2932\scratchpad\audit\cache owned by another user would not be detected on this platform. Keep the cache under your own user profile, or pass --cache with a private path.
- 1 dependencies are specified as a version range with no lockfile, so their advisories were matched against the current latest release rather than against what this project installs — commit a lockfile for an exact answer: fastapi
- Optional tooling detected: npm. Not installed, so not used: bundler-audit, cargo-audit, osv-scanner, pip-audit.
- Direct dependencies only. Advisories attach to the package that ships the affected code, so an umbrella package can look clean while its components are not — rails 5.0.0 reports 0 advisories where actionpack 5.0.0 reports 10. Transitive dependencies were not examined: no lockfile resolves the transitive tree (package-lock.json, uv.lock, or a go 1.17+ go.mod).
- HTTP sources: 22 fetched, 6 served from cache (oldest 0.0h old), 0 refetched as stale, 0 unavailable offline, 0 errors.
