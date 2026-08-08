# Architecture diagrams

**Source:** step 4 of [`../input/task.md`](../input/task.md) — *"Create an
architecture diagram."*
**Companion to:** [`architecture.md`](architecture.md) (decisions AD-1…AD-7)
and [`requirements.md`](requirements.md).
**Date:** 2026-08-07.

Written as Mermaid rather than an exported image so the diagrams are
diffable, reviewable in a commit, and cannot drift silently from the prose —
the same reasoning the manual gives for keeping everything else in git.
They render in VS Code, GitHub, and pandoc with a Mermaid filter.

---

## 1. Layers

Dependencies point downward only; a cycle is a defect. `run` is dotted
because it is ambient — used by every layer, depending on none.

```mermaid
flowchart TB
    subgraph L4["L4 · Claims"]
        verify["<b>verify</b><br/>claim · report<br/>PASS / FAIL / PARTIAL / UNDECIDABLE / GUARD"]
    end

    subgraph L3["L3 · Measurement"]
        count["<b>count</b><br/>distribution unit= · vocabulary<br/>hapax · tfidf · similarity"]
        structure["<b>structure</b><br/>Scheme · cover · score<br/>null_schemes kind="]
        stats["<b>stats</b><br/>policy wrappers only"]
        render["<b>doc.render</b>"]
    end

    subgraph L2["L2 · Typed access — the ONLY text entry points"]
        corpus["<b>corpus</b><br/>load source= · Word<br/>hits homographs= · fingerprint"]
        doc["<b>doc</b><br/>read · write · edit"]
    end

    subgraph L1["L1 · Foundation"]
        text["<b>text</b><br/>normalize · fold · same<br/>marks · audit"]
        schema["<b>schema</b><br/>versioned contracts"]
        run["<b>run</b><br/>paths · preflight · manifest"]
    end

    subgraph L0["L0 · Borrowed — never reimplemented"]
        stat_libs["scipy · scikit-learn · statsmodels"]
        conv["pandoc + Typst · python-bidi · pypdfium2"]
        misc["pandas · networkx · matplotlib<br/>jsonschema · pytest · hypothesis"]
        stdlib["<b>unicodedata</b> — stdlib"]
    end

    verify --> count
    verify --> structure
    verify --> stats
    count --> corpus
    count --> doc
    structure --> corpus
    stats --> stat_libs
    render --> doc
    render --> conv
    corpus --> text
    corpus --> schema
    doc --> text
    text --> stdlib
    schema --> misc
    count --> misc

    verify -.-> run
    count -.-> run
    structure -.-> run
    corpus -.-> run
    doc -.-> run

    style L0 fill:#eef,stroke:#88a
    style L2 fill:#efe,stroke:#8a8
    style stdlib fill:#ffe,stroke:#aa6
```

`unicodedata` is called out separately because it carries more of the design
than any installed dependency: `Mn` / `Cf` / `Pd` / `Po` replaces every
hand-maintained codepoint range, which is the direct fix for L-04 and D-01.

---

## 2. Data flow — AD-1 and AD-2

Two entry points, one normalization boundary, provenance travelling inside
the values.

```mermaid
flowchart LR
    subgraph sources["Sources"]
        wlc[("WLC / BHSA / SP<br/>LXX / SBLGNT / DSS")]
        md[("Markdown<br/>documents")]
    end

    pre{{"run.preflight<br/>binaries · modules · fonts<br/><b>AD-4: fail here, not mid-run</b>"}}

    norm["<b>text.normalize</b><br/>BOM → line endings →<br/>NFC/NFD → strip Cf<br/><b>AD-1: the only boundary</b>"]

    word["<b>Word</b> / <b>Document</b><br/><i>carries source, version,<br/>fingerprint — AD-2</i>"]

    meas["count · structure<br/><i>borrowed computation — AD-3</i>"]

    res["<b>Result</b><br/><i>carries method, seed, n,<br/>fingerprint, adjustment state</i>"]

    gate{"family size<br/>N > 1 ?"}
    adj["stats.p_adjust"]
    out["formatted output"]
    claim["verify.claim"]
    man[/"run.manifest<br/>seeds · versions · hashes"/]

    wlc --> norm
    md --> norm
    pre -.-> norm
    norm --> word --> meas --> res --> gate
    gate -- no --> out
    gate -- yes --> adj --> out
    gate -- "yes, unadjusted" --> blocked["<b>format() raises</b>"]
    out --> claim
    res -.-> man
    out --> render["doc.render<br/><i>display marks reintroduced<br/>here and nowhere else</i>"]

    style norm fill:#ffe,stroke:#aa6,stroke-width:2px
    style blocked fill:#fee,stroke:#a66,stroke-width:2px
    style gate fill:#eef,stroke:#88a
```

