# PatchProof

PatchProof turns acceptance criteria into a review record that cannot quietly drift with the conversation. A case pins one immutable specification. Each revision pins one immutable implementation file. GenLayer validators fetch both sources, judge every criterion, require an exact source quote for every finding, and store content digests with the result.

## Why consensus belongs here

Checking whether implementation evidence materially satisfies prose criteria is semantic work. A deterministic contract can enforce ownership, source immutability, revision limits, quote attribution, result shape, replay protection, and storage. GenLayer consensus handles the bounded judgment. Validators independently refetch the complete sources and reject a leader result that overstates a patch or changes its evidence receipts.

## Lifecycle

1. `open_case` records the owner, pinned specification URL, and two to six criteria.
2. `submit_revision` adds an immutable implementation URL and change note. Only the owner can submit, IDs cannot repeat, and each case accepts at most five revisions.
3. `inspect_revision` fetches both sources, produces one attributed finding per criterion, and stores `READY` only when every criterion is `MET`. Inspection is single-use per revision.
4. A failed revision stays visible. The remediation path is a new revision, not rewriting history.

This is not CI and does not execute untrusted code. It is an advisory, source-bound semantic review of public immutable text.

## Run locally

```bash
python -m pip install -r requirements.txt
python -m pytest tests -q
genvm-lint lint contracts/patchproof.py --json
cd frontend
npm ci
npm run lint
npm run build
```

Deploy with `GENLAYER_PRIVATE_KEY` set and `npm run deploy:contract`. Then set `CONTRACT_ADDRESS` and run `npm run smoke:contract`. Never commit wallet keys.

## Project identity

PatchProof uses a code-review workbench rather than a landing-page dashboard. Revisions form a vertical stack, the active rubric occupies the main surface, and validator evidence appears beside each acceptance criterion. Its voice is terse and release-oriented: spec, patch, finding, receipt.

