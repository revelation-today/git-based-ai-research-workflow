---
description: Check TODO.md for open items, and scan paper.md for wrong facts, contradictions, weak arguments, and misplaced citations
---

Run this repository's standard "adversarial reader" pass (department manual
Section 6.1) against `paper.md`, using `sources.md` and `TODO.md` as ground
truth. Do the following, in order, and report a short summary back to the
user at the end — don't just write files silently.

1. **Open items.** List every unresolved (`[ ]`) item currently in
   `TODO.md`, with the commit hash it references, so nothing sits forgotten.
2. **Wrong facts.** For each factual claim in `paper.md` that has a
   corresponding entry in `sources.md`, check whether the claim's current
   wording still matches what the source actually says — a source can be
   correct while a later edit to `paper.md` has quietly drifted from it.
   List any mismatch in `wrong_facts.md`: the claim, what `paper.md` says
   now, what the source actually supports.
3. **Contradictions.** Scan `paper.md` for statements that contradict each
   other, including a claim that contradicts something a `TODO.md` item
   already resolved. List them in `contradict.md`.
4. **Citation placement.** Flag any paragraph making more than one distinct
   claim with all its citations bundled at the end rather than attached
   per-sentence (see `../../../tutorial-git-markdown-pdf.md`, "Fixing
   citation/footnote placement").
5. **Weak arguments.** Flag any argument that reads as unusually thin or
   unsupported even where no specific citation is technically missing
   (Section 6.1's `weak_arg.md`).

**Archive this run like any recurring instruction (Section 6.2):** this
command file is the instruction file being used; log the run as its own
`ai-requests/NNNN-update-paper-check/` entry via the normal Step A, and
note in `question.md` that `/update_paper` was the instruction invoked.

**Do not edit `paper.md` itself in this pass** — this is a checking task,
not a drafting task. Findings go into `wrong_facts.md` / `contradict.md`
and the summary you report; applying any actual fix is a separate, later
AI-request cycle, proposed and confirmed like anything else (Section 6.6).
