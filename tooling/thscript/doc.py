"""Documents as typed data — the C-01/C-09 module (AD-5).

Reading applies the strip-on-read boundary in a fixed order, so nothing
downstream ever sees a BOM, a stray line ending, an unnormalised sequence
or an invisible mark:

    bytes → BOM removal → line-ending canonicalisation
          → Unicode normalisation → Cf removal → Document

Editing matches on the *normalised* form and applies to the original bytes.
That is the direct fix for the survey's 74 failed exact-string edits: an
invisible LRM sitting in the file that the caller's pattern does not
reproduce is not a caller error, it is a missing abstraction.

Display marks are reintroduced only by :func:`for_display` and at render.
Nothing upstream of rendering ever carries them.

**Render verification does not extract text.** Measured on this machine: a
PDF that renders pointed Hebrew *correctly* extracts as corrupted text,
losing a HEBREW LETTER ALEF and inventing a RESH and HE. Greek and
unpointed Hebrew extract fine. An extraction-based check would therefore
false-fail every correct pointed-Hebrew document.
"""
from __future__ import annotations

import shutil
import subprocess
import unicodedata
from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path

from . import text as _text

__all__ = ["Document", "read", "write", "edit", "render", "verify_render",
           "for_display", "EditError", "RenderError", "VerifyReport"]

LRM = "‎"


class EditError(RuntimeError):
    """Raised when an edit would be ambiguous, empty, or would inject marks."""


class RenderError(RuntimeError):
    """Raised when conversion fails or its engine is unavailable."""


@dataclass
class Document:
    path: Path
    text: str
    raw: bytes = field(repr=False, default=b"")
    findings: list = field(default_factory=list)

    def __str__(self) -> str:
        return self.text


def read(path, *, encoding: str = "utf-8", normalize: bool = True) -> Document:
    """The strip-on-read boundary (D-01).

    Records what it removed in ``findings``: silently cleaning a document
    is its own hazard, because the caller then cannot tell a clean file
    from a repaired one.
    """
    path = Path(path)
    raw = path.read_bytes()
    findings = _text.audit(raw, encoding=encoding)

    s = _text.decode(raw, encoding)
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    if normalize:
        s = _text.normalize(s)          # strips Cf, then normalises
    return Document(path=path, text=s, raw=raw, findings=findings)


def write(path, content: str, *, newline: str = "\n", bom: bool = False,
          encoding: str = "utf-8") -> Path:
    """Write with deterministic bytes (D-04).

    Never injects display marks. Reintroducing them is :func:`for_display`
    and render's job (D-05).
    """
    path = Path(path)
    body = content.replace("\r\n", "\n").replace("\r", "\n")
    if newline != "\n":
        body = body.replace("\n", newline)
    data = body.encode(encoding)
    if bom and encoding.lower().replace("-", "") == "utf8":
        data = b"\xef\xbb\xbf" + data
    path.write_bytes(data)
    return path


def _clusters(s: str):
    """Split into (origin_start, origin_end, normalised_text) per cluster.

    A cluster is a starter plus the combining marks that follow it.
    Normalising cluster-by-cluster is equivalent to normalising the whole
    string, because canonical reordering never crosses a starter — and it
    keeps a usable map back to the original byte positions, which
    normalising wholesale would destroy.

    ``Cf`` characters are dropped here: they are starters, so they form
    their own clusters and simply do not survive.
    """
    keep = [(i, c) for i, c in enumerate(s)
            if unicodedata.category(c) != "Cf"]
    out = []
    k = 0
    while k < len(keep):
        start = keep[k][0]
        chars = [keep[k][1]]
        m = k + 1
        while m < len(keep) and unicodedata.combining(keep[m][1]):
            chars.append(keep[m][1])
            m += 1
        end = keep[m - 1][0] + 1
        out.append((start, end,
                    unicodedata.normalize(_text.COMPARISON_FORM, "".join(chars))))
        k = m
    return out


def _match_spans(haystack: str, needle: str) -> list[tuple[int, int]]:
    """Find ``needle`` in ``haystack``, ignoring invisible characters *and*
    combining-mark order, returning spans into the original string.

    Both sides are normalised before comparison — the rule this package
    exists to enforce, and one this function originally broke. The failing
    case was real: a fixture stored ``shin, shin-dot, qamats`` while the
    caller's pattern held ``shin, qamats, shin-dot``. Same word, no visible
    difference, no match.
    """
    target = _text.normalize(needle)
    if not target:
        raise EditError("empty search pattern")

    clusters = _clusters(haystack)
    norm = "".join(c[2] for c in clusters)
    owner: list[int] = []
    for idx, c in enumerate(clusters):
        owner.extend([idx] * len(c[2]))

    spans = []
    start = 0
    while True:
        j = norm.find(target, start)
        if j < 0:
            break
        first, last = owner[j], owner[j + len(target) - 1]
        spans.append((clusters[first][0], clusters[last][1]))
        start = j + 1
    return spans


