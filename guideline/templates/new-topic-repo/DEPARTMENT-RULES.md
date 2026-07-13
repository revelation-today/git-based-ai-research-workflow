# Department/program-specific rules

**For department administrators:** fill this file in once, here in the
template (`templates/new-topic-repo/DEPARTMENT-RULES.md`), before
distributing it further. Every new topic repository created from
`cp -r templates/new-topic-repo ...` (see `README.md` Section 16) inherits
whatever this file says *at the time it's copied* — that's the whole
mechanism, no separate installation step. If your rules change later,
existing repositories keep the version they were created with (a feature,
not a bug — see Section 17 of the manual on why silently changing a
standing instruction after the fact is worse than a stale one you can see).

**For students/researchers:** this file, if your copy has one filled in, adds
to — and can only *tighten*, never loosen — the default process in the main
manual (`../../README.md`). Read it before your first AI request in this
repository. Your AI assistant is instructed (see `CLAUDE.md`, Step 0) to read
and follow it automatically.

---

## How to write a rule here so the AI can actually act on it

Same discipline as Section 7 of the manual applies to writing rules, not
just questions: a rule the AI can act on is specific and checkable. Compare:

- Good: *"All citations must use SBL (Society of Biblical Literature) style,
  not Chicago or MLA."* — checkable against a specific named standard.
- Bad: *"Cite properly."* — not actionable; "properly" by whose standard?
- Good: *"For any assignment marked `[no-AI]` in its own instructions, do
  not use this workflow at all — write and research without AI assistance,
  full stop."*
- Bad: *"Use good judgment about when AI is appropriate."* — pushes a
  judgment call onto the AI that only the instructor can actually make.

A rule that only a human can evaluate (e.g. "make sure the argument is
theologically sound") isn't wrong to state, but say so plainly — mark it as
something the AI should flag for human judgment, not something it can
verify itself (this mirrors Section 11.7's three-way split: scriptable,
AI-pattern-check, or human-only).

---

## Example department rules (replace this whole section with your own)

*(The block below is a worked example, not a real policy — delete or
replace it entirely when adopting this template. It's here so a first-time
department administrator has a concrete shape to copy, per Section 6.2's
"specify the exact format" advice applied to writing rules about rules.)*

### Citation style

All citations in `paper.md` and any generated book/paper must use **SBL
style** (Society of Biblical Literature Handbook of Style). If an AI answer
suggests a citation in a different format, reformat it before adding it to
`sources.md` — this is mechanical enough that the AI can do it itself.

### Language requirements

Seminar papers: English or German, either is acceptable. Thesis submissions:
German only, with an English abstract. If a draft is in the wrong language
for its target, flag it — don't translate it automatically, since translation
choices for a thesis are the student's own to make deliberately (Section 5).

### Per-assignment AI permission

Check the specific assignment instructions for an explicit AI policy tag
before starting:
- `[ai-ok]` — this workflow applies as described in the main manual.
- `[ai-disclosed-only]` — AI assistance is allowed but must be disclosed in
  a dedicated section of the final submission, generated from
  `ai-requests/` per Section 6 of the manual.
- `[no-ai]` — do not use this workflow, or any AI assistance, for this
  specific piece of work. If no tag is present, treat the assignment as
  `[ai-disclosed-only]` by default, and ask the instructor to confirm if
  genuinely unclear — never assume `[ai-ok]` by default.

### Stricter fact-checking for capstone/thesis work

For any repository whose `README.md` describes itself as a thesis or
capstone (not a regular seminar paper), every claim central to the argument
must reach at least "Moderately attested" (Section 6.5) before submission —
"Proposed, plausible" is not sufficient for a claim the thesis's own
conclusion depends on. Regular seminar papers follow the manual's normal
minimum bar (checked or logged in `TODO.md`) without this stricter
threshold.

### Additional required disclosure text

Beyond the standard disclosure statement (`CLAUDE.md` Step C, item 13), this
program requires the exact sentence: *"Generative AI was used in the
preparation of this work in accordance with [Department]'s AI-use policy,
version [X], and a full record of its use is available on request."*
Append this verbatim to any generated disclosure statement before
submission.
