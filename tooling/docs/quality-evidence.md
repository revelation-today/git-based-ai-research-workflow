# Software-quality evidence

**Asked:** show evidence for software quality — static analysis, code
coverage, test coverage.
**Method:** every number below was produced by running a tool in this
repository on 2026-08-07. Nothing is asserted. Reproduce with
`bash scripts/quality.sh`.
**Environment:** Python 3.13.14, Windows 11.

---

## 1. Summary

| Measure | Tool | Result |
|---|---|---|
| Tests passing | pytest 9.1.1 | **137 / 137** |
| Statement coverage | coverage 7.15.4 | **92 %** (751 statements, 59 missed) |
| Type checking | mypy 2.3.0 | **0 errors** in 8 source files |
| Static analysis, production code | ruff 0.16.1 | **3 findings**, all reviewed and justified |
| Cyclomatic complexity | radon 6.0.1 | **A (3.54 average)** over 103 blocks |
| Maintainability index | radon 6.0.1 | **A** for every module (52.8 – 100) |
| Requirement traceability | `thscript.verify` | **0 gaps** over 40 requirement IDs |
| Fixture self-check | `tests/fixtures/check_fixtures.py` | **14 / 14** |
| Repository invariants | `scripts/check-repo-invariants.sh` | **pass**, 1 declared exemption |

---

## 2. Coverage, per module

```
Name                   Stmts   Miss  Cover   Missing
thscript/__init__.py       1      0   100%
thscript/corpus.py       104      5    95%   105-106, 123, 134, 212
thscript/schema.py        53      1    98%   47
thscript/verify.py       127      4    97%   84, 107, 121, 230
thscript/doc.py          140     11    92%   56, 87, 137, 228, 239, ...
thscript/text.py         102      9    91%   106, 154-155, 200, 203, ...
thscript/run.py          110     14    87%   54, 58, 62, 65-67, 81, ...
thscript/stats.py        114     15    87%   77, 136, 144, 243-246, ...
TOTAL                    751     59    92%
```

**What the 8 % is, honestly.** The uncovered lines are concentrated in two
places and neither is accidental:

- `run.py` — `Paths` convenience properties, and the `PackageNotFoundError`
  branch of `_library_versions`. Exercising the latter means uninstalling a
  dependency mid-test.
- `stats.py` — `agreement()` and `bootstrap_ci()` are **untested wrappers**.
  They are thin delegations to sklearn and scipy, but "thin" is what was
  said about the workspace's own duplicated helpers before three of them
  turned out to disagree. **Recorded as a real gap, not written off.**

**Coverage is not the interesting number here.** A suite can reach 100 %
and assert nothing — this repository has already produced two tests that
executed code and checked nothing (the identical-halves fixture, and TC-02).
Which is why the next section exists.

---

## 3. Evidence that the tests are not vacuous

The failure mode this project keeps rediscovering is a check that passes
without checking. Coverage cannot detect it. These can:

| Guard | What it proves |
|---|---|
| **Paired "can-fire" tests** — `TC-02b`, `TC-10b`, `TC-37d`, `TC-44b` | Every source-scanning test has a sibling asserting the scan detects a known-bad input. A scan that matches nothing proves nothing. |
| **Preconditions inside tests** | Where a test could pass vacuously it first asserts the fixture is actually defective — e.g. TC-01 asserts the legacy range *does* eat the maqaf before checking that `fold` does not. |
| **Fixture self-check** | `check_fixtures.py` verifies the *test data* still reproduces its defect. It caught a fixture whose two halves were identical. |
| **Negative controls** | `TC-07` asserts `audit()` reports **nothing** on a clean file, catching a detector that always fires. |
| **TDD order, evidenced** | Every module's tests were run and confirmed **red** before implementation. Recorded in the commit messages. |
| **Mutation-style spot check** | TC-02 was corrected, run to confirm it **failed** on the real violation, then the code was fixed. |

Three tests are **GUARDs** rather than tests of this code — they assert
facts about Unicode, the corpus and PDF extraction that the design depends
on. If one fails, the design is wrong, not the code.

---

## 4. Static analysis

Ruff over `thscript/ tests/ spikes/` with `E,F,W,B,UP,SIM,S,C4,RET,ARG,PTH`:
**267 findings, of which 220 are `S101` (use of `assert`) inside the test
suite** — where asserts are the point. That ruleset is meant for production
code; applying it to tests produces noise, and reporting 267 without saying
so would be misleading.

**Production code alone (`thscript/`) had 7. Four were fixed:**

| Finding | Action |
|---|---|
| `F401` unused `dataclasses.field` import | removed |
| `UP035` deprecated `typing.Callable` import | moved to `collections.abc` |
| `UP017` `datetime.timezone.utc` | now `datetime.UTC` |
| **`B905` `zip()` without `strict=`** | **fixed — real bug risk**: `p_adjust` zipped results against adjusted p-values, so a length mismatch would have silently truncated the family rather than raising |

**Three remain, each justified rather than suppressed:**

- `S603` subprocess without `shell=True` — the pandoc invocation. Arguments
  are built from validated paths, never from user text; `shell=True` would
  be the actual vulnerability.
- `SIM105` `try/except/pass` in `configure_stdout` — the suppression is
  deliberate and commented; a stream that cannot be reconfigured is not an
  error worth propagating from a convenience helper.
- `S105` "possible hardcoded password" on `PASS = "PASS"` in
  `verify.Verdict` — a false positive on an enum member.

**mypy: 0 errors.** Five findings were fixed to get there, and one was a
genuine annotation bug: `preflight` and `manifest` declared `list[str]`
parameters with `()` tuple defaults.

---

## 5. Complexity

```
103 blocks analysed — average cyclomatic complexity: A (3.54)
Maintainability index: A for all 8 modules (52.8 – 100)
```

No block rated worse than A. That is expected rather than impressive:
AD-3 ("borrowed computation, owned policy") means the genuinely complex
work lives in scipy, and what remains here is short policy code. It does
mean there is no hidden complexity hotspot.

---

## 6. What these numbers do *not* show

Stated because a quality report that only lists green metrics is the same
overclaiming this project was built to catch.

- **No mutation testing.** 92 % coverage and 129 green tests say the code
  runs and the assertions hold; they do not prove the assertions would fail
  if the code were wrong. `mutmut` or `cosmic-ray` would measure that. The
  manual guards in §3 are a substitute for it, not an equivalent.
- **No CI.** Nothing runs any of this except a human choosing to (W-7 in
  [`review-code.md`](review-code.md)). Every number here is from one
  machine, one Python, one OS.
- **`agreement()` and `bootstrap_ci()` are untested.**
- ~~Two known-critical design weaknesses are open~~ — **both fixed
  2026-08-08** (W-1, W-2). Worth keeping the original wording in mind
  though: the suite was green *while* the central mechanism could be
  bypassed by not calling `family()`. No metric on this page detected
  that. A review did.
- **The library covers round 1 only.** [`use-cases.md`](use-cases.md)
  records eight use cases with no implementation at all — so "92 % covered"
  means 92 % of what was built, which is roughly half of what is needed.
