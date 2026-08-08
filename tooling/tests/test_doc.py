"""Tests for thscript.doc — TC-27..TC-34, TC-E17..TC-E21 (D-01..D-08).

The strip-on-read boundary, and the editing fix for the 74 failed exact
matches. The render tests skip cleanly when no PDF engine is installed
rather than pretending to pass — an unavailable engine is a real state,
and it was this machine's state until Typst was installed.
"""
import shutil
import unicodedata
from pathlib import Path

import pytest

from thscript import doc, text

FIX = Path(__file__).parent / "fixtures"

LRM = "‎"


def _engine():
    import os
    return os.environ.get("THSCRIPT_PDF_ENGINE") or shutil.which("typst")


needs_engine = pytest.mark.skipif(
    _engine() is None,
    reason="no PDF engine on PATH; install Typst and restart the shell")


# ------------------------------------------------------------- TC-27, D-01
def test_tc27_read_applies_the_whole_boundary():
    d = doc.read(FIX / "unicode/all_defects.md")
    assert not d.text.startswith("﻿"), "BOM must be gone"
    assert "\r" not in d.text, "line endings must be canonical"
    assert not any(unicodedata.category(c) == "Cf" for c in d.text), \
        "no invisible characters may survive read"
    assert d.text == unicodedata.normalize(text.COMPARISON_FORM, d.text)


def test_tc27b_read_records_what_it_removed():
    """Silent cleaning is its own hazard; the Document says what happened."""
    d = doc.read(FIX / "unicode/all_defects.md")
    kinds = {f.kind for f in d.findings}
    assert {"bom", "invisible"} <= kinds


def test_tc27c_the_clean_control_reports_nothing():
    d = doc.read(FIX / "unicode/clean.md")
    assert d.findings == []


# ------------------------------------------------------------- TC-28, D-02
def test_tc28_lrm_free_pattern_matches_lrm_bearing_bytes(tmp_path):
    """The direct fix for H-05: 74 failed exact-string edits."""
    src = FIX / "doc/edit_target.md"
    target = tmp_path / "t.md"
    target.write_bytes(src.read_bytes())

    raw = target.read_text(encoding="utf-8")
    pattern = "Replace this: שָׁלוֹם here."

    # Two independent reasons a naive match fails, both present here:
    assert LRM in raw, "precondition: the fixture must contain an LRM"
    assert pattern not in raw, "raw match must fail (invisible marks)"
    assert pattern not in raw.replace(LRM, ""), (
        "stripping LRM alone is still not enough: the fixture stores "
        "shin, shin-dot, qamats while the pattern holds shin, qamats, "
        "shin-dot — same word, different combining-mark order")

    # only normalising *and* ignoring invisibles finds it
    doc.edit(target, pattern, "Replaced.")
    assert "Replaced." in target.read_text(encoding="utf-8")


def test_tc28b_edit_preserves_bytes_it_did_not_touch(tmp_path):
    src = FIX / "doc/edit_target.md"
    target = tmp_path / "t.md"
    target.write_bytes(src.read_bytes())
    doc.edit(target, "Replace this: שָׁלוֹם here.", "Replaced.")
    after = target.read_text(encoding="utf-8")
    assert "# Draft" in after


# ------------------------------------------------------------- TC-29, D-03
def test_tc29_zero_matches_raises(tmp_path):
    target = tmp_path / "t.md"
    target.write_text("nothing to see\n", encoding="utf-8")
    with pytest.raises(doc.EditError, match="0 match"):
        doc.edit(target, "absent", "x")


def test_tc29b_ambiguous_match_raises(tmp_path):
    src = FIX / "doc/edit_target.md"
    target = tmp_path / "t.md"
    target.write_bytes(src.read_bytes())
    with pytest.raises(doc.EditError, match="2 match"):
        doc.edit(target, "And this ambiguous phrase appears twice.", "x")


def test_tc29c_ambiguity_can_be_resolved_explicitly(tmp_path):
    src = FIX / "doc/edit_target.md"
    target = tmp_path / "t.md"
    target.write_bytes(src.read_bytes())
    doc.edit(target, "And this ambiguous phrase appears twice.", "x", count=2)
    assert target.read_text(encoding="utf-8").count("x") >= 2


# ------------------------------------------------------------- TC-30, D-04
def test_tc30_write_emits_lf_and_no_bom(tmp_path):
    p = tmp_path / "o.md"
    doc.write(p, "a\nb\n")
    raw = p.read_bytes()
    assert b"\r\n" not in raw
    assert not raw.startswith(b"\xef\xbb\xbf")


def test_tc30b_bom_only_on_request(tmp_path):
    p = tmp_path / "o.md"
    doc.write(p, "a\n", bom=True)
    assert p.read_bytes().startswith(b"\xef\xbb\xbf")


# ------------------------------------------------------------- TC-31, D-05
def test_tc31_read_write_read_is_stable(tmp_path):
    original = doc.read(FIX / "unicode/lrm_wrapped.md")
    p = tmp_path / "rt.md"
    doc.write(p, original.text)
    again = doc.read(p)
    assert again.text == original.text


