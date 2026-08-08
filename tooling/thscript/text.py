"""Unicode handling for Hebrew and Greek — the C-01 module.

The design rule that shapes everything here (requirement T-01): **this
module contains no Hebrew or Greek codepoint range.** Classification goes
through ``unicodedata.category``, which already knows what the codepoints
are:

===========  =========================================================
Category     What it is here
===========  =========================================================
``Mn``       vowel points and cantillation — what "strip pointing" means
``Cf``       LRM, RLM, BOM, soft hyphen, embedding controls — invisible
``Pd``       U+05BE MAQAF — a word **joiner**, not a mark
``Po``       PASEQ, SOF PASUQ — punctuation
``Lo``       letters, including the U+FB1D-FB4F presentation forms
===========  =========================================================

The defect this replaces (L-04) was ``re.sub(r"[\\u0591-\\u05c7]", "", s)``
under a docstring reading "Remove vowels and cantillation". That range spans
three categories, so it also deleted the maqaf and silently merged two words
into one token. Categories make that class of error unrepresentable.
"""
from __future__ import annotations

import sys
import unicodedata
from dataclasses import dataclass
from typing import Literal

__all__ = [
    "normalize", "fold", "same", "strip_invisible", "marks", "audit",
    "tokens", "script_of", "decode", "open_text", "configure_stdout",
    "Finding", "Mark",
]

#: Normal form used for comparison. NFD is the conservative choice: it needs
#: no reasoning about the Composition Exclusion List to be correct. (Measured:
#: for Hebrew, NFC and NFD coincide anyway, because every Hebrew presentation
#: form is excluded from recomposition. For Greek they differ.)
COMPARISON_FORM: Literal["NFC", "NFD", "NFKC", "NFKD"] = "NFD"

MAQAF = "־"        # Pd. Named, not ranged.
_MARK = "Mn"
_INVISIBLE = "Cf"
_PUNCT = ("Pd", "Po")


# --------------------------------------------------------------------- types
@dataclass(frozen=True)
class Mark:
    index: int
    char: str
    name: str
    category: str


@dataclass(frozen=True)
class Finding:
    kind: str          # bom | line-endings | invisible | not-normalized
    detail: str


# ---------------------------------------------------------------- primitives
def decode(data: bytes, encoding: str = "utf-8") -> str:
    """Decode bytes, removing a leading BOM if present.

    A BOM read without ``utf-8-sig`` becomes a zero-width character on the
    first token, so the first heading of such a file silently fails every
    comparison (D-03).
    """
    if encoding.lower().replace("-", "") == "utf8" and data.startswith(b"\xef\xbb\xbf"):
        return data[3:].decode("utf-8")
    return data.decode(encoding)


def strip_invisible(s: str) -> str:
    """Remove every ``Cf`` character (T-03).

    Covers LRM, RLM, the embedding/isolate controls, soft hyphen and an
    inline BOM in one predicate, with no list to keep in sync.
    """
    return "".join(c for c in s if unicodedata.category(c) != _INVISIBLE)


def normalize(s: str, *,
              form: Literal["NFC", "NFD", "NFKC", "NFKD"] = COMPARISON_FORM,
              invisible: bool = True) -> str:
    """The single normalization entry point (AD-1).

    Idempotent by construction: both steps are (T-07).
    """
    if invisible:
        s = strip_invisible(s)
    return unicodedata.normalize(form, s)


def fold(s: str, *, points: bool = True, punctuation: bool = False,
         maqaf: str = "keep", invisible: bool = True) -> str:
    """Remove diacritics by *category*, never by range (T-01, T-02).

    ``points``      drop ``Mn`` — vowels and cantillation.
    ``punctuation`` drop ``Pd``/``Po`` — off by default, because the legacy
                    range dropped them silently and nobody could see it.
    ``maqaf``       ``keep`` | ``strip`` | ``separator``. Explicit because
                    the choice changes token counts (L-04).
    """
    if maqaf not in ("keep", "strip", "separator"):
        raise ValueError(f"maqaf must be keep|strip|separator, got {maqaf!r}")

    s = normalize(s, invisible=invisible)

    if maqaf == "separator":
        s = s.replace(MAQAF, " ")
    elif maqaf == "strip":
        s = s.replace(MAQAF, "")

    out = []
    for c in s:
        cat = unicodedata.category(c)
        if points and cat == _MARK:
            continue
        if punctuation and cat in _PUNCT:
            continue
        out.append(c)
    return "".join(out)


