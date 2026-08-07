"""Tests for thscript.run — TC-37..TC-41 (E-01..E-05).

Provenance and environment. These target the failures that cost the most
wall-clock in the survey: 30 FileNotFoundError from POSIX paths on Windows,
11 missing-binary failures discovered at the end of a pipeline, and the
complete absence of any record of which corpus version produced a number.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from thscript import run

REPO = Path(__file__).parent.parent


# ------------------------------------------------------------- TC-37, E-01
def test_tc37_paths_anchor_on_the_repo_root():
    p = run.paths()
    assert (p.root / "pyproject.toml").exists()
    assert p.root == REPO


def test_tc37b_paths_work_from_any_working_directory():
    """E-02/E-08: 16 scripts held absolute paths; others assumed cwd."""
    script = "from thscript import run; print(run.paths().root)"
    out = subprocess.run([sys.executable, "-c", script],
                         capture_output=True, text=True,
                         cwd=str(REPO / "tests" / "fixtures"),
                         env={**os.environ, "PYTHONPATH": str(REPO)})
    assert out.returncode == 0, out.stderr
    assert out.stdout.strip() == str(REPO)


def test_tc37c_no_absolute_paths_or_tmp_literals_in_package():
    """Parsed, not grepped — string constants only, so prose is exempt."""
    import ast
    import thscript
    offenders = []
    for f in Path(thscript.__file__).parent.rglob("*.py"):
        tree = ast.parse(f.read_text(encoding="utf-8"), filename=str(f))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
                continue
            v = node.value
            if v.startswith("/tmp") or (len(v) > 2 and v[1] == ":" and v[2] in "\\/"):
                offenders.append(f"{f.name}:{node.lineno}: {v!r}")
    assert not offenders, f"absolute/tmp path literals: {offenders}"


def test_tc37d_that_scan_can_fire():
    import ast
    tree = ast.parse('x = "/tmp/out.txt"\ny = "C:\\\\Users\\\\x"\nz = "rel/path"')
    hits = [n.value for n in ast.walk(tree)
            if isinstance(n, ast.Constant) and isinstance(n.value, str)
            and (n.value.startswith("/tmp")
                 or (len(n.value) > 2 and n.value[1] == ":" and n.value[2] in "\\/"))]
    assert len(hits) == 2, f"scan should flag both bad literals, got {hits}"


# ------------------------------------------------------------- TC-38, E-02
def test_tc38_preflight_names_the_missing_thing():
    with pytest.raises(run.PreflightError) as e:
        run.preflight(binaries=["definitely-not-a-real-binary-xyz"])
    assert "definitely-not-a-real-binary-xyz" in str(e.value)


def test_tc38b_preflight_names_a_missing_module():
    with pytest.raises(run.PreflightError) as e:
        run.preflight(modules=["no_such_module_xyz"])
    assert "no_such_module_xyz" in str(e.value)


def test_tc38c_preflight_passes_when_everything_is_present():
    run.preflight(modules=["numpy", "scipy"])       # must not raise


def test_tc38d_preflight_reports_everything_missing_at_once():
    """Fixing one missing dependency at a time is the slow failure mode."""
    with pytest.raises(run.PreflightError) as e:
        run.preflight(binaries=["nope-a"], modules=["nope_b"])
    msg = str(e.value)
    assert "nope-a" in msg and "nope_b" in msg


# ------------------------------------------------------------- TC-39, E-03
def test_tc39_manifest_is_complete(tmp_path):
    m = run.manifest(seed=42, corpora={"test": "abc123"},
                     inputs=[REPO / "pyproject.toml"],
                     outputs=[tmp_path / "result.csv"])
    d = m.as_dict()
    for key in ("seed", "corpora", "inputs", "outputs", "libraries",
                "python", "platform", "created"):
        assert key in d, f"manifest missing {key}"
    assert d["seed"] == 42
    assert d["corpora"]["test"] == "abc123"


def test_tc39b_manifest_hashes_inputs():
    m = run.manifest(seed=1, corpora={}, inputs=[REPO / "pyproject.toml"])
    entry = m.as_dict()["inputs"][0]
    assert len(entry["sha256"]) == 64


def test_tc39c_manifest_writes_next_to_its_output(tmp_path):
    out = tmp_path / "result.csv"
    out.write_text("x\n", encoding="utf-8")
    m = run.manifest(seed=1, corpora={}, outputs=[out])
    path = m.write()
    assert path.exists()
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert loaded["seed"] == 1


def test_tc39d_manifest_records_library_versions():
    m = run.manifest(seed=1, corpora={})
    libs = m.as_dict()["libraries"]
    assert "scipy" in libs and "numpy" in libs


# ------------------------------------------------------------- TC-40, E-04
def test_tc40_same_seed_same_bytes(tmp_path):
    """Two runs with the same seed must be byte-identical."""
    from thscript import stats

    def produce(path):
        r = stats.permutation_test(
            ([1.0, 2, 3, 4, 5], [2.0, 3, 4, 5, 9]),
            statistic=lambda x, y, axis=0: x.mean(axis=axis) - y.mean(axis=axis),
            rng=99, n=500, corpus="test@0")
        path.write_text(f"{r.p!r}\n", encoding="utf-8")

    a, b = tmp_path / "a.txt", tmp_path / "b.txt"
    produce(a)
    produce(b)
    assert a.read_bytes() == b.read_bytes()


# ------------------------------------------------------------- TC-41, E-05
def test_tc41_skipped_records_are_counted_not_swallowed():
    """L-12: 9 scripts had a bare pass in an except."""
    tally = run.Tally("parse")
    for value in ["1", "2", "not-a-number", "4"]:
        with tally.attempt(value):
            int(value)
    assert tally.ok == 3
    assert tally.skipped == 1
    assert "not-a-number" in tally.report()


def test_tc41b_tally_raises_if_everything_failed():
    tally = run.Tally("parse")
    for value in ["a", "b"]:
        with tally.attempt(value):
            int(value)
    with pytest.raises(run.AllFailedError):
        tally.check()


def test_tc41c_no_bare_pass_in_an_except_in_the_package():
    import ast
    import thscript
    offenders = []
    for f in Path(thscript.__file__).parent.rglob("*.py"):
        src = f.read_text(encoding="utf-8")
        tree = ast.parse(src, filename=str(f))
        lines = src.splitlines()
        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler) and \
                    all(isinstance(s, ast.Pass) for s in node.body):
                # a documented deliberate no-op is allowed if it says so
                context = "\n".join(lines[node.lineno - 1:node.end_lineno])
                if "pragma: no cover" not in context:
                    offenders.append(f"{f.name}:{node.lineno}")
    assert not offenders, f"silently swallowed exceptions: {offenders}"
