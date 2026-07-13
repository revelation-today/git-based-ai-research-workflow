# Example topic repository: `revelation-dating`

This folder is a real, git-initialized example of the workflow described in
the department manual (`../README.md`), applied to a small research question:

**Research question:** What is the evidence for dating the Book of Revelation
to the reign of Nero (60s AD) versus the reign of Domitian (90s AD), and
which external witnesses are cited for each?

This is intentionally a small slice of the topic — enough to show the full
propose → apply → fact-check cycle (Section 13), including a case where
fact-checking catches an AI hallucination (a fabricated journal article), not
a complete treatment of the dating question.

## How to read this example

Run, inside this folder:

```bash
git log -p
```

You will see five commits:

1. **Repository initialization** — the empty template structure (including
   `CLAUDE.md`), filled in with this specific research question.
2. **Proposal commit** — a question asked about the dating debate, with the
   AI's full answer archived verbatim under `ai-requests/0001-.../`. Nothing
   about the paper has changed yet; this commit is purely the record of what
   was asked and answered.
3. **Apply commit** — once the answer was reviewed and accepted, it's used
   to draft a section of `paper.md`. Every extracted claim defaults to NOT
   YET CHECKED in `TODO.md`, referencing the proposal commit's hash — no
   fact-checking has happened yet at this point, and that's a normal,
   expected commit to make.
4. **Fact-checking commit** — a later, separate commit that actually checks
   two of the three claims: the patristic witness in Irenaeus is confirmed
   against a citable primary source; a specific journal article the AI cited
   turns out not to exist at all — a textbook hallucination — which gets
   flagged in `TODO.md` and never makes it into `sources.md`. The third
   claim (about Clement of Alexandria) is deliberately left open, to show
   that not every item gets resolved right away — some genuinely need a
   specialist, not just a lookup.
5. **Repository-maintenance commit** — a later update to `CLAUDE.md` (the
   best-effort legal/institutional checks in Section 11.7) and the new
   `scripts/check-repo-invariants.sh`. This isn't an AI-request cycle, so
   it's its own plain commit rather than a proposal/apply pair — not every
   commit in a topic repository has to fit that shape, only the ones that
   stem from an actual AI question.

This is the payoff of the process: nothing about the fabricated citation
looked different from the real one in the AI's answer. It was caught only
because fact-checking against a real library catalog/database was a logged
step that happened *after* the paper already reflected the claim — not
because the error was somehow visible in the text itself, and not because
the process demanded it be caught before anything was drafted.
