#!/usr/bin/env python3
"""Generate the test fixtures deterministically.

Run:  python tests/fixtures/generate.py

Every fixture reproduces the *shape* of a defect recorded in
docs/problems.md. Per DEPARTMENT-RULES.md section 1, none of it carries
research content from a sibling repository: Hebrew and Greek words are
chosen for their Unicode properties (combining marks, presentation forms,
final forms, word-joining punctuation), never because a project argues
about them.

The fixtures are generated rather than committed as opaque bytes so that
what makes each one defective is readable in this file. verify.py then
asserts each fixture actually exhibits its defect -- a fixture that has
quietly stopped reproducing its bug is worse than no fixture at all.
"""
import os
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))

# --- Unicode building blocks, all chosen for their properties ------------
LRM = "‎"          # Cf  - left-to-right mark
RLM = "‏"          # Cf
BOM = "﻿"          # Cf  - as a signature, and inline
SHY = "­"          # Cf  - soft hyphen
MAQAF = "־"        # Pd  - word-JOINING; the character L-04 destroys
PASEQ = "׀"        # Po
SOF_PASUQ = "׃"    # Po

# "in the beginning" - dense with Mn marks, no research significance
BERESHIT = "בְּרֵאשִׁית"
# "the land" - takes a maqaf on its left in ordinary prose
HAARETS = "הָאָרֶץ"
# "et" - the object marker, the usual left half of a maqaf pair
ET = "אֶת"
# "peace" - ends in a final mem, tests final-form handling
SHALOM = "שָׁלוֹם"
# "field" - written two ways below to exercise the presentation form
SADEH_DECOMPOSED = "שָׂדֶה"   # shin + sin-dot
SADEH_PRESENTATION = "שָׂדֶה"       # U+FB2B precomposed

GREEK = "λόγος"                    # logos
GREEK_BREATHING = "ἀγάπη"          # agape, rough breathing
GREEK_FINAL_SIGMA = "ανθρωπος"


