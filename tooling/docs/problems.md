# Problem catalogue — AI-generated theological analysis scripts

> ## ⚠ INCOMPLETE — step 1 was re-opened on 2026-08-07
>
> A completeness check against eight use cases found all of them missing or
> materially under-covered, and exposed that the evidence base here was
> drawn from 32 of 1,692 transcripts. See
> [`use-cases.md`](use-cases.md) for what is missing and why the method
> failed. Nothing in this document is known to be *wrong*; it is
> systematically **incomplete**, and everything derived from it inherits
> the gap.


**Source:** step 1 of [`../input/task.md`](../input/task.md), framed by
[`../input/problem_description.md`](../input/problem_description.md).
**Derived from:** proposal commits `d664869`
([0001, scripts and errors](../ai-requests/0001-workspace-script-and-error-survey/answer.md))
and `a3f4bb9`
([0002, document editing](../ai-requests/0002-document-editing-situations/answer.md)).
**Surveyed:** 2026-08-07.

Every entry has a stable ID. Later steps of the task — the function list,
the requirements, the test cases — reference these IDs so that each
requirement can be traced back to an actual observed or latent failure
rather than to a guess about what might go wrong.

## Evidence base

| Source | Volume |
|---|---|
| Python files scanned (`*****`, `*****`, `*****`, `*****`, `AI`) | 102 |
| — of which AI-authored | **101** |
| — of which vendored upstream (`morphhbXML-to-JSON.py`, openscriptures) | 1 |
| Shell scripts | 2 |
| **Markdown documents in the workspace** | **3,222** (3,173 scanned in detail) |
| **`Edit` / `Write` invocations across all sessions** | **3,693 / 1,489 = 5,182 mutations** |
| Scripts that read or write `.md` | 28 |
| Claude Code session transcripts (`~/.claude/projects/`, 11 projects) | 32 sessions, 762 MB |
| Python tracebacks in those transcripts | 201 |

Scripts per project: ***** 46, ***** 28, ***** 25, ***** 2, AI 1.
Tracebacks per project: ***** 72, ***** 44, ***** 38, ***** 34,
***** 10, project-h 4, AI 2, theology_scripts 1.
Markdown documents per project: ***** 1,728, ***** 1,083, AI 239,
***** 63, ***** 49, project-h 43, ***** 11, ***** 4, project-f 2.

**Document editing is the larger activity.** 5,182 document mutations
against 102 scripts written — and 28 of those scripts *read* `.md`, so
documents are an interface into the measurement pipeline, not a terminal
output. Survey 0001 missed this; see Part 3b.

The `L-*` extent counts are stated out of the 102 files scanned. Only L-04
involves the single vendored file — and there it is the point of the
finding, not a contamination of it.

**Completeness caveat.** Transcripts cover sessions run through Claude Code.
A script generated in a browser chat and pasted in by hand leaves a file on
disk but no transcript, so the observed-error counts (E-\*, H-\*) are a lower
bound. The script inventory (S-\*) is complete for anything saved to disk.

---

# Part 1 — Situations that produced a script or a document

Thirteen recurring shapes: ten that produced a script (S-01..S-10, from
survey 0001) and three covering document editing (S-11..S-13, from survey
0002). The shapes matter more than the counts — the same operations recur
with different parameters, which is what makes a parameterized library
feasible instead of 102 bespoke scripts and 5,182 ad-hoc edits.

