# Proposal — licensing

**Asked:** propose licences, with pros and cons.
**Status:** proposal. Nothing added.
**Date:** 2026-08-07.

> **Not legal advice.** This is the same category as `CLAUDE.md` steps
> 11–13: pattern-matching and summary, not a determination. The manual's
> own Section 11 insists the human author makes the final call, and a
> licence is exactly such a call. Where real money or a real dispute is
> plausible, ask someone qualified.

---

## 1. The situation, measured

| Fact | Consequence |
|---|---|
| `git-based-ai-research-workflow` is **public and has NO LICENSE** | Default is **all rights reserved**. Nobody may legally copy the template — while the manual's Section 17 tells them to `cp -r templates/new-topic-repo …` |
| Every runtime dependency is permissive | BSD-3-Clause (scipy, scikit-learn, networkx, pypdf), BSD (statsmodels, pandas), MIT (pytest, jsonschema, pypandoc), PSF (matplotlib) |
| Two non-permissive dependencies, neither binding | `hypothesis` is **MPL-2.0** (file-level copyleft — triggers only if you modify hypothesis itself); `python-bidi` is **LGPL** (import is use, not derivation) |
| `pandoc` is **GPL** | Invoked as an external binary via `subprocess`, which does not create a derivative work |

**So no dependency forces a copyleft choice.** The decision is yours on the
merits, not forced by the stack.

**The un-licensed manual is the more urgent problem.** It is already public
and already instructs readers to copy from it.

---

## 2. The complication specific to this project

The manual documents it in Section 11.3, and it now applies to the manual's
own tooling: the **US Copyright Office's Part 2 report (January 2025)**
concluded that purely AI-generated output, without meaningful human
authorship, is **not copyrightable** in the US; a prompt alone is not enough
human control; but a human's creative selection, arrangement and
modification of AI output *can* be.

Most of `thscript/` and `docs/` was AI-drafted under your direction.

**You cannot license what you may not own.** That does not block anything —
it means:

- A **permissive** licence is the low-friction choice, because it grants
  broadly and so matters less if parts turn out to be uncopyrightable
  anyway.
- A **copyleft** licence is the one weakened by this: GPL's reciprocity is
  enforced *through* copyright. If the copyright is thin, so is the
  obligation, and you would be relying on a mechanism that may not hold.
- Either way, **say so plainly in a `NOTICE`** rather than claiming
  authorship you may not have. That is the same honesty the rest of this
  repository is built on, and it costs nothing.

---

## 3. Two different things need licensing

Common practice, and worth following: **code and prose take different
licences.** Software licences say nothing sensible about a document; CC
licences say nothing sensible about linking.

- **Code** — `thscript/`, `tests/`, `scripts/`, `spikes/`
- **Prose** — `docs/`, `guideline/`, the manual itself, `README.md`

---

## 4. Options

### For the code

| Licence | Pros | Cons |
|---|---|---|
| **MIT** | Shortest and most widely understood; near-zero friction for a student copying a template; compatible with everything in the stack | No explicit patent grant; no trademark clause; nothing to hang an AI-provenance statement on |
| **Apache-2.0** ⭐ | Explicit **patent grant**; explicit **`NOTICE` mechanism** — the natural place to state AI-assisted authorship; explicit "AS IS" disclaimer, which matters for a library that computes p-values; the de-facto standard for institutional open source | Longer, slightly more ceremony; per-file headers are conventional (not required) |
| **BSD-3-Clause** | Matches most of the scientific stack (scipy, sklearn); adds a no-endorsement clause, useful for a *department's* name | Like MIT, no patent grant and no NOTICE convention |
| **GPL-3.0** | Forces improvements back; ideologically consistent if the aim is that derived tooling stays open | Blocks use in any closed setting, which for a *department reference implementation* is friction with no upside; **reciprocity leans on copyright strength that §2 makes uncertain**; incompatible with some downstream academic reuse |
| **AGPL-3.0** | GPL plus network use | All of GPL's costs, and this is a library, not a service. **Not a fit** |
| **Unlicense / CC0** | Maximum reuse; sidesteps the ownership question by disclaiming rights entirely | No warranty disclaimer in some readings; not recognised in every jurisdiction; gives up attribution, which for academic work is the one thing usually worth keeping |