def same(a: str, b: str, **kw) -> bool:
    """Compare normalized forms. Never use raw ``==`` on corpus text (T-04).

    Generalises the rule the workspace's own ``tf_parse.same`` states:
    normalise both sides; raw comparison fails silently.
    """
    return normalize(a, **kw) == normalize(b, **kw)


def tokens(s: str, *, maqaf_splits: bool = True) -> list[str]:
    """Split into word tokens, treating the maqaf as a joiner (TC-E04).

    Never yields an empty token, including when a maqaf sits at a boundary.
    """
    text_ = normalize(s)
    if maqaf_splits:
        text_ = text_.replace(MAQAF, " ")
    return [t for t in text_.split() if t]


def script_of(s: str) -> str:
    """Report the script; never guess (TC-E05)."""
    seen = set()
    for c in s:
        if not c.isalpha():
            continue
        try:
            name = unicodedata.name(c)
        except ValueError:
            continue
        if name.startswith("HEBREW"):
            seen.add("hebrew")
        elif name.startswith("GREEK"):
            seen.add("greek")
        elif name.startswith("LATIN"):
            seen.add("latin")
    if not seen:
        return "unknown"
    if len(seen) > 1:
        return "mixed"
    return seen.pop()


# ---------------------------------------------------------------- diagnostic
def marks(s: str) -> list[Mark]:
    """Every invisible character, with its name. Diagnostic, not corrective.

    This is what would have surfaced the workspace's 5,902 LRM characters
    the first time anyone looked.
    """
    return [
        Mark(i, c, unicodedata.name(c, f"U+{ord(c):04X}"), unicodedata.category(c))
        for i, c in enumerate(s)
        if unicodedata.category(c) == _INVISIBLE
    ]


def audit(data: bytes | str, *, encoding: str = "utf-8") -> list[Finding]:
    """Report defects without altering the input (T-06).

    Takes bytes where possible: a BOM and the line-ending mix are byte
    facts, and reading them through ``str`` has already lost them.
    """
    findings: list[Finding] = []

    if isinstance(data, bytes):
        if data.startswith(b"\xef\xbb\xbf"):
            findings.append(Finding("bom", "file begins with a UTF-8 BOM"))
        crlf = data.count(b"\r\n")
        lf = data.replace(b"\r\n", b"").count(b"\n")
        if crlf and lf:
            findings.append(Finding(
                "line-endings", f"mixed: {crlf} CRLF and {lf} bare LF"))
        elif crlf:
            findings.append(Finding("line-endings", f"{crlf} CRLF"))
        s = decode(data, encoding)
    else:
        s = data

    found = marks(s)
    if found:
        names = sorted({m.name for m in found})
        findings.append(Finding(
            "invisible", f"{len(found)} invisible character(s): {', '.join(names)}"))

    # A file in a *consistent* normal form is fine, whichever one it is —
    # cross-form comparison is `same()`'s job, not a defect in the file.
    # What is genuinely wrong is text in neither form, which is what a
    # presentation form mixed with decomposed content produces.
    if s != unicodedata.normalize("NFC", s) and \
            s != unicodedata.normalize("NFD", s):
        findings.append(Finding(
            "not-normalized", "in neither NFC nor NFD — mixed forms"))

    return findings


# ------------------------------------------------------------------ file I/O
def open_text(path, mode: str = "r", *, encoding: str = "utf-8",
              newline: str = "\n", **kw):
    """``open`` with the encoding never left to the platform (T-05).

    18 scripts in the surveyed workspace called ``open()`` with no encoding,
    which on this machine means cp1252 and either ``UnicodeDecodeError`` or
    silent mojibake.
    """
    return open(path, mode, encoding=encoding, newline=newline, **kw)


def configure_stdout() -> None:
    """Force UTF-8 on stdout/stderr regardless of console codepage (T-05).

    Targets E-01, the single most frequent error in the surveyed workspace
    (~90 occurrences of ``UnicodeEncodeError: 'charmap'``).
    """
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(  # type: ignore[union-attr]  # not on plain TextIO
                encoding="utf-8", errors="backslashreplace")
        except (AttributeError, ValueError):  # pragma: no cover - exotic streams
            pass
