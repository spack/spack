# Branch state after the restructure (2026-08-31)

Status notes for `hs/test/property-based-tests` / `hs/test/spec-algebra-fuzz` (PR 52801).

## State

- The branch sits on upstream/develop with no extraction PR below it. The base commit
  `spec.py: round-trip abstract patches:=<checksum>` merged as #52928 and left the branch
  with the 08-31 rebase. Review replaced its `VariantMap.abbreviate_patches()` with a
  `string(abbreviate_patches=...)` method on `VariantMap` and `VariantValue`, which also
  removed the `not self._concrete` guard the commit had added to the `format` fast path.
  Abstract variants print exactly, so abstract specs round-trip through `str()`; only
  concrete specs render their patch checksums as 7-character `patches=` prefixes.
- The absorption extraction merged as #52916. Its `constrains_only_name_and_versions` rule
  is the virtual semantics in effect: a virtual constrains a name and versions only,
  anything else on a rhs virtual is satisfied by nothing, and such an edge stays a
  parallel edge in the meet. Review added a concretizer error for virtuals constrained
  beyond versions, and made the predicate public.
- A fifth commit left the branch with the 08-21 rebase onto the merged #52916, superseded
  by #52928: `spec.py: pin what the patches format leaves out` (the pinned round-trip
  disjointness is fixed under it; the corpus skip and the harness's `truncated_patch` gap
  left with it).
- Four commits left the branch on 08-21, superseded by develop or by PR 52916:
  `spec.py: widen the virtuals parameter of the edge constructors` (no caller needs it
  anymore), `spec.py: keep flag propagation when merging` (fix and most tests merged as
  #52858; the one uncovered assertion moved into `spec_algebra.py`), `spec.py: compare the
  provider's attributes too` (PR 52916 settles the comparison the other way), and
  `spec_parser.py: attach a ^dep only when its sub-dag is complete` (merged as #52859 with
  its tests; the replay had re-added a near-duplicate test block, its comment refinement
  is folded into the split-constrain commit).
- `spec.py: test the algebra of satisfies and constrain` dissolved on 08-21: each test
  went to the commit that introduces the behavior it checks. The twelve conditional-edge
  and provider-group tests squashed into the split-constrain commit, joining its tests in
  `spec_semantics.py`, and the file it started in `spec_algebra.py` left that commit with
  them. Five duplicates of tests the extractions carried to develop were dropped: the
  three target tests (develop's incomparable-bounds version is a superset and has the
  #52919 `ampere1:,neoverse_v3ae:` expectation), the parallel-edge copy test, and the
  self-meet idempotency test. The fourteen law and gap tests that remain all pass on
  plain develop; they are `spec_algebra.py: check each law on a hand-picked case`, the
  first commit above the PR head.
- The tips before the 08-31 rebase are kept at `backup-property-based-tests-20260831` and
  `backup-spec-algebra-fuzz-20260831`. The tips of 08-21 are at
  `backup-property-based-tests-20260821` and `property-rebase-backup-20260821`.
- `hs/test/spec-algebra-fuzz` (the PR head) points at the last code commit, the
  split-constrain commit, now the third commit above develop: `spec_algebra.py`, the
  harness scripts under `lib/spack/spack/test/` and these docs stay out of the PR.
- `formal/spec-semantics.tex` cites source line numbers, which the 08-20 rebase shifted by
  about seventy lines in `spec.py` and invalidated outright for the target code. They are
  left as they are. Its empty-set audit passage now records one consequence, the
  ∅-denoting concrete prefix states: the disjoint round-trip is gone with #52928 on
  develop, and the intersects asymmetry it listed does not reproduce on the branch (#52852
  applied the prefix rule to intersects before the audit) and is dropped.

## Rebase onto develop, 2026-09-17

- Both branches are rebased onto develop at `f30783afb4`. The split-constrain commit
  conflicted in `spec.py` on three upstream commits: #52963 (propagated variants as a
  separate attribute), #53010 (`ImmutableSpec` -> `CachedSpec`) and #52938 (mutability
  checks removed).
- #52963 closed the variant propagation gap. `_disjoint_node_attributes_reason` calls
  `_disjoint_variants_reason`, which reads both maps, instead of the inline loop over
  `variants` the commit was written against, and `_merge_variants` merges
  `propagated_variants` alongside `variants`. `Spec("pkg-a").satisfies("pkg-a++foo")` is
  now False, so the gap leaves `GAPS`, the corpus stops holding out propagating specs,
  and the hand-picked case records the law.
- `formal/spec-semantics.tex` is out of date on this point: its §propagation section, the
  abstract, the introduction and the dimension table still state that propagated variants
  follow non-contradiction and break transitivity. The Lean development carries the same
  claim. Neither is updated here.

See `bug-ledger.md` for the bug counts per PR.
