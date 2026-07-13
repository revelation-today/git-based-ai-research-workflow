#!/usr/bin/env bash
# Structural invariant checks for a topic repository following the
# department's AI research workflow (see ../../../README.md, Section 11.6).
#
# These two checks are fully mechanical — no legal or scholarly judgment
# needed, just git history — which is exactly why they belong in a script
# rather than relying on anyone remembering to follow the rule by hand.
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
    echo "        An archived answer must never be edited after its proposal commit (README.md Section 15)."
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

if [ "$fail" -eq 0 ]; then
  echo "All structural invariants hold."
else
  echo
  echo "One or more structural invariants failed — see above. This does not mean"
  echo "anything is factually wrong, only that the commit structure itself drifted"
  echo "from the process (e.g. an answer got edited, or a proposal and its apply"
  echo "got squashed together)."
  exit 1
fi

# --- Optional: wire this in as a pre-push hook ---
# From the repository root:
#   cp scripts/check-repo-invariants.sh .git/hooks/pre-push
#   chmod +x .git/hooks/pre-push
# This makes the check run automatically before every push, so a drift from
# the process is caught locally rather than discovered later.
