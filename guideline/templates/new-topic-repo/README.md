# <Topic title>

**Research question:** <one or two sentences stating exactly what this
repository is trying to answer>

**Status:** <e.g. "drafting", "fact-checking pending items in TODO.md",
"ready for supervisor review">

## Contents

- `paper.md` — the paper/notes being written for this topic.
- `sources.md` — bibliography, updated as sources are found and verified.
- `TODO.md` — open fact-checks and open questions. See
  [../../README.md](../../README.md) Section 14 for the workflow this
  supports.
- `ai-requests/` — one numbered folder per AI question asked in service of
  this paper, each containing the verbatim `question.md` and `answer.md`.
- `CLAUDE.md` — tells the AI assistant how to maintain this repo automatically.
- `DEPARTMENT-RULES.md` — optional local rules your program adds on top of
  the manual's defaults (Section 18).
- `.claude/settings.json` — a harness-enforced check that runs automatically
  after every commit (Section 11.7, Section 18).
- `.claude/commands/update_paper.md` — run as `/update_paper`: checks
  `TODO.md` for open items and scans `paper.md` for wrong facts,
  contradictions, weak arguments, and misplaced citations (Section 6.1).

## Convenience command: `/update_paper`

Run `/update_paper` any time you want a checking pass without re-typing the
Section 6.1 instructions by hand. It reads `paper.md` against `sources.md`
and `TODO.md`, writes findings to `wrong_facts.md` / `contradict.md`, and
reports a summary — it never edits `paper.md` itself; applying any fix it
finds is still its own separate, confirmed AI-request cycle.

## Workflow reminder

Every AI-assisted change to this repository follows the process in the
department manual: `../../README.md`, Section 14. In short, two lightweight
steps, each its own commit: **(A)** ask → archive the verbatim
question+answer under `ai-requests/` → commit immediately (nothing about the
paper changed yet, so nothing to decide first) — this is the *proposal*
commit. **(B)** only once you've actually decided to use it: apply it to the
paper/sources → default every claim to NOT YET CHECKED in `TODO.md` → answer
one optional "anything to add?" prompt if you have something → commit
separately, referencing the proposal commit (message per
`../commit-message-template.txt`). Skip both steps entirely for exploratory
questions that never touch the paper (Section 1).
