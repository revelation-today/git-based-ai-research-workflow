#!/usr/bin/env python3
"""Assert every fixture actually exhibits the defect it was built for.

Run:  python tests/fixtures/verify.py

This is not a test of the library -- the library does not exist yet. It is
a test of the *test data*. A fixture that has quietly stopped reproducing
its defect is worse than no fixture, because the suite built on it will go
green while checking nothing. Three extent counts in this repository were
already wrong because a pattern silently matched nothing; this file exists
so that failure mode cannot repeat in the fixtures themselves.
"""
import os
import re
import sys
import unicodedata

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))

BUGGY_RANGE = re.compile(r"[֑-ׇ]")     # the L-04 range, for comparison
CATEGORY_FOLD = lambda s: "".join(
    c for c in s if unicodedata.category(c) not in ("Mn", "Cf"))

results = []


def check(fixture, what, fn):
    try:
        fn()
        results.append((True, fixture, what))
    except AssertionError as e:
        results.append((False, fixture, f"{what} -- {e}"))


def raw(path):
    with open(os.path.join(HERE, path), "rb") as fh:
        return fh.read()


def txt(path, encoding="utf-8"):
    return raw(path).decode(encoding)


# --- F-U01 -----------------------------------------------------------------
def _u01():
    t = txt("unicode/lrm_wrapped.md")
    assert t.count("‎") >= 4, "expected LRM pairs around Hebrew"
    assert any("֐" <= c <= "׿" for c in t), "expected Hebrew"
check("F-U01 lrm_wrapped.md", "contains LRM adjacent to Hebrew", _u01)


# --- F-U02: the fixture must actually distinguish the two folds -------------
def _u02():
    t = txt("unicode/maqaf.txt").split("\n")[0]
    assert "־" in t, "expected a maqaf"
    buggy = BUGGY_RANGE.sub("", t)
    good = CATEGORY_FOLD(t)
    assert "־" not in buggy, "buggy range should have eaten the maqaf"
    assert "־" in good, "category fold must keep the maqaf"
    assert buggy != good, "fixture fails to distinguish the two folds"
check("F-U02 maqaf.txt", "buggy range merges words, category fold does not", _u02)


# --- F-U03 -----------------------------------------------------------------
def _u03():
    b = raw("unicode/bom_crlf.md")
    assert b.startswith(b"\xef\xbb\xbf"), "expected a UTF-8 BOM"
    assert b"\r\n" in b, "expected CRLF"
check("F-U03 bom_crlf.md", "has BOM and CRLF", _u03)


# --- F-U04 -----------------------------------------------------------------
def _u04():
    b = raw("unicode/mixed_endings.md")
    assert b"\r\n" in b, "expected CRLF"
    assert b.replace(b"\r\n", b"").count(b"\n") > 0, "expected bare LF too"
check("F-U04 mixed_endings.md", "genuinely mixes CRLF and LF", _u04)


# --- F-U05: raw == must fail, normalization must fix it ---------------------
def _u05():
    g_nfc, g_nfd, h_nfc, h_nfd = txt("unicode/nfc_nfd.txt").split("\n")[:4]
    # Greek: the two forms MUST differ, or the fixture tests nothing.
    assert g_nfc != g_nfd, "Greek NFC and NFD must differ"
    assert unicodedata.normalize("NFC", g_nfd) == g_nfc, "NFC must reconcile them"
    # Hebrew: a GUARD. NFC == NFD here because every Hebrew presentation
    # form is on the Unicode Composition Exclusion List. If this ever
    # fails, a Unicode revision changed something and every Hebrew
    # comparison in the library needs re-examining.
    assert h_nfc == h_nfd, \
        "GUARD BROKEN: Hebrew NFC/NFD now differ -- re-examine all comparisons"
check("F-U05 nfc_nfd.txt", "Greek NFC!=NFD; Hebrew NFC==NFD (guard)", _u05)


# --- F-U06 -----------------------------------------------------------------
def _u06():
    a, b = txt("unicode/presentation_form.txt").split("\n")[:2]
    assert a != b, "presentation form should differ from the decomposed form"
    assert unicodedata.normalize("NFD", a) == unicodedata.normalize("NFD", b), \
        "NFD should reconcile them"
check("F-U06 presentation_form.txt", "presentation form differs, NFD reconciles", _u06)


# --- F-U07 -----------------------------------------------------------------
def _u07():
    t = txt("unicode/invisibles.txt")
    cf = {c for c in t if unicodedata.category(c) == "Cf"}
    assert len(cf) >= 4, f"expected >=4 distinct Cf characters, got {len(cf)}"
    assert CATEGORY_FOLD(t).strip() == "abcde", \
        f"folding should leave 'abcde', got {CATEGORY_FOLD(t).strip()!r}"
check("F-U07 invisibles.txt", "carries >=4 distinct Cf chars, folds clean", _u07)


