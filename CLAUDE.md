# Maintenance instructions for the AI assistant working in this repository

This repository follows the department's git-based AI research workflow
(the full manual is `README.md` in the `guideline` folder this template came
from). Follow these steps automatically whenever the user asks you a research
question in this repository — do not wait to be told to "log this" or
"commit this," that is the default behavior here. Keep it lightweight: the
bookkeeping below is your job, done in the background, not a checklist you
hand to the user.

## Step A — archive the question and answer (do this for every real question)

Skip this entirely for pure exploration that touches no file (the user is
just thinking out loud, or asking something with no bearing on the paper).
Do it for anything that could plausibly end up informing the paper.

1. **Determine the next request number.** List the existing
   `ai-requests/NNNN-*` folders, take the highest `NNNN`, and use the next
   one, zero-padded to 4 digits. If there are none yet, start at `0001`.
2. **Create the request folder** `ai-requests/NNNN-<short-slug>/`.
3. **Write `question.md`** containing the user's question verbatim.
4. **Answer normally** in the conversation, and **also write the complete
   answer, verbatim, to `answer.md`** in the same folder — not trimmed or
   cleaned up even if your chat reply is more concise.
5. **Commit this immediately, on its own**, e.g. `Archive AI answer:
   <short-slug>`. Nothing about the paper has changed yet, so there is
   nothing to decide first — this commit is purely a record that the
   question was asked and what was answered. This is the **proposal
   commit**; note its hash, you'll reference it later.

## Step B — apply it, only once the user has actually decided to use it

Do not do this just because an answer exists. Apply it once the user's
intent to incorporate it is clear (they say so, or continue as if it's now
part of the paper).

6. **Apply the change** to `paper.md` / `sources.md` / wherever it belongs.
7. **Log every extracted factual claim in `TODO.md` as not-yet-checked by
   default** — referencing the proposal commit hash from Step A. This needs
   no input from the user; it's the safe default.
8. **Ask the user exactly one light, optional question**, and don't block on
   it:
   > "Anything to add here — a source you already know that confirms or
   > contradicts this, a caveat, or related work worth noting?"
   This is a standing invitation for outside knowledge only *you* don't
   have access to, not a demand that they personally verify every claim
   before you're allowed to commit. If they answer, fold it into
   `sources.md` (moving the relevant claim off `TODO.md` if it's now
   confirmed) and into the commit message below. If they don't, or say
   "nothing," proceed anyway — silence is not a blocker.
9. **Stage exactly what this apply-step touched** (`paper.md`, `sources.md`,
   `TODO.md` — not the `ai-requests/` folder again, that was Step A's
   commit) and **commit separately from the proposal commit**, referencing
   its hash:

   ```
   <short summary of what changed, imperative mood, ~50 chars>

   Applies proposal from commit <hash of the Step A commit>.

   Fact-check status:
     - <claim 1> — NOT YET CHECKED, added to TODO.md
     - <claim 2> — CHECKED against <source the user volunteered>, confirmed / corrected to <...>

   Additional considerations:
     - <whatever the user volunteered in step 8, plus anything you noticed
       yourself: a competing scholarly view you didn't cover, a caveat>
   ```

10. **Show the user what happened** — the commit message and the output of
    `git show --stat HEAD` — so they can see exactly what was committed
    without checking themselves.

## Rules

- The proposal commit (Step A) and the apply commit (Step B) are always
  **two separate commits**. A rejected or "not now" proposal still leaves a
  clean, committed record of having been considered, without ever mixing an
  undecided idea into the same commit as the paper's actual content.
- Never combine two distinct questions/answers into a single proposal commit.
- Never edit or delete a previously committed `answer.md`. If an earlier
  answer turns out to be wrong, record the correction in `TODO.md` and/or
  `sources.md`, referencing the commit hash that introduced the original
  claim — the wrong answer stays on record as documentation of the error.
- Never turn step 8 into a multi-question checklist walking through each
  claim one by one — one light, optional, easily-skippable question per
  apply-step is the ceiling, not the floor.
- If a task is a recurring type of request (e.g. "find gaps in this
  argument," "check every fact," run a task from `instructions/`), still
  archive it via Step A, and note in `question.md` which instruction file
  (and which commit of it) was used.
