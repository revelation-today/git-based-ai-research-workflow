"""Unified corpus access — the S-01 module.

The only part of this package with no free equivalent. ``text-fabric``
covers BHSA alone; nothing unifies WLC/OSHB, BHSA, the Samaritan
Pentateuch, LXX, SBLGNT and the DSS behind one record shape.

That unification is the point. It turns a cross-corpus comparison into a
*parameter* rather than a rewrite — the surveyed workspace's own
``test_seed_claims.py`` runs the same claim against MT, SP and LXX by
hand-instantiating three different classes, which is the thing worth
generalising.

Two policies are explicit here rather than implicit, because both change
counts silently when they are not:

**Normalisation** happens at load (AD-1), so no caller normalises again
and no comparison is left to raw ``==``.

**Homographs** are a parameter. OSHB follows Strong's and does not always
split lexemes that BHSA splits; the workspace's own notes record one root
where the two disagree, and its regression suite records the resulting
claim as ``UNDECIDABLE`` rather than picking a side. A ``Hits`` set
therefore carries the policy that produced it.
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path

from . import text as _text

__all__ = ["load", "Corpus", "Word", "Hits", "CorpusError"]


class CorpusError(RuntimeError):
    """Raised when a corpus cannot be parsed — never a partial result."""


@dataclass(frozen=True)
class Word:
    """One token, the same shape from every source (C-01)."""
    ref: str
    surface: str
    lemma: str
    strongs: str
    morph: str
    slot: int


class Hits(list):
    """Query results that remember the policy that produced them (C-03)."""

    def __init__(self, items, *, policy: str, query: str, corpus: str):
        super().__init__(items)
        self.policy = policy
        self.query = query
        self.corpus = corpus

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return (f"Hits({len(self)} for {self.query!r}, "
                f"policy={self.policy!r}, corpus={self.corpus!r})")


_VERSE = re.compile(r'<verse osisID="([^"]+)">(.*?)</verse>', re.S)
_W = re.compile(r"<w\b([^>]*)>(.*?)</w>", re.S)
_ATTR = re.compile(r'(\w+)="([^"]*)"')
_TAG = re.compile(r"<[^>]+>")

#: A lemma may carry a prefixed particle (``c/776``) and a homograph
#: suffix (``7965 a``). Named parts, so neither is stripped by accident.
_LEMMA = re.compile(r"^(?:(?P<prefix>[a-z]*)/)?(?P<root>\d+)(?: (?P<homo>[a-z]))?$")


@dataclass
class Corpus:
    source: str
    path: Path
    version: str
    verses: dict = field(default_factory=dict, repr=False)
    _fingerprint: str = ""

    # ------------------------------------------------------------ access
    def verse(self, ref: str) -> list:
        """Words of a verse. Raises on an unknown reference (C-05).

        Never returns an empty list for a reference that does not exist:
        an empty result read as "no occurrences" is a wrong answer, not a
        missing one.
        """
        try:
            return self.verses[ref]
        except KeyError:
            raise KeyError(
                f"{ref!r} is not in {self.source} ({self.path.name}); "
                f"known references look like "
                f"{next(iter(self.verses), '<none>')!r}") from None

    def words(self):
        for ws in self.verses.values():
            yield from ws

    def text(self, ref: str, *, points: bool = True) -> str:
        ws = self.verse(ref)
        return " ".join(w.surface if points else _text.fold(w.surface)
                        for w in ws)

    def hits(self, *, lemma: str | None = None, strongs: str | None = None,
             homographs: str = "all") -> Hits:
        """Find tokens by lemma or Strong's number.

        ``homographs``:
          ``all``     — match the root, ignoring any homograph suffix.
          ``split``   — match root and suffix, but tolerate a prefix.
          ``strict``  — match the lemma string exactly as written.
        """
        if homographs not in ("all", "split", "strict"):
            raise ValueError(
                f"homographs must be all|split|strict, got {homographs!r}")
        query = lemma if lemma is not None else strongs
        if query is None:
            raise ValueError("pass lemma= or strongs=")

        want = _LEMMA.match(query.strip())
        found = []
        for w in self.words():
            if homographs == "strict":
                if w.lemma == query:
                    found.append(w)
                continue
            got = _LEMMA.match(w.lemma)
            if not got or not want:
                continue
            if got["root"] != want["root"]:
                continue
            if homographs == "split" and got["homo"] != want["homo"]:
                continue
            found.append(w)

        return Hits(found, policy=homographs, query=query,
                    corpus=f"{self.source}@{self.fingerprint()[:12]}")

    # -------------------------------------------------------- provenance
    def fingerprint(self) -> str:
        """Content hash of the source bytes (C-02, L-13).

        This is what lets a number be tied to the data it came from a year
        later. No script in the survey recorded anything equivalent.
        """
        return self._fingerprint

    @property
    def n_verses(self) -> int:
        return len(self.verses)

    @property
    def n_words(self) -> int:
        return sum(len(v) for v in self.verses.values())


def _parse_osis(data: str, path: Path) -> dict:
    verses: dict = {}
    slot = 0
    for ref, body in _VERSE.findall(data):
        ws = []
        for attrs, inner in _W.findall(body):
            a = dict(_ATTR.findall(attrs))
            surface = _text.normalize(_TAG.sub("", inner))
            lemma = a.get("lemma", "")
            root = _LEMMA.match(lemma)
            ws.append(Word(
                ref=ref, surface=surface, lemma=lemma,
                strongs=root["root"] if root else "",
                morph=a.get("morph", ""), slot=slot))
            slot += 1
        verses[ref] = ws
    return verses


_LOADERS = {"osis": _parse_osis, "wlc-oshb": _parse_osis}


def load(source: str, *, path, version: str | None = None) -> Corpus:
    """Load a corpus. ``source`` is the parameter that makes cross-corpus
    comparison possible without rewriting the caller.

    A malformed source raises rather than yielding a partial parse (E-05,
    TC-E10): a total computed from fewer records than intended, reported
    as complete, is exactly the silent-wrongness this package exists to
    prevent.
    """
    if source not in _LOADERS:
        raise ValueError(
            f"unknown corpus source {source!r}; known: {sorted(_LOADERS)}")

    path = Path(path)
    raw = path.read_bytes()
    data = _text.decode(raw)

    opens = data.count("<verse ")
    closes = data.count("</verse>")
    if opens != closes or (opens and "</osisText>" not in data):
        raise CorpusError(
            f"{path.name} looks truncated or malformed: {opens} <verse> "
            f"open, {closes} close. Refusing to return a partial parse — a "
            f"count taken from fewer records than intended, reported as "
            f"complete, is the failure this check exists to prevent.")

    verses = _LOADERS[source](data, path)
    if not verses:
        raise CorpusError(f"{path.name}: no verses parsed")

    return Corpus(
        source=source, path=path,
        version=version or f"{path.name}",
        verses=verses,
        _fingerprint=hashlib.sha256(raw).hexdigest())