# --- F-U08 -----------------------------------------------------------------
def _u08():
    b = raw("unicode/all_defects.md")
    t = b.decode("utf-8")
    assert b.startswith(b"\xef\xbb\xbf"), "expected BOM"
    assert b"\r\n" in b, "expected CRLF"
    assert "‎" in t, "expected LRM"
    assert "־" in t, "expected maqaf"
    assert t != unicodedata.normalize("NFC", t), "expected non-NFC content"
check("F-U08 all_defects.md", "carries BOM + CRLF + LRM + maqaf + non-NFC", _u08)


# --- F-U09: the negative control must be genuinely clean --------------------
def _u09():
    b = raw("unicode/clean.md")
    t = b.decode("utf-8")
    assert not b.startswith(b"\xef\xbb\xbf"), "control must have no BOM"
    assert b"\r\n" not in b, "control must have no CRLF"
    assert not any(unicodedata.category(c) == "Cf" for c in t), "control must have no Cf"
    assert t == unicodedata.normalize("NFC", t), "control must already be NFC"
check("F-U09 clean.md", "negative control is genuinely clean", _u09)


# --- F-C01: maqaf must be a <seg>, never inside a <w> -----------------------
def _c01():
    t = txt("corpus/mini_osis.xml")
    words = re.findall(r"<w\b[^>]*>(.*?)</w>", t, re.S)
    assert words, "expected <w> tokens"
    assert not any("־" in x for x in words), \
        "maqaf must NOT be inside a <w> -- that is the measured corpus shape"
    assert "־" in t, "maqaf should still be present, as a <seg>"
    lemmas = re.findall(r'lemma="([^"]+)"', t)
    assert any(" a" in l or " b" in l for l in lemmas), "expected a homograph pair"
    assert any("/" in l for l in lemmas), "expected a prefixed-particle lemma"
check("F-C01 mini_osis.xml", "maqaf is a <seg>; has homographs and a prefix", _c01)


# --- F-S01/02: the schema drift must be real --------------------------------
def _s01():
    import json
    v1 = json.loads(txt("schema/produced_v1.json"))
    v2 = json.loads(txt("schema/produced_v2.json"))
    k1 = set(v1["rows"][0]); k2 = set(v2["rows"][0])
    assert k1 != k2, "fixture must actually drift"
    assert "total" in k1 and "total_words" in k2, "expected the observed rename"
check("F-S01/02 schema drift", "v1 and v2 disagree on a field name", _s01)


# --- F-D01 -----------------------------------------------------------------
def _d01():
    t = txt("doc/edit_target.md")
    assert "‎" in t, "expected an LRM in the edit target"
    assert t.count("And this ambiguous phrase appears twice.") == 2, \
        "expected a genuinely ambiguous match for the D-03 case"
check("F-D01 edit_target.md", "has an LRM trap and an ambiguous match", _d01)


# --- F-R01 -----------------------------------------------------------------
def _r01():
    t = txt("render/round_trip.md")
    assert any(unicodedata.category(c) == "Mn" for c in t), "expected pointed Hebrew"
    bare = [w for w in re.findall(r"[֐-׿]+", t)
            if not any(unicodedata.category(c) == "Mn" for c in w)]
    assert bare, "expected at least one unpointed Hebrew word"
    assert any("Ͱ" <= c <= "Ͽ" or "ἀ" <= c <= "῿" for c in t), \
        "expected Greek"
check("F-R01 round_trip.md", "has pointed + unpointed Hebrew and Greek", _r01)


# --- IP boundary: no fixture may carry sibling research content -------------
def _ip():
    # Terms come from outside the repository -- the list names what is
    # being protected, so it does not belong in a committed file. Absent,
    # this check reports that it could not run rather than passing.
    import os
    terms_file = os.environ.get("THEOLOGY_PROTECTED_TERMS") or os.path.join(
        HERE, "..", "..", "..", ".theology-protected-terms.txt")
    if not os.path.exists(terms_file):
        raise AssertionError(
            "protected-term list not found: this check is DISABLED, not "
            f"passing (looked in {terms_file})")
    with open(terms_file, encoding="utf-8") as fh:
        terms = [t.strip() for t in fh if t.strip() and not t.startswith("#")]
    banned = re.compile("|".join(re.escape(t) for t in terms), re.I)
    for dp, _, fns in os.walk(HERE):
        for fn in fns:
            if fn.endswith((".py", ".pyc")):
                continue
            p = os.path.join(dp, fn)
            body = open(p, "rb").read().decode("utf-8", "replace")
            assert not banned.search(body), f"{fn} references a sibling repository"
check("IP boundary", "no fixture references a sibling repository", _ip)


# --- report ----------------------------------------------------------------
ok = sum(1 for r in results if r[0])
for passed, fixture, what in results:
    print(f"  {'ok  ' if passed else 'FAIL'}  {fixture:32} {what}")
print(f"\n{ok}/{len(results)} fixture checks passed")
sys.exit(0 if ok == len(results) else 1)
