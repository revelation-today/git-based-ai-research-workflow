# tooling — `thscript`, a reference implementation of this workflow

**Everything you need to start is on this page.** For humans and for AI
assistants alike.


> **What this is.** A Python library built end to end through the workflow
> documented in [`../guideline/README.md`](../guideline/README.md) — survey,
> function list, architecture and requirements, diagram, test plan, then
> test-driven implementation.
>
> It is here as **evidence that the workflow produces something**, including
> the parts that did not survive contact with measurement: `docs/` records
> four extent counts that were falsified and two headline findings that
> evaporated once actually measured. A manual arguing for traceable,
> checkable claims should be able to show its own.
>
> The audit trail that produced it (`ai-requests/`) stays in the private
> working repository, along with the researcher's brief. What is here is
> the library, its tests, and the design record.

---

---

## What this is, and why

AI writes analysis scripts on the fly. They are patched when they break —
but they are never fully tested, and **they produce wrong answers silently**,
which matters most exactly where it hurts most: when a measurement ends up
in a paper.

This repository does two things about that:

1. **`thscript/`** — a Python library that makes specific silent failures
   structurally impossible rather than merely avoidable.
2. **`docs/`** — the evidence trail: what actually went wrong across ~1,700
   session transcripts and 102 scripts, measured, and what follows from it.

Every module here exists because something measurably went wrong. Nothing
was built against a hypothetical.

