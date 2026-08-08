# Generalized function list

> ## ⚠ INCOMPLETE — step 1 was re-opened on 2026-08-07
>
> A completeness check against eight use cases found all of them missing or
> materially under-covered, and exposed that the evidence base here was
> drawn from 32 of 1,692 transcripts. See
> [`use-cases.md`](use-cases.md) for what is missing and why the method
> failed. Nothing in this document is known to be *wrong*; it is
> systematically **incomplete**, and everything derived from it inherits
> the gap.


**Source:** step 2 of [`../input/task.md`](../input/task.md).
**Basis:** [`problems.md`](problems.md) situations S-01..S-13 and root causes
C-01..C-09, plus the duplication analysis below.
**Date:** 2026-08-07.

Proposed package name `thscript` throughout, purely so signatures read
unambiguously. Every function is traced to the situations it replaces and
the defects it removes; anything that fixes nothing real is not here.

> ## ⚠ Superseded in part by [`libraries.md`](libraries.md)
>
> A library-validation pass (proposal `0005`) executed every candidate
> against free public libraries and found that **most of this list already
> exists**. Read [`libraries.md`](libraries.md) alongside this document.
> The two changes that matter:
>
> - **§5 `thscript.stats` should not be built.** `scipy.stats` provides
>   `permutation_test`, `false_discovery_control`, `combine_pvalues`,
>   `bootstrap`, `hypergeom`, `binomtest`, `fisher_exact`; sklearn provides
>   `cohen_kappa_score`, `TfidfVectorizer`, `cosine_similarity`. scipy's
>   `permutation_test` was **verified to use the same (k+1)/(n+1)
>   estimator** as the workspace's copies, so adopting it moves no
>   published p-value.
> - **§2 `text.fold` needs no codepoint ranges.** `unicodedata.category`
>   already classifies them: `Mn` is exactly vowels+cantillation, `Cf` is
>   exactly the invisible/bidi set, and **MAQAF is `Pd`** — which is
>   precisely why the hardcoded U+0591–U+05C7 range was wrong. Rule R1
>   below is right; the implementation should be one stdlib call, not a
>   maintained table.
>
> Net: **~55 functions → roughly 18 genuinely ours.** What survives is the
> policy layer — required `rng`, provenance-carrying `Result`, enforced
> p-adjustment — because scipy enforces none of those, and the workspace's
> evidence shows availability was never the problem: `false_discovery_control`
> existed the whole time and 11 of 15 scripts still did not call it.

---

## 0. Why a library, measured

The case does not rest on taste. The same seven concepts appear **37 times
across the scripts in 20 mutually different implementations**:

| Concept | Copies | Distinct implementations |
|---|---|---|
| `pval` — permutation p-value | 8 | **3** |
| `build_space` — candidate point space | 9 | **3** |
| `joint_region` — joint marker statistic | 5 | **3** |
| `random_point_scheme` — null scheme generator | 5 | **4** |
| `fish` — Fisher combination | 4 | **3** |
| `cover` — window coverage mask | 3 | 2 |
| `cosine` — cosine similarity | 3 | 2 |
| **Total** | **37** | **20** |

Two examples of what the divergence actually means:

- `pval` in `run_align.py` is `(count(x >= obs) + 1)/(n + 1)`; in
  `run_levels.py` it takes a `lower_is_better` parameter and branches. The
  second is a strict generalization of the first — **exactly the
  parameter-dependent shape this step is asked to produce**, arrived at
  independently and then not shared.
- `fish` returns *(chi², p)* in `run2.py`, but only *chi²* in `run3.py` and
  `run4.py`. Callers must know which variant they imported.

`build_space` and `random_point_scheme` — which determine the null
distribution every p-value in the ***** work is measured against —
exist in 3 and 4 different versions respectively. Nothing records which
version produced which published number.

**This is the argument for the library, stated without exaggeration:** not
that the code is bad, but that the same statistic is computed by several
different functions with the same name, and no reader can tell which.

---

## 1. Design rules

Six rules, each traceable to a measured defect. They constrain every
signature below.

