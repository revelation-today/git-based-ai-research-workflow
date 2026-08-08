"""Claims and verdicts — the C-08 module (AD-6).

This generalises ``test_seed_claims.py``, which already existed in the
surveyed workspace and already worked: 45 assertions across 15 named
checks, with a stated purpose that *"a change to the parsers, or a corpus
version bump, cannot silently alter a published verdict."*

Its five-verdict vocabulary is kept because it says things pass/fail
cannot:

``PASS``          the claim holds.
``FAIL``          the claim is **falsified, and that is the finding**. Two
                  of the original suite's checks are recorded this way.
``PARTIAL``       true only under a narrower statement.
``UNDECIDABLE``   the corpora disagree; both readings are pinned here.
``GUARD``         an assumption about the outside world — Unicode, git, a
                  corpus format. If it breaks, the design is wrong, not
                  the code.

**What this module cannot do**, and must not appear to: decide whether a
claim is *true*. A claim can be fully supported by a passing check and
still be false — the circular marker found in the survey would satisfy
every check here. Recording judgment is not supplying it.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

__all__ = ["Verdict", "Result", "Suite", "Claim", "Claims", "pin", "compare",
           "Comparison", "traceability_gaps"]


class Verdict(Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    PARTIAL = "PARTIAL"
    UNDECIDABLE = "UNDECIDABLE"
    GUARD = "GUARD"


@dataclass
class Result:
    name: str
    expected: Verdict
    ok: bool
    detail: str = ""
    note: str = ""


@dataclass
class Suite:
    """A named set of checks, each with an expected verdict."""
    name: str
    results: list = field(default_factory=list)

    def check(self, name: str, expected: Verdict, fn, *, note: str = "") -> Result:
        if expected is Verdict.UNDECIDABLE and not note:
            raise ValueError(
                "an UNDECIDABLE verdict requires a note: recording that we do "
                "not know, without saying why, is not a record")

        try:
            fn()
            raised = None
        except Exception as exc:
            raised = exc

        if expected is Verdict.FAIL:
            # The claim is supposed to be false. It failing is correct.
            if raised is None:
                ok = False
                detail = (
                    f"{name}: recorded as FAIL (falsified) but the check now "
                    f"passes unexpectedly. Something changed — the corpus, the "
                    f"parser, or the claim. Review before trusting either.")
            else:
                ok, detail = True, f"falsified as recorded: {raised}"
        elif expected is Verdict.GUARD:
            if raised is None:
                ok, detail = True, "guard holds"
            else:
                ok = False
                detail = (
                    f"GUARD BROKEN — {name}: {raised}. This is an assumption "
                    f"about the outside world, so the design needs review, "
                    f"not the code.")
        else:
            ok = raised is None
            detail = "" if ok else f"{type(raised).__name__}: {raised}"

        r = Result(name=name, expected=expected, ok=ok, detail=detail, note=note)
        self.results.append(r)
        return r

    @property
    def failed(self) -> bool:
        return any(not r.ok for r in self.results)

    def by_name(self, name: str) -> Result | None:
        for r in self.results:
            if r.name == name:
                return r
        return None

    def report(self) -> str:
        counts: dict[str, int] = {}
        for r in self.results:
            counts[r.expected.value] = counts.get(r.expected.value, 0) + 1
        lines = [f"{self.name}: {len(self.results)} checks "
                 f"({', '.join(f'{k} {v}' for k, v in sorted(counts.items()))})"]
        for r in self.results:
            mark = "ok  " if r.ok else "**  "
            lines.append(f"  {mark}{r.expected.value:<12} {r.name}")
            if r.detail:
                lines.append(f"        {r.detail}")
            if r.note:
                lines.append(f"        note: {r.note}")
        return "\n".join(lines)


# ------------------------------------------------------------------- claims
@dataclass
class Claim:
    id: str
    statement: str
    source: str
    check: str | None = None


@dataclass
class Claims:
    """Ties statements in a paper to the checks that support them (V-02)."""
    entries: list = field(default_factory=list)

    def claim(self, id: str, statement: str, *, source: str,
              check: str | None = None) -> Claim:
        c = Claim(id=id, statement=statement, source=source, check=check)
        self.entries.append(c)
        return c

    def unsupported(self, *, suite: Suite | None = None) -> list:
        """Claims with no check, or whose check is absent or failing.

        This does **not** tell you whether a claim is true. A claim can be
        supported by a passing check and still be false; deciding that is
        human judgment, and no amount of test infrastructure supplies it.
        """
        out = []
        for c in self.entries:
            if c.check is None:
                out.append(c)
                continue
            if suite is None:
                continue
            r = suite.by_name(c.check)
            if r is None or not r.ok:
                out.append(c)
        return out

    def report(self, *, suite: Suite | None = None) -> str:
        bad = {c.id for c in self.unsupported(suite=suite)}
        lines = ["| Claim | Statement | Source | Check | Supported |",
                 "|---|---|---|---|---|"]
        for c in self.entries:
            lines.append(
                f"| {c.id} | {c.statement} | `{c.source}` | "
                f"{c.check or '—'} | {'no' if c.id in bad else 'yes'} |")
        return "\n".join(lines)


# ------------------------------------------------------------------- golden
@dataclass
class Comparison:
    ok: bool
    detail: str = ""


def pin(path, values: dict) -> Path:
    """Record a known-good state (V-04)."""
    path = Path(path)
    path.write_text(json.dumps(values, indent=2, sort_keys=True,
                               ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def compare(path, values: dict) -> Comparison:
    """Compare against a pinned state.

    Raises rather than creating the baseline if it is missing: a golden
    file that writes itself on first run pins whatever happened to be true
    that day, including a bug.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(
            f"no pinned baseline at {path}. Create it deliberately with "
            f"verify.pin() — a self-creating baseline pins whatever was true "
            f"the first time it ran, bug included.")
    want = json.loads(path.read_text(encoding="utf-8"))
    diffs = [f"{k}: pinned {want.get(k)!r}, got {values.get(k)!r}"
             for k in sorted(set(want) | set(values))
             if want.get(k) != values.get(k)]
    if diffs:
        return Comparison(False, "; ".join(diffs))
    return Comparison(True, f"{len(want)} pinned value(s) unchanged")


# ------------------------------------------------------------ traceability
_REQ_ID = re.compile(r"\*\*([TCSDXEV]-\d{2}[a-z]?)\*\*")


def traceability_gaps(*, requirement_ids: list | None = None,
                      root: Path | None = None) -> list:
    """Requirement IDs that no test mentions (V-03).

    Reads the IDs out of docs/requirements.md and greps the test suite
    for each. A requirement nobody tests is the gap this reports.
    """
    from .run import paths
    root = Path(root) if root else paths().root

    if requirement_ids is None:
        req = (root / "output" / "requirements.md")
        if not req.exists():
            return []
        requirement_ids = sorted(set(_REQ_ID.findall(
            req.read_text(encoding="utf-8"))))

    corpus = "\n".join(
        p.read_text(encoding="utf-8")
        for p in (root / "tests").rglob("test_*.py"))

    return [rid for rid in requirement_ids if rid not in corpus]
