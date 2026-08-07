# Architecture

> ## ⚠ INCOMPLETE — step 1 was re-opened on 2026-08-07
>
> A completeness check against eight use cases found all of them missing or
> materially under-covered, and exposed that the evidence base here was
> drawn from 32 of 1,692 transcripts. See
> [`use-cases.md`](use-cases.md) for what is missing and why the method
> failed. Nothing in this document is known to be *wrong*; it is
> systematically **incomplete**, and everything derived from it inherits
> the gap.


**Source:** step 3 of [`../input/task.md`](../input/task.md) — *"Define an
architecture for those."* Requirements are in
[`requirements.md`](requirements.md); the diagram is step 4.
**Basis:** [`problems.md`](problems.md), [`functions.md`](functions.md) as
revised by [`libraries.md`](libraries.md).
**Date:** 2026-08-07.

---

## 1. What this architecture is for

Not to compute statistics — `scipy` does that, correctly, and was verified
to produce the same p-values as the workspace's hand-rolled copies. The
architecture exists to make a specific class of *silent* failure
structurally impossible:

> A script runs to completion, prints a number, and the number is wrong.

Everything below follows from that one sentence. A design that merely
provided the same functions in one place would not have prevented a single
entry in `problems.md`, because the functions were never the problem —
`scipy.stats.false_discovery_control` existed the whole time and 11 of 15
scripts did not call it.

---

## 2. Seven architectural decisions

### AD-1 · One normalization boundary, at ingest

All text enters through `text.normalize`. Nothing downstream ever sees raw
bytes, a BOM, a bidi mark, or an unnormalized codepoint sequence.

*Because:* L-04, L-05, D-01–D-04. The defects were never in the comparison
code — they were in text that had already been mangled before comparison.
Normalization applied at each call site is normalization that will be
forgotten at one of them.

*Consequence:* `corpus.load` and `doc.read` are the **only** two entry
points for text. A function that takes a `str` from anywhere else is a
design error.

### AD-2 · Provenance travels with the value, not beside it

`Word`, `Hit`, `Result` and `Document` each carry their origin: corpus
source, version, content fingerprint, and — for anything resampled — the
seed and resample count.

*Because:* L-13, C-05. Nothing in the workspace records which corpus version
or which of 4 `random_point_scheme` variants produced a published number.
A manifest written *alongside* an output is a manifest that can be
separated from it; provenance carried *inside* the value cannot be.

*Consequence:* `Result.__format__` raises rather than printing a number
whose provenance is incomplete. This is the load-bearing mechanism of the
whole design (see §3).

### AD-3 · Borrowed computation, owned policy

Every statistical and conversion algorithm is imported. The library
contributes only constraints the upstream library does not enforce.

*Because:* the workspace reimplemented `scipy` 37 times in 20 mutually
different versions. But availability was never the gap — enforcement was.

*Consequence:* a wrapper is justified only if it adds a constraint. If a
proposed wrapper merely renames a scipy call, it does not get written.
`stats.permutation_test` exists solely to make `rng` required; it delegates
everything else.

### AD-4 · Fail at preflight, never mid-run

`run.preflight` verifies binaries, modules, fonts and corpus availability
before any work starts.

*Because:* E-05 (11×), E-07, E-02. Confirmed live in this environment: PDF
conversion was impossible until Typst was installed, and would have failed
only at the final step of a pipeline.

### AD-5 · Documents are typed data, not strings

`doc.read` returns a `Document`, not a `str`. Editing goes through
`doc.edit`, which matches on the normalized form and applies to the
original bytes.

*Because:* D-01, D-05, H-05 (74 failed edits). An invisible LRM in the file
that the caller's pattern does not reproduce is not a caller error — it is a
missing abstraction.

### AD-6 · Verdicts richer than pass/fail

`verify` supports `PASS`, `FAIL`, `PARTIAL`, `UNDECIDABLE`, `GUARD`.

*Because:* this vocabulary already exists in `test_seed_claims.py` and is
already used — two claims recorded as actively falsified, one as
*"UNDECIDABLE: corpora disagree; both encodings are pinned here."* A binary
framework would force that to be deleted or lied about.

### AD-7 · No orchestrator

The library provides no `run_analysis()`. Composition lives in the project
script.

*Because:* every generalization of "the whole pipeline" becomes a function
with thirty keyword arguments, and the task explicitly asks for
parameter-dependent functions rather than one per task — a mega-function is
the same failure wearing a different hat.

---

## 3. The central mechanism

Two invariants carry most of the design's value, and both are enforced by
the type rather than by discipline:

**A resampling function cannot be called without a seed.** `rng` is
positional-or-keyword with no default. `scipy.stats.permutation_test` will
happily run unseeded; the wrapper will not. Directly targets L-03 — 9
scripts, one of which reports a p-value that differs on every run.

