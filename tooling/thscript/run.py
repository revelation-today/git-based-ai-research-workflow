"""Execution environment and provenance — the C-04/C-05 module.

Three jobs, each targeting a measured failure:

``paths``      resolve everything from a discovered repository root, so no
               script carries an absolute path (16 did) or assumes ``/tmp``
               exists (which on Windows produced ``PermissionError`` on a
               file literally named ``/tmp_out.txt``).
``preflight``  check binaries, modules and fonts *before* work starts. The
               survey recorded 11 failures for a missing ``pdftoppm`` and 6
               for missing modules, all discovered at the end of a run.
``manifest``   record seed, corpus fingerprints, input hashes and library
               versions beside every output. No script in the survey
               recorded any of this, so no published number can be
               re-derived.

``Tally`` covers the fourth: a parse failure absorbed by a bare ``except:
pass`` (9 scripts) means a total computed from fewer records than intended,
reported as if complete.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import platform
import shutil
import sys
from collections.abc import Sequence
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, UTC
from pathlib import Path

__all__ = ["paths", "Paths", "preflight", "PreflightError", "manifest",
           "Manifest", "Tally", "AllFailedError"]

_ROOT_MARKERS = ("pyproject.toml", ".git")


class PreflightError(RuntimeError):
    """Raised before any work starts, naming everything that is missing."""


class AllFailedError(RuntimeError):
    """Raised when every record in a tallied loop failed."""


@dataclass(frozen=True)
class Paths:
    root: Path

    @property
    def tests(self) -> Path:
        return self.root / "tests"

    @property
    def fixtures(self) -> Path:
        return self.root / "tests" / "fixtures"

    @property
    def output(self) -> Path:
        return self.root / "output"

    def scratch(self, name: str) -> Path:
        d = self.root / ".scratch"
        d.mkdir(exist_ok=True)
        return d / name


def paths(start: Path | None = None) -> Paths:
    """Discover the repository root by walking up for a marker file.

    Never returns a hardcoded location, so the same code works from any
    working directory and on any machine (E-01).
    """
    here = Path(start or __file__).resolve()
    for candidate in (here, *here.parents):
        if candidate.is_dir() and any(
                (candidate / m).exists() for m in _ROOT_MARKERS):
            return Paths(candidate)
    raise RuntimeError(
        f"no repository root above {here}: expected one of {_ROOT_MARKERS}")


def preflight(*, binaries: Sequence[str] = (), modules: Sequence[str] = (),
              paths_exist: Sequence[Path] = ()) -> None:
    """Fail now, with everything that is missing, rather than mid-run.

    Reports *all* problems at once: discovering missing dependencies one at
    a time is the slow version of this failure.
    """
    missing: list[str] = []

    for b in binaries:
        if shutil.which(b) is None:
            missing.append(f"binary {b!r} not on PATH")
    for m in modules:
        if importlib.util.find_spec(m) is None:
            missing.append(f"python module {m!r} not importable")
    for p in paths_exist:
        if not Path(p).exists():
            missing.append(f"path {str(p)!r} does not exist")

    if missing:
        raise PreflightError(
            "preflight failed before any work started:\n  - "
            + "\n  - ".join(missing))


@dataclass
class Manifest:
    """Provenance recorded beside an output (E-03).

    Carries what makes a number re-derivable a year later: the seed, each
    corpus's fingerprint, the hash of every input, and the versions of the
    libraries that did the computing.
    """
    seed: int | None
    corpora: dict
    inputs: list = field(default_factory=list)
    outputs: list = field(default_factory=list)
    created: str = ""

    def as_dict(self) -> dict:
        return {
            "seed": self.seed,
            "corpora": dict(self.corpora),
            "inputs": [
                {"path": str(p), "sha256": _sha256(p)}
                for p in self.inputs if Path(p).exists()
            ],
            "outputs": [str(p) for p in self.outputs],
            "libraries": _library_versions(),
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "created": self.created,
        }

    def write(self, path: Path | None = None) -> Path:
        """Write beside the first output, or to an explicit path."""
        if path is None:
            if not self.outputs:
                raise ValueError("no outputs: pass an explicit path")
            first = Path(self.outputs[0])
            path = first.with_suffix(first.suffix + ".manifest.json")
        path = Path(path)
        path.write_text(
            json.dumps(self.as_dict(), indent=2, ensure_ascii=False),
            encoding="utf-8")
        return path


def manifest(*, seed: int | None, corpora: dict,
             inputs: Sequence = (), outputs: Sequence = ()) -> Manifest:
    return Manifest(seed=seed, corpora=dict(corpora), inputs=list(inputs),
                    outputs=list(outputs),
                    created=datetime.now(UTC).isoformat())


def _sha256(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _library_versions() -> dict:
    import importlib.metadata as md
    out = {}
    for name in ("numpy", "scipy", "scikit-learn", "statsmodels", "pandas",
                 "jsonschema", "pypandoc", "python-bidi"):
        try:
            out[name] = md.version(name)
        except md.PackageNotFoundError:
            continue
    return out


@dataclass
class Tally:
    """Count what was skipped instead of swallowing it (E-05, L-12).

        tally = Tally("parse")
        for row in rows:
            with tally.attempt(row.id):
                parse(row)
        tally.check()

    A run that silently processed 900 of 1000 records and reported a total
    is the failure this prevents.
    """
    name: str
    ok: int = 0
    failures: list = field(default_factory=list)

    @property
    def skipped(self) -> int:
        return len(self.failures)

    @contextmanager
    def attempt(self, label):
        try:
            yield
        except Exception as exc:
            self.failures.append((label, f"{type(exc).__name__}: {exc}"))
        else:
            self.ok += 1

    def report(self) -> str:
        lines = [f"{self.name}: {self.ok} ok, {self.skipped} skipped"]
        for label, why in self.failures:
            lines.append(f"  skipped {label!r}: {why}")
        return "\n".join(lines)

    def check(self, *, max_skipped: int | None = None) -> None:
        if self.ok == 0 and self.failures:
            raise AllFailedError(self.report())
        if max_skipped is not None and self.skipped > max_skipped:
            raise RuntimeError(
                f"too many skipped records\n{self.report()}")
