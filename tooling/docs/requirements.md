# Requirements

> ## ⚠ INCOMPLETE — step 1 was re-opened on 2026-08-07
>
> A completeness check against eight use cases found all of them missing or
> materially under-covered, and exposed that the evidence base here was
> drawn from 32 of 1,692 transcripts. See
> [`use-cases.md`](use-cases.md) for what is missing and why the method
> failed. Nothing in this document is known to be *wrong*; it is
> systematically **incomplete**, and everything derived from it inherits
> the gap.


**Source:** step 3 of [`../input/task.md`](../input/task.md) — *"write
requirements that need to be fulfilled."*
**Basis:** [`architecture.md`](architecture.md), traced to
[`problems.md`](problems.md).
**Date:** 2026-08-07.

Every requirement is **testable**, because steps 5 and 6 are test-driven:
each one names how it is verified, and each traces to a defect actually
observed or measured. A requirement that traces to nothing is not here.

`MUST` = the build fails without it. `SHOULD` = deliberate, overridable.

---

## R1 · Text and Unicode  (C-01)

| ID | Requirement | Traces to | Verified by |
|---|---|---|---|
| **T-01** | The public API **MUST NOT** expose or internally rely on a hardcoded Hebrew/Greek codepoint *range*. Classification **MUST** use `unicodedata.category`. | L-04 | Source scan asserts no `֑`-style range literal; unit test that U+05BE is retained by a marks-only fold |
| **T-02** | `fold` **MUST** remove `Mn` (points, cantillation) and **MUST NOT** remove `Pd`/`Po` (maqaf, paseq, sof pasuq) unless explicitly asked. | L-04 | `fold("אֶת־הָאָרֶץ") == "את־הארץ"` |
| **T-03** | `read` **MUST** remove all `Cf` characters (LRM, RLM, BOM, soft hyphen, embedding controls). | D-01, D-03 | Round-trip on a fixture containing each `Cf` character |
| **T-04** | Comparison **MUST** normalize both operands. Raw `==` on corpus text **MUST NOT** appear in the library. | L-05 | `same()` true across NFC/NFD and U+FB2B vs shin+sin-dot; source scan |
| **T-05** | All file reads and writes **MUST** specify an explicit encoding; stdout **MUST** be UTF-8 regardless of console codepage. | E-01 (≈90), E-09, L-06 | Source scan for bare `open()`; subprocess test writing Hebrew under `chcp 1252` |
| **T-06** | `audit()` **MUST** report invisible characters, mixed line endings, BOM and non-NFC content without altering input. | D-01–D-04 | Fixture with all four defects returns four findings |
| **T-07** | Normalization **SHOULD** be idempotent: `normalize(normalize(x)) == normalize(x)`. | — | Property test (hypothesis) over generated Hebrew/Greek strings |

---

## R2 · Corpus  (S-01, S-02)

| ID | Requirement | Traces to | Verified by |
|---|---|---|---|
| **C-01** | All sources **MUST** yield the same `Word` shape `(ref, surface, lemma, strongs, morph, slot)`. | S-01 (8 parsers) | Same assertion runs unchanged against ≥2 sources |
| **C-02** | Every `Corpus` **MUST** expose `version` and a content `fingerprint()`. | L-13, C-05 | Fingerprint changes iff source bytes change |
| **C-03** | Homograph policy **MUST** be an explicit parameter; a `Hit` set **MUST** record which policy produced it. | `wlc.py` ***** case; `t13` UNDECIDABLE | `homographs="split"` vs `"all"` give different, labelled counts |
| **C-04** | Text returned by `corpus` **MUST** already be normalized (AD-1). | L-05 | No caller-side normalization needed for `same()` to succeed |
| **C-05** | A reference that does not exist **MUST** raise, never return empty. | E-03 pattern | `verse("Gen.99.1")` raises |

---

## R3 · Statistics  (C-02)

| ID | Requirement | Traces to | Verified by |
|---|---|---|---|
| **S-01** | Any function consuming randomness **MUST** require `rng`; there **MUST** be no default. | L-03 (9 scripts) | `TypeError` when omitted; identical output for identical seeds |
| **S-02** | `permutation_test` **MUST** produce the `(k+1)/(n+1)` estimator. | 8 hand-rolled copies | Numeric equality with the hand-rolled formula — **verified: 0.269000 both ways** |
| **S-02b** | Structural nulls **MUST** route to `monte_carlo_test`, not `permutation_test`, and reproduce the hand-rolled result. | the null behind every ***** p-value | **Verified: 0.600570 both ways, difference 0.000000.** `permutation_test` cannot express this null at all |
| **S-03** | A `Result` carrying a p-value produced as one of N>1 **MUST** raise on format until `p_adjust` has processed the family. Bypass **MUST** be explicit and greppable. | L-02 (11 of 15) | Formatting an unadjusted family member raises; `.unadjusted_value` succeeds |
| **S-04** | Where a closed form exists, an exact test **MUST** be available and **SHOULD** be preferred over simulation. | L-10 | `exact_test("hypergeometric")` matches the Monte-Carlo estimate within tolerance |
| **S-05** | Every `Result` **MUST** carry method, seed, n, and corpus fingerprint. | L-13, AD-2 | Field presence; formatting raises if incomplete |
| **S-06** | Statistical computation **MUST** delegate to scipy/sklearn, not reimplement. | AD-3, 20 divergent versions | Source scan: no independent p-value arithmetic outside the wrapper |
| **S-07** | Bonferroni and Holm **MUST** be available alongside BH/BY. | scipy gap | Output matches `statsmodels.multipletests` |