**A p-value that belongs to a family cannot be printed until the family has
been adjusted.** `Result` knows whether it was produced alone or as one of
N. If N > 1 and `p_adjust` has not seen it, `__format__` raises.

That second one is the answer to the question `problems.md` could not
answer: *why did 11 of 15 scripts skip a correction that was one import
away?* Because producing 20 uncorrected p-values and producing 1 look
identical at the point of printing. The architecture makes them look
different.

---

## 4. Layers

Dependencies point downward only. A cycle is a defect.

| Layer | Modules | Role |
|---|---|---|
| **L4 — Claims** | `verify` | Ties a statement in a paper to a check that supports it |
| **L3 — Measurement** | `count`, `structure`, `doc.render` | Produces numbers and artifacts |
| **L2 — Typed access** | `corpus`, `doc` | The only two text entry points (AD-1) |
| **L1 — Foundation** | `text`, `schema`, `run` | Normalization, contracts, provenance, preflight |
| **L0 — Borrowed** | scipy, scikit-learn, pandas, networkx, matplotlib, pandoc+Typst, pytest, jsonschema, python-bidi | Computation and conversion |

`run` is used by every layer but depends on none — provenance and path
resolution are ambient, not injected.

### Module responsibilities

- **`text`** — `normalize`, `fold`, `same`, `marks`, `audit`, `open_text`,
  `configure_stdout`. Category-based (`Mn`/`Cf`/`Pd`/`Po` via
  `unicodedata.category`), never codepoint ranges.
- **`corpus`** — `load(source=...)` over WLC/BHSA/SP/LXX/SBLGNT/DSS behind
  one `Word` shape; `hits(homographs=...)`; `fingerprint()`. The only part
  with no free equivalent — `text-fabric` covers BHSA alone.
- **`doc`** — `read`/`write`/`edit`/`render`. Strip-on-read boundary in
  fixed order: BOM → line endings → Unicode normalization → `Cf` removal.
- **`count`** — `distribution(unit=...)`, `vocabulary`, `hapax`, `tfidf`,
  `similarity`. `unit` ∈ verse/chapter/book/speaker/panel/callable is the
  parameter that collapses most of S-02 and S-06.
- **`structure`** — `Scheme`, `cover`, `score`, `null_schemes(kind=...)`.
  Domain-specific; replaces 3 `build_space` and 4 `random_point_scheme`
  variants.
- **`stats`** — thin policy wrappers over scipy/sklearn. AD-3.
- **`schema`** — jsonschema-backed contracts validated at both ends.
- **`run`** — `paths`, `preflight`, `manifest`.
- **`verify`** — pytest-backed harness plus the `UNDECIDABLE` marker pytest
  lacks, and `claim()` linking paper sentences to checks.

---

## 5. Data flow

```
corpus source ─┐
               ├─► text.normalize ─► Word/Document ─► count/structure ─► Result ─► verify.claim
document ──────┘   (AD-1)            (carries          (borrowed        (refuses
                                      provenance,        computation,     to print
                                      AD-2)              AD-3)            unadjusted)
                                                                              │
                              run.preflight (AD-4) ─── run.manifest ──────────┘
```

Display marks are reintroduced only at `doc.render`, never upstream —
directly implementing the strip-on-read decision.

---

## 6. What the architecture does not address

Stated plainly, because a design claiming to solve these would be the false
confidence this project exists to avoid.

| Cause | Why it is out of scope |
|---|---|
| **C-07** — truncated generation (114 mid-stream cutoffs) | A library cannot detect that the script calling it was written by an interrupted response. Needs a pre-run integrity check outside the library. |
| **C-08** — validity defects | Nothing can mechanically determine that `*****` is circular, or that a count of ***** is wrong. `verify.claim` records the human judgment; it cannot supply it. |
| **Hebrew PDF render verification** | Established by measurement: text extracted from a *correct* pointed-Hebrew PDF is corrupted, losing and inventing characters. Only rasterization or a human can confirm it. |

---

## 7. Risks

1. ~~**`permutation_type` may not express the null models.**~~
   **RESOLVED 2026-08-07 by spike.** `permutation_test` indeed cannot — the
   structural null is not a relabelling of observed data. But
   `scipy.stats.monte_carlo_test` with a custom `rvs` expresses it exactly
   and reproduces the hand-rolled p-value to the digit (0.600570, difference
   0.000000). **AD-3 holds; `stats` stays a wrapper**, over two scipy entry
   points rather than one. The design's largest risk is closed.
2. **`corpus` is the only module with no free equivalent** and the largest
   to build — eight source formats behind one `Word` shape.
3. **The S-\* decomposition is an interpretation**, not a measurement.
   Everything here inherits it.
4. **`Result.__format__` raising is deliberately obstructive.** If it is
   experienced as noise, it will be worked around, and the central mechanism
   is lost. Requires an explicit, greppable escape hatch
   (`Result.unadjusted_value`) so bypassing is visible rather than casual.
