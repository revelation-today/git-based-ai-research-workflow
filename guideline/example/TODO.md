# Open fact-checks and questions

Each item: the claim, which commit introduced it, and what needs checking.
Check items off (`- [x]`) in a dedicated commit once resolved, and note in
that commit message what source resolved it. Do not delete resolved items —
a checked-off history is part of the audit trail.

- [x] Irenaeus, *Against Heresies* 5.30.3 dates John's vision to "the end of
      Domitian's reign" — introduced in commit `779d25b` — CHECKED against
      the public-domain Roberts-Donaldson translation (Ante-Nicene Fathers,
      vol. 1). Confirmed: the passage exists and says what the AI answer
      claimed. See `sources.md`.
- [ ] Clement of Alexandria, *Quis Dives Salvetur* 42, indirectly supports a
      Domitian-era dating — introduced in commit `779d25b` — still needs a
      patristics specialist read, not just a lookup. Left open deliberately:
      not every item gets resolved on the first pass.
- [x] Michael A. Thornbury, "The Neronic Redating of the Apocalypse,"
      *Journal of Early Christian Studies* 12 (2004), 45-67 — introduced in
      commit `779d25b` — CHECKED: no such article found in the Journal of
      Early Christian Studies via Project MUSE, and no author of this name
      found in the ATLA Religion Database. Conclusion: fabricated citation
      (hallucination). Do not cite. Removed from `sources.md`.