Note the last edge: bidi display marks are reintroduced **only** at render.
Nothing upstream ever sees them — the strip-on-read decision, drawn.

---

## 3. The central mechanism

The one diagram worth reading closely. It is the structural answer to why 11
of 15 scripts skipped a multiple-comparison correction that was one import
away: **producing 20 uncorrected p-values and producing 1 looked identical
at the point of printing.**

```mermaid
stateDiagram-v2
    [*] --> Computed : stats.permutation_test, rng required

    Computed --> Solo : declared family size = 1
    Computed --> Family : declared family size N > 1

    Solo --> Printable
    Family --> Adjusted : p_adjust saw the whole family
    Adjusted --> Printable

    Family --> Blocked : format() attempted
    Blocked --> Family : raises, nothing printed

    Family --> Escaped : .unadjusted_value
    note right of Escaped
        Deliberate, explicit, greppable.
        Bypassing is visible in review,
        never casual.
    end note

    Printable --> [*]
    Escaped --> [*]

    note left of Computed
        rng has NO default.
        scipy will run unseeded;
        the wrapper will not. (L-03)
    end note
```

---

## 4. Traceability — defect to requirement

Every module exists because something measurably went wrong. Nothing in the
design traces to a hypothetical.

```mermaid
flowchart LR
    subgraph obs["Measured defects"]
        d1["L-04 · D-01<br/>ranges & invisible marks"]
        d2["L-02 · L-03 · L-10<br/>20 divergent stat impls"]
        d3["E-03 · L-14<br/>24 KeyError"]
        d4["E-02 · E-05 · E-07<br/>environment"]
        d5["L-13<br/>no provenance"]
        d6["H-05 · D-05<br/>159 failed edits"]
        d7["L-09 · miscounts<br/>validity"]
    end

    subgraph cause["Root causes"]
        c1["C-01"]
        c2["C-02"]
        c3["C-03"]
        c4["C-04"]
        c5["C-05"]
        c9["C-09"]
        c8["C-08"]
        c7["C-07"]
    end

    subgraph mod["Modules"]
        m1["text · doc.read"]
        m2["stats"]
        m3["schema"]
        m4["run.preflight"]
        m5["run.manifest"]
        m6["doc.edit"]
        m7["verify.claim"]
        none["<b>nothing</b>"]
    end

    subgraph req["Requirements"]
        r1["T-01…T-07<br/>D-01…D-08"]
        r2["S-01…S-07"]
        r3["X-01…X-03"]
        r4["E-01 · E-02"]
        r5["E-03 · E-04"]
        r6["D-02 · D-03"]
        r7["V-01 · V-02"]
    end

    d1 --> c1 --> m1 --> r1
    d2 --> c2 --> m2 --> r2
    d3 --> c3 --> m3 --> r3
    d4 --> c4 --> m4 --> r4
    d5 --> c5 --> m5 --> r5
    d6 --> c9 --> m6 --> r6
    d7 --> c8 --> m7 --> r7
    c7 --> none

    style none fill:#fee,stroke:#a66
    style c7 fill:#fee,stroke:#a66
```

**C-07 deliberately terminates in nothing.** 114 mid-stream truncations are
real and unaddressed: a library cannot detect that the script calling it was
written by an interrupted response. Drawing an arrow there would be the
false confidence this project exists to avoid.

C-08 reaches `verify.claim`, which **records** a human judgment about
validity — it does not supply one. C-06 appears nowhere: it is reduced only
as a side effect of there being less code to generate wrongly.

---

## 5. Reading order

1. §3 first — it is the design's actual argument.
2. §1 for structure, §2 for how text moves.
3. §4 last, as the audit: every box traces back to something measured.

Two boxes in §1 are riskier than they look. **`corpus`** is the only module
with no free equivalent and the largest to build — eight source formats
behind one `Word` shape, verified so far for WLC and three Text-Fabric
corpora only. **`stats`** is drawn as a thin wrapper on the assumption that
scipy's `permutation_type` can express the workspace's null models; that is
untested, and if it fails, `stats` grows real code and AD-3 weakens.
