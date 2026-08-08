# Public-library validation

**Source:** step 2 follow-up — *"validate which functionality is already
available for free as public libraries and make use of it."*
**Method:** every row was **executed** in this environment, not recalled.
**Environment:** Python 3.13.14, Windows 11.
**Date:** 2026-08-07.

---

## 1. Headline

**The largest module I proposed does not need to exist.** `thscript.stats`
— which [`functions.md`](functions.md) called "the most important module,
because it is where wrong answers are most expensive" — is already free in
`scipy.stats`, and the workspace's 37 hand-rolled copies were reimplementing
it.

**The most important defect in the catalogue is fixed by the standard
library**, with no dependency and no codepoint range.

Net effect: **~55 proposed functions → roughly 18 that are genuinely ours.**

---

## 2. What is installed here

| Package | Status |
|---|---|
| numpy 2.5.1, scipy 1.18.0, scikit-learn 1.9.0, networkx 3.6.1, matplotlib 3.11.1 | **installed** |
| pandoc 3.10 | **installed** |
| statsmodels, pandas, pytest, hypothesis, python-bidi, pypandoc, jsonschema | missing *(→ **installed**, §8)* |
| text-fabric, regex, pydantic | missing, not adopted |
| **PDF engines** — xelatex, pdflatex, weasyprint, wkhtmltopdf, pdftoppm | **all missing** *(→ **Typst installed**, §8)* |

*The rows above record the state at the time of validation. Everything was
installed afterwards on the same day — see §8 for what worked and what did
not.*

**Reproduced E-05 live.** `pandoc md → html` renders Hebrew and Greek
perfectly, maqaf intact:

```
$ pandoc ip.md -t html
<p>Hebrew: אֶת־הָאָרֶץ Greek: *****</p>

$ pandoc ip.md -o ip.pdf
'pdflatex' not found. Please select a different --pdf-engine
```

Document conversion to PDF could not work on this machine at all. That is
the same class as E-05's 11 `pdftoppm is not installed` failures, and it is
precisely what `run.preflight` exists to catch before an hour of work rather
than after. **Now fixed with Typst — see §8.**

---

## 3. The finding that matters most: `unicodedata.category`

L-04 (the over-wide strip range) and D-01 (invisible bidi marks) are **the
same bug**: a hand-written codepoint range that does not know what the
codepoints *are*. The standard library does know.

Executed:

| Codepoint | Name | `unicodedata.category` |
|---|---|---|
| U+05B8 | QAMATS (vowel) | **Mn** |
| U+0591 | ETNAHTA (cantillation) | **Mn** |
| U+05C7 | QAMATS QATAN | **Mn** |
| U+05BE | **MAQAF** | **Pd** — *dash punctuation, not a mark* |
| U+05C0 | PASEQ | **Po** |
| U+05C3 | SOF PASUQ | **Po** |
| U+200E | LRM | **Cf** |
| U+FEFF | BOM | **Cf** |
| U+00AD | SOFT HYPHEN | **Cf** |
| U+FB2B | shin+sin presentation form | **Lo** |

So:

- **`Mn` is exactly "vowels and cantillation"** — what `strip_points` meant.
- **`Cf` is exactly the invisible/bidi set** — D-01, with no list to maintain.
- **`Pd`/`Po` is the punctuation the hardcoded range wrongly swallowed** — L-04.

Demonstrated side by side on real input:

```
maqaf-joined   stored        : 'אֶת־הָאָרֶץ'
               buggy range   : 'אתהארץ'      <- two words merged
               category fold : 'את־הארץ'     <- boundary preserved

LRM-wrapped    stored        : '<LRM>קָנָה<LRM>'
               buggy range   : '<LRM>קנה<LRM>'  <- invisible marks survive
               category fold : 'קנה'            <- clean
```

The whole of `text.fold`'s hand-maintained range logic collapses to:

