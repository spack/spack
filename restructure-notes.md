# Branch state after the rebase onto develop (2026-08-20)

Status notes for `hs/test/property-based-tests` / `hs/test/spec-algebra-fuzz` (PR 52801).

## State

- The branch sits on plain upstream/develop and carries only its own content. The last
  extraction PR, `hs/fix/arch-target-ranges` (PR 52856), merged on 08-20, so the five target
  commits that used to sit at the bottom were dropped in this rebase. Develop's version of
  the target semantics, which grew further while the PR was in review, is the one in effect.
- The `spec_algebra.py` tests those commits carried are kept, folded into
  `spec.py: test the algebra of satisfies and constrain`, which is where that file lands.
  One expectation moved with the archspec update of #52919: `armv8.6a:` meet `neoverse_n1:`
  now reads `ampere1:,neoverse_v3ae:`, since `ampere1a` is no longer minimal and
  `neoverse_v3ae` is new.
- The remaining commits replayed onto develop with no conflicts.
- The old tip is kept at `backup-property-based-tests-20260820`.
- `hs/test/spec-algebra-fuzz` (the PR head) points at the last code commit: the harness
  scripts under `lib/spack/spack/test/` and these docs stay out of the PR.
- `formal/spec-semantics.tex` cites source line numbers, which this rebase shifted by about
  seventy lines in `spec.py` and invalidated outright for the target code. They are left as
  they are.

See `bug-ledger.md` for the bug counts per PR.