| ID | Situation | Representative scripts |
|---|---|---|
| **S-01** | **Corpus ingestion** — parse a tagged primary text (WLC, morphhb, Text-Fabric, SBLGNT, LXX, DSS, Samaritan Pentateuch) from XML/JSON/TSV into per-verse, per-word records with lemma and morphology | `*****/input/wlc.py`, `*****/input/tf_parse.py`, `*****/input/hebrew/morphhb/morphhbXML-to-JSON.py`, `*****/output/todo/approach-2/tools/{lxx,dss,sp,lex,egypt}.py` |
| **S-02** | **Concordance / occurrence counting** — given a lemma, root or Strong's number, find every occurrence and report distribution by chapter/verse/speaker | `*****/input/{hebrew,greek}/concordance.py`, `*****/structure_analysis/attestation.py`, `*****/output/paper/r5_genesis.py` |
| **S-03** | **Structural hypothesis scoring** — score a proposed compositional structure (*****, panel, cycle, sevenfold scheme) against textual markers | `*****/structure_analysis/{schemes,panels,run_cycle,run_levels,run_rows,run_align,run_confine,run_direction}.py`, `*****/output/todo/*****/tools/*.py` (16), `*****/structures/r5/scripts/r5_*.py` |
| **S-04** | **Permutation / Monte-Carlo significance testing** — build a null by resampling, compare an observed statistic, report a p-value | `*****/r5/*****/run{,2,3,3b,4,5}.py`, `*****/r5/*****-{amos,arnion,negative-control,thematic-all,thematic-cprime}/run.py`, `*****/output3/scripts/08_monte_carlo.py`, `*****/output/paper/{control_test,compression_test}.py` |
| **S-05** | **Similarity / distance / network metrics** — TF-IDF, cosine similarity, citation and lexical-sharing networks | `*****/output2/scripts/{01_similarity,04_network}.py`, `*****/output/scripts/14_tfidf_chapter.py`, `*****/output4/scripts/11_citation_network.py` |
| **S-06** | **Discourse tagging** — speaker, addressee, speech act, question type | `*****/output2/scripts/{02_p2ms_addressee,05_questions,06_speech_verbs,08_addressee_verse,speaker_map}.py`, `*****/output4/scripts/13_question_types.py` |
| **S-07** | **Lexical profiling** — hapax legomena, register progression, vocabulary richness | `*****/output2/scripts/07_hapax.py`, `*****/output3/scripts/{09_register_progression,10_hapax_prayer_correlation}.py` |
| **S-08** | **Figure generation** — heatmaps, arc diagrams, network plots, distribution charts | `*****/output2/scripts/figs/f1_heatmap.py` … `f6_hapax.py` (6) |
| **S-09** | **Document build and conversion** — Markdown → PDF/HTML with Hebrew/Greek surviving the round trip | `*****/output/scripts/build_pdf.sh`, `*****/pdf-build/build.py`, `guideline/build-html.py` |
| **S-10** | **Agreement / reliability measurement** — Cohen's kappa between coding schemes | `*****/output/todo/approach-2/c1/kappa.py`, `*****/structure_analysis/run_agreement.py` |
| **S-11** | **Direct document editing** — exact-string `Edit` and whole-file `Write` against Markdown drafts, papers, appendices, notes (5,182 operations over 3,222 documents) | `*****/output/paper/*****.md`, `*****/gen_story/writer_books/*.md` (7,800–11,900 lines each) |
| **S-12** | **Programmatic document transformation** — scripts that emit or rewrite Markdown rather than editing it by hand | `*****/output/todo/*****/tools/seg_table.py`, `*****/structure_analysis/schemes.py`, `*****/pdf-build/build.py`, `AI/output/training/build_decks.py` (28 total) |
| **S-13** | **Document-derived measurement** — a script reads a `.md` document and counts from it, making the document an input to a statistic rather than an output | the 28 scripts above, feeding S-02, S-05, S-07 |

---

# Part 2 — Errors that occurred

## 2a. Script runtime failures (201 tracebacks)

| ID | Error | Count | Root cause |
|---|---|---|---|
| **E-01** | `UnicodeEncodeError: 'charmap' codec can't encode…` | ~90 | Hebrew/Greek printed to a Windows console defaulting to cp1252 |
| **E-02** | `FileNotFoundError` | ~30 | POSIX `/tmp/...` paths used on Windows; intermediate artifacts from an earlier step missing |
| **E-03** | `KeyError` | ~24 | Schema drift between scripts: `'words'`, `'total_words'`, `'target_chapter'`, `'hapax_per_1000'`, `'OUT'`, `'id'`, `'q'`, `(int,int)` tuples |
| **E-04** | `SyntaxError` | ~12 | Unterminated string literal, bad line continuation, invalid decimal — from generating a script inline through a heredoc |
| **E-05** | `pdftoppm is not installed` | 11 | External binary (poppler) assumed present |
| **E-06** | `PatternError` (`bad escape`, `unterminated character set`) | ~8 | Regex over Hebrew/Greek codepoint ranges |
| **E-07** | `ModuleNotFoundError` (`matplotlib`, `yaml`, `markdown`) | ~6 | Dependency assumed present |
| **E-08** | `PermissionError: '/tmp_out.txt'` | 2 | Windows misparse of a POSIX path into a root-level filename |
| **E-09** | `UnicodeDecodeError: 'charmap'` | 2 | Reading a UTF-8 file without `encoding=` |
| **E-10** | `NameError: '__file__' is not defined` | 2 | Path resolution breaking under `-c`/stdin execution |
| **E-11** | `TypeError`, `IndexError`, `ValueError` | ~8 | Assorted |

