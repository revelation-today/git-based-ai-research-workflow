# Working with AI in Theological Research and Paper Writing

A manual for the department: colleagues and students, on how to use AI assistance
responsibly and traceably when writing papers and doing research, organized with
standard software Configuration Management (CM) practice — i.e. git.

This manual is the entry point. It links to a copyable **template repository**
(`templates/new-topic-repo/`), a **worked example** (`example/`) that shows the
whole process on a small, real research question with real git commits,
[`access-control-for-it.md`](access-control-for-it.md) (IT-facing guidance on
keeping each researcher's repository private by default), and
[`tutorial-git-markdown-pdf.md`](tutorial-git-markdown-pdf.md) (a beginner's
walkthrough of git, Markdown, and producing a properly-cited PDF from your
draft — start there if any of those are new to you).

---

## How to read this manual: guideline vs. best practices

Not everything below carries the same weight, and treating a good idea as
if it were a rule (or a rule as if it were just a suggestion) is its own
kind of mistake. Three categories, used consistently throughout:

- 🔵 **Context** — background you need to understand *why* the guideline
  looks the way it does. Not itself a checklist item.
- 🟢 **Best practice** — recommended, genuinely useful, but a judgment call:
  adapt or skip based on the situation.
- 🔴 **Guideline (required)** — the actual process: the repository
  structure, the commit discipline, the legal/compliance points, the
  checklist. This is what "following this manual" means in practice.

| # | Section | Category |
|---|---|---|
| 1 | Why this process exists | 🔵 Context |
| 2 | How AI language models actually work | 🔵 Context |
| 3 | What hallucination is, and why you must check everything | 🔵 Context |
| 4 | What AI is genuinely good for | 🔵 Context |
| 5 | Division of labor: what you contribute, what AI contributes | 🔵 Context |
| 6 | Six techniques worth adopting deliberately | 🟢 Best practice (except 6.6, which is 🔴 required — Section 14 depends on it) |
| 7 | Writing good research questions | 🟢 Best practice |
| 8 | Recognizing flawed AI answers and feeding that back into better prompts | 🟢 Best practice |
| 9 | Using more than one AI to cover each other's blind spots | 🟢 Best practice |
| 10 | Cost awareness: using AI economically | 🟢 Best practice |
| 11 | Legal and institutional considerations | 🔴 Required |
| 12 | Configuration Management setup: repositories and folders | 🔴 Required |
| 13 | Collaborative work: co-authorship and supervision feedback | 🔴 Required (when applicable) |
| 14 | The request → document → commit → fact-check workflow | 🔴 Required |
| 15 | Commit message template | 🔴 Required |
| 16 | File and folder naming conventions | 🔴 Required |
| 17 | Using the template | 🔴 Required |
| 18 | Introducing department- or program-specific rules | 🔴 Required (when applicable) |
| 19 | Worked example | 🔵 Context (illustrative, not itself a rule) |
| 20 | Quick checklist | 🔴 Required |

In short: if you only have time to actually *follow* something, that's
Sections 11–18 and 20 (plus 6.6). Sections 1–5, 19 explain the reasoning;
Sections 6 (mostly), 7, 8, 9, 10 make you noticeably better at this without
being things a supervisor should check you did.

## Table of contents

1. [Why this process exists](#1-why-this-process-exists) 🔵
2. [How AI language models actually work](#2-how-ai-language-models-actually-work) 🔵
3. [What hallucination is, and why you must check everything](#3-what-hallucination-is-and-why-you-must-check-everything) 🔵
4. [What AI is genuinely good for](#4-what-ai-is-genuinely-good-for) 🔵
5. [Division of labor: what you contribute, what AI contributes](#5-division-of-labor-what-you-contribute-what-ai-contributes) 🔵
6. [Six techniques worth adopting deliberately](#6-six-techniques-worth-adopting-deliberately) 🟢
7. [Writing good research questions: what separates a good prompt from a bad one](#7-writing-good-research-questions-what-separates-a-good-prompt-from-a-bad-one) 🟢
8. [Recognizing flawed AI answers and feeding that back into better prompts](#8-recognizing-flawed-ai-answers-and-feeding-that-back-into-better-prompts) 🟢
9. [Using more than one AI to cover each other's blind spots](#9-using-more-than-one-ai-to-cover-each-others-blind-spots) 🟢
10. [Cost awareness: using AI economically](#10-cost-awareness-using-ai-economically) 🟢
11. [Legal and institutional considerations](#11-legal-and-institutional-considerations) 🔴
12. [Configuration Management setup: repositories and folders](#12-configuration-management-setup-repositories-and-folders) 🔴
13. [Collaborative work: co-authorship and supervision feedback](#13-collaborative-work-co-authorship-and-supervision-feedback) 🔴
14. [The request → document → commit → fact-check workflow](#14-the-request--document--commit--fact-check-workflow) 🔴
15. [Commit message template](#15-commit-message-template) 🔴
16. [File and folder naming conventions](#16-file-and-folder-naming-conventions) 🔴
17. [Using the template](#17-using-the-template) 🔴
18. [Introducing department- or program-specific rules](#18-introducing-department--or-program-specific-rules) 🔴
19. [Worked example](#19-worked-example) 🔵
20. [Quick checklist](#20-quick-checklist) 🔴

---

## 1. Why this process exists

*🔵 Context*

AI assistants (ChatGPT, Claude, and similar large language models) are now good
enough to genuinely speed up research and writing. They are also good enough to
be *convincing while wrong*. Theological scholarship lives or dies by the
verifiability of its claims — a date, a manuscript reading, a translation
choice, a citation of a Church Father. We cannot outsource that verification to
the tool that produced the claim.

The process in this manual exists to get the speed benefit of AI without
losing:

- **Traceability** — anyone (a supervisor, a peer reviewer, your future self)
  can see exactly what was asked, what the AI answered, and what you did with
  it.
- **Accountability** — every AI-influenced change to a paper is a distinct,
  attributable git commit, not silently blended into your prose.
- **Verification discipline** — nothing from an AI answer enters your paper as
  a factual claim until it has been checked against a primary or reputable
  secondary source. If you cannot check it immediately, it is logged as a
  TODO, not forgotten.
- **A real, recoverable history of your own thinking** — not just the AI's.
  If you have ever maintained a single running "open questions" or "plan"
  file and periodically rewritten it to drop resolved items and fold in new
  findings, you have already discovered the actual problem this manual
  solves: the moment you overwrite that file, the previous state — what you
  used to think, what changed your mind, when — is gone unless you kept it
  somewhere. A plain folder of Markdown files has no memory of its own past.
  Git gives the file that memory for free: you can overwrite `plan.md`
  freely, keep it clean and current, and still recover *exactly* what it said
  before, because the previous version lives in the commit before yours,
  forever, without cluttering the file you actually read day to day.
- **Your job, not put at risk by any of this.** Everything AI is actually
  good at (Section 4) is mechanical, error-prone-for-humans busywork;
  everything that makes the work worth doing — the hypothesis, the
  interpretive judgment, the verification, the pastoral framing (Section 5)
  — stays irreducibly yours. The point of this process is to spend less
  time on the parts nobody enjoys, not to make the scholar optional.
- **Privacy and confidentiality, taken seriously, not as an afterthought.**
  Real personal data has a firm rule keeping it out of AI prompts entirely
  (Section 11.2); the record this process creates of *your own* thinking is
  protected by the same care (Section 11.6) and by concrete, IT-enforced
  access controls (`access-control-for-it.md`) — private by default, access
  granted deliberately, never standing or continuous.

This is Configuration Management applied to research: the same discipline
software engineers use to keep large codebases correct and auditable, applied
instead to arguments, citations, and drafts.

### This is meant to run in the background, not slow you down

None of this should feel like paperwork. The archiving, the commit messages,
the TODO bookkeeping — all of it is mechanical, which means it belongs to the
AI assistant, not to you (Section 17's `CLAUDE.md` does exactly this: it
writes the files and drafts the commit automatically). Your actual overhead
per question should be a few seconds: glance at what it filed, answer one
short prompt about what you've checked, say yes or no to applying it. If the
process ever feels like it's slowing down the actual thinking, that's a sign
the automation isn't doing its job, not a sign you should skip the record.

It also does not apply uniformly to every single exchange. Scale it to the
stakes:

- **Pure exploration or a clarifying question** ("what do scholars usually
  say about X," "does this argument make sense," a back-and-forth that never
  touches `paper.md` or `sources.md`) needs no folder and no commit at all —
  it produced nothing that needs to be traced yet. If it later turns into
  something you want to use, log it *then*.
- **Anything whose answer actually changes the paper, the sources, or a
  claim you intend to rely on** gets the full treatment: archived, fact-check
  status noted, committed (Section 14). This is the boundary that matters —
  not "did I talk to the AI," but "did something the AI said just become
  part of what I'm claiming."

## 2. How AI language models actually work

*🔵 Context*

You do not need to be able to implement one, but you do need a working mental
model, because that model explains *why* hallucination happens and *why*
verification is non-negotiable.

- A large language model (LLM) is a statistical model trained on enormous
  amounts of text. During training it repeatedly does one task: given the text
  so far, predict the next word (technically, the next *token*, a word-piece).
  It adjusts billions of internal parameters (numeric weights) to get better
  and better at this prediction, across trillions of examples.
- After training, "using" the model means running that same next-token
  prediction over and over, feeding each predicted word back in, to generate a
  whole answer. There is no lookup step where it "checks a fact" against a
  database — everything it produces is generated from learned statistical
  patterns of how language and ideas co-occur.
- It also has no persistent memory of a specific book, verse, or article
  unless something very similar to that content appeared often enough, and
  clearly enough, in its training data for the pattern to be captured in its
  weights. Rare sources (an obscure Syriac commentary, a niche monograph, a
  named modern commentator's precise page-level argument) are systematically
  under-represented or absent — which is exactly why, as in the worked example
  in Section 19, checking a specific claim often means going to a named
  commentary or database yourself, not asking the AI to check itself.
- A further round of training ("fine-tuning" / reinforcement learning from
  human feedback) shapes the model to produce answers that *sound* helpful,
  confident, and well-structured. This optimizes for the *appearance* of a
  good answer, which is not the same thing as optimizing for truth.

The upshot: an LLM produces the text that is *statistically plausible as a
continuation*, not a text that has been checked against reality. Most of the
time these coincide, because plausible theological or historical language
usually is accurate — the model has seen a great deal of correct information.
But "usually" is exactly the gap that scholarship cannot tolerate.

## 3. What hallucination is, and why you must check everything

*🔵 Context*

**Hallucination** is the term for when a model generates a statement that is
false, fabricated, or unsupported, but presents it with the same fluent
confidence as a true statement. It is not a bug that occasionally misfires and
is otherwise absent — it is the direct, expected consequence of how the model
works (Section 2): it always generates the *most plausible-sounding*
continuation, whether or not a true continuation was in its training data.

Typical shapes hallucination takes in theological/historical research:

- **Fabricated citations** — a plausible-looking book title, author, page
  number, or journal article that does not exist, or that exists but does not
  say what is claimed. (See Section 19 for a worked case of exactly this.)
- **Misattributed quotations** — a real quotation attached to the wrong
  author, council, or century.
- **Invented specificity** — confidently giving a precise date, manuscript
  number, or statistic where the real scholarly answer is contested or
  unknown, because a specific-sounding answer is more "plausible" as text than
  a hedged one.
- **Conflation** — merging two similar things (two councils, two people with
  the same name, two textual variants) into one incorrect composite.
- **Confident wrongness on minority positions** — flattening genuine scholarly
  disagreement into a single answer, usually the majority or best-documented
  view, silently.
- **Quiet compression of nuance** — asked to summarize a set of source files,
  an AI will often merge, shorten, or soften caveats and exceptions unless
  explicitly told not to. This is not "wrong" in the fabrication sense, but it
  is a real, common failure mode: an argument that was hedged in the source
  comes out flat and confident in the summary. If a task depends on every
  distinct statement surviving intact, say so explicitly in the instruction
  ("do not compress or comprehend statements; use them in full length, list
  contradicting arguments too") rather than assuming a summary preserves them.

None of these come with a warning label. The text reads exactly as fluently
and confidently whether it is correct or invented. **This is why every
factual claim taken from an AI answer must be checked against a primary
source or a reputable, citable secondary source before it is used in a
paper.** Section 14 makes this a mandatory, logged step in the workflow, and
Section 14 also tells you what to do when you cannot check something
immediately: you log it, you do not let it slide.

## 4. What AI is genuinely good for

*🔵 Context*

None of the above means AI is not useful — it means its usefulness lies in a
specific place: **tedious, mechanical, error-prone-for-humans work that is
cheap to check**, not in being an oracle of settled fact. Concretely, AI is
strong at:

- **Applying a fixed method across a lot of text** — e.g. "list every use of
  the Greek word *ekklesia* in this chapter and classify it as
  local-congregation vs. universal-church sense." A human doing this for 40
  pages will get tired and miss instances around page 25. The AI does not get
  tired. It will still make some errors — but a different, more *checkable*
  kind: you are verifying a classification against text right in front of
  you, not verifying an unsupported claim.
- **Finding candidate resources** — suggesting commentaries, articles, or
  primary sources that might be relevant, as a starting list to independently
  verify exist and are on-topic — not as a finished bibliography.
- **Summarizing a topic or a long text** as a first-pass orientation, to be
  checked against the source, not as a citable substitute for the source.
- **Formulating and drafting** — turning rough notes or bullet points into
  readable prose, restructuring a clunky paragraph, suggesting a clearer
  argument order. Style suggestions carry none of the factual risk that claims
  do, though they still deserve a read for theological nuance the AI may have
  flattened.
- **Consistency checks** — "does chapter 3 use this term the same way chapter
  1 defined it?", "did I number these footnotes correctly?", "does this
  argument contradict something I said on page 4?" This is exactly the kind
  of mechanical cross-referencing where humans have blind spots simply from
  having read their own draft too many times.

The unifying theme, worth stating as plainly as possible: **AI takes over
tedious work, not jobs.** It reduces the number of errors and closes blind
spots that come from human tedium and fatigue. It never fully eliminates
errors, and it can introduce new ones of its own (hallucination) that a human
would not have made. It is a very good assistant and a bad final authority.
Every output is a draft to be checked, never a citation to be trusted — which
is exactly why the scholar doing the checking, the interpreting, and the
deciding remains essential (Section 5), not a role this process is trying to
shrink.

## 5. Division of labor: what you contribute, what AI contributes

*🔵 Context*

It helps to say plainly what each side of this collaboration is actually for,
both so credit is attributed honestly and so you spend your own limited time
where it matters.

### What only you can contribute

- **The original theological question or hypothesis worth pursuing.** Noticing
  that a particular verse sits at a structurally significant point, wondering
  whether two seemingly unrelated episodes echo each other, proposing that a
  character's arc reflects a psychological or social dynamic — this is the
  genuinely creative, interpretive work. AI can extend, test, and help
  articulate a hypothesis once you have it; it rarely originates the
  theologically interesting one on its own initiative from nothing.
- **Judging whether a proposed parallel or pattern is actually sound**, not
  just interesting-looking. AI will readily produce a comparison; only your
  domain judgment can tell you whether it is a real authorial signal or a
  coincidence dressed up as one (see Section 8 for concrete cases).
- **The decision to accept, defer, or reject any specific proposal.** Nothing
  an AI drafts should be treated as part of the paper until a human has
  explicitly said so — a plain "yes," "not now, revisit later," or "no,
  ignore this" after each proposal is not excessive caution, it is the actual
  mechanism by which the paper stays yours. See Section 6.6 for making this a
  standing habit rather than something you only remember to do sometimes.
- **All primary-source verification and citation-checking** (Section 3) —
  this cannot be delegated back to the tool whose output is being checked.
- **Ethical and pastoral framing decisions** — deciding what terminology is
  appropriate, what a text should and should not be claimed to say, and how a
  sensitive topic should be presented to a given audience are judgment calls
  only a human is positioned to make and be accountable for.
- **Deciding when "good enough" isn't** — recognizing when an AI-produced
  structure, summary, or argument is superficially plausible but actually
  thin, and pushing back rather than accepting the first fluent answer.

### What AI reliably contributes

- Fast synthesis across many source files, chapters, or a large existing
  document.
- Drafting readable prose from rough notes, bullet points, or an outline.
- Mechanical consistency checks and cross-referencing across a long text.
- Producing several candidate options or comparisons quickly, when explicitly
  asked for options rather than a single converged answer (Section 8).
- Restructuring or reorganizing content on request, without the fatigue that
  makes a full human reorganization of a long document unappealing to
  attempt.
- A first-pass structured breakdown of a broad task — e.g. splitting a long
  paper into per-chapter or per-audience files (Section 6.3) — ready for you
  to review piece by piece.

### Why the split matters in practice

Naming this split keeps the paper's actual intellectual contribution
correctly attributed: the thesis, the interpretive judgment, and the
verification are yours; the synthesis and drafting labor is borrowed. It also
tells you where to spend your own limited time — not drafting prose the AI
can draft just as well, but forming the hypothesis in the first place and
deciding, case by case, whether the AI's proposal actually holds up. None of
this labor-saving is labor-*replacing*: the list above is deliberately all
mechanical/synthetic work, and the "what only you can contribute" list is
deliberately everything that actually constitutes scholarship.

## 6. Six techniques worth adopting deliberately

*🟢 Best practice — except 6.6, which is 🔴 required*

These are not theoretical. They are patterns that already work in practice
for exactly this kind of research; naming them explicitly makes it easier to
reuse them on purpose rather than reinvent them ad hoc each time.

### 6.1 Turn the AI into an adversarial reader of your own draft

Rather than asking generally "is this any good?", ask for specific,
separately-filed categories of critique. For example, ask it to read a
draft and produce:

- `wrong_facts.md` — the claim, what is wrong, what would be correct.
- `weak_arg.md` — the argument, what makes it weak, how to strengthen it.
- `contradict.md` — pairs of statements in the draft that contradict each
  other.
- `wrong_citations.md` — the reference used, and what the correct reference
  should be.
- `critic.md` — anything else, uncategorized.

Splitting critique into separate, single-purpose files (rather than one
freeform "review") makes each category independently actionable, easy to
turn into `TODO.md` items, and easy to re-run later to check whether a
category is now empty. It also tends to surface more issues than a single
"review this" prompt, because the AI is forced to actually fill each bucket
rather than produce one general paragraph of praise-plus-caveats.

The template packages exactly this as a one-word convenience: run
`/update_paper` (`.claude/commands/update_paper.md`) to get open `TODO.md`
items, `wrong_facts.md`, `contradict.md`, weak-argument flags, and a
citation-placement check in one pass, without retyping this section's
instructions by hand each time. It never edits `paper.md` itself — only
reports findings — so it stays a checking tool, not a drafting one.

### 6.2 Keep reusable "instruction files" for recurring tasks, separate from one-off questions

Section 14's `ai-requests/NNNN-.../question.md` is for a specific question
asked once. But some tasks recur across a project in the same shape — "find
every gap in this argument," "check every fact against the sources," "expand
every claim in this chapter with full supporting citations." For those, keep
a standing instruction file (e.g. `instructions/instruction_find_gaps.md`)
that states the task, the rules, and the exact output file(s) expected, and
reuse and refine that file every time you run the task, instead of retyping
a similar prompt slightly differently each time. Two things matter for this
to stay traceable:

- The instruction file itself is a versioned file in the repository, so
  improving *how* you ask a recurring question is visible in the git history
  like anything else.
  Each *run* of it is still logged as its own `ai-requests/NNNN-.../` entry
  per Section 14, noting which instruction file (and which commit of it) was
  used, so a later reader can tell "gap-finding was run with v3 of the
  instruction, which by then excluded literature checks" rather than
  assuming every gap-finding run used the same method.
- Specify the exact output format and files in the instruction itself (e.g.
  "use `# header (topic)` / `## fact 1` / `## evidence` ...", "write results
  to `wrong_facts.md`"). A precise, fixed format is what makes runs from
  different dates actually comparable, and prevents the AI from silently
  restructuring the output in a way that hides whether something was missed.

### 6.3 Expand a paper into one file per claim, when depth-review matters

For a finished draft that needs to hold up point by point (a thesis chapter
close to submission, a paper making contested claims), it is worth going
further than a single review pass: create one file per
chapter/subchapter/individual statement and have the AI argue *that specific
statement* in full, with exhaustive supporting references, in its own file.
This turns "is this paper well-argued?" into a checklist of individually
reviewable, individually fact-checkable units, each small enough to actually
verify claim-by-claim rather than skimmed as one long document.

### 6.4 State a falsifiable prediction before you check, not after

When a claim genuinely cannot be checked immediately (the source needs
library or database access, say), it is tempting to defer judgment entirely.
A stronger habit: write down, in `TODO.md` or the relevant note, what you
*expect* the check to show and why, before you actually look. For example:
"expect this patristic commentary's divisions to partially, not strongly,
overlap our proposed structure, because its divisions are keyed to a
numerological pattern rather than to content boundaries." Then when the
check is finally done, the result is compared against a prediction already
on record — it cannot be quietly reframed as confirming whatever you already
believed, which is a real risk once a claim has sat unresolved for a while
and started to feel true by familiarity.

### 6.5 Rate how well-attested each claim is, not just whether it was checked

A single CHECKED / NOT-CHECKED flag (Section 14's minimum bar) is necessary
but coarse. For claims that matter to a paper's central argument, consider a
three-tier confidence rating instead:

- **Strongly attested** — confirmed by two or more independent
  sources/methods.
- **Moderately attested** — confirmed by one source/method beyond your own
  reasoning.
- **Proposed, plausible** — your own argument or inference; not independently
  attested, and the paper should say so plainly rather than imply otherwise.

Adding this as an explicit column or tag (in a summary table, in
`sources.md`, or inline) converts an open-ended "how sure are we, really"
question into a stated, checkable claim — which is both more honest and more
useful to a reader deciding how much weight to put on a given point than a
confident tone that does not distinguish its best-supported claims from its
most speculative ones.

### 6.6 Propose, then confirm, before anything touches the paper

Default to a two-step pattern for anything beyond a small, obviously-correct
edit: ask the AI to draft or propose the change into a scratch file (or just
into the conversation) first, review it, and only then explicitly tell it to
apply the change to `paper.md`/`sources.md`/wherever it belongs. A plain
"yes, please add," "not now, revisit later," or "no, ignore this" after each
proposal costs a few seconds and is what actually keeps the paper's content
under your control rather than the AI's default judgment. This matters most
exactly when you are tempted to skip it — on a proposal that sounds
plausible and you're in a hurry, which is precisely when an unsound parallel
or an overclaim is most likely to slip through unexamined (Section 8).

The proposal and the apply are **two separate commits**, not one (Section
14). The proposal can be archived and committed the moment it exists — it's
just a record of what was asked and answered, nothing about the paper
changed yet, so there's nothing to decide before committing it. The apply
commit happens later, only once you've said yes, and is the one that
actually touches `paper.md`/`sources.md`/`TODO.md`. Keeping them apart means
a rejected or "not now" proposal still leaves a clean record of having been
considered, without ever mixing an undecided idea into the same commit as
the paper's actual content.

## 7. Writing good research questions: what separates a good prompt from a bad one

*🟢 Best practice*

Looking back over a large number of real AI requests written for actual
research and writing work, the quality of the *request itself* — independent
of how good the underlying idea was — reliably predicted whether the result
added real value or had to be redone. None of the pairs below are quotes;
they are constructed to illustrate each pattern.

**Bounded scope and an explicit source list.**
Good: *"Read only `smith-commentary-ch3.md` and `jones-article-2019.md`.
Ignore every other file in this folder. List every place these two sources
disagree about the date of composition, quoting the specific sentence from
each."* Bad: *"Look into everything we have on this topic and tell me what's
true about when it was written."* — "everything we have" is not a set the AI
can actually enumerate or a reader can later re-derive, and "what's true"
invites it to flatten genuine disagreement into one confident answer.

**Output format specified in advance.**
Good: *"For each argument found, output `## <claim>`, then `### Evidence
for`, then `### Evidence against`; one file per chapter, named
`ch<N>-evidence.md`."* Bad: *"Give me a thorough write-up of the arguments
for and against."* — with no fixed shape, a rerun next month may organize
the same material completely differently, so you can't tell whether a later
run found something new or just reorganized old content.

**Naming what the AI cannot reliably do, and routing it to a human instead.**
Good: *"Summarize the argument structure of these two files. Do not attempt
to verify any citation yourself — just list every citation you find so I can
check them by hand."* Bad: *"Make sure every citation is accurate and up to
date."* — an LLM cannot "make sure" of this; it can only generate text that
*looks* like a checked citation, so an instruction phrased this way manufactures
false confidence rather than accuracy.

**Invented material labeled as invented.**
Good: *"Where the sources don't specify a detail you need for the narrative,
invent a plausible one, but list every invented detail separately in
`assumptions.md`."* Bad: leaving this unsaid, so invented detail is allowed
implicitly with no requirement to flag it — an invented date, name, or
number that is never flagged is indistinguishable from a hallucinated one
once it is sitting in the draft, because the very thing that would let you
tell them apart was never created.

**One self-contained request per reviewable unit.**
Good: *"Take chapter 4 alone. Argue its central claim in full, with every
supporting reference, in `ch4-argument.md."* (repeated per chapter). Bad:
*"Write out the complete, exhaustive argument for the whole book, with full
supporting detail for every chapter, in one file."* — "exhaustive" applied to
a large scope in a single pass all but guarantees thin sections get padded
with plausible-sounding but unverified specifics to match the requested
exhaustiveness, and the result ends up too large for anyone to actually
check end to end. (This is Section 6.3's technique stated as a rule: prefer
several small, checkable requests over one large one whenever the material
allows it.)

**Firm terminology and framing rules, stated once, up front.**
Good: *"Throughout, refer to this pattern as 'coercive control,' never
'quarreling' or 'conflict' — this is a fixed choice, not a style preference
to vary."* Bad: leaving terminology unstated and only correcting it
after the fact, document by document — each new AI run reintroduces the same
drift from scratch, since the AI has no memory of a correction made last
time unless it is written into the instruction itself.

**A required self-critique section, built into the task, not bolted on after.**
Good: *"After writing the paper, add a final section listing every claim in
it that rests only on this paper's own reasoning, not on an outside source,
and label it as such."* Bad: asking for this only occasionally, as an
afterthought, on documents that "seem important" — the documents most likely
to contain unlabeled speculative claims are exactly the ones nobody thought
to flag as important enough to double-check.

The common thread: a good request is bounded, specifies its own output shape,
is explicit about what must be labeled (assumptions, uncertain claims,
terminology), and is sized so a human can actually verify the whole answer.
A bad request substitutes an adjective ("thorough," "exhaustive," "make
sure") for an actual constraint, which reads as more rigorous but produces a
result that is *harder*, not easier, to verify.

## 8. Recognizing flawed AI answers and feeding that back into better prompts

*🟢 Best practice*

Section 7 is about how to phrase a request well the first time. This section
is about what to do when, despite that, the answer still isn't right — which
will keep happening, because it follows directly from Section 2: the model is
always producing its most plausible-sounding continuation, and "plausible" and
"correct" are not the same thing. The skill worth building is a habit of
**recognize → correct now → encode permanently**, so the same flaw doesn't
have to be caught fresh every time it recurs.

### Recurring categories of flaw, and what to do about each

- **Scope creep** — the answer draws on or refers to material you did not
  intend as input for this task, and you can't immediately tell where it came
  from. *Correct now:* ask directly which specific input licensed the claim,
  and have it retract anything that didn't come from an intended source.
  *Encode permanently:* tighten the source list in the relevant instruction
  file (Section 6.2) or in this specific request (Section 7) so the same
  boundary is explicit next time, not just corrected this once.
- **A parallel or pattern claimed too eagerly** — the AI draws a comparison
  between two things that only partly holds, treating them as equivalent when
  a specific element actually differs. *Correct now:* name the exact element
  that breaks the parallel, and ask for a redo without yet applying it
  anywhere (Section 6.6). *Encode permanently:* make it a standing
  instruction, wherever comparisons are being drawn, to state both the
  similarities *and* the specific respects in which the comparison does not
  hold — every time, not just after you catch one that didn't.
- **A genuinely ambiguous question collapses into one falsely-confident
  answer** — where the sources or reasoned inference actually support two or
  more live readings, the model converges on a single one anyway, because a
  confident single answer is a more "plausible" continuation than a hedge
  (Section 2). *Correct now:* explicitly ask for the alternative readings and
  what each would imply, rather than accepting the first synthesis. *Encode
  permanently:* add "if more than one reading is defensible, present them as
  separate options rather than choosing one" to the recurring instruction
  where this has happened before.
- **A deliberately careful, hedged claim drafts as more sweeping than
  intended** — an argument meant as "this challenges the standard view"
  comes out reading like "this proves X" once it becomes prose. *Correct
  now:* fix the specific overclaim. *Encode permanently:* state up front,
  before drafting, a short list of what the argument is explicitly *not*
  claiming — the same technique Section 7 recommends for terminology,
  applied to argument strength instead of vocabulary.

### Turning a one-off correction into a lasting fix

Each time you catch one of these, ask: *would this same mistake recur on the
next similar request?* If yes, the fix belongs in a reusable instruction file
(Section 6.2) or a standing framing rule (Section 7), not only in this one
conversation's memory. A short running note — even a simple
`prompting_notes.md` listing "lessons learned" per recurring task type —
keeps a hard-won correction from having to be rediscovered from scratch by
whoever (including your own future self) next runs a similar request on this
or another topic.

## 9. Using more than one AI to cover each other's blind spots

*🟢 Best practice*

Different AI systems (for example Claude, ChatGPT/GPT, or Gemini) are trained
on different data mixes and tuned by different teams, so their errors are not
perfectly correlated. A fabricated citation or a flattened nuance produced by
one model is often *not* reproduced by another, simply because it isn't the
same statistical artifact recurring. This makes a second, independent system a
cheap additional filter — not a replacement for the fact-checking discipline
in Section 3, but a useful check before you spend real verification time.

- **Independent second opinion on a specific claim or citation.** Ask a
  second AI system the same precise factual question, independently, without
  showing it the first system's answer (showing it the first answer risks it
  simply agreeing with a flawed premise rather than checking it fresh).
  Agreement across two independently-trained systems is still not proof —
  both can share the same gap if neither was trained on an obscure primary
  source — but disagreement is a strong, cheap signal that something needs a
  real, by-hand check.
- **Adversarial review across systems, not within one.** Have one system
  draft an argument, then ask a *different* system to critique it (using the
  structured-critique files from Section 6.1), rather than asking the same
  system that wrote it to critique itself — a model tends to be more lenient
  toward a continuation that reads like its own style, so critique from a
  genuinely different model doesn't share that particular blind spot.
- **Different systems for different jobs.** A model with strong long-context
  handling may suit cross-referencing one very long document consistently; a
  faster, lighter model may be entirely sufficient for high-volume mechanical
  extraction where each individual answer is small and cheap to check; the
  strongest available "reasoning"-oriented model is worth reserving for the
  hardest interpretive synthesis (see Section 10 on matching model cost to
  task difficulty).
- **Record which system answered what.** Extend `question.md`/`answer.md`
  (Section 14) with the model name and version used. This makes it possible
  to later ask "does a newer or different model still make this same error?"
  and stops a correction found while using one system from quietly getting
  lost when you switch to another for a later request on the same topic.

## 10. Cost awareness: using AI economically

*🟢 Best practice*

Even with a flat-fee subscription, AI usage is not free in an unlimited
sense, and it is worth understanding what you are actually spending before a
deadline forces you to find out the hard way.

- **A subscription is usually still a quota, not unlimited access.** Many AI
  subscription plans meter your usage internally against a weekly or
  session-based allowance even though you are not billed per question. A
  long run of large, context-heavy requests can exhaust that allowance and
  temporarily drop you to a slower tier or lock you out — worth knowing your
  own plan's actual limits (check its documentation directly) before you are
  relying on it under time pressure, not while you are.
- **If you are billed by usage (API/token pricing) instead of a flat
  subscription, cost scales with both directions:** what you send (all the
  source material and context included in the request) and what comes back
  (a long generated chapter costs far more than a short, targeted answer).
  An "exhaustive," maximal-context request — already flagged in Section 7 as
  a *bad* prompting pattern for verifiability — is also simply the most
  expensive way to ask.
- **A usage indicator in your editor or subscription dashboard measures a
  specific thing** — check what, rather than assuming a displayed "cost" or
  "usage today" number means an extra charge on top of a flat subscription.
  The two can coexist (a subscription with an internal, non-billed usage
  meter shown for your own awareness) — confusing them either causes
  needless worry or, in the opposite direction, a genuine surprise bill if
  your plan actually is metered. When in doubt, check your specific plan's
  documentation rather than guessing from the number alone.

**Practical habits:**

- Don't include more source material in a request than the task actually
  needs — a bounded source list (Section 7) is both cheaper and more
  checkable.
- Reserve your most capable model tier for genuinely hard interpretive or
  synthesis work; use a faster/cheaper tier for high-volume mechanical tasks
  (extracting a list, reformatting, converting a file) where a lighter model
  performs just as well.
- Split a large task into several small, targeted requests (Section 6.3), not
  only because the result is more checkable, but because a wrong or wasted
  large request costs far more than a wrong small one.
- If several people share a plan or a budget, keep a rough sense of which
  topics or weeks consume the most usage — it surfaces a badly-scoped or
  runaway request pattern (Section 7's "bad prompt" patterns are often also
  the expensive ones) before it becomes a recurring cost problem rather than
  a one-time surprise.

## 11. Legal and institutional considerations

*🔴 Required*

None of this manual overrides law, university policy, or an AI provider's
own terms — it's a research-hygiene process, not a legal opinion. Each
subsection below is grounded in a real, current (2025-2026) development,
cited at the end, but still needs to be checked against the actual relevant
authority (your program's regulations, your data protection officer, a
lawyer if it's genuinely material) — treat citations as a starting point for
verification (Section 3's discipline applies to this section too), not as
this manual having done that verification for you.

### 11.1 Publisher and institutional AI-disclosure requirements

Major academic publishers — Elsevier, Springer Nature, Wiley, Taylor &
Francis, SAGE — now require disclosure of generative AI use in manuscripts
and explicitly prohibit listing AI as an author, since authorship requires
an accountability (consenting to ethical review, approving the final
version, being answerable for errors) that an AI cannot bear. Elsevier
specifically requires a "Declaration of Generative AI and AI-assisted
technologies in the writing process" placed immediately above the
references, disclosed in *both* the submission form and the manuscript
text. University policy is moving the same direction: the 2025-2026 trend
is away from blanket bans and toward "AI may be used only with disclosure
and within instructor-defined limits," distinguishing *assistive* use
(grammar/proofreading, often undisclosed) from *substantive* use (generating
or interpreting content, analysis, or argument, which must be disclosed).
Caltech's policy, for instance, requires confirming AI is permitted for a
given piece of work *before* using it, and treats undisclosed AI text in a
thesis as an integrity violation, not a style issue.

**Check your specific program's and target journal's current policy before
applying this workflow to anything graded or submitted** — this manual
cannot override either, and both are still changing year to year.

*Automatable:* generating a disclosure statement from the repo's own
`ai-requests/` audit trail (`CLAUDE.md` step 13) is a strict superset of
what any of the formats above need, since it has the complete record — a
human then trims it to whatever specific format the target journal or
program currently requires.
*Not automatable:* which specific disclosure format a given journal or
program requires, or whether AI is even permitted for a given assessment —
check the current policy directly.

### 11.2 GDPR and personal data in AI prompts

EU regulators moved fast on this in 2025: the European Data Protection
Board adopted an opinion addressing when an AI model can be considered
anonymous (assessed case-by-case — a model must be very unlikely to let
someone extract personal data used to train it, directly or indirectly, via
queries) and issued guidelines on anonymisation and web-scraping for
generative AI; the European Data Protection Supervisor separately issued
revised generative-AI guidance in October 2025. None of this changes the
department's basic rule: real pastoral, counseling, or case material
involving identifiable living people is personal data, and in the EU falls
under GDPR the moment it's typed into any AI prompt. Treat pseudonymization
as a firm rule, not a per-instance judgment call — strip names, locations,
and dates specific enough to narrow down who someone is, *before* the
material reaches a prompt, the same way you would before sharing it in any
other non-confidential channel.

*Automatable:* `CLAUDE.md` step 11's pattern check — flagging text that
looks like it names a real, identifiable person before it's archived — as a
best-effort nudge to double-check, not a determination.
*Not automatable:* whether a specific anonymization is actually adequate
under current regulatory guidance (the EDPB's own guidelines note this is
assessed case-by-case) — ask your institution's data protection contact.

### 11.3 Copyright status of AI-assisted work

The US Copyright Office's Part 2 report (published January 29, 2025)
concluded: purely AI-generated output, without meaningful human authorship,
is not copyrightable in the US; a prompt alone does not give enough human
control to establish authorship; but a human's creative selection,
arrangement, or modification of AI output *can* itself be copyrightable,
assessed case by case. (A separate Part 3, from May 2025, addresses AI
*training* on copyrighted material — not directly relevant to who owns the
output.) The position specifically on output ownership still differs by
jurisdiction and continues to develop elsewhere.

**What this means in practice:** a paper that is mostly AI-drafted prose
with light human editing sits on genuinely shaky ground for exclusive US
copyright; the department's own interpretive argument — the human
contribution Section 5 describes as irreplaceable — is both the part most
clearly protectable and, usefully, the part the audit trail can help
demonstrate was substantively human-authored if that's ever actually
disputed.

*Automatable:* none of the legal determination itself — but the
`ai-requests/` log is exactly the kind of evidence (what was AI-drafted,
what was a human addition or edit) such a determination would need to
examine.
*Not automatable:* the legal conclusion — a case-by-case call under
guidance that is still evolving.

### 11.4 AI provider terms: training data and retention

Concretely, for Anthropic's Claude, as of mid-2026: **consumer accounts**
(Free, Pro, Team, under the Consumer Terms) default, since an August 2025
change, to allowing conversations to be used for model training, with data
retention extended to five years for accounts that leave this enabled (30
days if you opt out). Opt out under Account Settings → Privacy → "Help
improve Claude." **Commercial-tier accounts** — Claude for Work, Claude
Enterprise, Claude for Education, Claude for Government, and API/Bedrock
access — are covered by separate Commercial Terms that prohibit training on
your inputs by default, with no toggle needed. One caveat worth knowing
either way: even opted-out content can still be used if it's flagged for a
safety review.

**Recommendation for this department:** use Claude for Education or a
similar commercial-tier account for anything touching unpublished research
or any of the personal-data categories in 11.2, rather than a personal
consumer account; if only a consumer account is available, turn the
training toggle off before starting real work, and note this isn't
retroactive for anything typed before the toggle was changed.

*Automatable:* none directly — this is an account-level setting outside
what a coding assistant can see or change. `CLAUDE.md` can only remind, once,
at repository setup.
*Not automatable:* actually setting the toggle, or choosing the right
account tier — a one-time human action.

### 11.5 Defamation and false-statement risk about real people

Real, live cases test this directly. In *Walters v. OpenAI* (Georgia state
court, May 2025), OpenAI won summary judgment on a claim that ChatGPT had
falsely told a user a radio host embezzled funds — the court reasoned that a
reasonable user already knows chatbots can fabricate, so the output wasn't
understood as a factual assertion. In the ongoing *Starbuck v. Google*
(Delaware, filed October 2025) and the settled *Starbuck v. Meta* (August
2025), plaintiffs allege chatbots fabricated serious accusations —
assault, extremism — attributed to fictitious sources. So far, courts are
mostly protecting the AI companies under traditional defamation frameworks,
largely on the strength of disclaimers and the difficulty of proving harm.

**The catch for this department specifically: that protection belongs to
the AI provider, not to whoever republishes the claim.** If a hallucinated
statement about a real, identifiable person — a named scholar, pastor, or
institution — makes it from `ai-requests/.../answer.md` into a published
paper or sermon under a human author's name, the "the chatbot said it, not
me, and everyone knows chatbots can be wrong" defense that has worked for
OpenAI and Google in court does not obviously extend to a human author who
repeated it as settled fact in their own published work. This is exactly
why Section 3's fact-checking discipline exists, applied here for a reason
with real legal teeth and not only scholarly accuracy.

*Automatable:* `CLAUDE.md` step 12's identifiability flag — a pattern check
for unusually specific references to real people or institutions before
they're drafted into illustrative or composite material.
*Not automatable:* whether a specific statement about a specific real,
named person is actually true — Section 3, no shortcut.

### 11.6 The psychological dimension: a full, permanent record of your own thinking

This workflow doesn't just archive facts — it archives every question you
asked, every proposal you rejected, every hypothesis that turned out to be
wrong, forever, in a log anyone with access can read start to finish. That
is a different kind of exposure than a normal draft, and it is reasonable to
feel uneasy about it, not a sign of having something to hide. Research on
monitored work environments backs this up directly: excessive visibility
into someone's in-progress thinking produces a measurable *chilling
effect* — people self-censor, avoid asking questions that might look naive,
and stop admitting knowledge gaps once they know the record is being read by
someone with power over them (one survey found roughly 60% of students
uncomfortable expressing honest opinions under digital surveillance;
monitored employees report substantially higher intent to leave than
unmonitored ones). GDPR's own employee-monitoring principles point the same
way: monitoring must be proportionate to a real need, disclosed in advance,
and the monitored person retains rights to see and, where no longer needed,
have erased what's held on them — a real German enforcement action
(H&M, a €35 million fine) shows regulators take this seriously, not as a
theoretical concern. There is a genuine tension here worth naming directly:
this manual's Section 16 rule against ever editing an archived `answer.md`
is in some tension with a data subject's usual right to have something
erased — the resolution is that the *research content* (a wrong hypothesis,
a rejected proposal) is not personal data about a third party and stays on
record as the whole point of the audit trail; genuinely personal content
that leaked into an exchange by accident (Section 11.2) is the narrow
exception where removing it is appropriate, and should be treated as a rare
correction, not a routine cleanup.

**Concrete steps to actually settle this, not just acknowledge it:**

- **The repository is the researcher's own** (Section 12) — they decide who
  gets read access, and when, not the department by default. Access should
  be granted deliberately (an advisor added for a specific supervision
  meeting, an examiner added at submission), not standing and continuous.
  See the separate IT access-control note below, and Section 13 for how
  supervision feedback itself works within that constraint.
- **A stated, written norm that the log is for tracing claims, not judging
  the person.** Advisors and examiners should be told explicitly, in
  writing, to evaluate the final paper and the diligence of the fact-checks
  — not to penalize a student for a naive early question or a rejected
  hypothesis sitting in the history. This is the same "blameless" norm
  software teams use for incident post-mortems: the record exists so
  mistakes are visible and fixable, not so the person who made them is
  penalized for having made them.
- **Discrimination risk is real and specific, not hypothetical**: a raw
  question history can incidentally reveal things — a disability
  accommodation pattern, a non-native speaker's phrasing, a personal or
  faith struggle behind a research question — that have nothing to do with
  the quality of the work and everything to do with who's allowed to see
  the record and why. Scope access tightly (see below) and keep the written
  evaluation norm above in place specifically *because* of this risk, not
  just the general discomfort of being watched.
- **This is proportionate, not absolute, transparency.** Nothing in this
  manual requires broadcasting the log beyond the people who need it for
  supervision or examination — private-by-default (Section 12, and the IT
  note below) is the actual default, not an afterthought.

### 11.7 What can actually be enforced by scripting, versus AI judgment, versus only a human

Not everything above is the same kind of check. It's worth being precise
about which category each falls into, since treating a fuzzy judgment call
as if it were a hard guarantee is itself a kind of overclaiming this manual
argues against elsewhere (Section 7):

| Check | Category | Where |
|---|---|---|
| An `answer.md` was never edited after its proposal commit | **Scriptable, deterministic** — pure git history | `scripts/check-repo-invariants.sh` in the template |
| A proposal and its apply are always two separate commits | **Scriptable, deterministic** — pure git history | same script |
| The above two, checked automatically after every commit, with no one needing to remember to run it | **Harness-enforced, deterministic** — runs regardless of AI diligence | `.claude/settings.json` hook (Section 18) |
| A disclosure statement reflects the actual `ai-requests/` record | **Scriptable, mechanical assembly** — but the *choice* of what a target journal needs is not | `CLAUDE.md` step 13 |
| Text plausibly names a real, identifiable person | **AI pattern-matching, best-effort** — flags, never decides | `CLAUDE.md` steps 11-12 |
| An anonymization is legally adequate | **Human/legal judgment only** | data protection contact |
| A specific factual claim is true | **Human judgment, using real sources** | Section 3, TODO.md |
| Which disclosure format/policy currently applies | **Human judgment** — check the current source | Sections 11.1, 11.4 |

The template includes `scripts/check-repo-invariants.sh`, which implements
the two fully-deterministic checks in the table above and can be run by
hand or wired into a pre-push hook — see the script's own comments. It
deliberately does not attempt anything from the bottom three rows; a script
that claimed to check GDPR adequacy or factual truth would be exactly the
kind of false confidence Section 3 warns against, just implemented as code
instead of as a prompt.

**Sources:** [Publisher AI Policies and Disclosure Rules](https://www.enago.com/responsible-ai-movement/resources/publisher-ai-policies-disclosure-rules-authors) · [Generative AI policies for journals (Elsevier)](https://www.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals) · [Journal AI Policies 2026](https://manusights.com/blog/journal-ai-policies-2026) · [Generative AI Policies at the World's Top Universities: October 2025 Update](https://www.thesify.ai/blog/gen-ai-policies-update-2025) · [EDPS Guidance on Generative AI (Oct 2025)](https://www.edps.europa.eu/press-publications/press-news/press-releases/2025/edps-unveils-revised-guidance-generative-ai-strengthening-data-protection-rapidly-changing-digital-era_en) · [EDPB anonymisation/web-scraping guidelines](https://www.edpb.europa.eu/news/edpb-sheds-light-on-anonymisation-and-web-scraping-for-generative-ai-and-adopts-final-version_en) · [US Copyright Office, Copyright and Artificial Intelligence, Part 2: Copyrightability](https://www.copyright.gov/ai/Copyright-and-Artificial-Intelligence-Part-2-Copyrightability-Report.pdf) · [Anthropic: Updates to Consumer Terms and Privacy Policy](https://www.anthropic.com/news/updates-to-our-consumer-terms) · [Anthropic users face a new choice (TechCrunch)](https://techcrunch.com/2025/08/28/anthropic-users-face-a-new-choice-opt-out-or-share-your-data-for-ai-training/) · [When ChatGPT Lies: the first wave of AI defamation cases](https://www.beneschlaw.com/insight/when-chatgpt-lies-what-the-first-wave-of-ai-defamation-cases-means-for-plaintiffs/) · [Courts test new frontier of defamation law as AI enters the mix](https://thedailyrecord.com/2025/11/12/ai-defamation-lawsuits-libel-law/) · [Negative Effects of Employee Monitoring](https://apploye.com/blog/employee-monitoring-negative-effects/) · [The Psychological Cost of Workplace Surveillance](https://www.softwareseni.com/the-psychological-cost-of-workplace-surveillance-on-developer-teams-and-company-culture/)

## 12. Configuration Management setup: repositories and folders

*🔴 Required*

We use git, the same tool software engineers use to track and audit changes to
code, to track and audit research and writing. Two rules:

1. **Everyone gets their own git repository space.** Each member of the
   department (faculty and students) works from their own git identity
   (their own commits, their own name/email in `git config`) and keeps their
   own collection of repositories, e.g. under a personal folder such as
   `~/research/<your-name>/`.
2. **Each individual research topic gets its own repository.** Do not lump
   unrelated papers into one giant repository. A repository is the unit of
   history for one topic — one seminar paper, one thesis chapter, one article
   draft. This keeps `git log` for a topic meaningful (it only ever shows work
   on that topic) and keeps repositories a manageable, reviewable size.
   (Section 13 covers the exception: a paper genuinely co-authored by more
   than one person.)

   ```
   ~/research/<your-name>/
     revelation-dating/          <- one git repo, one topic
     pauline-authorship-eph/     <- another git repo, another topic
     ecclesiology-1clement/      <- another git repo, another topic
   ```

Each topic repository has this shape (see the ready-to-copy version in
[`templates/new-topic-repo/`](templates/new-topic-repo/)):

```
<topic-repo>/
  README.md            <- what the topic/research question is, current status
  CLAUDE.md            <- maintenance instructions for the AI assistant (Section 14)
  DEPARTMENT-RULES.md  <- optional: department/program-specific rules (Section 18)
  TODO.md              <- open fact-checks and open questions (Section 14)
  paper.md              <- the actual paper/notes being written
  sources.md           <- bibliography, growing as sources are verified
  ai-requests/
    0001-<short-slug>/
      question.md      <- exact prompt/question given to the AI
      answer.md         <- the AI's full answer, verbatim
    0002-<short-slug>/
      ...
  instructions/         <- optional: reusable task instructions (Section 6.2)
    instruction_<task>.md
  scripts/
    check-repo-invariants.sh  <- mechanical structure checks (Section 11.7)
  .claude/
    settings.json       <- harness-enforced checks, e.g. auto-running the
                            script above after every commit (Section 18)
    commands/
      update_paper.md   <- /update_paper: checks TODO.md, wrong facts,
                            contradictions, weak arguments (Section 6.1)
```

Access to this repository (who can read it, and when) is a separate,
deliberate decision — see
[`access-control-for-it.md`](access-control-for-it.md) for the department's
IT-facing guidance on keeping each person's repository private by default.

`ai-requests/` is the audit trail: every AI interaction that influenced the
paper is a numbered, dated folder containing the exact question and the
exact answer, so anyone can later see precisely what was asked and what the
model said, independent of how it was paraphrased into the paper.

## 13. Collaborative work: co-authorship and supervision feedback

*🔴 Required (when applicable)*

Section 12's one-person-per-repository default covers most of this
department's work, but two genuinely collaborative situations need their
own guidance: a paper written jointly by more than one person, and the very
common case of a supervisor reviewing a student's progress.

### 13.1 Co-authorship: more than one person writing the same repository

When a paper genuinely has multiple human authors (two professors
co-writing an article, a student and supervisor co-authoring), the
repository is jointly owned rather than following the one-person default —
but the rest of the process doesn't change:

- Each co-author uses their own git identity (their own name/email in git
  config, per Section 12) — never a shared generic account — so `git log`
  still shows who actually asked and applied what, the same accountability
  Section 1 asks for within a single-author repository.
- The propose-then-confirm gate (Section 6.6) still applies per person:
  whichever co-author's research direction an AI answer would affect is the
  one who has to say yes before it's applied, not whoever happens to be at
  the keyboard.
- Coordinate who is actively writing to avoid stepping on each other
  mid-session (a quick message beats a merge conflict); for anything beyond
  light coordination, use a normal git branch per co-author and merge
  regularly rather than working in the same file at the same moment.

### 13.2 Supervision: a professor reviewing a student's progress

This is the concrete case Section 11.6 and `access-control-for-it.md` were
written for. Putting the pieces together:

1. **Access is scoped and time-boxed**, granted with the notice-of-access
   statement, exactly as `access-control-for-it.md` describes — not
   standing, continuous read access to every repository a student will ever
   create.
2. **Review at defined checkpoints, not continuously.** Reviewing every
   commit as it happens recreates the exact chilling effect Section 11.6
   warns about — a student who knows every exploratory question is being
   watched live will stop asking naive-sounding ones, which is precisely the
   opposite of what supervision is for. Review at a normal cadence instead:
   the end of a chapter, a scheduled supervision meeting, a submission
   checkpoint.
3. **Feedback goes through the same discipline research claims do.** A
   supervisor's comment is itself a claim ("this argument is weak," "check
   this against Beale") that the student should be free to accept, push back
   on, or discuss — not a silent edit to the student's own files. Two
   practical options, in order of preference:
   - If the git host supports comments/issues for read-only collaborators
     (GitHub, GitLab, and most hosted platforms do), use that — the
     supervisor never needs write access to leave feedback.
   - Otherwise, keep a `FEEDBACK.md` in the repository (parallel to
     `TODO.md`): the supervisor's comments, given verbally or in writing,
     get recorded there by the student verbatim (same "don't silently edit
     the record" discipline as `answer.md`, Section 16), dated, and
     referencing the specific commit or section they're about. The student
     adds their own response next to each item as they address it —
     accepted, pushed back on with reasoning, or open for the next meeting.
4. **A committee (more than one reviewer) is just this procedure repeated
   once per reviewer** — each examiner gets their own scoped access grant
   and their own notice-of-access; there is no single shared "faculty"
   access role (`access-control-for-it.md`).

**Why this doesn't undermine Section 11.6's privacy concerns:** scoped,
checkpoint-based, disclosed access is exactly what settles that concern
rather than reopening it — the student knows in advance who can see what,
when, and for what stated purpose, and the "evaluate the work, not the
person" norm still applies to what a supervisor does with that access once
granted.

## 14. The request → document → commit → fact-check workflow

*🔴 Required*

This is the core discipline, and it is deliberately light per step — the
weight comes from doing it every time, not from any single step being
onerous. If your AI assistant supports project-level instructions (e.g.
Claude Code reading a `CLAUDE.md`), the template's `CLAUDE.md` (Section 17)
performs essentially all of this automatically; what follows is what it is
doing, and what's still genuinely yours to decide.

**Step A — the proposal (archived and committed immediately, no decision needed yet):**

1. **Ask.** Put your question to the AI assistant (or run a reusable
   instruction file per Section 6.2). Skip everything below for exchanges
   that never touch the paper — see Section 1.
2. **Save the exchange to disk.** `ai-requests/NNNN-short-slug/question.md`
   (the exact question) and `answer.md` (the AI's full answer, verbatim —
   not trimmed).
3. **Commit this on its own**, right away — e.g. "Archive AI answer:
   <slug>." Nothing about the paper changed, so there's nothing to weigh
   first; this is purely the record that the question was asked. Call this
   the **proposal commit** and note its hash.

**Step B — applying it, only once you've actually decided to use it:**

4. **Use the answer** to update `paper.md` / `sources.md` / wherever it
   belongs — but only after you've explicitly said yes (Section 6.6). "Not
   now" or "no" is a perfectly good outcome and needs no further action; the
   proposal commit already preserved the record.
5. **Default every extracted factual claim to NOT YET CHECKED in
   `TODO.md`**, referencing the proposal commit's hash. This is automatic and
   needs no input from you — per Section 6.5, add a confidence tier only for
   claims central to the paper's argument.
6. **You get asked exactly one light, optional question** — not a checklist:
   "anything to add — a source you already know, a caveat, related work?"
   Answer if you have something; if not, move on. This is where *your*
   fact-checking (Section 3) enters the record when you already have it —
   it's an invitation for outside contribution, not a gate you must clear.
7. **Commit the apply step separately from the proposal commit**, referencing
   its hash, using the template in Section 15.
8. **When you later close a TODO item** (at whatever point you actually get
   around to checking it), check it off in `TODO.md` in its own small commit,
   noting what was checked, against what, and with what result, referencing
   the original proposal commit.

The result is a `git log` for the topic that is simultaneously a research
diary, an AI-usage audit trail, and a running record of what has and has not
been independently verified — built almost entirely as a byproduct of asking
questions the way you already would, not as separate overhead.

### When your own hand-editing and an AI apply-step touch the same file

`paper.md` doesn't belong exclusively to Step B — you will often be
directly editing it yourself (in your own editor, by hand) in between, or
even during, AI-assisted work. That creates a real, specific way for the
two to interfere: an AI apply-step (Step B, item 4) typically works from
whatever it last read of `paper.md`, so if you've hand-edited a passage
since then and the AI applies a change to that same area without knowing
about your edit, one of two bad things happens — your hand-edit gets
silently overwritten, or the apply-commit produces a confusing merge of two
different edits to the same sentence.

- **Commit your own hand-edits before asking the AI to apply anything new**,
  the same "one cause per commit" discipline Section 6.6 already asks of
  proposal/apply — a plain, ordinary commit (no special template needed;
  it's not an AI-request cycle, see Section 1) that's just your own
  writing. This keeps `git log` accurate about who changed what, and gives
  the AI a current, correct file to work from on the next request.
- **If you're mid-edit and want the AI's help right now, say so explicitly**
  — "I'm currently rewriting the second paragraph of section 2, here's
  where it stands, take that into account" — rather than letting the AI
  work from a mental model of the file that's already out of date. This is
  the same "don't leave it implicit" principle Section 7 asks of any
  request, applied to the state of the file itself, not just the question.
- **After an AI apply-commit, re-read the affected section before you keep
  hand-editing it** — wording may have shifted under a passage you were
  about to continue, and catching that by reading beats catching it by
  fighting a confusing diff later.
- **If a collision already happened, nothing is actually lost** — this is
  one of the concrete payoffs of the whole process being git-backed rather
  than a live shared document. `git diff <commit-before-apply> <commit-after-apply> -- paper.md`
  shows exactly what the apply-commit changed; `git show <hash>:paper.md`
  recovers the full file as it stood at any earlier commit, including your
  hand-edit if the apply-commit overwrote it. Recover the lost text from
  there and reapply it, then commit that recovery on its own.
- **For genuinely simultaneous editing by more than one person**, this is
  the same problem Section 13.1 (co-authorship) already covers — coordinate
  directly, or use a git branch per person and merge deliberately, rather
  than relying on commit ordering alone to sort it out.

## 15. Commit message template

*🔴 Required*

Two small, distinct message shapes, matching the two commits in Section 14.

**The proposal commit (Step A)** — needs almost nothing, since nothing about
the paper changed yet:

```
Archive AI answer: <short-slug>

AI question: <one-line restatement of what was asked; full text in
  ai-requests/NNNN-.../question.md>
AI answer summary: <1-3 sentences on what the AI answered>
```

**The apply commit (Step B)** — this is the one with fact-check content (see
the plain-text copy in
[`templates/commit-message-template.txt`](templates/commit-message-template.txt)):

```
<short summary of what changed, imperative mood, ~50 chars>

Applies proposal from commit <hash of the Step A commit>.

Fact-check status:
  - <claim 1> — NOT YET CHECKED, added to TODO.md (the default)
  - <claim 2> — CHECKED against <source>, confirmed / corrected to <...>
    [optionally: attestation = Strongly attested / Moderately attested /
    Proposed, plausible — see Section 6.5]

Additional considerations:
  - <whatever you volunteered when asked in Step B, plus anything the AI
    noticed itself: a competing scholarly view, a caveat, follow-up this
    suggests>
```

Keep both sections in the apply commit even when short ("none outstanding" /
"n/a") — their presence is what makes the commit log auditable; a missing
section reads as an oversight, not as "there was nothing to say." Neither
section requires you to have actually checked anything before committing —
"NOT YET CHECKED" for every claim is a completely normal, expected commit.

## 16. File and folder naming conventions

*🔴 Required*

- Topic repository names: `kebab-case`, short, descriptive
  (`revelation-dating`, not `Revelation_Research_FINAL2`).
- `ai-requests/` subfolders: zero-padded sequence number + short slug,
  `0001-date-of-revelation-external-attestation`. The number gives a stable
  chronological order independent of git's own history, which matters once
  branches or rebases are involved.
- Reusable instruction files (Section 6.2): `instructions/instruction_<task>.md`,
  named after the task, not the date or the paper — `instruction_find_gaps.md`,
  not `instruction_july.md`, since the same instruction is meant to be reused
  across dates and even across topic repositories.
- Never delete or edit a saved `answer.md` after the fact. If the AI was
  wrong, that is exactly what makes the archived answer valuable — it
  documents the error and, combined with your `TODO.md`/`sources.md`
  correction, becomes part of the record of how the mistake was caught.

## 17. Using the template

*🔴 Required*

Copy [`templates/new-topic-repo/`](templates/new-topic-repo/) to start a new
topic:

```bash
cp -r templates/new-topic-repo ~/research/<your-name>/<new-topic-slug>
cd ~/research/<your-name>/<new-topic-slug>
git init
git add .
git commit -m "Initialize <topic> research repository"
```

New to git, Markdown, or turning a draft into a properly-cited PDF? See
[`tutorial-git-markdown-pdf.md`](tutorial-git-markdown-pdf.md) before or
alongside your first topic repository — it covers all three from scratch.

The template includes:

- A `CLAUDE.md` with maintenance instructions so that a Claude Code (or
  compatible) assistant working in the new repository already knows to
  archive every question/answer, prompt you for fact-check status, and
  commit per Section 15 without being told each time — see
  [`templates/new-topic-repo/CLAUDE.md`](templates/new-topic-repo/CLAUDE.md).
- A `DEPARTMENT-RULES.md` for any local rules your program adds on top of
  this manual's defaults — see Section 18.
- A `.claude/settings.json` with a working example of a harness-enforced
  check (Section 11.7, Section 18) — no per-repository setup needed beyond
  copying the template.

Then follow the workflow in Section 14 for every subsequent AI-assisted step.

## 18. Introducing department- or program-specific rules

*🔴 Required (when applicable)*

The template and this manual describe one default process. A specific
department, program, or even a single course may need to add its own rules
on top — a required citation style, a language requirement, a stricter
fact-checking bar for thesis work, a per-assignment AI-permission tag.
`templates/new-topic-repo/DEPARTMENT-RULES.md` is where these live.

### How it works

- **An administrator fills in `DEPARTMENT-RULES.md` once, in the template
  itself**, before it's distributed further. Every new topic repository
  created via `cp -r templates/new-topic-repo ...` (Section 17) inherits
  whatever the file says *at the moment it's copied* — there is no separate
  installation step.
- **A department rule can only add or tighten a constraint, never loosen one
  of the defaults in the main manual or `CLAUDE.md`.** If a local rule reads
  like it's trying to skip fact-check logging or the archive step, the AI is
  instructed (`CLAUDE.md` Step 0) to flag that specific line and ask before
  proceeding, not silently honor it.
- **Existing repositories keep the rules they were created with**, even
  after the template's `DEPARTMENT-RULES.md` changes later. This is
  deliberate, not a gap: a visibly-stale rule you can go check is safer than
  one that silently changed underneath a piece of work already in progress
  — the same principle behind never editing an archived `answer.md`
  (Section 16).

### Writing a rule the AI can actually act on

The same discipline Section 7 asks of research questions applies to writing
rules: bounded and checkable, not a vague appeal to judgment.

- Good: *"All citations must use SBL style, not Chicago or MLA."* —
  checkable against a named standard.
- Bad: *"Cite properly."* — properly by whose standard?
- Good: *"For any assignment marked `[no-AI]`, do not use this workflow at
  all."*
- Bad: *"Use good judgment about when AI is appropriate."* — this pushes a
  call onto the AI that only the instructor can actually make; if a rule
  genuinely needs human judgment, say so explicitly rather than phrasing it
  as an instruction the AI can just follow.

See `templates/new-topic-repo/DEPARTMENT-RULES.md` for a fully worked
example (citation style, language requirements, per-assignment
AI-permission tags, a stricter thesis fact-checking bar, and required
disclosure text) — replace it entirely rather than editing around it when
adopting the template.

### Making a mechanical rule actually automatic, not just written down

Some rules are simple enough to enforce with the harness itself rather than
relying on the AI to remember them every time. The template's
`.claude/settings.json` includes a working example: a hook that
automatically re-runs `scripts/check-repo-invariants.sh` (Section 11.7)
after every commit containing "git commit," surfacing a warning immediately
if the proposal/apply separation or the never-edit-`answer.md` rule was
violated — without anyone having to remember to check. This is the
strongest of the three enforcement tiers from Section 11.7's table: stronger
than an AI instruction (which depends on the AI remembering), because the
harness runs it regardless. Use `.claude/settings.json` for rules that
reduce to a simple, deterministic check over files or git history; keep
prose rules in `DEPARTMENT-RULES.md` for anything that needs actual
judgment (a citation style, a permission tag) to interpret.

### Should `/update_paper` also run automatically after every commit? Deliberately, no.

It's tempting to wire `/update_paper` (Section 6.1) into the same
after-every-commit hook as `scripts/check-repo-invariants.sh`, so the
adversarial-reader pass runs as an automatic aftermath of each apply-step
with no one needing to remember to invoke it. This is possible — the
underlying hook mechanism supports triggering an AI pass, not just a shell
script, on the same `PostToolUse`/"contains git commit" trigger already in
place — but it isn't what this template does by default, for a reason
worth stating rather than leaving implicit:

- **`check-repo-invariants.sh` runs in a fraction of a second**, because
  it's a deterministic script over git history. `/update_paper` is a full
  AI reasoning pass over the entire current state of `paper.md`,
  `sources.md`, and `TODO.md` — it takes real, noticeable time, and that
  time lands as a delay in the middle of whatever conversation triggered
  the commit. Section 1's "meant to run in the background, not slow you
  down" is a real constraint here, not a nicety: a check that visibly
  stalls every single commit is exactly the kind of friction that gets
  disabled the first time it's inconvenient.
- **Cost scales with frequency** (Section 10) — a full-paper review after
  every small apply-commit is a much larger, more frequent expense than
  running the same review deliberately, at a natural checkpoint, once
  enough new material has actually accumulated to be worth re-checking.
- **Most individual commits are small.** A full adversarial pass makes
  more sense triggered by "a meaningful chunk of writing has happened"
  than by "any commit happened," and git commit boundaries don't reliably
  track that.

**The actual default is a middle ground, not a binary choice between
"automatic" and "you have to remember it yourself":** `CLAUDE.md` has the
AI *ask*, every time, right after an apply-commit — "want me to run
`/update_paper` now?" — and only actually run it if you say yes (Step B,
item 10). Asking costs nothing and happens every time by default, so the
option is never just forgotten; running it — the part with real latency
and cost — stays entirely opt-in, per commit, exactly the "never block,
always ask, never run uninvited" shape Section 8's Step C/D checks already
use. This also lines up naturally with Section 13.2's checkpoint cadence:
in practice you'll say yes at the end of a writing session or before a
supervision meeting, and skip it on the small commits in between, without
having to decide that policy in advance.

A fully automatic version is still possible if a department wants it
despite the tradeoff — an `agent`-type hook on the same
`PostToolUse`/`Bash` event already used for the invariant check, invoking
`/update_paper`'s instructions directly rather than a shell command — but
this has not been built into the template or verified end-to-end the way
`check-repo-invariants.sh`'s hook has, so treat it as a documented
possibility to configure deliberately, not a tested default to expect out
of the box.

## 18.5 Reference implementation: `tooling/`

*🔵 Context*

[`../tooling/`](../tooling/) holds `thscript`, a Python library built end to
end through this manual's own process — Sections 14's request/document/
commit cycle, applied through survey, function list, architecture,
requirements, diagram, test plan, and test-driven implementation.

It is included as evidence that the process produces something, and — more
usefully for a manual about not overclaiming — as evidence of what the
process *catches*. Its `docs/problems.md` records four extent counts that
were falsified and two headline findings that evaporated when finally
measured, each with the correction and the reason. Section 3 argues that
AI output must be checked; `tooling/docs/` is what that checking looks like
when it is actually done and the results are kept.

Read [`../tooling/README.md`](../tooling/README.md) first. The library is
Apache-2.0; its documentation is CC BY 4.0.

## 19. Worked example

*🔵 Context*

[`example/`](example/) contains a small, real, git-initialized repository
that applies this entire process to an actual (deliberately small) research
question: *when was the Book of Revelation written — the 60s AD or the 90s
AD?* It has real commits, a real `TODO.md` with an item left open on purpose,
and an answer that turns out to need a correction, so you can see the
fact-check step actually catching something. Read its `README.md` first, then
run `git log -p` inside it to see the full history.

## 20. Quick checklist

*🔴 Required*

For a question worth archiving at all (Section 1 — skip pure exploration):

- [ ] Question and full answer saved verbatim under `ai-requests/NNNN-.../`,
      committed on its own as the proposal commit (Section 14, Step A)
- [ ] Paper/sources/notes only updated after explicit yes/no (Section 6.6),
      as a separate apply commit referencing the proposal commit's hash
- [ ] Every factual claim defaulted to NOT YET CHECKED in `TODO.md` unless
      you volunteered a check when asked the one optional question (Section 14, Step B)
- [ ] Apply commit message follows the template in Section 15
- [ ] Proposal and apply are two separate commits — never merged into one
