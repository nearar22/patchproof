# Steward remediation: independent evidence validation

| Steward concern | Contract path | Automated proof | Deployment proof | Status |
| --- | --- | --- | --- | --- |
| Validators independently obtain both pinned source bodies. | `_inspect.fetch_sources` runs inside `strict_eq`; every validator fetches both immutable URLs. | PASS: public `inspect_revision` lifecycle and boundary tests cross the consensus path. | PASS: deployed source is a byte-for-byte match. | PASS |
| Both SHA-256 receipts are recomputed and bound to the agreed bodies. | The contract recomputes each digest after `strict_eq` and creates receipts only from that verified snapshot. | PASS: receipt mismatch fails closed. | PASS: live result stores two 64-character receipts. | PASS |
| Every state and quote is checked against the evidence. | `_normalize` proves quote attribution; `prompt_non_comparative` checks the semantic state for every ordered criterion against the frozen bodies. | PASS: unsupported but well-shaped `MET` fails at the semantic boundary. | PASS: live result has one attributed finding per criterion. | PASS |
| Source text cannot instruct the reviewer. | Producer and validator treat source bodies as untrusted evidence. | PASS: source-driven prompt injection fails closed. | PASS: deployed source and stored result match the reviewed path. | PASS |
| Review documentation describes the actual implementation. | `docs/review-matrix.md` references `strict_eq`, deterministic receipt verification, and semantic validation. | PASS: documentation reviewed with the implementation. | PASS: published repository contains the aligned matrix. | PASS |
