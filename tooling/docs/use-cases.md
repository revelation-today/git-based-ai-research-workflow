# Step 1, round 2 — use-case-driven survey

**Trigger:** a completeness check against seven use cases named by the
researcher. **All seven were missing or materially under-covered**, and an eighth (tooling that *produces* scripts and outputs) was added mid-review.
**Verdict:** step 1 is re-opened. [`problems.md`](problems.md) is not wrong,
but it is **incomplete in a systematic way**, and everything derived from it
inherits the gap.
**Date:** 2026-08-07.

---

## 1. Why round 1 missed them

Round 1 was **artifact-driven**. It inventoried two things: Python scripts
on disk, and error traces in session transcripts. That method finds work
which *left evidence of having been done, and of having failed loudly*.

It is structurally blind to:

- work done **by hand** because no script was ever written for it;
- work done **inside a chat** with no script and no traceback;
- work whose failures are **silent** — a dropped caveat, an inconsistent
  edit, a stale list — which produce no exception to count;
- work the researcher **needs** but has not yet attempted.

Every one of the named use cases falls into at least one of those
categories. Worse, the third category — silent failure — is precisely the
class `problem_description.md` says matters most: *"they are never fully
tested and create wrong answers."* Round 1's method was best at finding the
loud failures and worst at finding the ones that matter.

### And the evidence base itself was understated

Checking this exposed a fourth falsified extent count, the most
consequential so far. Round 1 scanned `~/.claude/projects/*/*.jsonl` — the
**top level only**.

| | Round 1 said | Actual |
|---|---|---|
| Transcripts | 32 sessions | **1,692** |
| — top-level sessions | 32 | 32 |
| — subagent / workflow transcripts | *not scanned* | **1,660** |
| Python tracebacks | 201 | **341** |
| `UnicodeEncodeError` | ~90 | **217** |

The 1,660 unscanned files include entire multi-agent workflow runs — one
`workflows/wf_…` directory alone holds 331 transcripts. So round 1's error
counts were drawn from roughly 2% of the transcript corpus by file count,
and understated tracebacks by ~70% and encoding errors by ~140%.

That is also direct evidence for use case 4: **orchestration across many
agents is already happening at scale**, and round 1 did not see any of it.

---

## 2. The use cases, with evidence

### U-01 · Handling caveats
**Not covered anywhere.** One passing mention in `problems.md`; nothing in
the functions, architecture, requirements or tests.

| Marker in the researcher's documents | Occurrences |
|---|---|
| "caveat" | **678** |
| "may be" | 495 |
| "however" | 488 |
| "uncertain" | 147 |
| "arguably" | 117 |
| "provisional" | 35 |
| "tentative" | 13 |
| "not attested" | 7 |

Caveats are pervasive in the writing and tracked by nothing. The failure
mode is already named in `problems.md` §3 as a hallucination shape —
*"quiet compression of nuance … an argument that was hedged in the source
comes out flat and confident in the summary"* — and then nothing in the
design addresses it. A hedge lost during summarising or moving text
produces no error and changes what the paper claims.

Related and also absent: the manual's three-tier attestation scale
(strongly / moderately attested / proposed-plausible). `functions.md`
mentions it once and no requirement implements it.

### U-02 · Making consistent changes across documents
**Zero** mentions of cross-file or multi-file editing anywhere in the
design. `doc.edit` is single-file and **refuses** ambiguity — for one
document that is right, but it makes it the wrong tool for this use case
rather than a partial one.

Surface: 3,222 Markdown documents. Terms needing consistent treatment span
files — "open question" in 50, "cf." in 45, "TODO" in 28, "section N"
cross-references in 26.

The need is: *find every relevant occurrence, decide once, apply
everywhere, and prove nothing was missed.* Silent failure: three of four
occurrences updated, no error, a document that now contradicts itself.

### U-03 · Keeping lists consistent
**Not covered.** 1,102 documents contain list structures; 15 carry a
bibliography-style heading. The department manual itself requires
`sources.md` and `TODO.md` to stay consistent with `paper.md`.

Silent failure: an entry added to a bibliography but not to the claim that
cites it, or a TODO checked off in one place and left open in another.

### U-04 · Tracking and orchestrating changes across chats
Recorded in round 1 only as a *problem* (H-08 subagent limit, H-03
truncations) — never as a capability. And the transcript recount above
shows the scale was invisible: **1,660 subagent and workflow transcripts**
across 11 projects.

Needs: know which session changed what; reconcile concurrent edits; carry a
decision made in one chat into another. Git provides the substrate; nothing
provides the reconciliation.

### U-05 · Creating tables and visualisations
**Deliberately excluded by me in `functions.md` §11**, on the grounds that
the 6 figure scripts were "thin matplotlib wrappers, no measured defect."
That reasoning was artifact-driven and therefore circular: no defect was
measured because no measurement looked.

Surface: **668 documents contain Markdown tables, 15,056 table rows.**
Tables are one of the largest activities in the workspace, and the design
covers them only as data I/O (`schema.read_table`), never as presentation
artifacts that must stay consistent with the numbers behind them.

### U-06 · Parsing PDFs and other input
**Not covered at all.** The design handles PDF as *output* only.

| Input format present | Count |
|---|---|
| PDF | **225** |
| XML | 123 |
| HTML | 67 |
| JSON | 34 |
| CSV | 32 |
| DOCX | 12 |

