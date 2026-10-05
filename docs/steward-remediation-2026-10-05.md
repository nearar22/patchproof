# Steward remediation: independent evidence validation

| Steward concern | Contract path | Automated proof | Deployment proof | Status |
| --- | --- | --- | --- | --- |
| Validators independently obtain both pinned source bodies. | `_inspect.fetch_sources` runs inside `strict_eq`; every validator fetches both immutable URLs. | Public `inspect_revision` lifecycle test crosses the consensus boundary. | Redeploy reviewed source and verify byte-for-byte source match. | UNVERIFIED |
| Both SHA-256 receipts are recomputed and bound to the agreed bodies. | The contract recomputes each digest after `strict_eq` and creates receipts only from that verified snapshot. | Receipt-mismatch boundary test must fail closed. | Live inspection must store two 64-character receipts. | UNVERIFIED |
| Every state and quote is checked against the evidence. | `_normalize` proves quote attribution; `prompt_non_comparative` checks the semantic state for every ordered criterion against the frozen bodies. | Unsupported but well-shaped `MET` test must fail at the semantic boundary. | Live result must contain exactly one attributed finding per criterion. | UNVERIFIED |
| Source text cannot instruct the reviewer. | Producer and comparator treat source bodies as untrusted evidence. | Source-driven prompt-injection boundary test must fail closed. | Deployed source and stored result must match the reviewed path. | UNVERIFIED |
| Review documentation describes the actual implementation. | `docs/review-matrix.md` references `strict_eq`, deterministic receipt verification, and comparative semantic validation. | Documentation is reviewed with the same commit. | Published repository contains the aligned matrix. | UNVERIFIED |