**E-01 and E-03 are this workspace's signature failures.** E-01 is Hebrew and
Greek meeting a Windows console. E-03 is one script reading a key a
*different* script was supposed to have written — the direct consequence of
a chain of independently generated scripts with no agreed data contract.

## 2b. Harness-level interruptions

Not script bugs, but they damage a run without leaving a traceback.

| ID | Event | Count |
|---|---|---|
| **H-01** | `Error: Exit code <N>` (non-zero, unclassified) | 176 |
| **H-02** | Rate limited | 139 |
| **H-03** | **Response stalled / connection closed mid-stream** | **114** |
| **H-04** | Output blocked by content filtering | 47 |
| **H-05** | `String to replace not found in file` (failed edit) | **74** |
| **H-06** | `File has not been read yet` | **60** |
| **H-09** | `old_string and new_string are exactly the same` | 11 |
| **H-10** | `File has been modified since read` | 10 |
| **H-11** | `Found N matches of the string to replace` (ambiguous target) | 4 |
| **H-07** | File/content exceeds token or size limit | 18 |
| **H-08** | Concurrent subagent limit reached | 12 |

**H-03 is the dangerous one.** A script written by a truncated response is
silently incomplete; if it still parses, it runs and produces a number.

**H-05/H-06 counts corrected upward** from survey 0001, which used an
extraction regex requiring a literal `Error: ` prefix and stopping at
escaped characters. H-05 was reported as 32 and is 74; H-06 was reported as
23 and is 60. H-09..H-11 were missed entirely. Corrected total: **159
failed document mutations** — each one an edit the AI believed it had made
and had not, or made against a stale view of the file.

## 2c. Wrong results that ran cleanly and were caught by hand

The failure mode `problem_description.md` names. Quoted from session records:

- *"miscount in *****'s own occurrence count, later restated and corrected"*
- *"a direct count against the primary Greek text (SBLGNT, morphological) … miscount"*
- *"miscounted (***** attributed to Job)"* — a speaker-attribution
  error, i.e. S-06 output silently corrupting S-05 and S-07 statistics
- *"recounted verse by verse against the tagged Masoretic text and supersede it"*
- *"the number is wrong and appears in a table of shared lexemes"*
- **"a miscount that gets corrected on the spot and leaves no trace beyond the correction"**

The last quotation is the entire problem in one sentence: the script produced
a wrong number, a human caught it by hand, and neither the wrongness nor the
correction is recoverable from the script or its output.

---

# Part 3 — Errors that could occur

Latent defects found by static analysis of all 102 scripts. **None of these
raise an exception.** Ordered by how badly each corrupts a measurement while
the run looks completely successful.

| ID | Defect | Extent |
|---|---|---|
| **L-01** | **No test coverage** — with one substantial exception | **101 of 102**; see the correction below |
| **L-02** | Multiple-comparison correction missing in most, divergent where present | **11 of 15** apply none; 4 apply Benjamini-Hochberg in **3 different implementations** (corrected) |
| **L-03** | **Unseeded randomness** | 9 scripts |
| **L-04** | Hebrew diacritic strip range too wide — deletes word-joining punctuation. **Latent: measured impact zero** | 2 sites, identical range, one inherited from upstream |
| **L-05** | **No unicode normalization** (NFC/NFD) | **99 of 102** |
| **L-06** | `open()` without `encoding=` | 18 scripts, 24 call sites |
| **L-07** | Patched-in-place dead logic | ≥1 confirmed |
| **L-08** | Import hidden inside a function body | ≥1 confirmed |
| **L-09** | Circular evidence scored as independent | 1 self-documented |
| **L-10** | Monte-Carlo approximation where a closed form exists | 1 confirmed |
| **L-11** | Hardcoded absolute paths | 16 scripts |
| **L-12** | Swallowed exceptions (bare `pass` in `except`) | 9 scripts |
| **L-13** | No input provenance recorded | all scripts |
| **L-14** | Implicit producer/consumer data contract | 74 scripts index a dict by string literal |