```python
''.join(c for c in s if unicodedata.category(c) not in ('Mn', 'Cf'))
```

**Nothing to install. Nothing to keep in sync with a Unicode revision.**

### A correction this produced

`problems.md` recorded L-04 as latent with measured impact zero, because
maqaf never appears inside a `<w>` token in the WLC corpus. That holds for
the **corpus** path. It does not hold for the **document** path: **243
inline maqaf characters across 44 Markdown documents**. So L-04 is
corpus-path dead but **document-path live** — and S-13 (document-derived
measurement) is exactly the situation the library is meant to enable. Still
unfired, because no script folds those documents today.

---

## 4. `scipy.stats` replaces the entire statistics module

Every one of these was confirmed present in scipy 1.18.0 by attribute check
and, where it matters, by execution:

| `functions.md` proposed | Free replacement | Verified |
|---|---|---|
| `stats.permutation_test` (two-sample) | `scipy.stats.permutation_test` | ✅ executed |
| `stats.permutation_test` (**structural nulls**) | **`scipy.stats.monte_carlo_test`** with a custom `rvs` | ✅ executed — see the correction below |
| `stats.exact_test(kind="hypergeometric")` | `scipy.stats.hypergeom` | ✅ present |
| `stats.exact_test(kind="binomial"/"fisher-exact")` | `scipy.stats.binomtest`, `fisher_exact` | ✅ present |
| `stats.p_adjust(method="bh"/"by")` | `scipy.stats.false_discovery_control` | ✅ executed |
| `stats.combine(method="fisher"/"stouffer")` | `scipy.stats.combine_pvalues` | ✅ present |
| `stats.bootstrap_ci` | `scipy.stats.bootstrap` | ✅ present |
| `stats.agreement(method="cohen")` | `sklearn.metrics.cohen_kappa_score` | ✅ present |
| `count.tfidf` | `sklearn.feature_extraction.text.TfidfVectorizer` | ✅ present |
| `count.similarity`, `count.matrix` | `sklearn.metrics.pairwise.cosine_similarity` | ✅ present |
| — | `scipy.stats.monte_carlo_test` | ✅ present (bonus) |

### The decisive check

The eight hand-rolled `pval` copies use `(k+1)/(n+1)`. Does scipy agree, or
would adopting it silently change published numbers?

```
scipy p     = 0.269000
(k+1)/(n+1) = 0.269000     <- workspace's formula
k/n         = 0.268268
MATCHES: True
```

**scipy uses the same +1 estimator.** Replacing all 8 copies with
`scipy.stats.permutation_test` does not move a single published p-value.
That removes the main risk of adopting it.

And `false_discovery_control` executed correctly on a known BH input,
returning both `bh` and `by` — replacing the 3 divergent `bh`/`bh_correction`
implementations.

### Correction, 2026-08-07 — which scipy function

This section originally named `permutation_test` as the replacement for all
8 hand-rolled `pval` copies. **That is right for two-sample comparisons and
wrong for the structural nulls**, which are the majority of S-04.

The workspace's structural null — k marker positions drawn from N, each
covering ±W, statistic = target points covered — is not a relabelling of
observed data. There is no second sample and no pairing, so none of
`permutation_test`'s three `permutation_type` values can express it.

**`scipy.stats.monte_carlo_test` can, exactly.** Spiked by execution:

```
hand-rolled loop            p = 0.600570
scipy.stats.monte_carlo_test p = 0.600570     difference 0.000000
```

It also uses the same `(k+1)/(n+1)` estimator. AD-3 survives — `stats`
stays a policy wrapper — but over **two** scipy entry points, not one.

**Only Bonferroni and Holm are absent from scipy.** `statsmodels`
(`multipletests`) has them, or they are four lines each. Not a reason for a
module.

---

## 5. The rest