---

## R4 · Documents  (C-01, C-09)

| ID | Requirement | Traces to | Verified by |
|---|---|---|---|
| **D-01** | `read` **MUST** apply, in order: BOM removal → line-ending canonicalization → Unicode normalization → `Cf` removal. | D-01–D-04, strip-on-read decision | Fixture with all four defects; order-sensitivity test |
| **D-02** | `edit` **MUST** match on the normalized form and apply to original bytes, so a pattern lacking an invisible mark still matches. | H-05 (74 failures) | Edit an LRM-bearing fixture with an LRM-free pattern; succeeds |
| **D-03** | `edit` **MUST** fail loudly on zero or ambiguous matches, never silently no-op. | H-05, H-11 | Raises on 0 matches and on N>expected |
| **D-04** | `write` **MUST** emit consistent line endings and **MUST NOT** emit a BOM unless asked. | D-02, D-03 | Byte-level assertion |
| **D-05** | Display marks **MUST** be reintroduced only at render, never by `write` into a source document. | strip-on-read decision | `read(write(read(x))) == read(x)` |
| **D-06** | `render` **MUST** fail at preflight if its engine is unavailable, before conversion begins. | E-05 (11×), verified live | Preflight raises with no engine installed |
| **D-07** | Render verification **MUST NOT** rely on PDF text extraction for pointed Hebrew. It **MUST** use font-glyph coverage and/or rasterization. | **Measured**: a correct PDF extracts as corrupted text, losing an ALEF and inventing a RESH and HE | Extraction-based check would false-fail the known-good fixture; glyph-coverage check passes it |
| **D-08** | Greek and unpointed Hebrew **SHOULD** be verified by extraction, where it is reliable. | Measured: both survive extraction intact | Round-trip on a Greek fixture |

---

## R5 · Data contracts  (C-03)

| ID | Requirement | Traces to | Verified by |
|---|---|---|---|
| **X-01** | Every file written for another script **MUST** declare a schema, validated on write **and** read. | E-03 (24 `KeyError`), L-14 | Writing a row missing a field raises at write time |
| **X-02** | A schema **MUST** carry a version; reading a mismatched version **MUST** raise. | L-14 | Version bump raises on old file |
| **X-03** | Consumers **MUST NOT** index results by bare string literal. | 74 scripts do | Typed row access; source scan |

---

## R6 · Execution and provenance  (C-04, C-05)

| ID | Requirement | Traces to | Verified by |
|---|---|---|---|
| **E-01** | Paths **MUST** resolve relative to a discovered root. Absolute paths and `/tmp` literals **MUST NOT** appear. | E-02, E-08, L-11 (16 files) | Source scan; suite passes from any working directory |
| **E-02** | `preflight` **MUST** verify binaries, modules and fonts before work begins and name what is missing. | E-05, E-07 | Raises listing the specific missing item |
| **E-03** | Every output **MUST** be accompanied by a manifest: seeds, corpus versions and fingerprints, input hashes, library versions, timestamp. | L-13, C-05 | Manifest present and complete for every produced artifact |
| **E-04** | Identical inputs plus identical seed **MUST** produce byte-identical output. | L-03 | Two runs diff clean |
| **E-05** | Exceptions **MUST NOT** be silently swallowed; a caught parse failure **MUST** be counted and reported. | L-12 (9 scripts) | Malformed-record fixture reports a nonzero skip count |

---

## R7 · Verification and claims  (C-08, L-01)

| ID | Requirement | Traces to | Verified by |
|---|---|---|---|
| **V-01** | The harness **MUST** support `PASS`, `FAIL`, `PARTIAL`, `UNDECIDABLE`, `GUARD`. | `test_seed_claims.py` uses all five | A `FAIL`-expected check that starts passing is itself reported |
| **V-02** | `claim()` **MUST** link a paper statement to the check supporting it and report unsupported claims. | C-08, §2c miscounts | Report lists claims whose check is absent or failing |
| **V-03** | Every requirement above **MUST** have at least one automated test. | L-01 | Traceability report: requirement ID → test ID, no gaps |
| **V-04** | The suite **MUST** fail if a corpus fingerprint changes without a recorded verdict review. | `test_seed_claims.py`'s stated purpose | Altering a fixture corpus fails the suite |

---

## 8. Coverage and honest gaps

**39 requirements.** Coverage against `problems.md` root causes:

| Cause | Requirements | Status |
|---|---|---|
| C-01 encoding/normalization | T-01…T-07, D-01…D-05 | **covered** |
| C-02 untested statistics | S-01…S-07, V-03 | **covered** |
| C-03 data contracts | X-01…X-03 | **covered** |
| C-04 path/environment | E-01, E-02 | **covered** |
| C-05 non-reproducibility | C-02, S-01, S-05, E-03, E-04 | **covered** |
| C-06 generation artifacts | — | *reduced only*, by there being less code to generate |
| C-07 truncated generation | — | **not addressed** — outside a library |
| C-08 validity defects | V-01, V-02 | *recorded, not solved* |
| C-09 mutation without verification | D-02, D-03 | *matching fixed; intent not verifiable* |

Two requirements rest on assumptions not yet tested, and would need revision
if the assumptions fail:

- ~~**S-06** assumes `permutation_type` can express the workspace's null
  models.~~ **SETTLED 2026-08-07.** It cannot — but `monte_carlo_test` can,
  exactly (see S-02b). AD-3 holds. This was the largest open risk and it is
  closed.
- **C-01/C-02** assume the eight corpus formats can share one `Word` shape.
  Only WLC and the three Text-Fabric corpora were inspected.