## Measured, 2026-08-07 — two severity corrections and one wrong count

The two findings this catalogue originally called critical were measured
against the real corpora (proposal `0003`). **Both deflate. No retraction of
existing results is needed on this evidence.**

**L-04 does not fire.** In the WLC OSIS corpus (23,213 verses, 306,785 `<w>`
tokens), U+05BE MAQAF occurs **42,587** times — **42,577 of them as a
standalone `<seg>` element and 0 inside a `<w>` token**. U+05C0, U+05C3 and
U+05C6 likewise never appear inside a `<w>`. And `strip_points()` has
exactly three call sites (`wlc.py:77`, `wlc.py:88`,
`test_seed_claims.py:58`), all over `<w>` surface forms. The over-wide range
never meets a maqaf, so it has never merged a token. The range is still
wrong and still copied from upstream into AI-authored code — but the earlier
claim that it was "the clearest instance of a defect producing a confident
wrong measurement" was **wrong**. It produces none here.

**D-01 inflation is real but unmeasured by anything.** Across all 3,173
documents: 30 of the 81 LRM-bearing files show inflation, **222 spurious
distinct Hebrew tokens, 10.5% aggregate** (worst: `*****.md` 82,
`*****.md` 18, `*****.md` 13). But the 28 `.md`-reading
scripts reference only four paths — `README.md`, `outline.md`,
`segmentation.md`, `*****/*****.md` — and **none is an inflated
document**. The one Hebrew-bearing document a script does read contains
**zero LRM**. So no computed statistic is affected. What survives is the
editing cost (H-05, 74 failed edits) and search misses — plus the standing
hazard that pointing any counting script at `*****/output/` makes the 10.5%
real immediately.

**L-02 was also wrong** — see the L-02 detail below. 4 scripts do apply
Benjamini-Hochberg; the pattern was case-sensitive and one alternative
false-matched `freq.values()`. Corrected to 11 of 15 applying none.

**L-01 was wrong.** "No test coverage, 102 of 102" was a grep artifact: the
pattern looked for `def test_`, and `*****/input/test_seed_claims.py` names
its checks `t1_`, `t2_`, … It contains **45 assertions across 15 named
checks**, with verdicts `PASS` / `FAIL` / `PARTIAL` / `UNDECIDABLE` /
`GUARD` — including two claims recorded as actively **falsified** and kept
on record, and one as *"UNDECIDABLE — corpora disagree; both encodings are
pinned here."* Its stated purpose:

> *"Every assertion here was verified by hand on 2026-08-06. The suite
> exists so that a change to the parsers, or a corpus version bump, cannot
> silently alter a published verdict."*

`*****/input/tf_parse.py` alongside it already defines `nfc()`, `norm()` and
`same()`, with the comparison rule stated explicitly — *"always use this,
never raw `==`. NORMALISE BOTH SIDES. Raw comparison fails silently."* — and
a docstring that records its own earlier misdiagnosis because *"misdiagnosing
a Unicode failure is exactly the kind of confident-and-wrong claim this
project studies."*

**Three of my extent counts have now been falsified** (H-05/H-06
undercounted, L-01, L-02), all by the same mechanism: a grep pattern that
assumed a naming or casing convention. The remaining unverified `L-*` counts
should be read as indicative, not settled.

**This changes the mandate for the rest of the task.** The workspace already
contains one working instance of the discipline being designed. The
architecture should generalize `tf_parse.norm`/`same` and the
`check(name, verdict, fn)` verdict harness rather than invent a parallel
mechanism — and the verdict vocabulary, which can express *falsified* and
*undecidable* rather than only pass/fail, is worth keeping.

## Decision recorded — strip on read

**The library strips bidi and invisible marks when reading a document.**
Marks may still be written into documents for display.

The document-read boundary applies, in order: BOM removal, line-ending
canonicalization, Unicode normalization, then removal of U+200E, U+200F,
U+202A–U+202E, U+2066–U+2069, U+00AD and inline U+FEFF. Measurement consumes
only the stripped form; rendering (S-09) may reintroduce display marks.

**This does not fix H-05.** Stripping on read does nothing for an
exact-string edit against on-disk bytes that still contain the marks.
Whether to normalize the documents themselves is a separate, still-open
decision.

## Detail on the load-bearing ones