def w(path, text, *, encoding="utf-8", newline="\n", bom=False):
    full = os.path.join(HERE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    data = ((BOM if bom else "") + text).encode(encoding)
    if newline != "\n":
        data = data.replace(b"\n", newline.encode(encoding))
    with open(full, "wb") as fh:
        fh.write(data)
    return path


def main():
    made = []

    # === F-U · Unicode ===================================================

    # F-U01 -- D-01. Hebrew wrapped in LRM the way the real documents do it.
    made.append(w("unicode/lrm_wrapped.md",
        f"# Inline Hebrew\n\nThe word {LRM}{BERESHIT}{LRM} opens the book, "
        f"and {LRM}{SHALOM}{LRM} closes the greeting.\n\n"
        f"Greek needs no marks: {GREEK}.\n"))

    # F-U02 -- L-04. Maqaf-joined pair. The buggy range merges these into one
    # token; a category-based fold keeps the boundary.
    made.append(w("unicode/maqaf.txt",
        f"{ET}{MAQAF}{HAARETS}\n{BERESHIT} {PASEQ} {SHALOM}{SOF_PASUQ}\n"))

    # F-U03 -- D-03/D-02. BOM plus CRLF.
    made.append(w("unicode/bom_crlf.md",
        f"# Heading\n\n{BERESHIT}\n", newline="\r\n", bom=True))

    # F-U04 -- D-02. Genuinely mixed line endings in one file.
    made.append(w("unicode/mixed_endings.md",
        "# Heading\r\n\r\nfirst line\nsecond line\r\nthird line\n"))

    # F-U05 -- L-05/T-04. Same word, two encodings.
    #
    # MEASURED, and not what was first assumed: for HEBREW, NFC == NFD.
    # Every Hebrew presentation form (U+FB1D-FB4F) is on the Unicode
    # Composition Exclusion List, so NFC decomposes them and declines to
    # recompose -- both normal forms land on the same codepoints. The first
    # version of this fixture used Hebrew alone and therefore tested
    # nothing; verify.py caught it. This independently reconfirms the
    # correction already recorded in the workspace's own tf_parse.py
    # docstring, which notes an earlier claim that NFC fails on Hebrew was
    # itself disproved by its test 15.
    #
    # GREEK is where the two forms genuinely differ: precomposed accented
    # vowels are NOT excluded, so NFC does recompose them.
    #   lines 1-2: Greek NFC vs NFD -- must differ.
    #   lines 3-4: Hebrew NFC vs NFD -- a GUARD that they stay equal.
    made.append(w("unicode/nfc_nfd.txt",
        unicodedata.normalize("NFC", GREEK_BREATHING) + "\n"
        + unicodedata.normalize("NFD", GREEK_BREATHING) + "\n"
        + unicodedata.normalize("NFC", BERESHIT) + "\n"
        + unicodedata.normalize("NFD", BERESHIT) + "\n"))

    # F-U06 -- T-04. Presentation form vs decomposed shin+sin-dot. The case
    # tf_parse.norm documents as silently breaking raw comparison.
    made.append(w("unicode/presentation_form.txt",
        SADEH_DECOMPOSED + "\n" + SADEH_PRESENTATION + "\n"))

    # F-U07 -- T-03/T-06. Every Cf character this project has seen, at once.
    made.append(w("unicode/invisibles.txt",
        f"a{LRM}b{RLM}c{SHY}d{BOM}e\n"))

    # F-U08 -- the composite. Every text defect in one document, for T-06.
    made.append(w("unicode/all_defects.md",
        f"# Everything wrong at once\r\n\r\n"
        f"{LRM}{ET}{MAQAF}{HAARETS}{LRM}\n"
        f"{unicodedata.normalize('NFD', SHALOM)}\r\n"
        f"{SADEH_PRESENTATION}\n{GREEK_BREATHING}\n",
        bom=True))

    # F-U09 -- negative control. Clean file; every check must pass silently.
    made.append(w("unicode/clean.md",
        f"# Clean\n\n{unicodedata.normalize('NFC', BERESHIT)} {GREEK}\n"))

    # === F-C · Corpus =====================================================

    # F-C01 -- a miniature OSIS book in the shape wlc.py expects. Maqaf is a
    # separate <seg>, exactly as the real corpus carries it (measured), so
    # this fixture pins the fact that made L-04 harmless on the corpus path.
    made.append(w("corpus/mini_osis.xml",
        '<?xml version="1.0" encoding="utf-8"?>\n<osis><osisText><div>\n'
        '<chapter osisID="Tst.1">\n'
        f'<verse osisID="Tst.1.1"><w lemma="7225" morph="HNcfsa">{BERESHIT}</w>'
        f'<seg type="x-maqqef">{MAQAF}</seg>'
        f'<w lemma="c/776" morph="HTd/Ncbsa">{HAARETS}</w>'
        f'<seg type="x-sof-pasuq">{SOF_PASUQ}</seg></verse>\n'
        f'<verse osisID="Tst.1.2"><w lemma="7965 a" morph="HNcmsa">{SHALOM}</w>'
        f'<w lemma="7965 b" morph="HNcmsa">{SHALOM}</w></verse>\n'
        '</chapter>\n</div></osisText></osis>\n'))
    # note: lemma "7965 a" / "7965 b" are homographs -- fixture for C-03.
    #       lemma "c/776" carries a prefixed particle -- fixture for lemma_re.

    # === F-S · Schema =====================================================

    # F-S01/F-S02 -- E-03. A producer writes 'total'; a consumer expects
    # 'total_words'. This is the 24-KeyError shape, minimised.
    made.append(w("schema/produced_v1.json",
        '{"schema": "counts", "version": 1, '
        '"rows": [{"unit": "Tst.1", "total": 2}]}\n'))
    made.append(w("schema/produced_v2.json",
        '{"schema": "counts", "version": 2, '
        '"rows": [{"unit": "Tst.1", "total_words": 2}]}\n'))

    # === F-D · Documents ==================================================

    # F-D01 -- H-05. The exact-match failure: an LRM sits between the words,
    # so a caller's clean pattern does not match the bytes on disk.
    made.append(w("doc/edit_target.md",
        f"# Draft\n\nReplace this: {LRM}{SHALOM}{LRM} here.\n\n"
        f"And this ambiguous phrase appears twice.\n"
        f"And this ambiguous phrase appears twice.\n"))

    # === F-R · Render =====================================================

    # F-R01 -- D-07. Pointed Hebrew, unpointed Hebrew and Greek in one file.
    # Measured: after conversion to PDF, extraction corrupts the pointed
    # Hebrew while Greek and unpointed Hebrew survive intact.
    made.append(w("render/round_trip.md",
        f"# Round trip\n\nPointed: {ET}{MAQAF}{HAARETS}\n\n"
        f"Unpointed: שלום\n\n"
        f"Greek: {GREEK_BREATHING} {GREEK_FINAL_SIGMA}\n"))

    for p in made:
        print("  wrote", p)
    print(f"{len(made)} fixtures generated")


if __name__ == "__main__":
    main()
