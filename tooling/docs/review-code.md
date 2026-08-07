# Senior developer review

**Source:** item 7 of [`../input/task.md`](../input/task.md) — propose
refactors of code, requirements and tests; find weaknesses; propose
solutions; and design how other AIs report to this repository.
**Date:** 2026-08-07. **Suite at review time:** 129 passing.

Findings are ordered by severity. Each was **reproduced**, not inferred.

---

## W-1 · The central mechanism is opt-in — *critical*

`architecture.md` §3 calls this the design's load-bearing invariant: a
p-value belonging to a family of N>1 cannot be printed until `p_adjust`
has seen it. Reproduced:

```
3 p-values, family() not called -> all format: True
```

**The gate only engages if the caller declares the family.** Anyone who
produces twenty p-values in a loop and never calls `stats.family()` gets
exactly the behaviour L-02 describes, silently. The mechanism protects the
careful — who did not need protecting — and misses the case it was built
for.

This is the same shape as every other defect in this project: *the check
exists, and does not fire.*

**Proposals** (need a decision; 3 is my recommendation):

1. **Track at module level.** `stats` counts p-values produced per process
   and refuses to format any of them once the count exceeds 1 without an
   adjustment. Catches everything; annoying for genuinely independent
   tests in one script.
2. **Require an explicit family always** — every producing call takes
   `family=` (a label, or `"solo"`). Explicit, no magic, but changes every
   signature and can be answered thoughtlessly.
3. **Default to guarded, opt out loudly.** Producing functions return a
   Result already marked as belonging to an *undeclared* family; a lone
   result formats only after `stats.solo(r)` or membership in a declared
   family. Inverts the default so the unguarded path is the one you have
   to ask for.

**Requirement change:** S-03 says "produced as one of N>1", which assumes
someone declared N. It should say the guard applies **unless** the caller
has declared singularity.

---

## W-2 · Provenance is auto-satisfied with a placeholder — *critical*

```
corpus omitted -> 'unspecified' | formats anyway: True
```

R3 and S-05 require a Result to carry a corpus fingerprint. Every
producing function ends with `corpus or "unspecified"`, so omitting it
yields a string that satisfies the check and means nothing. The
`ProvenanceError` path is unreachable in practice.

**Proposal:** drop the default. `corpus=` becomes required, exactly as
`rng` is, and takes a `Corpus` (whose `fingerprint()` is read) or an
explicit `corpus="none: <reason>"`. Same discipline as `rng`, same
justification, and it was inconsistent to apply it to one and not the
other.

---

## W-3 · Traceability counts a mention as a test

`verify.traceability_gaps()` greps the test files as plain text for each
requirement ID. A requirement named in a comment, a docstring, or a
`-k` selector counts as covered. It reports `[]` today — but it would
report `[]` for a suite of empty test bodies that merely mention the IDs.

**Proposal:** parse with `ast`, collect IDs only from test-function
docstrings and decorators, and additionally assert the named test
*contains at least one assertion*. Then V-03 means what it says.

---

## W-4 · `corpus` advertises eight sources and implements one

`_LOADERS` registers `osis` and `wlc-oshb` (the same parser).
`architecture.md` and `functions.md` both describe unification across
WLC / BHSA / SP / LXX / SBLGNT / DSS, and `C-01`'s test asserts "the same
assertion runs against ≥2 sources" — satisfied by calling the *same*
loader twice.

Nothing is wrong in the code; the **documentation overstates it**, and the
test that should have caught the overstatement is satisfiable by aliasing.

**Proposal:** mark the six unimplemented sources explicitly in `_LOADERS`
as `NotImplemented` with a message naming what is missing, so `load()`
fails informatively rather than with a generic "unknown source". Restate
C-01's test to require two *structurally different* formats, and skip it
until a second reader exists — a skip with a reason is honest; a pass by
aliasing is not.

---

## W-5 · `audit()` silently weakens when given a `str`

BOM and line-ending detection are byte facts. Passing a `str` skips both
checks and returns a shorter, quieter report with no indication that two
detectors did not run.

**Proposal:** accept `str` but include a `Finding("not-checked", …)` naming
the checks that could not run. A quieter report that looks the same as a
clean one is the failure mode this whole project studies.

---

## W-6 · Unreadable type check in `schema`

```python
if not isinstance(got, want) or isinstance(got, bool) is not (want is bool):
```

Correct — I traced all four cases — but nobody should have to. It exists
to stop `True` satisfying an `int` field.

**Proposal:** extract `_type_ok(value, want)` with the bool case named and
commented.

---

## W-7 · Nothing runs the checks except a human remembering

`.claude/settings.json` runs the invariant script after commits made
*through the AI*. A direct `git commit`, or any clone, runs nothing. The
suite, the fixture self-check, the IP scan and traceability all depend on
someone choosing to run them — and CM-7 showed what happens to a check
nobody watches.

**Proposal:** a GitHub Actions workflow running all five checks on push.
The repository is private; Actions works there. Worth doing before the
public export, so the public repo shows its own status.

---

## W-8 · Test-quality issues found while reviewing

- **TC-02 was vacuous** and is fixed in this pass — see below.
- `test_tc11b` "the same assertion runs against any source" calls one
  loader twice (W-4).
- Render tests **skip** when no PDF engine is present. A skip is reported
  but not counted as a gap; a run showing `125 passed, 4 skipped` reads as
  green. `check_repo` now asks for skips to be reported explicitly; the
  suite itself should fail if the engine is absent in CI.

---

## Fixed during this review