### L-03 — unseeded randomness
`*****/input/tf_parse.py`,
`*****/output/todo/*****/tools/{axes,centred,centred_structure,corpus,more_schemes,scheme}.py`,
`*****/output4/scripts/12_macro_balance.py`,
`*****/structure_analysis/check_k8_supplementary.py`.

`*****/output4/scripts/12_macro_balance.py` **both resamples and reports a
p-value with no seed.** That number is different on every run and cannot be
reproduced by anyone, including its author. Single most serious individual
finding in the workspace.

### L-04 — diacritic strip deletes word-joining punctuation

Two sites, in two different projects, using the **identical** codepoint
range — one vendored, one AI-authored:

```python
# *****/input/hebrew/morphhb/morphhbXML-to-JSON.py:130  (vendored, openscriptures)
def stripPointingFunc(string):
    return re.sub(r"[֑-ׇ]", "", string)

# *****/input/wlc.py:35,39  (AI-authored; same range, written as literal characters)
_POINTS = re.compile(r"[U+0591-U+05C7]")   # shown as codepoints; the file has the literal chars
def strip_points(s):
    """Remove vowels and cantillation."""
    return _POINTS.sub("", s or "")
```

`wlc.py`'s literal range was verified programmatically to be exactly
U+0591-U+05C7 — the same range as the vendored tool, i.e. **copied from
upstream rather than derived**.

U+0591-U+05C7 is not the set of vowels and cantillation marks. It also
contains **U+05BE MAQAF** (the Hebrew word-joining hyphen), **U+05C0
PASEQ** and **U+05C3 SOF PASUQ**. Stripping the maqaf silently
concatenates two words into one token. Every downstream word count, hapax
count (S-07), TF-IDF vector (S-05) and lemma frequency (S-02) computed from
stripped text is wrong by an unknown amount, and nothing raises.

>  **Measured 2026-08-07: this never fires.** Maqaf occurs 42,587 times in
>  the WLC corpus, always as a standalone `<seg>`, never inside a `<w>`
>  token — and `strip_points()` is applied only to `<w>` text. Zero tokens
>  are affected. See "Measured, 2026-08-07" above.

The range is still wrong, and still copied verbatim from a trusted upstream
tool into AI-authored code — which remains the argument for C-01 owning
normalization in one tested place instead of each script copying a range
that looks right. But it is a latent defect, not an active one.

> **Refined 2026-08-07 (proposal `0005`): corpus-path dead, document-path
> live.** The zero above holds for the WLC corpus, where maqaf is always a
> separate `<seg>`. It does **not** hold for documents: **243 inline U+05BE
> MAQAF across 44 Markdown files.** Folding those with the buggy range turns
> `אֶת־הָאָרֶץ` into `אתהארץ` — two words merged. Still unfired, because no
> script folds those documents today; but S-13 (document-derived
> measurement) is exactly what the library enables.
>
> **And the fix needs no range at all.** `unicodedata.category` returns
> `Mn` for vowels and cantillation, `Pd` for MAQAF, `Po` for PASEQ and SOF
> PASUQ, `Cf` for LRM/BOM/soft-hyphen. The whole defect class — L-04 *and*
> D-01 — is one stdlib predicate. See [`libraries.md`](libraries.md).

### L-02 — multiple comparisons, corrected 2026-08-07

> **The original claim "0 of 15 apply any correction" was wrong** — a third
> grep artifact. The pattern was case-sensitive (`benjamini` misses
> "Benjamini-Hochberg" in a docstring) and `q.?value` false-matched
> `freq.values()`. **4 scripts do apply Benjamini-Hochberg**: `bh()` in
> `run_levels.py` and `run_rows.py` (identical), `bh_correction()` in
> `r5_v2_books.py` and, differently again, in `r5_v2_structures.py` — 3
> distinct implementations.

The surviving finding is narrower and more interesting than the original.
`*****/r5/*****/run.py` prints a per-marker p-value table across
every marker in `BOUNDARY` and `CONTENT` (~20 markers), then combines with
Fisher. The Fisher combination is defensible; the per-marker table alongside
it is uncorrected. So the workspace **knows** about FDR — it just applies it
in 4 of 15 places, via 3 implementations, with nothing recording which.
Only 1 of 102 scripts imports scipy; the machinery is hand-rolled throughout.

### L-07 / L-08 — on-the-fly generation artifacts
`*****/r5/*****/run.py:26`:

```python
return (null>=cover(ALL[name])[pts].sum() if False else (null>= (...)).sum()+1)/(len(null)+1)
```

The `if False` branch is a leftover from a live fix. The surviving branch is
the correct +1 permutation estimator, so this instance is harmless — but it
is the exact fingerprint of "generated on the fly, patched, never tested,"
and the next such patch may not land on the correct branch. The same file
hides `import scipy.stats as st` inside `fisher()`, deferring a possible
`ModuleNotFoundError` to the end of a long run (L-08).

### L-09 — circular evidence
`*****/output/paper/control_test.py:44`, the script's own comment:

```python
"*****":  pt in COOCCUR,      # CIRCULAR: ~= definition of crossing point
```

The circularity is documented and the marker is scored anyway. A validity
defect no linter will ever find.

### L-13 / L-14 — provenance and contracts
No script records which edition of WLC, morphhb, SBLGNT or Strong's it read,
so two runs months apart against a silently updated corpus differ with no way
to attribute the difference (L-13). Scripts communicate through CSV/JSON in
`output2/stats/`, `output3/stats/` with column and key names agreed nowhere;
`KeyError` (E-03, 24 observed) is the *lucky* outcome — the unlucky one is a
key that exists but means something other than the consumer assumes (L-14).

---

# Part 3b — Document-editing defects

Survey 0001 catalogued document *build and conversion* (S-09) but omitted
document *editing*. That was a gap, not a scope decision — and it hid the
best-evidenced case of silent measurement corruption in the workspace.

| ID | Defect | Extent |
|---|---|---|
| **D-01** | Invisible bidi marks embedded in documents. **Latent for measurement; real for editing and search** | 5,902 U+200E in 81 files; 222 spurious tokens in 30 files; read by no script |
| **D-02** | Inconsistent line endings | 187 files CRLF; **2 files mixed CRLF+LF** |
| **D-03** | UTF-8 BOM at file start | 6 files |
| **D-04** | Documents not NFC-normalized | 7 of 240 Hebrew-containing files |
| **D-05** | No verification that an edit produced the intended state | all 5,182 mutations |
| **D-06** | Cross-reference / anchor drift | transcript-evidenced only; weak mechanical signal |

## D-01 — the headline finding, and it is measured

Inline Hebrew in these documents is wrapped in **U+200E LEFT-TO-RIGHT MARK**
so it displays correctly inside left-to-right prose — stored as
`<U+200E>קנה<U+200E>`, displayed as if the marks were not there.
That is a reasonable thing to do *for display*. The problem is everything
downstream.

Distribution: `*****/output/paper/*****.md` **1,166**,
`*****/output/todo/*****.md` 502,
`*****/output/todo/approach-2/_appendix_distributions_raw.md` 488.
No RLM, LRE, RLE, LRO, RLO, LRI, RLI, FSI or PDI anywhere — only LRM, plus
6 stray inline U+FEFF and 2 soft hyphens.

**Exactly 1 of 102 scripts references U+200E** (`*****/pdf-build/build.py`),
and it *includes* the marks in its Hebrew-run regex for PDF layout rather
than stripping them. **No script removes them before measuring.**

The workspace's own diacritic stripper does not remove them either, because
U+200E lies outside the U+0591–U+05C7 range of L-04. Verified by execution:

```
token as stored in the .md   : '‎קָנָה‎'
after wlc.py strip_points()  : '‎קנה‎'
LRM survives                 : True
equals bare consonants קנה   : False
```

**Measured consequence on the actual paper** — `*****/output/paper/*****.md`:

| | distinct Hebrew tokens |
|---|---|
| as stored | **518** |
| after removing LRM | **436** |
| **spurious** | **82 (~16%)** |

>  **Measured 2026-08-07: nothing computes a statistic from this document.**
>  The inflation is real — 222 spurious distinct tokens across 30 files,
>  10.5% aggregate — but the 28 `.md`-reading scripts reference only four
>  paths, none of them an inflated document, and the one Hebrew document
>  they do read has zero LRM. No published count is affected. See
>  "Measured, 2026-08-07" above.

Any vocabulary count, hapax count, type-token ratio or lexical-overlap
statistic taken from these documents *would* be wrong by roughly that
margin, and nothing would raise. That makes this a loaded gun rather than a
fired one: the moment a counting script is pointed at `*****/output/`, the
10.5% becomes real numbers in a table.