| # | Rule | Because |
|---|---|---|
| R1 | **No raw codepoint ranges in a public API.** Callers name *categories* (`points`, `cantillation`, `punctuation`); the range lives in one tested place. | L-04: an over-wide range copied verbatim from upstream into AI-authored code |
| R2 | **`rng` is a required argument with no default.** A function that resamples cannot be called without a seed. | L-03: 9 unseeded scripts, one reporting a p-value |
| R3 | **A result object carries its own provenance** — seed, n, corpus version, adjustment status — and refuses to format as a bare number. | L-13, C-05: no script records corpus version |
| R4 | **Normalize on read, compare only normalized.** Generalizes the existing `tf_parse.norm` rule. | D-01..D-04, L-05, and your strip-on-read decision |
| R5 | **Every cross-script file has a declared schema, validated at both ends.** | E-03 (24 `KeyError`), L-14 |
| R6 | **Exact where exact exists**; Monte-Carlo only when there is no closed form, and it says so. | L-10 |

---

## 2. `thscript.text` — Unicode  ·  C-01

Replaces the hand-rolled stripping in `wlc.py`, `concordance.py`,
`tf_parse.py`, `build.py`. Fixes L-04, L-05, L-06, D-01..D-04, E-01, E-06, E-09.

```python
normalize(s, *, form="NFD", strip=("bidi", "invisible"),
          points=False, cantillation=False, presentation=True) -> str
```
The single entry point. `strip` names *categories*, never ranges (R1).
`presentation=True` folds U+FB1D–FB4F presentation forms — the case
`tf_parse.norm` documents as silently breaking raw `==`.

```python
fold(s, *, points=True, cantillation=True, punctuation=False,
     maqaf="separator") -> str
```
The correct replacement for `re.sub(r"[֑-ׇ]", "", s)`.
`maqaf=` is explicit — `"separator"` (split into two tokens), `"keep"`, or
`"strip"` — because the buggy range silently chose `"strip"` and nobody
could see it. Same for `paseq` and `sof_pasuq`.

```python
same(a, b, **normalize_opts) -> bool
sort_key(s, *, script="auto") -> tuple
```
`same` is the promotion of `tf_parse.same` to the rule everywhere: *never
raw `==` on Hebrew or Greek*.

```python
marks(s) -> list[Mark]          # (index, codepoint, name, category)
audit(s) -> Report              # invisible chars, mixed line endings, BOM, non-NFC
```
Diagnostic, not corrective. `marks()` is what would have surfaced the 5,902
LRM characters the first time anyone looked at a document.

```python
open_text(path, mode="r", *, encoding="utf-8", newline="\n", bom=False)
configure_stdout()              # UTF-8 regardless of console codepage
```
Fixes E-01 (≈90 `UnicodeEncodeError`) and E-09 at the boundary, once,
instead of the 28 scripts that each remembered `sys.stdout.reconfigure`
and the 18 that call `open()` with no `encoding=`.

---

## 3. `thscript.corpus` — Corpus access  ·  S-01

Replaces `wlc.py`, `tf_parse.py`, `morphhbXML-to-JSON.py`, `lxx.py`,
`dss.py`, `sp.py`, `lex.py`, `egypt.py` — 8 parsers, one interface.

```python
load(source, *, version=None, cache=True, normalize=True) -> Corpus
```
`source` ∈ `{"wlc-oshb", "bhsa", "sp", "lxx-morph", "sblgnt", "dss",
"strongs-heb", "strongs-grk"}`. **This is the central parameterization**:
`test_seed_claims.py` already runs the same claim against MT, SP and LXX
by hand-instantiating three different classes.

```python
Corpus.verse(ref) -> list[Word]
Corpus.words(*, scope=None, lemma=None, strongs=None, morph=None) -> Iterator[Word]
Corpus.text(ref, *, points=True, normalize=True) -> str
Corpus.version -> str
Corpus.fingerprint() -> str        # content hash — R3, fixes L-13
```