| Proposed | Free replacement | Keep? |
|---|---|---|
| `text.normalize` | `unicodedata.normalize` | thin wrapper (defaults only) |
| `text.fold` | `unicodedata.category` | **~20 lines**, not a range table |
| `text.same`, `open_text`, `configure_stdout` | stdlib | trivial, keep |
| `doc.render` | **pandoc 3.10** (+ `pypandoc`) | wrapper only |
| `doc.read/write/edit` | `python-bidi` for display marks | **keep** — the strip-on-read boundary and normalized-match editing are ours |
| `schema.*` | `jsonschema` / `pydantic` / `pandera` | **delete** — adopt one |
| `verify.check` | `pytest` + `@pytest.mark.xfail(strict=True)` | **mostly delete** — see below |
| `count.distribution(unit=)` | `pandas` groupby | thin wrapper |
| `structure.*` | `networkx` for graphs only | **keep** — scheme scoring and null generation are domain-specific |
| `corpus.load` | `text-fabric` (BHSA only), `pysword` | **keep** — nothing free unifies WLC/BHSA/SP/LXX/SBLGNT/DSS behind one `Word` shape |
| `run.manifest`, `run.preflight`, `run.paths` | — | **keep**, small |

### On `verify`

`pytest` supplies the harness. Its `xfail(strict=True)` is a close match for
the `FAIL` verdict — *"this claim is falsified, and that is the recorded
finding."* What pytest has no vocabulary for is **`UNDECIDABLE`** — *"the
corpora disagree and both encodings are pinned here"* — which
`test_seed_claims.py` already needed and used. That stays ours, as a thin
marker layer over pytest, not a replacement for it.

---

## 6. Revised shape of the library

**Ours (~18 functions):**

- `corpus` — multi-source unification, `Word` shape, version fingerprint (S-01)
- `text.fold` / `same` — category-based, Hebrew/Greek-aware defaults (C-01)
- `doc.read` / `write` / `edit` — strip-on-read boundary, normalized matching (D-01..D-05, H-05)
- `structure` — scheme scoring, null-scheme generation (S-03)
- `run` — `paths`, `preflight`, `manifest` (C-04, C-05)
- `verify.claim` + `UNDECIDABLE` marker (C-08)

**Borrowed:** scipy, scikit-learn, numpy, networkx, matplotlib, pandoc,
pytest, jsonschema, python-bidi, pandas.

**The library's job changes.** It is no longer "implement statistics" — it
is **"make the free implementations impossible to misuse."** Concretely, the
three guard rails from `functions.md` are now the main contribution, because
scipy does not enforce them:

- **R2** — `scipy.stats.permutation_test`'s `rng` has a default, so it runs
  unseeded without complaint. That is L-03 (9 scripts, one reporting a
  p-value). Our wrapper makes `rng` required.
- **R3** — scipy returns a bare float. It cannot know the corpus version.
  Our `Result` carries seed, corpus fingerprint and method.
- **R5** — `scipy.stats.false_discovery_control` exists and 11 of 15 scripts
  still did not call it. Availability was never the problem. Our `Result`
  refuses to format an unadjusted member of a p-value family.

That is a smaller library and a better one: the parts most likely to be
wrong are now maintained by people who test them, and what remains is the
policy layer that the workspace's evidence shows was actually missing.

## 7. To install

```
scipy numpy scikit-learn networkx matplotlib   # present
pytest pypandoc python-bidi jsonschema pandas  # add
statsmodels                                    # only if Bonferroni/Holm wanted
```

Plus **a PDF engine** — none is installed, so `doc.render(to="pdf")` cannot
work today. `weasyprint` (pip, no LaTeX) is the lightest fix; Typst or
TeX Live are alternatives. Whichever is chosen, `run.preflight` must check
it, because this is E-05 waiting to happen again.

## 8. Installed 2026-08-07 — results

All requested packages installed and verified by execution. See
[`../requirements.txt`](../requirements.txt) for the pinned set.