D-01 also explains part of H-05's 74 failed edits: an invisible LRM sits in
the file, the model's `old_string` does not reproduce it, and the exact
match fails for a reason invisible in both strings.

## D-02 / D-03 / D-04 — the same class, smaller

Mixed line endings (D-02) break exact-string editing exactly as D-01 does,
and turn a one-line change into a whole-file diff that hides it. A BOM read
without `encoding='utf-8-sig'` (D-03) prepends `﻿` to the first token,
so the first heading of those 6 files silently fails any comparison.
Non-NFC documents (D-04) combined with L-05 (99 of 102 scripts do not
normalize) make the same word compare unequal across two files.

## D-05 — edits are never verified

159 mutations failed loudly (H-05, H-06, H-09, H-10, H-11). Nothing checks
whether a *successful* edit produced the intended document state: no
post-edit assertion, no diff review step, no round-trip check that a count
taken before the edit still holds after it.

## D-06 — stated weakly on purpose

Transcript evidence exists — *"doesn't match the bibliography anchor
`goreham` in `about/ressources/_index.md`"* (10 occurrences). But a
mechanical sweep found little to confirm it: only 6 reference-style links
exist workspace-wide, and my footnote check produced false positives from
regex syntax inside fenced code blocks. **Recorded as transcript-evidenced
only. I would not build a requirement on this without a better check.**

---

# Part 4 — Root causes

Eight causes account for every entry above. This is the list the function
library, the architecture and the test cases should be built against.

| ID | Cause | Covers | Addressable by a shared library? |
|---|---|---|---|
| **C-01** | **Encoding and normalization of Hebrew/Greek** | E-01, E-06, E-09; L-04, L-05, L-06 | **Yes** — highest volume, and L-04 shows it corrupts results, not just console output |
| **C-02** | **Untested, hand-rolled statistical machinery** | L-01, L-02, L-03, L-10 | **Yes** — one tested implementation replaces 15 ad-hoc ones |
| **C-03** | **Undefined data contracts between scripts** | E-03, L-14 | **Yes** — a declared schema with validation at both ends |
| **C-04** | **Path and environment assumptions** | E-02, E-05, E-07, E-08, E-10; L-11 | **Yes** — one resolver plus a dependency preflight |
| **C-05** | **Non-reproducibility** | L-03, L-13 | **Yes** — mandatory seed and corpus-version stamping in a run manifest |
| **C-06** | **On-the-fly generation artifacts** | E-04; L-07, L-08, L-12 | **Partly** — a library shrinks the surface; lint/import checks catch the rest |
| **C-07** | **Truncated or interrupted generation** | H-03 (114), H-01, H-05 | **No** — needs an integrity check on a generated script *before* it runs |
| **C-08** | **Validity defects invisible to mechanical checking** | L-09, and every miscount in §2c | **No** — needs a stated, testable check against the primary text; this is what the hand-caught miscounts were doing manually and unrecorded |
| **C-09** | **Document mutation without verification** | D-05, H-05, H-06, H-09, H-10, H-11 | **Partly** — a normalized document I/O boundary removes the D-01/D-02/D-03 causes of failed matching; verifying that an edit did what was meant is a process control |

**C-01 widens because of Part 3b.** Encoding and normalization are not a
script-input concern but a *document-lifecycle* concern: D-01 shows the
corruption is introduced during editing, for display reasons, and then read
back by 28 scripts as if it were plain text. Likewise **C-03** now covers
documents, not just CSV/JSON — a Markdown file is an interface between an
editing step and a measuring step, with no declared contract about what may
appear in it.

The practical consequence for step 2: the library needs a **document I/O
boundary**, not only a corpus I/O boundary. One place that reads a document
and normalizes it (NFC, strip bidi and invisible marks, canonical line
endings, BOM handling), one place that writes it back under the same rules,
with stripping applied *before* any measurement and display marks
reintroduced only at render time (S-09). Had that boundary existed, D-01
would have been impossible and the 82 spurious tokens in `*****.md`
would never have entered a count.

C-01 through C-05 are the mandate for the parameterized function library that
step 2 of the task asks for. C-06, C-07 and the verification half of C-09
are process controls around generation and editing rather than library
functions. C-08 is the residue that cannot be automated away — the point at which a human verification step has
to be designed in deliberately, and recorded, rather than left to whoever
happens to notice.