```python
Word = NamedTuple(ref, surface, lemma, strongs, morph, slot)
ref_parse(s) / ref_range(book, lo, hi) / ref_sort_key(ref)
```
One `Word` shape across all eight sources is what makes a cross-corpus
comparison a parameter rather than a rewrite.

**Homographs are a parameter, not a silent policy.** `wlc.py`'s docstring
already records that OSHB gives ******* one lemma where BHSA gives two, and
`test_seed_claims.py` records the resulting claim as `UNDECIDABLE`. So:

```python
hits(corpus, *, lemma=None, strongs=None, root=None, morph=None,
     scope=None, homographs="all", normalize=True) -> list[Hit]
```
`homographs` ∈ `{"all", "split", "strict"}`, and a `Hit` set knows which
policy produced it.

---

## 4. `thscript.count` — Counting and distribution  ·  S-02, S-05, S-07

Replaces `concordance.py` ×2, `attestation.py`, `r5_genesis.py`,
`07_hapax.py`, `14_tfidf_chapter.py`, `01_similarity.py` ×2,
`09_register_progression.py`.

```python
distribution(hits, *, unit="chapter", normalize_by=None) -> Distribution
```
`unit` ∈ `{"verse", "chapter", "book", "speaker", "panel", callable}`.
**This one parameter collapses most of S-02 and S-06's per-unit variants**,
which are otherwise separate scripts differing only in how they bucket.

```python
vocabulary(units, *, key="lemma", normalize=True) -> dict
hapax(units, *, scope="corpus", per=1000) -> Result
tfidf(units, *, key="lemma", sublinear=False, smooth=True) -> Matrix
similarity(a, b, *, metric="cosine") -> Result
matrix(units, *, metric="cosine") -> Matrix
```
`metric` ∈ `{"cosine", "jaccard", "jensen-shannon", "euclidean"}` — the two
divergent `cosine` implementations become one argument.

`key=` accepts `"lemma" | "strongs" | "surface" | "root" | callable`, which
is the difference between several existing scripts.

---

## 5. `thscript.stats` — Statistics  ·  S-04, S-10

The most important module, because it is where wrong answers are most
expensive. Replaces the 37 copies in §0. Fixes L-02, L-03, L-10.

```python
rng(seed) -> Generator                     # R2: no default, ever
```

```python
permutation_test(observed, *, resample, statistic, n=20_000, rng,
                 alternative="greater", plus_one=True) -> Result
```
One function for all 8 `pval` copies. `alternative` ∈
`{"greater", "less", "two-sided"}` subsumes `run_levels.py`'s
`lower_is_better`. `plus_one=True` is the default because every correct
copy in the workspace already uses the +1 estimator; setting it `False`
requires saying so.

```python
exact_test(kind, **params) -> Result
```
`kind` ∈ `{"hypergeometric", "binomial", "fisher-exact", "chi2"}`. **R6:**
`08_monte_carlo.py` states in its own docstring that its quantity is
hypergeometric and then simulates it. This function is what it should have
called.

```python
p_adjust(pvals, *, method="bh", q=0.05) -> Adjusted
combine(pvals, *, method="fisher") -> Result
```
`method` ∈ `{"bh", "bonferroni", "holm", "by"}`. **Four scripts already
implement Benjamini-Hochberg in 3 divergent versions** (`bh` in
`run_levels.py` and `run_rows.py`; `bh_correction` in `r5_v2_books.py` and,
differently again, in `r5_v2_structures.py`). This makes one of them
canonical.

```python
agreement(a, b, *, method="cohen", weights=None) -> Result
bootstrap_ci(data, *, statistic, n=10_000, rng, level=0.95) -> Interval
```

### The `Result` object is the point

```python
Result.value          # the statistic
Result.p              # p-value, or None
Result.n              # resamples, or None
Result.seed           # R2
Result.corpus         # (source, version, fingerprint) — R3
Result.adjusted       # None until p_adjust has seen it
Result.method         # "permutation" | "exact:hypergeometric" | ...
Result.__format__     # raises if .p is set, .adjusted is None,
                      # and this Result was one of several
```

