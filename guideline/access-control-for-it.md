# Access control for research git repositories — instructions for IT

Audience: whoever administers storage/hosting for the department's research
repositories (Section 12 of `README.md`: every researcher gets their own git
repository per topic). This document exists for one reason: **a repository
under this workflow contains a researcher's raw, unpublished thinking — every
question, every rejected hypothesis, every wrong turn — not just a finished
paper.** An idea sitting unpublished in someone else's `ai-requests/` folder
or `paper.md` draft is exactly as real, and exactly as theirs, as a physical
notebook, and needs the same expectation of privacy a physical notebook
would get. This document is about preventing two related but distinct risks:
another researcher (or an administrator without a need to) reading someone
else's unpublished ideas before they're ready to be shared, and a technical
setup that makes that easy to do by accident, not just by malice.

## The core rule

**Private by default, one owner, access granted deliberately — never a
shared space where everyone can read everyone else's repository.** This
follows directly from Section 12's "everyone gets their own git repository
space": that only works as a privacy boundary if it's enforced technically,
not just described in a manual.

## If repositories live in a shared folder-sync tool (Dropbox, OneDrive, etc.)

This is the setup already in use for some of this department's work, and it
is the easiest one to get wrong by accident, because the failure mode is
silent: a parent folder shared with a whole team, with every researcher's
subfolder nested underneath, gives everyone in that share read access to
everyone else's unpublished thinking by default — no one has to do anything
wrong for this to happen; it's the default shape of "one shared folder tree."

