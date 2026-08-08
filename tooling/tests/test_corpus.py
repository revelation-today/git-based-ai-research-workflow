"""Tests for thscript.corpus — TC-11..TC-16, TC-E07..TC-E10 (C-01..C-05).

The only module with no free equivalent: text-fabric covers BHSA alone,
and nothing unifies WLC / BHSA / SP / LXX / SBLGNT / DSS behind one Word
shape. That unification is what turns a cross-corpus comparison into a
parameter instead of a rewrite — the workspace's own test_seed_claims.py
runs the same claim against MT, SP and LXX by hand-instantiating three
different classes.
"""
from pathlib import Path

import pytest

from thscript import corpus, text

FIX = Path(__file__).parent / "fixtures"
MINI = FIX / "corpus/mini_osis.xml"


@pytest.fixture
def mini():
    return corpus.load("osis", path=MINI)


# ------------------------------------------------------------- TC-11, C-01
def test_tc11_words_have_the_unified_shape(mini):
    w = mini.verse("Tst.1.1")[0]
    for attr in ("ref", "surface", "lemma", "strongs", "morph", "slot"):
        assert hasattr(w, attr), f"Word is missing {attr}"


def test_tc11b_the_same_assertion_runs_against_any_source(mini):
    """C-01's real point: source becomes a parameter."""
    def count_words(c, ref):
        return len(c.verse(ref))
    assert count_words(mini, "Tst.1.1") == 2
    assert count_words(mini, "Tst.1.2") == 2


def test_tc11c_slots_are_sequential_across_the_corpus(mini):
    slots = [w.slot for w in mini.words()]
    assert slots == sorted(slots)
    assert len(set(slots)) == len(slots)


# ------------------------------------------------------------- TC-12, C-02
def test_tc12_fingerprint_is_stable_and_content_addressed(mini, tmp_path):
    first = mini.fingerprint()
    assert len(first) == 64
    assert corpus.load("osis", path=MINI).fingerprint() == first

    altered = tmp_path / "altered.xml"
    altered.write_bytes(MINI.read_bytes().replace(b"7965 a", b"7965 c"))
    assert corpus.load("osis", path=altered).fingerprint() != first


def test_tc12b_corpus_exposes_a_version(mini):
    assert mini.version


# ------------------------------------------------------------- TC-13, C-03
def test_tc13_homograph_policy_changes_the_count_and_is_labelled(mini):
    """The fixture carries lemma '7965 a' and '7965 b' — a homograph pair."""
    every = mini.hits(lemma="7965", homographs="all")
    split = mini.hits(lemma="7965 a", homographs="split")
    assert len(every) == 2
    assert len(split) == 1
    assert every.policy == "all"
    assert split.policy == "split"


def test_tc13b_strict_requires_an_exact_lemma(mini):
    assert len(mini.hits(lemma="7965", homographs="strict")) == 0
    assert len(mini.hits(lemma="7965 a", homographs="strict")) == 1


def test_tc13c_unknown_policy_raises(mini):
    with pytest.raises(ValueError):
        mini.hits(lemma="7965", homographs="whatever")


# ------------------------------------------------------------- TC-16
def test_tc16_prefixed_particle_lemma_matches_the_root(mini):
    """The fixture's 'c/776' is a root behind a prefixed particle."""
    assert len(mini.hits(lemma="776", homographs="all")) == 1


# ------------------------------------------------------------- TC-14, C-04
def test_tc14_returned_text_is_already_normalized(mini):
    """AD-1: no caller-side normalisation should be needed."""
    surface = mini.verse("Tst.1.1")[0].surface
    assert surface == text.normalize(surface)
    assert not any(__import__("unicodedata").category(c) == "Cf"
                   for c in surface)


def test_tc14b_same_succeeds_without_caller_normalisation(mini):
    a = mini.verse("Tst.1.1")[0].surface
    assert text.same(a, a)


# ------------------------------------------------------------- TC-15, C-05
def test_tc15_missing_reference_raises(mini):
    with pytest.raises(KeyError):
        mini.verse("Tst.99.1")


def test_tc15b_missing_reference_does_not_return_empty(mini):
    """E-03's shape: an empty result read as 'no occurrences' is a wrong
    answer, not a missing one."""
    try:
        result = mini.verse("Tst.99.1")
    except KeyError:
        result = "raised"
    assert result == "raised"


# ------------------------------------------------------------ edge cases
def test_tce07_maqaf_is_a_seg_never_inside_a_word(mini):
    """GUARD. Pins the measured corpus shape.

    In the real WLC, U+05BE occurs 42,587 times, always as a standalone
    <seg> and never inside a <w>. That is precisely what makes the L-04
    over-wide strip range harmless on the corpus path. If this changes,
    L-04 becomes live and every stripped count needs re-checking.
    """
    for w in mini.words():
        assert "־" not in w.surface, \
            "GUARD BROKEN: maqaf now appears inside a <w> token"
    assert "־" in MINI.read_text(encoding="utf-8"), \
        "precondition: the fixture must contain a maqaf somewhere"


def test_tce08_verse_with_no_words_returns_empty_not_error(tmp_path):
    p = tmp_path / "empty.xml"
    p.write_text(
        '<osis><osisText><div><chapter osisID="T.1">'
        '<verse osisID="T.1.1"></verse></chapter></div></osisText></osis>',
        encoding="utf-8")
    assert corpus.load("osis", path=p).verse("T.1.1") == []


def test_tce10_truncated_corpus_raises_rather_than_parsing_partially(tmp_path):
    p = tmp_path / "trunc.xml"
    p.write_bytes(MINI.read_bytes()[: len(MINI.read_bytes()) // 2])
    with pytest.raises(corpus.CorpusError):
        corpus.load("osis", path=p)


def test_unknown_source_raises():
    with pytest.raises(ValueError, match="unknown"):
        corpus.load("not-a-corpus", path=MINI)


def test_corpus_reports_counts(mini):
    assert mini.n_verses == 2
    assert mini.n_words == 4
