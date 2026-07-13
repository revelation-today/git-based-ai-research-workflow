#!/usr/bin/env bash
# Structural invariant checks for a topic repository following the
# department's AI research workflow (see ../../../README.md, Section 11.7).
#
# The first two checks are fully mechanical -- no legal or scholarly
# judgment needed, just git history -- which is exactly why they belong in
# a script rather than relying on anyone remembering to follow the rule by
# hand. The third is a heuristic (keyword) check, weaker than the first
# two but still deterministic and still worth running automatically.
# Everything else in Section 11 (personal data, defamation risk, copyright)
# needs a human; this script does not attempt those.
#
# Run manually, or wire into a pre-push hook (see bottom of this file).
set -euo pipefail

fail=0

echo "Checking: every answer.md is touched by exactly one commit (never edited after archiving)..."
while IFS= read -r -d '' f; do
  count=$(git log --follow --format=%H -- "$f" | wc -l)
  if [ "$count" -ne 1 ]; then
    echo "  FAIL: $f has been touched by $count commit(s) (expected exactly 1)."
    echo "        An archived answer must never be edited after its proposal commit (README.md Section 16)."
    fail=1
  fi
done < <(git ls-files -z -- 'ai-requests/*/answer.md' 2>/dev/null || true)

echo "Checking: no commit mixes an ai-requests/ proposal with a paper/sources/TODO apply..."
for commit in $(git log --format=%H); do
  touches_requests=false
  touches_apply=false
  while IFS= read -r f; do
    [ -z "$f" ] && continue
    case "$f" in
      ai-requests/*) touches_requests=true ;;
      paper.md|sources.md|TODO.md) touches_apply=true ;;
    esac
  done < <(git show --name-only --format= "$commit")
  if $touches_requests && $touches_apply; then
    echo "  FAIL: commit $commit touches both ai-requests/ and paper.md/sources.md/TODO.md."
    echo "        Proposal and apply must always be two separate commits (README.md Section 6.6)."
    fail=1
  fi
done

echo "Checking: DEPARTMENT-RULES.md doesn't read like it's trying to weaken a core rule..."
# This is a keyword heuristic, not a semantic understanding of the file --
# it will miss cleverly-worded attempts and can false-positive on an
# innocent sentence that happens to contain one of these phrases. Treat a
# hit as "a human should read this line and confirm it's not actually
# loosening a default," per README.md Section 18 -- not proof of a problem.
if [ -f DEPARTMENT-RULES.md ]; then
  # One pattern per line; extend this list as new weakening phrasings turn up.
  patterns=(
    'skip.*(archiv|ai-requests|proposal)'
    "don'?t (need to |)archive"
    'no need to archive'
    'skip.*fact.?check'
    "don'?t (need to |)(log|check).*TODO"
    'combine.*(proposal|apply).*(one|single) commit'
    'one commit instead of two'
    'skip the (proposal|apply) commit'
    "don'?t commit"
    'no commit needed'
    '(edit|modify|delete|overwrite).*answer\.md'
  )
  hit=0
  for pat in "${patterns[@]}"; do
    if grep -inE "$pat" DEPARTMENT-RULES.md > /tmp/dept-rule-hit.$$ 2>/dev/null; then
      hit=1
      echo "  FLAG: DEPARTMENT-RULES.md contains a phrase matching /$pat/:"
      sed 's/^/    /' /tmp/dept-rule-hit.$$
    fi
    rm -f /tmp/dept-rule-hit.$$
  done
  if [ "$hit" -eq 1 ]; then
    echo "        A department rule may only ADD or TIGHTEN a constraint, never loosen"
    echo "        one of the defaults above (README.md Section 18). Confirm the flagged"
    echo "        line(s) are not actually weakening a default before proceeding."
    fail=1
  fi
else
  echo "  (no DEPARTMENT-RULES.md in this repository -- nothing to check)"
fi

if [ "$fail" -eq 0 ]; then
  echo "All checks passed."
else
  echo
  echo "One or more checks failed -- see above. The first two mean the commit"
  echo "structure itself drifted from the process (e.g. an answer got edited, or"
  echo "a proposal and its apply got squashed together). The third means"
  echo "DEPARTMENT-RULES.md contains wording worth a human double-checking --"
  echo "it is a flag, not a verdict."
  exit 1
fi

# --- Optional: wire this in as a pre-push hook ---
# From the repository root:
#   cp scripts/check-repo-invariants.sh .git/hooks/pre-push
#   chmod +x .git/hooks/pre-push
# This makes the check run automatically before every push, so a drift from
# the process is caught locally rather than discovered later. The
# .claude/settings.json hook (README.md Section 18) already runs this
# script after every commit containing "git commit", so the pre-push hook
# is a redundant second layer, not the only one.
