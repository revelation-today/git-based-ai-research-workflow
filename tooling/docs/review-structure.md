# Configuration-management review

**Source:** item 8 of [`../input/task.md`](../input/task.md) — review the
file structure, filenames and content; propose improvements; **no
functionality may break.**
**Status:** applied and verified. 129 tests, 14 fixture checks, both repo
scripts, the spike and the traceability scan were re-run after every move.
**Date:** 2026-08-07.

---

## 1. Findings and what was done

| # | Finding | Action | Risk handled |
|---|---|---|---|
| **CM-1** | `output/` held **design documents**, not program output. The name promised generated artifacts and delivered specifications — and it collided with the `output/` directories the sibling projects genuinely use for results. | `output/` → **`docs/`** | `thscript/verify.py` and `tests/test_verify.py` read `output/requirements.md`; both repointed and re-run |
| **CM-2** | `paper.md` and `sources.md` were **template leftovers**, 19 and 11 lines of placeholder, never used. This is a tooling repository, not a paper. Worse, `check-repo-invariants.sh` still named them as the "apply side" of the proposal/apply split, so the invariant was guarding files that did not participate in anything. | Removed; invariant now guards `docs/*` and `TODO.md` — the artifacts that *are* the apply side here | Invariant re-run: passes, and still correctly separates proposal from apply |
| **CM-3** | `tests/spike_null_model.py` lived in `tests/` but is **not a test** — no `test_` prefix, never collected. A reader scanning `tests/` would count it as coverage. | → **`spikes/null_model.py`** | Re-run standalone; still reproduces 0.600570 |
| **CM-4** | `tests/fixtures/verify.py` shadowed `thscript/verify.py` by name while doing something entirely different (checking fixtures, not claims). | → `tests/fixtures/**check_fixtures.py**` | Re-run: 14/14 |
| **CM-5** | `commit-message-template.txt` sat at the repository root among governance files, though it is reference documentation. | → `docs/` | README link updated |
| **CM-6** | `.claude/commands/update_paper.md` was a **stale template command**: it operates on `paper.md`, which no longer exists, and instructs an AI to check a paper this repository does not contain. | Renamed to `check_repo.md`; rewritten for this repository | — |
| **CM-7** | **The invariant script had been failing on every commit since 2026-08-07.** | Fixed, with a *visible* exemption marker | See below — the most serious finding |

---

## 2. CM-7 in full: a check that always fails

`scripts/check-repo-invariants.sh` runs after every commit via
`.claude/settings.json`. Since `DEPARTMENT-RULES.md` was written it had
returned **exit 1 every single time**, on this line:

```
FLAG: DEPARTMENT-RULES.md contains a phrase matching
      /(edit|modify|delete|overwrite).*answer\.md/:
  60: forbids editing a committed `answer.md` (Section 16), and
```

The rules file *quotes a prohibition in order to uphold it*, and the
keyword scan cannot tell that from an attempt to weaken it. I noted this
once as a false positive when it first appeared and then left it — so the
hook emitted a warning on every subsequent commit.

**That is the failure the department manual explicitly warns about**: a
check that visibly fires on every commit is the kind that "gets disabled
the first time it's inconvenient." Worse than disabled, it was *trained
away*: a red check nobody acts on is indistinguishable from no check.

**Fix, and the shape of it matters.** A line may now be exempted with a
`[restates-rule]` marker, and **exemptions are counted and reported**:

```
(1 line(s) exempted with [restates-rule] -- these quote a
 prohibition in order to uphold it. Read them if the count changes.)
```

Never silent. An invisible allowlist is how a check quietly stops
checking, which would have traded a loud useless failure for a quiet
useless pass.

---

## 3. Verification — nothing broke

Run after the moves, from a clean checkout of the working tree:

| Check | Before | After |
|---|---|---|
| `pytest tests/` | 129 passed | **129 passed** |
| `tests/fixtures/check_fixtures.py` | 14/14 | **14/14** |
| `scripts/check-repo-invariants.sh` | **exit 1** (CM-7) | **exit 0** |
| `scripts/check-ip-boundary.sh` | 102 refs, 0 shareable | 105 refs, **36 shareable** |
| `spikes/null_model.py` | 0.600570 | **0.600570** |
| `verify.traceability_gaps()` | `[]` | **`[]`** |

One test did break and was caught: `test_tc44_is_not_vacuous` hardcoded
`output/requirements.md`. I had updated `thscript/verify.py` but missed
its test — precisely the class of breakage this item was told to prevent,
found by running rather than by reasoning.

**The IP-boundary change is correct, not a regression.** `docs/` now
matches the shareable-zone pattern, so its 36 sibling references are
reported. Under the chosen Option 4 those documents *will* be exported,
so they must be pseudonymised — the script is now telling the truth it
previously could not.

---

## 4. Resulting structure

```
theology_scripts/
  README.md              entry point for humans and AIs
  CLAUDE.md              how an AI maintains this repository
  DEPARTMENT-RULES.md    local rules; IP boundary; reproducibility floor
  TODO.md                open questions and fact-checks
  pyproject.toml  requirements.txt  .gitattributes  .gitignore

  thscript/              the library — 7 modules
  tests/                 129 tests + fixtures/ (generated, self-checking)
  spikes/                experiments that are not tests
  docs/                  design record: problems, use-cases, functions,
                         libraries, architecture(+diagram), requirements,
                         test-plan, ip-cleanup-proposal, this review
  input/                 the researcher's brief
  ai-requests/           verbatim audit trail, never edited
  scripts/               invariant and IP-boundary checks
  .claude/               settings + commands
```

---

## 5. Proposed, not done — needs your decision

| # | Proposal | Why not yet |
|---|---|---|
| **CM-8** | Consolidate dependencies into `pyproject.toml`, leaving `requirements.txt` as a pinned lock with a pointer. | Two sources of truth today; harmless but duplicated. Wanted your call on packaging style. |
| **CM-9** | Add a `LICENSE`. The public export needs one. | Choosing a licence is yours — MIT and Apache-2.0 are the usual candidates for a library like this. |
| **CM-10** | Number the design documents for reading order (`01-problems.md`, …). | Would break every existing cross-link and every `ai-requests` reference to them. An index in the README achieves the same for less. **Recommend rejecting.** |
| **CM-11** | Make `check-ip-boundary.sh` fail the hook rather than report. | You asked this in the IP proposal and it is still open. Note it would fail *today*, on the 36 `docs/` references — so it should land together with pseudonymisation, not before. |
