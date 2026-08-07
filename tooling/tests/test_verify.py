"""Tests for thscript.verify — TC-42..TC-45 (V-01..V-04).

Generalises the workspace's own test_seed_claims.py, which already worked:
45 assertions across 15 named checks, with verdicts PASS / FAIL / PARTIAL /
UNDECIDABLE / GUARD, and a stated purpose that "a change to the parsers, or
a corpus version bump, cannot silently alter a published verdict".

The vocabulary is kept intact because it says things pass/fail cannot. Two
of its checks record claims as actively *falsified* and one as
*undecidable — corpora disagree, both encodings pinned here*. A binary
framework would force those to be deleted or lied about.
"""
import pytest

from thscript import verify


# ------------------------------------------------------------- TC-42, V-01
def test_tc42_all_five_verdicts_exist():
    assert set(verify.Verdict) >= {
        verify.Verdict.PASS, verify.Verdict.FAIL, verify.Verdict.PARTIAL,
        verify.Verdict.UNDECIDABLE, verify.Verdict.GUARD}


def test_tc42b_a_check_expected_to_pass_and_passing_is_ok():
    s = verify.Suite("t")
    s.check("holds", verify.Verdict.PASS, lambda: None)
    assert s.results[0].ok


def test_tc42c_a_falsified_claim_is_recorded_not_deleted():
    """FAIL means 'this claim is false, and that IS the finding'."""
    s = verify.Suite("t")
    s.check("refuted", verify.Verdict.FAIL,
            lambda: (_ for _ in ()).throw(AssertionError("no evidence")))
    r = s.results[0]
    assert r.ok, "a FAIL-expected check that fails is behaving correctly"
    assert r.expected is verify.Verdict.FAIL


def test_tc42d_a_falsified_claim_that_starts_passing_is_reported():
    """The case a binary framework cannot express.

    If a claim recorded as refuted suddenly holds, something changed —
    the corpus, the parser, or the claim. That must surface, not go green.
    """
    s = verify.Suite("t")
    s.check("was refuted", verify.Verdict.FAIL, lambda: None)   # now passes
    r = s.results[0]
    assert not r.ok
    assert "unexpectedly" in r.detail.lower()
    assert s.failed


def test_tc42e_undecidable_pins_both_readings():
    s = verify.Suite("t")
    s.check("corpora disagree", verify.Verdict.UNDECIDABLE, lambda: None,
            note="MT has one lexeme, BHSA splits two; both pinned")
    r = s.results[0]
    assert r.ok
    assert "both pinned" in r.note


def test_tc42f_undecidable_requires_a_note():
    """Recording 'we don't know' without saying why is not a record."""
    s = verify.Suite("t")
    with pytest.raises(ValueError, match="note"):
        s.check("unclear", verify.Verdict.UNDECIDABLE, lambda: None)


def test_tc42g_guard_failure_says_the_world_moved():
    s = verify.Suite("t")
    s.check("unicode assumption", verify.Verdict.GUARD,
            lambda: (_ for _ in ()).throw(AssertionError("NFC != NFD now")))
    r = s.results[0]
    assert not r.ok
    assert "guard" in r.detail.lower()


def test_tc42h_a_suite_reports_counts_per_verdict():
    s = verify.Suite("t")
    s.check("a", verify.Verdict.PASS, lambda: None)
    s.check("b", verify.Verdict.FAIL,
            lambda: (_ for _ in ()).throw(AssertionError("x")))
    text = s.report()
    assert "PASS" in text and "FAIL" in text
    assert "2" in text


# ------------------------------------------------------------- TC-43, V-02
def test_tc43_claims_without_a_supporting_check_are_listed():
    reg = verify.Claims()
    reg.claim("C1", "The word occurs 3 times.", source="paper.md:12",
              check="counts_three")
    reg.claim("C2", "The structure is chiastic.", source="paper.md:40",
              check=None)
    unsupported = reg.unsupported()
    assert [c.id for c in unsupported] == ["C2"]


def test_tc43b_a_claim_whose_check_fails_is_listed_too():
    reg = verify.Claims()
    reg.claim("C1", "x", source="p:1", check="check_x")
    s = verify.Suite("t")
    s.check("check_x", verify.Verdict.PASS,
            lambda: (_ for _ in ()).throw(AssertionError("nope")))
    unsupported = reg.unsupported(suite=s)
    assert [c.id for c in unsupported] == ["C1"]


def test_tc43c_a_claim_whose_check_passes_is_supported():
    reg = verify.Claims()
    reg.claim("C1", "x", source="p:1", check="check_x")
    s = verify.Suite("t")
    s.check("check_x", verify.Verdict.PASS, lambda: None)
    assert reg.unsupported(suite=s) == []


def test_tc43d_report_is_markdown_and_names_the_source():
    reg = verify.Claims()
    reg.claim("C1", "The word occurs 3 times.", source="paper.md:12",
              check="counts_three")
    md = reg.report()
    assert "C1" in md and "paper.md:12" in md


def test_tc43e_verify_cannot_tell_whether_a_claim_is_true():
    """C-08 stated in code, not just prose.

    A claim can be fully 'supported' and still be false — the circular
    marker in the survey would pass every check here. The module must not
    imply otherwise.
    """
    assert not hasattr(verify.Claims, "is_true")
    doc = verify.Claims.unsupported.__doc__ or ""
    assert "not" in doc.lower() and "true" in doc.lower()


# ------------------------------------------------------------- TC-44, V-03
def test_tc44_traceability_finds_every_requirement_id():
    """Every requirement must map to at least one test."""
    missing = verify.traceability_gaps()
    assert missing == [], f"requirements with no test: {missing}"


def test_tc44_is_not_vacuous():
    """It would pass trivially if the regex found no requirement IDs."""
    from thscript.run import paths
    import re
    src = (paths().root / "docs" / "requirements.md").read_text(encoding="utf-8")
    ids = set(re.findall(r"\*\*([TCSDXEV]-\d{2}[a-z]?)\*\*", src))
    assert len(ids) >= 30, f"expected the full requirement set, found {len(ids)}"


def test_tc44b_the_traceability_scan_can_fire(tmp_path):
    """Run against an isolated root.

    The first version of this test passed the sentinel 'ZZ-99' against the
    real repository — and the scan greps the test suite, which contains
    this very file, so the sentinel found itself and the scan reported no
    gap. A self-referential check that can never fail is the same defect
    this project keeps finding.
    """
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_nothing.py").write_text(
        "def test_x():\n    pass\n", encoding="utf-8")
    gaps = verify.traceability_gaps(requirement_ids=["ZZ-99"], root=tmp_path)
    assert gaps == ["ZZ-99"], "a requirement nothing mentions must be reported"


# ------------------------------------------------------------- TC-45, V-04
def test_tc45_golden_detects_a_changed_fingerprint(tmp_path):
    g = tmp_path / "g.json"
    verify.pin(g, {"corpus": "abc123", "count": 42})
    assert verify.compare(g, {"corpus": "abc123", "count": 42}).ok
    r = verify.compare(g, {"corpus": "def456", "count": 42})
    assert not r.ok
    assert "corpus" in r.detail


def test_tc45b_golden_refuses_to_silently_create_itself(tmp_path):
    with pytest.raises(FileNotFoundError):
        verify.compare(tmp_path / "absent.json", {"a": 1})