### For the prose

| Licence | Pros | Cons |
|---|---|---|
| **CC BY 4.0** ⭐ | Anyone may copy, adapt and teach from the manual **with attribution** — exactly what a department manual wants; standard in academia; internationally drafted | Permits commercial reuse, which some find uncomfortable |
| **CC BY-SA 4.0** | Adaptations stay open | "Share-alike" complicates mixing into other course material — friction against the manual's purpose |
| **CC BY-NC 4.0** | Blocks commercial reuse | "Non-commercial" is notoriously ill-defined; blocks a paid workshop or a publisher's textbook — plausible futures for a manual |
| **CC0** | Frictionless | Gives up attribution, which is the currency of academic work |

---

## 5. Recommendation

**Apache-2.0 for code + CC BY 4.0 for prose**, with a `NOTICE` stating
AI-assisted authorship.

Reasoning, in order of weight:

1. **Attribution is the thing worth keeping**, and the only thing. Both
   licences preserve it; neither obstructs the audience — students,
   colleagues, other departments — this work exists for.
2. **Apache-2.0's `NOTICE` is the right home for the AI-provenance
   statement.** No other permissive licence has a designated place for it.
3. **The "AS IS" disclaimer is not boilerplate here.** This library
   computes p-values that may end up in published papers. `docs/` already
   states plainly that two critical weaknesses are open. A licence that
   disclaims warranty is consistent with documentation that admits its own
   gaps.
4. **Copyleft buys nothing in this setting** and relies on a copyright
   strength §2 makes uncertain.

**If you want less ceremony: MIT + CC BY 4.0.** Nearly the same practical
outcome, one paragraph instead of a page. The loss is the patent grant and
the NOTICE convention — put the AI statement in the README instead.

---

## 6. Suggested `NOTICE`

```
thscript / git-based-ai-research-workflow
Copyright 2026 Hagen Schilder

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy at http://www.apache.org/licenses/LICENSE-2.0

AUTHORSHIP AND AI ASSISTANCE
This work was produced with substantial AI assistance, under human
direction, using the workflow this repository documents. The complete
record of what was asked and answered was kept as the work proceeded.

The US Copyright Office (Copyright and Artificial Intelligence, Part 2,
January 2025) holds that purely AI-generated material is not
copyrightable, while a human's creative selection, arrangement and
modification of such material may be. No claim is made here as to which
portions fall on which side of that line. The licence above is granted
over whatever is owned; nothing in it asserts ownership of what is not.

Documentation (docs/, guideline/) is licensed separately under
Creative Commons Attribution 4.0 International (CC BY 4.0).
```

That last paragraph is the part I would not omit. It is honest, it costs
nothing, and it is the same discipline as recording the four falsified
counts rather than quietly deleting them.

---

## 7. To apply

1. `LICENSE` — Apache-2.0 text, repository root
2. `NOTICE` — as above
3. `docs/LICENSE-docs` — CC BY 4.0, or a one-line pointer in each README
4. `pyproject.toml` — `license = "Apache-2.0"`
5. `README.md` — one line stating the split

**Do it in the workflow repository first**, before the tooling lands there.
It is public today, has readers today, and tells them to copy — with no
licence permitting it.

---

## 8. What I need from you

1. **Apache-2.0 + CC BY 4.0**, or **MIT + CC BY 4.0**, or something else?
2. **Copyright holder** — you personally, or the department/institution?
   If you produced this in an employed capacity, the institution may own it
   regardless of what the file says, and that is worth checking before
   publishing rather than after.
3. **Keep the AI-authorship paragraph?** I recommend yes and would argue
   for it, but it is an unusual thing to publish and the choice is yours.