| Package | Version | Verified |
|---|---|---|
| statsmodels | 0.14.6 | ✅ `multipletests` gives bonferroni + holm; its `fdr_bh` output is **identical** to scipy's `false_discovery_control(method="bh")` — a useful cross-check between two independent implementations |
| pandas | 3.0.5 | ✅ imports |
| pytest | 9.1.1 | ✅ imports |
| hypothesis | 6.165.2 | ✅ imports |
| jsonschema | 4.26.0 | ✅ imports |
| pypandoc | 1.17 | ✅ imports |
| python-bidi | 0.6.11 | ✅ `get_display` reorders a Hebrew run correctly |
| pypdf, pypdfium2 | 6.4.0, 5.0.4 | ✅ — but see §9 |

**`weasyprint` does not work on this machine.** `pip install` succeeds;
`import weasyprint` fails with `cannot load library 'libgobject-2.0-0'`. It
needs GTK, which is not installed. **Do not depend on it.**

**The working PDF engine is Typst 0.15.1**, installed via
`winget install Typst.Typst`. A single binary, no LaTeX, no GTK. pandoc must
be given its full path (`--pdf-engine=C:\...	ypst.exe`) until the Typst
directory is added to PATH.

Also note: pip console scripts land in a directory not on PATH. Use
`python -m pytest`, not `pytest`.

---

## 9. Hebrew PDF verification cannot be done by extracting text

Testing the full chain end to end produced the most useful result of this
pass, and it invalidates part of what `functions.md` proposed.

`pandoc t.md -o t.pdf --pdf-engine=typst` on a file containing
`אֶת־הָאָרֶץ`, `קנה` and `***** ἀρνίον`:

- **The PDF renders correctly.** Verified by rasterizing page 1 with
  `pypdfium2` and looking at it: right-to-left order correct, maqaf present,
  vowel points correctly positioned, Greek breathing marks intact.
- **Text extracted from that same correct PDF is wrong.** `pypdf` returns
  `ץרֶאָרֶההָת־רֶ` for `אֶת־הָאָרֶץ`.
- **It is not merely reordered.** The character *multiset* does not match
  either: extraction **loses a HEBREW LETTER ALEF** and **invents a second
  RESH and HE**. Unpointed `קנה` and Greek both survive extraction fine — it
  is specifically pointed RTL text that breaks.

**Consequence for `doc.verify_render`.** The design in `functions.md` said
it would "re-extract text from the rendered artifact and check that every
Hebrew and Greek run survived." **That cannot work.** Applied here it would
report a corrupted PDF that is in fact perfect — a false alarm on every
pointed-Hebrew document, which is the fastest way to get a check disabled.

What can actually work, in order of cost:

1. **Greek and unpointed Hebrew** — text extraction is reliable; check them
   this way.
2. **Embedded font coverage** — assert the PDF's fonts contain glyphs for
   every codepoint in the source. Cheap, and catches the common real
   failure (a font silently dropping pointing). Necessary, not sufficient.
3. **Rasterize and compare** — the only check that verifies pointed Hebrew
   actually rendered. Expensive, and needs a reference image.
4. **A human looking at the page** — which is what happened here, and what
   C-08 already says cannot be automated away.

---

## 10. What was *not* validated

Availability was tested; **suitability was not**. Specifically untested:

- whether `scipy.stats.permutation_test`'s `permutation_type` options cover
  the null models `build_space` / `random_point_scheme` actually implement
  (4 divergent versions — they may not all be expressible);
- whether `TfidfVectorizer`'s tokenizer can be driven from a lemma list
  rather than surface text without fighting it;
- `text-fabric` — still not installed; its row remains a judgment.
  (`python-bidi`, `pypandoc`, `jsonschema`, `pandas` and `statsmodels` were
  installed and executed on 2026-08-07 — see §8.)
- Whether Typst's bidi handling is correct for *every* Hebrew construction,
  or only for the one test string rendered here. One correct page is
  evidence, not coverage.