That last line is the mechanism, not a decoration. **L-02's real failure was
not "nobody knows about FDR" — four scripts did. It was that producing 20
p-values and reporting them uncorrected is indistinguishable, in the output,
from producing one.** A family of p-values that has not been through
`p_adjust` cannot be printed. That is a check a script cannot forget.

---

## 6. `thscript.structure` — Structural hypotheses  ·  S-03

Replaces `schemes.py`, `panels.py`, `run_cycle/levels/rows/align/confine/
direction.py`, the 16 `*****/tools/*.py`, and the `******/run*.py` family.

```python
Scheme(name, boundaries, *, unit="verse") 
cover(points, *, window, n) -> ndarray[bool]
score(scheme, markers, *, window=2, statistic="hits") -> Result
```

```python
null_schemes(kind, *, rng, n, constraints=None) -> Iterator[Scheme]
```
`kind` ∈ `{"random_points", "shuffle", "block_bootstrap", "rotation"}`.
**This replaces the 4 divergent `random_point_scheme` implementations and
the 3 `build_space` ones** — the functions that define what every
***** p-value is measured against.

```python
marker_set(name, *, kind="boundary"|"content", source=...) -> Markers
Markers.independent_of(other) -> bool | None
```
`independent_of` returns `None` for "cannot be determined mechanically" —
the honest answer for L-09's self-labelled `# CIRCULAR` marker, and a place
to record the judgment rather than leave it in a comment.

---

## 7. `thscript.doc` — Documents  ·  S-09, S-11, S-12, S-13

Fixes D-01..D-05 and, partly, H-05. Implements your strip-on-read decision.

```python
read(path, *, strip_marks=True, normalize="NFD", newline="\n") -> Document
write(path, doc, *, newline="\n", bom=False, marks="display")
```
**The read boundary, in fixed order:** BOM removal → line-ending
canonicalization → Unicode normalization → removal of U+200E, U+200F,
U+202A–202E, U+2066–2069, U+00AD, inline U+FEFF. Measurement sees only this
form. `marks="display"` on write may reintroduce LRM around Hebrew runs.

```python
edit(path, old, new, *, count=1, match="normalized") -> Edit
```
`match="normalized"` normalizes **both the file and the pattern** before
locating, then applies the change to the original bytes. This is the direct
fix for the part of H-05's 74 failures caused by invisible marks — an
`old_string` without an LRM will match a file that has one.

```python
render(doc, to="pdf", *, engine="weasyprint", fonts=None,
       bidi=True, verify=True) -> Path
verify_render(source, rendered) -> Report
```
`to` ∈ `{"pdf", "html", "docx", "tex"}`. `verify=True` re-extracts text from
the rendered artifact and checks that every Hebrew and Greek run survived —
which is the only mechanical way to catch a font that silently dropped
pointing. `engine` is checked by `run.preflight` before work starts, fixing
E-05 (11 `pdftoppm is not installed`).

---

## 8. `thscript.run` — Execution environment  ·  C-04, C-05

Fixes E-02, E-05, E-07, E-08, E-10, L-11, L-13.

```python
paths(root=None) -> Paths            # anchored on repo root, never absolute
preflight(*, binaries=(), modules=(), fonts=()) -> None    # raises up front
manifest(*, seed, corpora, inputs, outputs) -> Manifest
```
`preflight` moves E-05/E-07 from "fails 40 minutes in" to "fails
immediately". `paths` removes the 16 hardcoded absolute paths and the
`/tmp` assumptions that caused E-02 and E-08 on Windows.

`manifest()` writes, next to every output: seed, each corpus's source +
version + fingerprint, input file hashes, git commit, package version,
timestamp. **This is what makes a number re-derivable a year later**, and it
is the thing no script in the workspace currently does.

---

## 9. `thscript.schema` — Cross-script data contracts  ·  C-03

Fixes E-03 (24 `KeyError`) and L-14.

```python
define(name, fields, *, version=1) -> Schema
write_table(path, rows, *, schema)
read_table(path, *, schema) -> list[Row]
```
Validation at both ends. A producer that omits `total_words` fails at write
time, not in a consumer three scripts later. The 74 scripts indexing dicts
by string literal become typed row access.

