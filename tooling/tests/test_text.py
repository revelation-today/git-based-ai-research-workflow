"""Tests for thscript.text — cases TC-01..TC-10, TC-E01..TC-E06.

Written before the implementation. Each test names the requirement it
verifies and, where the case could be vacuous, asserts the precondition
that makes it non-vacuous first.
"""
import subprocess
import sys
import unicodedata
from pathlib import Path

import pytest

from thscript import text

FIX = Path(__file__).parent / "fixtures"
LEGACY_RANGE = "[֑-ׇ]"      # the L-04 range, referenced never used


def read_fixture(name, encoding="utf-8"):
    return (FIX / name).read_bytes().decode(encoding)


def _package_files():
    import thscript
    return sorted(Path(thscript.__file__).parent.rglob("*.py"))


# --------------------------------------------------------------- TC-01, T-02
def test_tc01_fold_keeps_maqaf_where_legacy_range_destroys_it():
    """fold() removes Mn but must keep Pd. The legacy range removed both."""
    import re
    line = read_fixture("unicode/maqaf.txt").split("\n")[0]
    assert "־" in line, "precondition: fixture must contain a maqaf"

    legacy = re.sub(LEGACY_RANGE, "", line)
    assert "־" not in legacy, "precondition: legacy range must eat the maqaf"

    folded = text.fold(line)
    assert "־" in folded, "maqaf (Pd) must survive a marks-only fold"
    assert folded != legacy, "fold must differ from the legacy behaviour"
    # and the vowels really are gone
    assert not any(unicodedata.category(c) == "Mn" for c in folded)


def test_tc01b_fold_can_be_asked_to_drop_punctuation():
    line = read_fixture("unicode/maqaf.txt").split("\n")[0]
    assert "־" not in text.fold(line, punctuation=True)


def test_tc01c_maqaf_policy_is_explicit():
    """The legacy range silently chose 'strip'. Here it must be named."""
    line = read_fixture("unicode/maqaf.txt").split("\n")[0]
    assert "־" in text.fold(line, maqaf="keep")
    assert "־" not in text.fold(line, maqaf="strip")
    assert " " in text.fold(line, maqaf="separator")


# --------------------------------------------------------------- TC-02, T-01
def test_tc02_no_codepoint_range_literal_in_package():
    """T-01: classification must go through unicodedata.category."""
    import re
    import thscript
    pkg = Path(thscript.__file__).parent
    # a range literal over the Hebrew or Greek blocks, escaped or literal
    pattern = re.compile(
        r"\[\\u0[35][0-9a-fA-F]{2}-|\[[֐-׿Ͱ-Ͽ]-")
    import ast
    offenders = []
    for f in pkg.rglob("*.py"):
        tree = ast.parse(f.read_text(encoding="utf-8"), filename=str(f))

        # Docstrings are exempt: text.py *documents* the legacy range it
        # replaces, and prose about a bug is not the bug. Everything else,
        # including regex literals, is in scope.
        #
        # An earlier version of this test skipped ALL string tokens to
        # silence that docstring, which made it unable to see a range in a
        # regex literal — i.e. the only place one can occur. It passed
        # while doc.py:196 held exactly such a range. Exempting docstrings
        # specifically, rather than strings generally, is the difference
        # between a check and a decoration.
        exempt = set()
        for node in ast.walk(tree):
            if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef,
                                 ast.AsyncFunctionDef)):
                if node.body and isinstance(node.body[0], ast.Expr) and \
                        isinstance(node.body[0].value, ast.Constant) and \
                        isinstance(node.body[0].value.value, str):
                    exempt.add(id(node.body[0].value))

        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str) \
                    and id(node) not in exempt and pattern.search(node.value):
                offenders.append(f"{f.name}:{node.lineno}")
    assert not offenders, f"codepoint range literals found: {offenders}"


def test_tc02b_the_scan_can_actually_fire():
    """A scan that matches nothing proves nothing (three counts died that way)."""
    import re
    pattern = re.compile(
        r"\[\\u0[35][0-9a-fA-F]{2}-|\[[֐-׿Ͱ-Ͽ]-")
    assert pattern.search('re.sub(r"[\\u0591-\\u05c7]", "", s)'), \
        "the scan pattern must match the known-bad legacy form"


# --------------------------------------------------------------- TC-03, T-03
def test_tc03_strip_removes_every_cf_character():
    raw = read_fixture("unicode/invisibles.txt")
    cf = {c for c in raw if unicodedata.category(c) == "Cf"}
    assert len(cf) >= 4, "precondition: fixture needs >=4 distinct Cf chars"
    assert text.strip_invisible(raw).strip() == "abcde"


# --------------------------------------------------------------- TC-04, T-04
def test_tc04_same_reconciles_greek_nfc_and_nfd():
    lines = read_fixture("unicode/nfc_nfd.txt").split("\n")
    g_nfc, g_nfd = lines[0], lines[1]
    assert g_nfc != g_nfd, "precondition: Greek NFC and NFD must differ"
    assert text.same(g_nfc, g_nfd)


def test_tce02_hebrew_nfc_equals_nfd_guard():
    """GUARD, not a test of our code.

    Every Hebrew presentation form is on the Unicode Composition Exclusion
    List, so NFC decomposes and declines to recompose. If this fails, a
    Unicode revision moved and every Hebrew comparison needs re-examining.
    """
    lines = read_fixture("unicode/nfc_nfd.txt").split("\n")
    h_nfc, h_nfd = lines[2], lines[3]
    assert h_nfc == h_nfd, "GUARD BROKEN: Hebrew NFC/NFD now differ"