225 PDFs and **zero** PDF-reading scripts. That work is being done by hand
or inside a chat — leaving no artifact, which is exactly why round 1 could
not see it.

Note the sharp constraint already measured: PDF text extraction **corrupts
pointed Hebrew**, losing and inventing characters. Any PDF-input capability
inherits that limit on day one.

### U-07 · Creating HTML
Barely covered: `doc.render` would pass `to="html"` to pandoc, but there is
no requirement and no test. Surface: 67 HTML files, a `raw_html` corpus of
53 documents, three `build-html.py` scripts, and a Hugo site.

Verified earlier: pandoc renders Hebrew and Greek to HTML **correctly** —
so unlike PDF, this path is sound. It simply was never specified.

### U-08 · Tools that *produce* the scripts and outputs
**Not covered, and previously written off.** Added by the researcher during
this round.

The original problem statement is that *AI generates scripts on the fly*
and they are never fully tested. Round 1 responded by building a library
for those scripts to call — which helps only if whoever writes the script
remembers to call it. Nothing generates the script.

A generator changes what is guaranteed rather than merely available:

- The boilerplate that goes wrong — `configure_stdout`, `preflight`,
  a seeded `rng`, a `manifest`, a declared `schema` — is emitted, not
  remembered. That is C-06 (generation artifacts: `SyntaxError` from
  heredocs, dead patched-in branches, imports hidden inside functions).
- **It reopens C-07**, which round 1 called unfixable. 114 mid-stream
  truncations produced scripts that were silently incomplete. A library
  cannot detect that its caller was truncated — but a *generator* can
  emit a completeness marker and a checksum, and a runner can refuse to
  execute a script that does not match. That is not detecting truncation
  in general; it is making generated scripts verifiable, which is enough.
- Output artifacts too: a table, a figure, an HTML page or a PDF produced
  through a generator carries its manifest by construction, rather than
  depending on the author to attach one.

This is the one use case that acts on the *cause* named in
`problem_description.md` rather than on the consequences.

---

## 3. What this invalidates

| Document | Status |
|---|---|
| [`problems.md`](problems.md) | **incomplete** — evidence base understated; S-\* misses U-01..U-07 |
| [`functions.md`](functions.md) | **incomplete** — and §11's exclusion of S-08 is now known to be wrongly reasoned |
| [`libraries.md`](libraries.md) | sound as far as it goes; no library validated for PDF input, tables or HTML |
| [`architecture.md`](architecture.md) | **incomplete** — no layer owns cross-document consistency |
| [`requirements.md`](requirements.md) | **incomplete** — 0 of 40 requirements cover U-01..U-07 |
| [`test-plan.md`](test-plan.md) | **incomplete** — same gap |
| `thscript` (129 passing tests) | **sound but partial.** Nothing built is wrong; it covers the artifact-driven half only |

The seven modules already built do not need reworking. They are the correct
response to what round 1 found. What is missing is a second half.

---

## 4. Provisional new situations

Offered as the starting point for the revised step 1, not as a settled
inventory — the lesson of this round is that a decomposition asserted
without evidence is worth little.

| ID | Situation | Use case |
|---|---|---|
| **S-14** | Caveat and attestation tracking — a qualification attached to a claim, surviving every move and summary | U-01 |
| **S-15** | Cross-document consistent change — find all, decide once, apply everywhere, prove completeness | U-02 |
| **S-16** | List/registry consistency — bibliography, TODO, marker sets, kept in sync across files | U-03 |
| **S-17** | Multi-session reconciliation — which session changed what, and merging concurrent work | U-04 |
| **S-18** | Table generation and consistency — a table that cannot drift from the numbers behind it | U-05 |
| **S-19** | Non-corpus input ingestion — PDF, DOCX, HTML, CSV into normalised text | U-06 |
| **S-20** | HTML output — the path already verified sound for Hebrew and Greek | U-07 |
| **S-21** | Script and output generation — emit correct scaffolding rather than relying on it being remembered | U-08 |

### And a new root cause

**C-10 · Consistency across artifacts.** Every one of U-01, U-02, U-03,
U-05 is the same underlying failure: *a fact stated in more than one place,
updated in fewer places than it appears.* It raises no exception and no
test catches it, because each file is individually valid. This is a
different failure class from anything C-01..C-09 covers, and it is the one
the use cases mostly describe.

**And two existing causes change status.** C-06 (generation artifacts) moves
from "reduced only" to addressable, and **C-07 (truncated generation) moves
from "not addressed — outside a library" to addressable**, because a
generator can emit a completeness marker and checksum that a runner
verifies before executing. `architecture.md` §6 and the traceability
diagram both state C-07 terminates in nothing; that is now wrong and must
be revised.

---

## 5. Method correction for round 2

Round 1's method must not simply be repeated at greater volume.

1. **Scan all 1,692 transcripts**, not the top-level 32.
2. **Survey by use case, not only by artifact** — ask what the researcher
   does, not only what left a `.py` file behind.
3. **Look for silent failures explicitly**: contradictions between
   documents, stale list entries, tables disagreeing with their source
   numbers. These produce no traceback, so counting exceptions will never
   find them.
4. **Treat "no measured defect" as "not measured"** until a measurement
   actually looked. That inference is what wrongly excluded S-08.