---

## 10. `thscript.verify` — Claims and regression  ·  C-08, L-01

**Generalizes `*****/input/test_seed_claims.py`, which already works.** Its
verdict vocabulary is kept intact because it is better than pass/fail.

```python
check(name, expect, fn) -> Verdict
```
`expect` ∈ `{"PASS", "FAIL", "PARTIAL", "UNDECIDABLE", "GUARD"}` — the
existing vocabulary. `FAIL` means *the claim is falsified and that is the
recorded finding*; `UNDECIDABLE` means *the corpora disagree and both
encodings are pinned here*. Neither is expressible in a normal test
framework, and both are needed for this kind of work.

```python
claim(id, statement, *, source, verdict, evidence, checked_by, date) -> Claim
claims_report(*, format="markdown") -> str
golden(path, *, tolerance=0) -> Comparator
```
`claim()` ties a sentence in a paper to the check that supports it, so
`claims_report()` can answer "which published statements currently rest on a
check that passes?" — the question §2c's hand-caught miscounts were
answering manually and unrecorded.

---

## 11. Coverage

| Situation | Covered by |
|---|---|
| S-01 corpus ingestion | `corpus.load` |
| S-02 concordance | `corpus.hits`, `count.distribution` |
| S-03 structure scoring | `structure.*` |
| S-04 permutation testing | `stats.permutation_test`, `stats.exact_test` |
| S-05 similarity/networks | `count.similarity`, `count.matrix` |
| S-06 discourse tagging | `count.distribution(unit="speaker")` + project tagger |
| S-07 lexical profiling | `count.vocabulary`, `count.hapax`, `count.tfidf` |
| S-08 figures | *(see below — deliberately not covered)* |
| S-09 document conversion | `doc.render`, `doc.verify_render` |
| S-10 agreement | `stats.agreement` |
| S-11 document editing | `doc.read`, `doc.write`, `doc.edit` |
| S-12 programmatic transformation | `doc.*` + `schema.*` |
| S-13 document-derived measurement | `doc.read` → `count.*` |

| Root cause | Status |
|---|---|
| C-01 encoding/normalization | **fixed** — `text`, `doc.read` |
| C-02 untested statistics | **fixed** — `stats` + `verify` |
| C-03 data contracts | **fixed** — `schema` |
| C-04 path/environment | **fixed** — `run.paths`, `run.preflight` |
| C-05 non-reproducibility | **fixed** — R2, R3, `run.manifest` |
| C-06 generation artifacts | **reduced** — less code to generate wrongly |
| C-07 truncated generation | **not fixed** — needs a pre-run integrity check |
| C-08 validity defects | **not fixed** — `verify.claim` records judgment, cannot supply it |
| C-09 mutation without verification | **partly** — `doc.edit` fixes matching, not intent |

### Deliberately not included

- **S-08 figure generation.** 6 scripts, all thin matplotlib wrappers,
  no measured defect. A plotting API here would be a function per chart —
  precisely what the task says not to build.
- **A `run_analysis()` orchestrator.** Every attempt to generalize "the
  whole pipeline" ends as a function with 30 keyword arguments. Composition
  belongs in the project script.
- **Anything for C-07 or C-08.** A library function claiming to detect a
  truncated script or a circular argument would be the false confidence
  this project exists to avoid.

---

## 12. Honest scope

**~55 functions across 9 modules, replacing 102 scripts of copy-paste.** The
three modules that would have prevented the most measured harm are `stats`
(20 divergent implementations of 7 statistical concepts), `text` (C-01) and
`run` (reproducibility).

The residue is real and worth naming: this library would not have caught the
***** miscount, the ***** attributed to Job, or the circular
`*****` marker. Those need `verify.claim` plus a human — which is why
§10 exists and why C-08 is marked unfixed rather than quietly folded into a
function.

One thing this list assumes and I could not verify: that the S-\* categories
are the right decomposition. If they are wrong, this function list inherits
the error.
