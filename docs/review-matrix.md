# Review matrix

| Requirement | Contract path | Automated proof | Live proof | Status |
| --- | --- | --- | --- | --- |
| Immutable full-SHA sources | `_url`, `open_case`, `submit_revision` | moving ref and foreign host rejection | two source receipts stored | PASS |
| One attributed finding per criterion | `_normalize`, `_inspect` | lifecycle and forged quote tests | finalized READY result with two quotes | PASS |
| Validators independently fetch both sources | `_inspect.fetch_sources` under `strict_eq` | PASS: receipt-mismatched snapshot rejected through `inspect_revision` | PASS: finalized inspection stores two verified receipts | PASS |
| Validator checks every state and quote | `_normalize` plus `prompt_non_comparative` over frozen source bodies | PASS: unsupported but well-shaped `MET` rejected through `inspect_revision` | PASS: live READY result contains two attributed MET findings | PASS |
| Source-driven prompt injection fails closed | producer and validator untrusted-evidence rules | PASS: injected instruction rejected through `inspect_revision` | PASS: deployed reviewed source matches locally | PASS |
| Owner-only revision submission | `submit_revision` | unauthorized caller test | deployed source match | PASS |
| Immutable revision history | revision state checks | duplicate and replay tests | finalized open, submit, inspect lifecycle | PASS |

## Mechanism comparison

PatchProof is not a citation audit, generic evidence vault, policy adjudicator, provenance graph, or semantic idempotency key. Its state primitive is a revision stack under one immutable specification. Its consensus question is criterion-by-criterion implementation coverage. Its remediation transition adds a new reviewable revision while preserving every earlier finding.
