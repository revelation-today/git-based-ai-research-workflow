# Using this methodology as an independent researcher (no university, no IT department)

Everything in `README.md` is written assuming a department: colleagues,
students, an IT department, a supervisor. None of that is actually
load-bearing. The core methodology — the propose/apply commit pattern,
the fact-check discipline, `CLAUDE.md`'s automation, `/update_paper` — has
no institutional dependency at all. This document is the adaptation guide:
what to skip, what matters *more* without an institution behind you, and
how to replace the one thing a department's IT staff would otherwise
handle for you — backup and hosting.

## What stays exactly the same

- Sections 1–10 of `README.md` (why this works, and the six techniques,
  good/bad prompting, recognizing flawed answers, multi-AI, cost
  awareness) — none of this assumes a department.
- Section 12 (one git repository per topic) — still the right structure,
  just under your own personal folder instead of a department-managed one.
- Section 14 (the propose → apply → fact-check workflow) — unchanged.
- Sections 15–17 (commit message template, naming conventions, using the
  template) — unchanged; `cp -r templates/new-topic-repo ...` works
  identically.
- Section 19 (the worked example) — still a good reference for what the
  commit history should look like.
- Section 20 (the quick checklist) — unchanged.
- `templates/new-topic-repo/CLAUDE.md` (Steps A–D), `/update_paper`
  (`.claude/commands/update_paper.md`), and
  `scripts/check-repo-invariants.sh` with its `.claude/settings.json` hook
  — all work with zero modification. None of them reference a department
  anywhere in their logic.

## What to skip

- **`DEPARTMENT-RULES.md`** — delete it from your copy of the template, or
  leave it untouched; nothing enforces its presence, and
  `check-repo-invariants.sh` already reports "nothing to check" when the
  file doesn't exist (this is exactly what the worked example's own
  repository does — it has no `DEPARTMENT-RULES.md` either).
- **Section 13** (collaborative work: co-authorship and supervision
  feedback) — not applicable unless you actually gain a co-author or a
  supervisor later; revisit it then, if it happens.
- **Section 18** (introducing department-specific rules) — not applicable;
  there's no department to add rules on top of your own defaults.
- **Section 11.1** (publisher/institutional AI-disclosure requirements) —
  not relevant until you actually submit somewhere with such a policy;
  worth reading again *at that point*, not now.
- **Most of `access-control-for-it.md`** — its scoped-access,
  notice-of-access, and multi-collaborator procedures collapse to a single
  sentence when there's no one else involved: don't put the repo in a
  shared or publicly-visible location. The one part of that document worth
  reading anyway is the section below.

## What matters *more* to you than it did to the department version

- **Section 11.4 (AI provider training/retention settings)** is now
  entirely your own responsibility, with no IT department defaulting you
  into a safer account tier. Concretely: check your AI subscription's
  privacy settings (for Claude: Account Settings → Privacy → "Help improve
  Claude") and turn training off if you want your prompts kept out of any
  shared model, especially before discussing anything unpublished.
- **Section 11.2 (GDPR)** still applies to *you personally*, not just
  institutions, the moment your research involves real living people's
  identifiable data — a narrower exemption than it sounds covers genuinely
  personal/household activity, and doesn't reliably cover material you
  might later publish or share. The pseudonymization rule applies
  regardless of who, if anyone, you're accountable to.
- **Section 3's fact-checking discipline** doesn't get less important
  without anyone grading you. The only thing that changes without an
  institution is who would catch a skipped check — which is exactly the
  reason to keep doing it rather than the reason to relax it.

## Replacing the IT department: backup and hosting

This is the one piece an institution would otherwise provide for you.

### Day to day: a synced folder is fine

Keeping your topic repositories inside a folder synced by Dropbox,
OneDrive, or similar gives you automatic, versioned, off-machine backup
with no extra setup — exactly what this document's own example repository
does. One caveat: **don't edit the same repository from two devices at the
same time.** Git's `.git` folder is many small files that change on every
commit; committing on one device while the sync service is mid-transfer on
another can produce a conflict inside `.git` itself. Wait for a full sync
before switching machines.

### Real backup: a free private git host, independent of the sync folder

A synced folder protects against your laptop dying. It does *not*
protect against a bad sync event or an accidental deletion propagating to
the cloud copy, because file-sync mirrors whatever state the file is in,
good or bad. A `git push` to a separate host is a different, complementary
kind of backup: an independent, content-addressed copy of your commit
history, not just a mirrored file.

GitHub and GitLab both offer unlimited free **private** repositories for
individual accounts — genuinely private, invisible to anyone without an
explicit invite, no institutional account needed. Setup, once per machine:

1. Create an account at [github.com](https://github.com) (or GitLab,
   Codeberg, sourcehut — same idea).
2. For each topic repository, create a new **private** repository on the
   host — don't let it auto-generate a README/license, since your local
   repo already has content.
3. Connect your existing local repo to it:

   ```bash
   cd ~/research/<your-name>/<topic-slug>
   git remote add origin https://github.com/<your-username>/<topic-slug>.git
   git branch -M main
   git push -u origin main
   ```

   On Windows, Git for Windows' bundled Credential Manager handles login
   with a one-time browser popup on first push — no manual token or SSH
   key needed, though either is a fine alternative if you prefer them.
4. From then on, `git push` after a commit (or a batch of commits) keeps
   the independent copy current.

One remote per topic repository, matching one local repository per topic
(Section 12).

### "Private" is a strong protection, not an absolute one

Worth being precise about this rather than either dismissing or
overstating it. "Private" on GitHub means: not indexed, not browsable,
not visible to anyone without an explicit invite. It does not mean
"unhackable" — nothing connected to the internet is. The realistic threat
model, in actual order of likelihood:

1. **Your own account gets compromised** — a weak or reused password, or a
   successful phishing attempt — by far the most likely path, and the only
   one entirely in your control. **Enable two-factor authentication on
   your GitHub/GitLab account.** This one step closes the realistic attack
   path almost completely, even against a leaked password.
2. **Your own device gets compromised** (malware, physical access to an
   unlocked machine stealing a cached login) — mitigated by ordinary
   device hygiene, not specific to git.
3. **A leaked token or SSH key**, if you use one instead of the browser-based
   Credential Manager flow and it ends up exposed somewhere (accidentally
   committed, stored unencrypted) — never commit credentials into a repo;
   rotate immediately if one ever leaks.
4. **The hosting platform itself being breached**, or **insider access** at
   the company running it — both real categories of risk in the abstract,
   neither specific to this choice (Dropbox, Google Drive, or any other
   cloud service carries the same category of risk), and neither
   meaningfully actionable beyond choosing a reputable provider.

A private repository with two-factor authentication enabled is a genuinely
appropriate level of security for keeping personal research private from
other people — comparable to, not weaker than, what an institution would
actually provide. If you want a higher bar than "hosted by a trusted third
party" at all, the alternative is local-only git with no remote (accepting
the backup tradeoff that comes with it), or encrypting specific files
before they ever enter git.

## Quick-start checklist for an independent researcher

- [ ] Two-factor authentication enabled on your git hosting account
- [ ] AI provider's training/retention setting checked and set the way you
      want (Section 11.4)
- [ ] `templates/new-topic-repo/` copied for your first topic, with
      `DEPARTMENT-RULES.md` deleted
- [ ] `git init`, `git add`, `git commit` for the initial state
- [ ] A private repository created on GitHub/GitLab, connected via
      `git remote add` + `git push -u origin main`
- [ ] Section 14's propose → apply → fact-check workflow followed as
      normal from here on — nothing else about the process changes
