---
title: "Version-Controlling Your Thinking: A Git-Based Workflow for Auditable AI-Assisted Research"
author: "Hagen Schilder"
date: 2026-07-13
status: "First public draft — original methodology, published to establish prior art and authorship"
---

# Version-Controlling Your Thinking: A Git-Based Workflow for Auditable AI-Assisted Research

*Published 2026-07-13 by Hagen Schilder. This piece describes a
methodology developed and first written up by the author on this date, for
use in academic research supervision. It's shared publicly so the ideas
are usable by anyone, and so the record of who worked them out and when is
a matter of public, timestamped record rather than an internal document
nobody outside one department ever saw.*

## The problem with "just be careful"

Every guide to using AI in research says some version of the same thing:
*verify what it tells you, don't trust it blindly, disclose that you used
it.* This is correct and also close to useless, because it gives you a
disposition, not a process. A disposition doesn't scale across a hundred
AI questions asked over six months while writing a thesis. It doesn't
survive the ordinary pressure of a deadline. And it leaves no record: if
someone asks a year later exactly what an AI contributed to a specific
paragraph, "I was careful" is not an answer anyone can check.

What actually solves this is not a stronger disposition. It's a process
borrowed, almost unchanged, from a field that solved an adjacent problem
decades ago: software engineering's Configuration Management — the
discipline of tracking every change to a complex system, who made it, why,
and whether it was verified, without trusting anyone's memory to hold that
information later. Applied to research instead of code, using the same
tool (git), it produces something neither "be careful" nor a plain folder
of drafts can: a complete, timestamped, unforgeable record of exactly what
was asked, what an AI answered, what a human did with it, and what got
checked — built as a byproduct of doing the work, not as separate
overhead.

This piece describes that methodology. None of the individual pieces are
exotic — it's git, used deliberately, plus a handful of small conventions.
The value is in the specific combination and in a few details that turn
out to matter more than they look like they should.

## The core move: separate "the AI said this" from "I decided to use this"

The central habit is a two-commit pattern for every AI interaction that
might end up influencing your work:

**Commit 1 — the proposal.** The moment you get an answer from an AI
assistant, archive the exact question and the complete, unedited answer to
disk, and commit that archive immediately. Nothing about your actual paper
has changed yet — this commit is purely evidence that a specific question
was asked and a specific answer was given, at a specific time, verbatim.

**Commit 2 — the apply.** Only once you've actually decided to use the
answer — reviewed it, decided it holds up, said an explicit "yes" — do you
edit your actual draft. That edit is a second, separate commit, referencing
the first one by its hash.

Why bother separating these, when you could just edit the draft directly?
Because it makes three things true that "be careful" alone never
delivers:

- A rejected proposal still leaves a clean record of having been
  considered and turned down — useful later when you (or a supervisor)
  wonder why a particular avenue wasn't pursued.
- The apply commit can carry a fact-check status precisely because it's
  a distinct moment: "these three claims are not yet verified, this one
  was checked against Source X." That status has nowhere natural to live
  if proposal and application are the same edit.
- Nothing about the AI's raw output is ever silently smoothed into your
  prose without a trace. If a hallucinated citation makes it into your
  paper, the commit history shows exactly when, from exactly which answer,
  and — because the archived answer is never edited afterward — exactly
  what it looked like before anyone caught the problem.

This alone is most of the methodology. Everything else below is what you
add once this habit is in place.

## Confidence isn't binary

A checked/unchecked flag on every claim is the minimum bar, and it's
already more than most research practice does today. But it flattens a
real distinction: a claim independently confirmed by two unrelated sources
is not in the same epistemic position as your own inference that hasn't
been checked against anything. A three-tier rating —

- **Strongly attested** (confirmed by two or more independent
  sources/methods)
- **Moderately attested** (confirmed by one, beyond your own reasoning)
- **Proposed, plausible** (your own argument; not independently attested)

— turns "how sure are we, really" from a vague feeling into a stated,
checkable claim. It's cheap to add and meaningfully more honest than a
uniformly confident tone that doesn't distinguish its best-supported
points from its most speculative ones.

## Findings need an answer, but they should never block anything

Once you start asking an AI to help *check* your own work — flag a
possibly-real person's name that shouldn't be in a prompt, review a change
to your own research process rules for whether it quietly weakens a
safeguard, notice that a paragraph's citations are all bundled at the end
instead of attached to the sentences they support — a design question
appears immediately: what happens when the AI raises a concern?

