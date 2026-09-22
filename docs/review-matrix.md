# Review matrix

| Requirement | Contract path | Automated proof | Live proof | Status |
| --- | --- | --- | --- | --- |
| Immutable full-SHA sources | `_url`, `open_case`, `submit_revision` | moving ref and foreign host rejection | pending deployment | LOCAL PASS |
| One attributed finding per criterion | `_normalize`, `_inspect` | lifecycle and forged quote tests | pending deployment | LOCAL PASS |
| Validator refetches both sources | `_inspect.validate` | changed snapshot rejection | pending deployment | LOCAL PASS |
| Validator rejects an overstated result | semantic validator | false validator decision test | pending deployment | LOCAL PASS |
| Owner-only revision submission | `submit_revision` | unauthorized caller test | deployed source match | LOCAL PASS |
| Immutable revision history | revision state checks | duplicate and replay tests | pending deployment | LOCAL PASS |

## Mechanism comparison

PatchProof is not a citation audit, generic evidence vault, policy adjudicator, provenance graph, or semantic idempotency key. Its state primitive is a revision stack under one immutable specification. Its consensus question is criterion-by-criterion implementation coverage. Its remediation transition adds a new reviewable revision while preserving every earlier finding.