# --------------------------------------------------------------- TC-05, T-04
def test_tc05_same_reconciles_presentation_form():
    a, b = read_fixture("unicode/presentation_form.txt").split("\n")[:2]
    assert a != b, "precondition: the two spellings must differ raw"
    assert text.same(a, b)


# --------------------------------------------------------------- TC-06, T-06
def test_tc06_audit_reports_all_four_defects():
    raw = (FIX / "unicode/all_defects.md").read_bytes()
    report = text.audit(raw)
    kinds = {f.kind for f in report}
    assert {"bom", "line-endings", "invisible", "not-normalized"} <= kinds, \
        f"expected all four defect kinds, got {kinds}"


def test_tc06b_audit_does_not_mutate():
    raw = (FIX / "unicode/all_defects.md").read_bytes()
    before = bytes(raw)
    text.audit(raw)
    assert raw == before


# --------------------------------------------------------------- TC-07, T-06
def test_tc07_audit_is_silent_on_the_clean_control():
    """Negative control: catches an audit that always fires."""
    raw = (FIX / "unicode/clean.md").read_bytes()
    assert text.audit(raw) == []


# --------------------------------------------------------------- TC-08, T-07
def test_tc08_normalize_is_idempotent():
    from hypothesis import given, settings
    from hypothesis import strategies as st

    alphabet = st.sampled_from(
        "אבשתֶָּׁׂ־"
        "‎‏﻿αβἀ̓ς \n")

    @given(st.text(alphabet=alphabet, max_size=40))
    @settings(max_examples=200, deadline=None)
    def check(s):
        once = text.normalize(s)
        assert text.normalize(once) == once

    check()


# --------------------------------------------------------------- TC-09, T-05
def test_tc09_hebrew_to_stdout_under_a_legacy_codepage():
    """E-01 reproduced: ~90 UnicodeEncodeError in the workspace, and one
    hit accidentally while building these fixtures."""
    script = (
        "from thscript import text; text.configure_stdout();"
        "print('בְּרֵאשִׁית')"
    )
    env_check = subprocess.run(
        [sys.executable, "-c", script],
        capture_output=True,
        cwd=str(Path(__file__).parent.parent),
    )
    assert env_check.returncode == 0, env_check.stderr.decode("utf-8", "replace")


# --------------------------------------------------------------- TC-10, T-05
def test_tc10_no_open_without_encoding_in_package():
    """Parsed with ast, not grepped.

    The first version of this test was a regex over lines, and it matched
    the phrase ``open()`` inside a docstring — the same naive-pattern
    failure that falsified three extent counts in docs/problems.md.
    """
    import ast
    bad = []
    for f in _package_files():
        tree = ast.parse(f.read_text(encoding="utf-8"), filename=str(f))
        for node in ast.walk(tree):
            if not (isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Name)
                    and node.func.id == "open"):
                continue
            mode = ""
            if len(node.args) > 1 and isinstance(node.args[1], ast.Constant):
                mode = str(node.args[1].value)
            if "b" in mode:
                continue                      # binary mode takes no encoding
            if "encoding" not in {k.arg for k in node.keywords}:
                bad.append(f"{f.name}:{node.lineno}")
    assert not bad, f"open() without encoding=: {bad}"


def test_tc10b_the_ast_scan_can_actually_fire():
    """A scan that cannot fail proves nothing."""
    import ast
    tree = ast.parse("open('x')\nopen('y', encoding='utf-8')\nopen('z','rb')")
    hits = [
        n for n in ast.walk(tree)
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
        and n.func.id == "open"
        and "encoding" not in {k.arg for k in n.keywords}
        and not (len(n.args) > 1 and isinstance(n.args[1], ast.Constant)
                 and "b" in str(n.args[1].value))
    ]
    assert len(hits) == 1, f"expected exactly one bare open(), got {len(hits)}"


# ------------------------------------------------------------- edge cases
def test_tce01_empty_and_marks_only():
    assert text.fold("") == ""
    assert text.normalize("") == ""
    assert text.fold("ֶָ") == ""          # only combining marks


def test_tce03_lone_combining_mark_is_a_decision_not_an_accident():
    """A mark with no base must be handled deliberately."""
    assert text.fold("ָ") == ""
    assert text.strip_invisible("ָ") == "ָ"   # Mn is not Cf


def test_tce04_maqaf_at_a_boundary_produces_no_empty_token():
    assert text.tokens("־אב") == ["אב"]
    assert text.tokens("אב־") == ["אב"]
    assert text.tokens("א־ב") == ["א", "ב"]


def test_tce05_mixed_script_is_reported_not_guessed():
    assert text.script_of("אב") == "hebrew"
    assert text.script_of("αβ") == "greek"
    assert text.script_of("abc") == "latin"
    assert text.script_of("א α a") == "mixed"
    assert text.script_of("") == "unknown"


def test_tce06_inline_feff_is_stripped_as_cf_not_treated_as_bom():
    s = "a﻿b"
    assert text.strip_invisible(s) == "ab"
    # and as a *leading* byte sequence it is a BOM, handled by decode()
    assert text.decode("﻿ab".encode("utf-8")) == "ab"