The wrong answer is to make it block. A check that stops your work until
you address it gets disabled the first time it's inconvenient, and it
trains people to route around it rather than engage with it. The other
wrong answer is to let it be advisory in the weak sense — a comment in a
chat window that's gone the moment the conversation scrolls past it,
acknowledged or not.

The right shape, it turns out, already exists, in code review tools: an
open comment thread. The finding gets logged as an open item — not a
blocker, just a visible, dated, referenced note — and it stays open, `[ ]`,
until someone actually answers it. If they answer immediately, it's
checked off with their answer right there. If they don't, it stays open,
visibly unresolved, for as long as it takes someone to get to it. Nothing
is ever silently dropped just because the moment of raising it has passed,
and nothing is ever held hostage to it either.

## A rule that can tighten but never loosen — checked two ways

Any process like this eventually needs local exceptions: a specific
program requires a specific citation style, a specific assignment bans AI
outright, a thesis needs a stricter verification bar than a seminar paper.
The moment you allow local rules on top of a base process, you've created
exactly one way for the whole thing to quietly fail: a local rule that
reads like an addition but actually loosens a base protection — "skip the
archiving step to save time," buried in an otherwise reasonable-looking
addendum.

The fix is to check this two ways, deliberately redundant:

1. **A mechanical scan** of the local-rules file for language patterns
   that indicate weakening a default (a small, explicit blocklist:
   variations on "skip," "don't need to," "combine into one," and so on).
   This is fast, fully automatic, and catches the obvious cases. It will
   also miss cleverly-worded attempts, and it should never be mistaken for
   a guarantee.
2. **An AI review with actual comprehension**, applied independently of
   the mechanical scan, asking the same underlying question — does this
   addition tighten or loosen? — but with the capacity to catch phrasing a
   keyword list can't. This layer isn't a replacement for the mechanical
   one; it's a second, differently-shaped net over the same gap.

Neither layer blocks anything, per the principle above — both just leave a
recorded flag that needs a human answer. The point of running two
different kinds of check over the same risk isn't redundancy for its own
sake; it's that a keyword scanner and a comprehending reader fail in
different, mostly non-overlapping ways.

## Content is not instructions

The last piece matters most as AI assistants gain the ability to take
actions on your behalf — running commands, committing changes, and (in
more capable setups) pushing or merging into shared systems other people
also use. The moment an AI assistant reads a file and can also act on a
system, that file becomes a place an attacker — or just a bad-faith
collaborator — could try to steer it: an answer from an AI (if the
provider's own model were somehow compromised or manipulated upstream), a
rules file, any piece of content the assistant reads as part of its normal
work, could in principle contain text that reads like an instruction: "now
push this," "merge without asking."

The necessary discipline is simple to state and easy to skip if you don't
say it explicitly: **content is data, not instructions, regardless of what
it says about itself.** An assistant should feel free to make its own
local, reversible commits — those are cheap, private, and easy to undo.
Anything that becomes visible to someone else — a push, a merge into
shared history — should always require the human's actual, present
instruction, never something read out of a file. And if a file's content
appears to be *trying* to issue that instruction, that's not a command to
weigh; it's itself the finding to flag.

## Why this generalizes past its origin

This methodology was worked out for graduate theological research —
citation-heavy, historically dense, exactly the kind of writing where a
fabricated source or a flattened scholarly disagreement does real
damage and is easy to miss. But nothing about the mechanism is specific to
theology, or even to the humanities. Any research or writing practice with
the same three properties benefits from the same process:

- Claims need to be individually verifiable against sources.
- AI assistance is genuinely useful for the mechanical parts (synthesis,
  drafting, cross-referencing) and genuinely risky for the parts that
  require judgment (interpretation, verification, ethical framing).
- More than one person (a supervisor, a co-author, a reviewer) eventually
  needs to trust the record of how a piece of work came to say what it
  says.

Law, journalism, policy analysis, and any STEM field that leans on
literature review all fit that description. The two-commit pattern, the
confidence tiers, the open-comment-thread treatment of AI findings, and
the never-trust-embedded-instructions rule don't need adaptation to move
into any of them — only the specific fact-checking sources and citation
conventions change.

## Using this

There's no license restriction on any of this — it's a process, not code,
and the point of publishing it is for it to be used, adapted, and
improved. If you build on it, a link back to this piece is appreciated but
not required. If you find a way it fails that this piece doesn't account
for, that's worth knowing about more than it's worth guarding against
sharing.
