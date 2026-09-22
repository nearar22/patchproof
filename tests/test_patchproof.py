import json, importlib

CONTRACT = "contracts/patchproof.py"
SPEC = "https://raw.githubusercontent.com/nearar22/threadmark/992484c4d145c4c0d3d82e94c248e097714637c6/README.md"
PATCH = "https://raw.githubusercontent.com/nearar22/threadmark/992484c4d145c4c0d3d82e94c248e097714637c6/contracts/threadmark.py"
SPEC_TEXT = "Acceptance requires strict address validation and owner-only author management. Every implementation must reject malformed wallet input."
PATCH_TEXT = "def set_author(self, board_id: str, author: str, allowed: bool):\n    if board owner != sender: raise Only owner\n    address = _address(author)\n"
CRITERIA = ["Validate every author wallet before changing state.", "Allow only the board owner to manage authors."]

def setup(vm, contract, states=("MET", "MET"), validator=True):
    vm.mock_web(SPEC, {"method":"GET","status":200,"body":SPEC_TEXT}); vm.mock_web(PATCH, {"method":"GET","status":200,"body":PATCH_TEXT})
    rows = [{"index":0,"state":states[0],"source_indexes":[1],"pinpoint_quote":"address = _address(author)"},{"index":1,"state":states[1],"source_indexes":[1],"pinpoint_quote":"Only owner"}]
    vm.mock_llm("PATCHPROOF_PRODUCER", json.dumps(json.dumps({"findings":rows}))); vm.mock_llm("PATCHPROOF_VALIDATOR", json.dumps({"valid":validator}))

def test_complete_review_lifecycle(direct_vm, direct_deploy, direct_alice):
    c = direct_deploy(CONTRACT); direct_vm.sender = direct_alice
    c.open_case("author-fix", "Author management repair", SPEC, CRITERIA); c.submit_revision("author-fix", "revision-one", PATCH, "Implements strict address and owner checks")
    setup(direct_vm, c); result = c.inspect_revision("author-fix", "revision-one")
    assert result["overall"] == "READY" and c.get_revision("author-fix", "revision-one")["status"] == "READY"
    assert len(result["source_receipts"]) == 2 and all(len(x["sha256"]) == 64 for x in result["source_receipts"])

def test_owner_duplicates_and_replay(direct_vm, direct_deploy, direct_alice, direct_bob):
    c = direct_deploy(CONTRACT); direct_vm.sender = direct_alice; c.open_case("author-fix", "Author management repair", SPEC, CRITERIA)
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("Only the case owner"): c.submit_revision("author-fix", "revision-one", PATCH, "Unauthorized revision attempt")
    direct_vm.sender = direct_alice; c.submit_revision("author-fix", "revision-one", PATCH, "Implements strict address checks")
    with direct_vm.expect_revert("already exists"): c.submit_revision("author-fix", "revision-one", PATCH, "Duplicate revision attempt")
    setup(direct_vm, c); c.inspect_revision("author-fix", "revision-one")
    with direct_vm.expect_revert("already inspected"): c.inspect_revision("author-fix", "revision-one")

def test_urls_and_quote_attribution_fail_closed(direct_vm, direct_deploy):
    c = direct_deploy(CONTRACT)
    with direct_vm.expect_revert("pinned raw GitHub"): c.open_case("bad-case", "Unsafe source review", "https://example.com/spec", CRITERIA)
    with direct_vm.expect_revert("full commit SHA"): c.open_case("bad-ref", "Moving source review", "https://raw.githubusercontent.com/nearar22/threadmark/main/README.md", CRITERIA)
    c.open_case("author-fix", "Author management repair", SPEC, CRITERIA); c.submit_revision("author-fix", "revision-one", PATCH, "Implements strict address checks")
    direct_vm.mock_web(SPEC,{"method":"GET","status":200,"body":SPEC_TEXT}); direct_vm.mock_web(PATCH,{"method":"GET","status":200,"body":PATCH_TEXT})
    rows=[{"index":0,"state":"MET","source_indexes":[1],"pinpoint_quote":"invented code"},{"index":1,"state":"MET","source_indexes":[1],"pinpoint_quote":"Only owner"}]
    direct_vm.mock_llm("PATCHPROOF_PRODUCER",json.dumps(json.dumps({"findings":rows})))
    with direct_vm.expect_revert("Pinpoint quote"): c.inspect_revision("author-fix", "revision-one")

def test_validator_rejects_forged_ready_result(direct_vm, direct_deploy):
    c=direct_deploy(CONTRACT); c.open_case("author-fix","Author management repair",SPEC,CRITERIA); c.submit_revision("author-fix","revision-one",PATCH,"Implements strict address checks")
    setup(direct_vm,c,validator=False); c.inspect_revision("author-fix","revision-one")
    assert direct_vm.run_validator() is False

def test_validator_rejects_changed_snapshot(direct_vm, direct_deploy, monkeypatch):
    c=direct_deploy(CONTRACT); c.open_case("author-fix","Author management repair",SPEC,CRITERIA); c.submit_revision("author-fix","revision-one",PATCH,"Implements strict address checks"); setup(direct_vm,c); c.inspect_revision("author-fix","revision-one")
    direct_vm.clear_mocks(); direct_vm.mock_web(SPEC,{"method":"GET","status":200,"body":SPEC_TEXT}); direct_vm.mock_web(PATCH,{"method":"GET","status":200,"body":PATCH_TEXT + " altered"})
    gl=importlib.import_module("genlayer"); monkeypatch.setattr(gl.vm,"spawn_sandbox",lambda fn: gl.vm.Return(fn()))
    assert direct_vm.run_validator() is False