> **Honest status:** the library covers about **half** of the identified
> need. Seven modules are built and tested; eight use cases have no
> implementation yet. Two known-critical design weaknesses are open. See
> [Status](#status) — that section is not decoration.

---

## Quick start

```bash
git clone https://github.com/revelation-today/git-based-ai-research-workflow
cd git-based-ai-research-workflow/tooling
python -m pip install -r requirements.txt

python -m pytest tests/ -q          # 129 tests
bash scripts/quality.sh             # every quality metric, reproducible
```

**Windows note:** pip console scripts install outside `PATH`. Use
`python -m pytest`, not `pytest`.

**PDF output** needs a PDF engine. `weasyprint` does **not** work on Windows
(needs GTK). Use Typst: `winget install Typst.Typst`, then restart your
shell so `PATH` updates.

### Five-minute tour

```python
from thscript import text, corpus, stats, doc

text.fold("אֶת־הָאָרֶץ")           # 'את־הארץ'  — maqaf survives; the
                                     # legacy range merged the two words
text.same(a, b)                      # never use raw == on Hebrew or Greek

c = corpus.load("osis", path="…/book.xml")
c.fingerprint()                      # ties any number to the exact bytes
c.hits(lemma="7965", homographs="all")   # policy is explicit, and recorded

d = doc.read("paper.md")             # BOM, line endings, normalisation,
                                     # invisible marks — all handled at read
doc.edit("paper.md", "old text", "new text")   # matches past invisible
                                     # characters and mark-order differences

r = stats.permutation_test(data, statistic=f, rng=20260807)   # rng required
```

---

## The library

Seven modules. Dependencies point downward; a cycle is a defect.

| Module | Does | Exists because |
|---|---|---|
| **`text`** | `normalize` `fold` `same` `marks` `audit` `tokens` `script_of` | ~217 `UnicodeEncodeError`; a strip range that deleted the word-joining maqaf; 99 of 102 scripts never normalising |
| **`corpus`** | `load(source=…)` → one `Word` shape; `hits(homographs=…)`; `fingerprint()` | 8 incompatible parsers; no script recorded which corpus version produced a number |
| **`stats`** | `permutation_test` `monte_carlo_test` `exact_test` `p_adjust` `combine` | 7 concepts implemented **37 times in 20 mutually different versions**; 11 of 15 p-value scripts applied no correction |
| **`doc`** | `read` `write` `edit` `render` `verify_render` | 5,902 invisible marks in documents; 159 failed exact-string edits |
| **`schema`** | `define` `read_table` `write_table` | 24 `KeyError` from one script writing `total` and another reading `total_words` |
| **`run`** | `paths` `preflight` `manifest` `Tally` | 16 scripts with absolute paths; 11 missing-binary failures found at the *end* of long runs |
| **`verify`** | `Suite` `Claims` `pin`/`compare` `traceability_gaps` | claims in papers with nothing tying them to a check |

### Two rules the library enforces that no library gives you free

- **`rng` is required.** `scipy.stats.permutation_test` runs unseeded
  without complaint. Nine scripts did; one reported a p-value that differed
  on every run.
- **A p-value in a family cannot be printed unadjusted.** Not because FDR
  is obscure — `scipy.stats.false_discovery_control` was always one import
  away — but because producing 20 uncorrected p-values and producing 1 look
  identical at the point of printing.

`thscript` computes almost nothing itself. scipy, scikit-learn, statsmodels,
pandoc and unicodedata do the work; this library makes them hard to misuse.

---

## The design record — read in this order

| # | Document | What it answers |
|---|---|---|
| 1 | [`docs/problems.md`](docs/problems.md) | What actually goes wrong, measured. IDs `S-*` `E-*` `H-*` `L-*` `D-*` `C-*` |
| 2 | [`docs/use-cases.md`](docs/use-cases.md) | **Read this second.** What round 1 missed, and why the method failed |
| 3 | [`docs/functions.md`](docs/functions.md) | The generalised function list |
| 4 | [`docs/libraries.md`](docs/libraries.md) | What already exists free, executed rather than recalled |
| 5 | [`docs/architecture.md`](docs/architecture.md) | 7 decisions, 4 layers, and what is *not* addressed |
| 6 | [`docs/architecture-diagram.md`](docs/architecture-diagram.md) | Four Mermaid diagrams; §3 is the design's actual argument |
| 7 | [`docs/requirements.md`](docs/requirements.md) | 40 testable requirements, each traced to a real defect |
| 8 | [`docs/test-plan.md`](docs/test-plan.md) | 46 cases + 21 edge cases |
| 9 | [`docs/quality-evidence.md`](docs/quality-evidence.md) | Coverage, static analysis, complexity — and §6, what they don't show |
| 10 | [`docs/review-code.md`](docs/review-code.md) | Weaknesses, refactor proposals, the inter-AI protocol |
| 11 | [`docs/review-structure.md`](docs/review-structure.md) | Configuration-management review |
| 12 | [`docs/ip-cleanup-proposal.md`](docs/ip-cleanup-proposal.md) | Removing sibling-repo IP; the chosen approach |

**In a hurry?** `problems.md` §"Measured 2026-08-07" and
`architecture.md` §3 carry most of the argument between them.

---

## Repository layout

```
thscript/     the library — 7 modules
tests/        129 tests; fixtures/ are generated and self-checking
spikes/       experiments that are NOT tests
docs/         the design record (table above)
```

---

## Status

### Built and tested

129 tests, 92% statement coverage, mypy clean, complexity A. Modules
`text` `corpus` `stats` `doc` `schema` `run` `verify`.

### Open — known and recorded, not hidden

| | Issue | Where |
|---|---|---|
| 🔴 | **The p-adjustment gate is opt-in.** Produce 3 p-values without `stats.family()` and the central invariant never engages | `review-code.md` W-1 |
| 🔴 | **Provenance auto-satisfies** with `corpus="unspecified"` | `review-code.md` W-2 |
| 🟠 | **Eight use cases have no implementation**: caveats, cross-document consistency, list consistency, multi-session reconciliation, tables/visualisations, PDF input, HTML output, script generation | `use-cases.md` |
| 🟠 | `corpus` advertises 8 sources, implements 1 (OSIS) | `review-code.md` W-4 |
| 🟠 | **No CI.** Nothing runs the checks but a human choosing to | `review-code.md` W-7 |
| 🟡 | `agreement()` and `bootstrap_ci()` untested | `quality-evidence.md` §2 |
| 🟡 | No mutation testing | `quality-evidence.md` §6 |

### Waiting on a decision from the researcher

- A **LICENSE** — required before the public export can be published.
- Whether `check-ip-boundary.sh` should **fail** the hook rather than
  report (it would fail today, on 36 `docs/` references).
- The `*****` identifiability question, open since the first commit
  (`TODO.md`).
- W-1's fix: three options proposed, one recommended.

### Publishing

This repository is **private and stays private** — it contains references
to unpublished sibling research. The shareable subset is *generated*, never
hand-edited:

```bash
bash scripts/export-public.sh <outdir> <pseudonym-map>
```

It refuses to publish if any sibling name survives or if the tests fail in
the export. The pseudonym map lives **outside** the repository — it is the
key that reverses the anonymisation.

---

## Licence

**Code** (`thscript/`, `tests/`, `scripts/`, `spikes/`) — Apache License
2.0, see [`LICENSE`](LICENSE).
**Prose** (`docs/`, this README) — CC BY 4.0, see
[`docs/LICENSE-docs.md`](docs/LICENSE-docs.md).
Copyright 2026 Hagen Schilder.

[`NOTICE`](NOTICE) records that this work was produced with substantial AI
assistance and makes no claim about which portions are copyrightable —
stated deliberately, on the same grounds as everything else here.

---