def test_tc31b_write_never_injects_display_marks(tmp_path):
    p = tmp_path / "rt.md"
    doc.write(p, doc.read(FIX / "unicode/lrm_wrapped.md").text)
    assert LRM not in p.read_text(encoding="utf-8")


def test_tc31c_display_marks_are_available_but_only_on_request():
    """AD-1: marks reappear at render, never upstream."""
    plain = "the word בְּרֵאשִׁית opens"
    marked = doc.for_display(plain)
    assert LRM in marked
    assert text.strip_invisible(marked) == plain


# ------------------------------------------------------------- TC-32, D-06
def test_tc32_render_preflights_the_engine(tmp_path):
    with pytest.raises(Exception) as e:
        doc.render(FIX / "render/round_trip.md", tmp_path / "o.pdf",
                   engine="definitely-not-an-engine")
    assert "definitely-not-an-engine" in str(e.value)


@needs_engine
def test_tc32b_render_produces_a_pdf(tmp_path):
    out = doc.render(FIX / "render/round_trip.md", tmp_path / "o.pdf",
                     engine=_engine())
    assert out.exists() and out.stat().st_size > 1000


# ------------------------------------------------------------- TC-33, D-07
@needs_engine
def test_tc33_verification_does_not_use_text_extraction_for_pointed_hebrew(tmp_path):
    """Measured: a *correct* PDF extracts as corrupted pointed Hebrew.

    An extraction-based check would false-fail this known-good file, which
    is the fastest way to get a check disabled.
    """
    out = doc.render(FIX / "render/round_trip.md", tmp_path / "o.pdf",
                     engine=_engine())
    report = doc.verify_render(FIX / "render/round_trip.md", out)
    assert report.ok, report.detail
    assert report.method != "extraction", \
        "pointed Hebrew must not be verified by extracting text"


@needs_engine
def test_tc33b_extraction_really_would_have_false_failed(tmp_path):
    """Pins the measurement the design rests on. If this ever passes,
    extraction became reliable and D-07 can be revisited."""
    pytest.importorskip("pypdf")
    from pypdf import PdfReader
    out = doc.render(FIX / "render/round_trip.md", tmp_path / "o.pdf",
                     engine=_engine())
    extracted = "".join(p.extract_text() for p in PdfReader(out).pages)
    source = (FIX / "render/round_trip.md").read_text(encoding="utf-8")
    pointed = "אֶת־הָאָרֶץ"
    assert pointed in source
    assert pointed not in extracted, \
        "extraction now preserves pointed Hebrew — revisit D-07"


# ------------------------------------------------------------- TC-34, D-08
@needs_engine
def test_tc34_greek_survives_extraction(tmp_path):
    pytest.importorskip("pypdf")
    from pypdf import PdfReader
    out = doc.render(FIX / "render/round_trip.md", tmp_path / "o.pdf",
                     engine=_engine())
    extracted = "".join(p.extract_text() for p in PdfReader(out).pages)
    assert "ἀγάπη" in extracted


# ------------------------------------------------------------- edge cases
def test_tce17_replacement_carrying_an_invisible_mark_is_rejected(tmp_path):
    p = tmp_path / "t.md"
    p.write_text("hello\n", encoding="utf-8")
    with pytest.raises(doc.EditError, match="invisible"):
        doc.edit(p, "hello", f"good{LRM}bye")


def test_tce18_bom_only_file_reads_as_empty(tmp_path):
    p = tmp_path / "b.md"
    p.write_bytes(b"\xef\xbb\xbf")
    assert doc.read(p).text == ""


def test_tce19_committed_bytes_are_checked_not_the_working_tree():
    """core.autocrlf silently stripped CRLF from two committed fixtures.
    The working tree looked fine; the repository did not.

    Skips outside a git checkout — there are no committed bytes to check.
    That case is real: the public export is a plain directory until it is
    initialised, and this test failed there before being guarded.
    """
    import subprocess
    root = Path(__file__).parent.parent
    inside = subprocess.run(
        ["git", "rev-parse", "--verify", "HEAD"],
        capture_output=True, cwd=str(root))
    if inside.returncode != 0:
        pytest.skip("not a git checkout: no committed bytes to verify")

    # The package may sit in a subdirectory of the repository rather than at
    # its root — it does exactly that once vendored into the workflow repo
    # as tooling/. `git show HEAD:<path>` is repo-root-relative, so the
    # prefix has to be asked for rather than assumed. An earlier version
    # assumed root == repo root and failed the moment that stopped holding.
    prefix = subprocess.run(
        ["git", "rev-parse", "--show-prefix"],
        capture_output=True, text=True, cwd=str(root)).stdout.strip()

    blob = subprocess.run(
        ["git", "show", f"HEAD:{prefix}tests/fixtures/unicode/mixed_endings.md"],
        capture_output=True, cwd=str(root)).stdout
    if not blob:
        pytest.skip("fixture not committed at this path yet (fresh import)")
    assert b"\r\n" in blob, "CRLF must survive into the repository"
    assert blob.replace(b"\r\n", b"").count(b"\n") > 0, "and bare LF too"