- **Each researcher's topic-repository folder should be its own share, not a
  subfolder of one big shared team folder.** If the sync tool supports
  folder-level sharing (Dropbox and OneDrive both do), share at the level of
  the individual repository, with only the people who actually need access
  (the researcher, and anyone they've explicitly added) — not at the level
  of a department-wide folder that happens to contain everyone's repositories
  as subfolders.
- **Audit existing shared folder trees for this specific mistake** — a
  folder like `Bibel/` shared broadly, with individual researchers' work
  nested inside it, is the pattern to look for and correct.
- **A synced folder is not a substitute for git-level access control** even
  once scoped correctly — see below for what to do when repositories are
  also hosted on a git server.

## If repositories live on a shared git server (self-hosted GitLab/Gitea, GitHub/GitLab organization, etc.)

- **Every topic repository defaults to private, owned by the individual
  researcher**, not created inside a department-wide group/organization with
  broad member read access. If your platform's org-level default is "all
  members can read all repos," override it per-repository or restructure so
  personal research repos live outside that org.
- **Collaborator access (an advisor, an examiner) is added explicitly, per
  repository, by the owner** — not granted automatically to a role (e.g.
  "all faculty can read all student repos"). A supervisor who needs to see a
  specific student's work gets added to that specific repository, ideally
  for a specific period (a supervision meeting, a submission window), not
  standing indefinite access to every repository that student will ever
  create.
- **Authentication**: SSH keys or platform-enforced two-factor
  authentication for all accounts with repository access — this is a
  standard baseline for any private-repository setup, not something specific
  to this workflow, but worth confirming it's actually enforced rather than
  optional.
- **IT/admin accounts should not have blanket standing read access to every
  private repository "for convenience."** Where an admin-level bypass is
  technically necessary (backups, platform maintenance), it should be
  logged/audited — the same audit-trail philosophy this manual applies to
  research claims (Section 12) applies to *access* to that research: if
  someone with elevated access did read a private repository, there should be
  a record of it.
- **Backups preserve the same access restrictions as the live system.** A
  backup console or restore tool that any admin can browse defeats
  per-repository privacy just as thoroughly as a misconfigured live share
  would, and is easy to overlook because it isn't the system anyone thinks
  of as "the repository."

## Granting a supervisor or examiner access to one specific repository (a worked procedure)

This is the concrete version of the "collaborator access added explicitly,
per repository" rule above, for the single most common real case: a
supervisor or examiner needs to read a student's thesis repository —
including its `ai-requests/` history — while supervising or grading it.

1. **Confirm the request is scoped to one specific repository.** One topic
   is one repository (Section 12), so a thesis's git history is already
   naturally isolated from that student's other, unrelated topic
   repositories. Never grant access to "all of this student's repositories"
   for a request that is actually about one piece of work.
2. **Add the supervisor/examiner as a read-only collaborator on that one
   repository** — write access only if they are actually expected to make
   edits themselves.
3. **Set an end date wherever the platform supports time-boxed access**
   (several enterprise git-hosting tiers support expiring repository
   membership). If yours doesn't, set a calendar reminder to revoke access
   once the examination period ends, and log the revocation date.
4. **Give the student the notice below at or before the point access is
   granted, not after the fact.** This is what actually settles the concern
   raised in Section 11.6: the student knows exactly who can see the
   repository, why, and for how long, *before* it happens — not informed
   after the fact, and not left to assume the worst.

### Notice-of-access statement (fill in and give to the student)

> **Notice of repository access**
> **Granted to:** *[supervisor/examiner name and role]*
> **Repository:** *[this one topic repository, named explicitly — not "all
> repositories"]*
> **Purpose:** *[e.g. "thesis supervision meeting on [date]" or "formal
> examination of the submitted thesis"]*
> **What will be reviewed:** the final paper and the `ai-requests/` / commit
> history behind it, evaluated against the department's stated norm of
> assessing the work and the diligence of its fact-checking — **not** used
> to judge exploratory questions, naive early attempts, or rejected
> hypotheses found in the history (Section 11.6).
> **Access period:** *[start date]* to *[end date]*; access is revoked after
> this date unless renewed with a new notice.
> **Your rights:** you may ask *[data protection contact]* what was
> accessed and when. This access is limited to the repository named above
> and does not extend to any other repository you maintain.

Keep a copy of every completed notice (who, which repository, why, for how
long) in the department's own access log — the human-readable twin of the
technical audit log this document asks IT to keep for admin/backup access
above. Together, the two mean that *every* access to a private repository —
by a supervisor or by an administrator — has a record of who, why, and for
how long, matching the same audit-trail standard this manual holds research
claims to (Section 12).

## Supporting the tooling itself: hooks, shell, and account tier

The workflow described in `README.md` and `templates/new-topic-repo/` now
depends on a few things actually working on each researcher's machine that
go beyond "git is installed." None of these are optional extras — without
them, features the manual describes as automatic silently don't run, which
is worse than not having them, since nobody notices.

- **A POSIX shell must be available.** `scripts/check-repo-invariants.sh`
  and the `.claude/settings.json` hook that runs it are shell scripts
  (`bash`, `grep`, `sed`). On Windows machines this means **Git for
  Windows** (which bundles Git Bash) needs to actually be part of the
  standard department machine image, not just any git client — a
  GUI-only git installation without Git Bash leaves these scripts with
  nothing to run them.
- **Don't let a managed/enterprise Claude Code configuration silently
  disable project-level hooks.** If IT deploys a centrally-managed
  configuration (an admin policy file), check it doesn't set
  `disableAllHooks: true` or `allowManagedHooksOnly: true` — either would
  silently stop the `.claude/settings.json` hook (Section 18) from ever
  running, with no error a student would notice; the invariant check would
  just quietly never fire.
- **A hook added to `.claude/settings.json` *after* a project's first
  session may need a manual reload to take effect** (opening the `/hooks`
  menu once, or restarting) — a known quirk of how the underlying tool
  watches for new settings files. This does not affect the department
  template itself (`.claude/settings.json` ships inside
  `templates/new-topic-repo/` from the start, so it's present before any
  session begins), but is worth knowing if IT or a student adds a hook to
  an *existing*, already-in-use repository later.
- **Provision Claude for Education/Work/Enterprise accounts department-wide
  rather than leaving individuals on personal consumer accounts.** This is
  the concrete action behind `README.md` Section 11.4's recommendation: a
  commercial-tier account is what actually makes "not used for model
  training by default" true, with no per-user toggle to forget. Leaving
  this to individual students to opt out of on a personal account is a
  weaker default than IT provisioning the right account tier centrally.
- **The new review-comment mechanism (`TODO.md` entries for Step
  C/D flags, README.md Section 18) needs no new IT infrastructure at
  all** — it's the same plain Markdown file already covered by the access
  controls above. Worth stating explicitly so this document's scope stays
  clear: everything in this section is about what makes the *tooling* run,
  not an expansion of what needs to be secured or provisioned beyond it.

## When someone leaves the department

- **Revoke access promptly** — a departing student or staff member's
  collaborator access to others' repositories should be removed as part of
  offboarding, not left to lapse naturally.
- **Decide and document, in advance, who owns a repository after its creator
  leaves.** The researcher's own unpublished ideas remain theirs; give
  departing researchers a clear, simple way to export or retain their own
  repositories (a `git clone` of their own work is enough) rather than
  leaving ownership ambiguous.

## The norms layer, not just the technical one

Technical access control only works alongside a stated policy that **reading
a colleague's private repository without being explicitly granted access is
a policy violation**, equivalent to reading someone's private notebook,
regardless of whether it happens to be technically reachable (a
misconfigured share, a forgotten permission). Publish this as an explicit,
short policy statement, not just an assumption — the easiest way for an idea
to be "read" before its author is ready is a technical default nobody
thought to check, not a deliberate act, which is exactly why the defaults in
this document matter more than any single rule about intent.

## Quick checklist for a new repository host/share

- [ ] Private by default, one owner per topic repository
- [ ] No department-wide folder or group grants blanket read access to
      individual research repositories
- [ ] Collaborator access added explicitly, per repository, by the owner
- [ ] SSH keys or 2FA enforced for all accounts with any repository access
- [ ] Admin/backup access to private repository contents is logged
- [ ] Offboarding process includes prompt revocation and clear ownership
      handoff
- [ ] A short, published policy states that reading a colleague's private
      repository without granted access is a violation, independent of
      technical reachability
- [ ] Git for Windows (with Git Bash) is part of the standard machine
      image, not just a GUI git client
- [ ] Managed AI-tool configuration doesn't set `disableAllHooks` or
      `allowManagedHooksOnly`, which would silently stop the department's
      invariant-check hook from running
- [ ] Department-wide Claude for Education/Work/Enterprise accounts are
      provisioned, rather than leaving individuals on personal consumer
      accounts