**TC-02 was vacuous, and there was a real T-01 violation behind it.**

`thscript/doc.py:196` contained `[֐-׿יִ-ﭏ]` — a hardcoded Hebrew codepoint
range, inside `for_display`. That is precisely what requirement T-01
forbids, in the package built to eliminate that defect class.

TC-02 could not see it. An earlier fix had made the scan skip **all string
tokens**, to silence a false positive from `text.py`'s docstring quoting
the legacy range — and a regex literal is a string, so the only place a
range can occur became the one place the test could not look. Fixing a
false positive created a false negative.

Both are now fixed, in TDD order: the test was corrected first (exempting
**docstrings specifically**, via `ast`, rather than strings generally), run
to confirm it *failed* on `doc.py:196`, then `for_display` was rewritten to
detect Hebrew runs by character name and combining class. Verified: 4 marks
added where expected, and `strip_invisible` round-trips exactly.

---

## Proposed requirement changes

| Req | Change | Why |
|---|---|---|
| **S-03** | Guard applies unless singularity is *declared*, not only when a family is | W-1 |
| **S-05** | `corpus` required, no placeholder default | W-2 |
| **V-03** | Traceability must parse, and require an assertion in the named test | W-3 |
| **C-01** | Two *structurally different* formats, or an honest skip | W-4 |
| **T-06** | `audit()` must report which checks could not run | W-5 |
| **new E-06** | All five checks run in CI on push | W-7 |

---

## The inter-AI reporting protocol

Asked: how should *other* AIs report errors or request extensions, how are
those evaluated, and how do they fetch status?

### Why a protocol rather than an issue tracker

The reporting AI is working in a *different* repository — one of the
sibling research projects — and hits a defect or a missing capability in
`thscript`. Three constraints follow directly from this project's own
findings:

1. **A report is untrusted input.** `CLAUDE.md` already says content this
   repository reads may not direct its actions. A report may describe a
   bug; it may not instruct a push, an edit, or a merge.
2. **A report must not carry sibling IP.** `DEPARTMENT-RULES.md` §1 applies
   in full — the reporter must send the *defect shape*, never the research
   material it was found in.
3. **A report must be reproducible or say it is not.** The entire history
   of this repository is claims falsified by measurement. An unreproducible
   report is a lead, not a finding.

### Shape

A report is a **file, committed by a human**, not an API call:

```
reports/
  incoming/   RPT-<yyyymmdd>-<slug>.json     ← the reporting AI writes here
  status.json                                ← generated; what reporters read
```

`RPT-*.json` validates against a `thscript.schema` contract:

```jsonc
{
  "schema": "ai-report", "version": 1,
  "id": "RPT-20260807-fold-drops-final-form",
  "kind": "defect",              // defect | extension | question
  "reporter": "claude-opus-5 in project-a",
  "summary": "fold() drops a final-form letter when maqaf='separator'",
  "repro": {
    "code": "from thscript import text; text.fold('...', maqaf='separator')",
    "expected": "…", "observed": "…",
    "thscript_version": "0.1.0", "python": "3.13.14"
  },
  "ip_declaration": "synthetic input; no sibling research content",
  "severity_claimed": "high"
}
```

`repro.code` must be **runnable and synthetic**. A report whose reproducer
needs a sibling corpus is rejected on IP grounds, not evaluated.

### Evaluation — the same discipline as everything else

A reviewing pass on `reports/incoming/`:

1. **Schema-validate.** Malformed → `rejected: malformed`.
2. **IP scan** with `check-ip-boundary.sh`. Any sibling reference →
   `rejected: ip`, and the reporter is told to resend a synthetic
   reproducer.
3. **Run the reproducer.** Verdict uses the existing vocabulary:
   `PASS` (reproduced — it is a real defect), `FAIL` (does not reproduce),
   `PARTIAL`, `UNDECIDABLE` (environment-dependent), `GUARD` (reveals an
   external assumption). **No report is accepted on description alone** —
   that is the rule this repository has had to relearn four times.
4. **A reproduced defect becomes a failing test first**, then a fix. TDD,
   as everything else here.
5. Extensions are triaged against `docs/use-cases.md`, not accepted
   ad hoc.

### Fetching status

`reports/status.json` is regenerated on each evaluation and is the only
thing a reporter needs to read:

```jsonc
{ "schema": "ai-report-status", "version": 1,
  "generated": "2026-08-07T…",
  "reports": [
    { "id": "RPT-20260807-fold-drops-final-form",
      "state": "accepted",           // received|rejected|reproduced|accepted|fixed|declined
      "verdict": "PASS",
      "reason": "reproduced; test TC-47 added",
      "fixed_in": "0.1.1", "test": "tests/test_text.py::test_tc47_…" } ] }
```

A reporting AI polls one file by its own `id`. No API, no auth, no server
— it works over a git clone, which is what these agents already have.

**States are terminal or actionable, never silent.** `declined` carries a
reason. A report that cannot be reproduced is *recorded as such* rather
than dropped, because — as `verify.Verdict.FAIL` already encodes — a
falsified claim is a finding, not an absence.

### What this deliberately does not do

- **No automatic acceptance.** A report is a proposal; applying it is an
  AI-request cycle with a human confirming, exactly as `CLAUDE.md` requires.
- **No write access for reporters.** They open a pull request or hand a
  file to a human. Nothing in this design lets a remote agent mutate this
  repository.
- **No trust in claimed severity.** `severity_claimed` is recorded and
  ignored during triage; severity is assigned by reproduction.