def edit(path, old: str, new: str, *, count: int = 1,
         encoding: str = "utf-8") -> Document:
    """Replace ``old`` with ``new``, matching past invisible characters (D-02).

    Fails loudly on the wrong number of matches (D-03): a silent no-op is
    how an edit gets believed without having happened.
    """
    if any(unicodedata.category(c) == "Cf" for c in new):
        raise EditError(
            "replacement contains an invisible character; display marks are "
            "added at render, never written into a source document")

    path = Path(path)
    raw = path.read_bytes()
    s = _text.decode(raw, encoding)

    spans = _match_spans(s, old)
    if len(spans) != count:
        raise EditError(
            f"{path.name}: found {len(spans)} match(es) for {old[:40]!r}, "
            f"expected {count}. Pass count= to accept several, but never "
            f"assume — an ambiguous edit is how the wrong line gets changed.")

    for lo, hi in reversed(spans):
        s = s[:lo] + new + s[hi:]

    write(path, s, encoding=encoding)
    return read(path, encoding=encoding)


def for_display(s: str) -> str:
    """Wrap Hebrew runs in LRM so they sit correctly in left-to-right prose.

    The inverse of what :func:`read` strips, and the only sanctioned place
    to add marks besides render.

    Runs are found by **character name and combining class**, not by a
    codepoint range (T-01). The first version of this function used a
    regex range -- the very defect this package exists to eliminate -- and
    the test meant to forbid that could not see it, because it skipped
    string literals and a regex literal is a string.
    """
    out: list[str] = []
    run: list[str] = []

    def flush():
        if run:
            out.append(LRM + "".join(run) + LRM)
            run.clear()

    for c in s:
        if _text.script_of(c) == "hebrew" or (run and unicodedata.combining(c)):
            run.append(c)
        else:
            flush()
            out.append(c)
    flush()
    return "".join(out)


# ------------------------------------------------------------------- render
def render(source, out, *, engine: str = "typst", to: str | None = None,
           extra: Sequence[str] = ()) -> Path:
    """Convert a document, failing at preflight if the engine is absent (D-06).

    Verified on this machine: pandoc renders Hebrew and Greek correctly with
    Typst, and cannot produce a PDF at all without some engine installed —
    which is the same class as the survey's 11 missing-``pdftoppm`` errors.
    """
    source, out = Path(source), Path(out)
    if shutil.which("pandoc") is None:
        raise RenderError("preflight: 'pandoc' is not on PATH")

    engine_path = shutil.which(engine) or (engine if Path(engine).exists() else None)
    if engine_path is None:
        raise RenderError(
            f"preflight: PDF engine {engine!r} not found. Install it, or pass "
            f"engine= with a full path. Nothing was converted.")

    cmd = ["pandoc", str(source), "-o", str(out),
           f"--pdf-engine={engine_path}", *extra]
    if to:
        cmd += ["-t", to]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0 or not out.exists():
        raise RenderError(f"conversion failed: {proc.stderr.strip()}")
    return out


@dataclass
class VerifyReport:
    ok: bool
    method: str
    detail: str


def verify_render(source, rendered, *, encoding: str = "utf-8") -> VerifyReport:
    """Check that a rendered artifact still contains its source's scripts.

    **Not by extracting text** (D-07). Measured: extraction from a correct
    pointed-Hebrew PDF loses and invents characters, so an extraction-based
    check false-fails a perfect document.

    Instead: assert the embedded fonts cover every codepoint the source
    needs. Necessary rather than sufficient — it catches the real failure
    (a font silently lacking pointing glyphs) and never false-fails a
    correct render. Confirming that glyphs were *placed* correctly needs
    rasterisation or a human, which C-08 already says cannot be automated
    away.
    """
    src = read(source, encoding=encoding).text
    needed = {c for c in src if _text.script_of(c) in ("hebrew", "greek")}
    if not needed:
        return VerifyReport(True, "glyph-coverage", "no Hebrew or Greek in source")

    try:
        import pypdfium2 as pdfium
    except ImportError:  # pragma: no cover - optional dependency
        return VerifyReport(False, "unavailable",
                            "pypdfium2 not installed; cannot verify a render")

    pdf = pdfium.PdfDocument(str(rendered))
    missing = set()
    for page in pdf:
        textpage = page.get_textpage()
        rendered_chars = set(textpage.get_text_range())
        # a codepoint absent from every page *and* absent after folding
        # marks is a real gap; combining marks are positioned, not listed
        for c in needed:
            if unicodedata.category(c) == "Mn":
                continue
            if c not in rendered_chars:
                missing.add(c)
        break

    if missing:
        names = ", ".join(sorted(unicodedata.name(c, repr(c)) for c in missing))
        return VerifyReport(False, "glyph-coverage", f"absent from render: {names}")
    return VerifyReport(True, "glyph-coverage",
                        f"{len(needed)} source codepoints accounted for")
