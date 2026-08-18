# Distinct spec bugs fixed, 2026-07-17 to 2026-08-20

Scope: PRs by haampie from the last month that fix bugs in spec algebra (`satisfies`,
`intersects`, `constrain`, comparison), spec parsing, or (de)serialization (`to_dict`/
`from_dict` and the str round-trip). Sources: PR descriptions, regression tests, and the two
bug lists in #52801. A bug is one independently reproducible wrong verdict, wrong denoted set,
or unwarranted raise; a non-canonical result counts only where it leaks into hashing or
round-trips. The two semantic changes of #52801 (duplicate `^` clauses stay parallel edges,
stateless comparison with frozen provided virtuals) are not counted as bugs.

## Counter

| Bucket | Bugs | PRs |
|---|---|---|
| Merged to develop | **47** | 22 |
| Left only in the umbrella #52801 | **4** | 1 |
| **Total** | **51** | 23 |

#52801's own arithmetic said 19 + 21 = 40 when its description was written. The recount is
higher because the extraction PRs surfaced more distinct bugs as they were reviewed and
re-derived against develop: nos. 23-25 during #52876/#52877, and nine more in the parallel-edge
work (#52893, nos. 27-35, of which nos. 34-35 appear only in its final description) plus the
edge-query filter #52910 (no. 41). The star constrain raise (no. 17) is counted here where the
umbrella folded it into "star (2 bugs)".

## Merged (47 bugs)

**#52788 — round-trip abstract specs through to_dict** (merged 08-07)
1. `to_dict` drops the abstract hash of an abstract spec.
2. `to_dict` drops an edge's `when` condition.
3. `to_dict` drops an edge's propagation policy (`%%`).
4. `to_dict` records flag propagation per flag type, so `cflags=-g cflags==-O2` reads back
   with both flags propagating.

**#52844 — parallel edges round-trip to_dict, constrain commutative** (merged 08-10)
5. `from_dict` folds two parallel edges to one package name into one edge.
6. Parallel edges have no canonical order, so the dag hash of a meet depends on which operand
   came first.
7. `DependencySpec._cmp_iter` skips the child spec, so two parallel edges differing only in
   the child compare equal.

**#52846 — keep commas in a when= edge attribute** (merged 08-07)
8. The parser stops the `when=` spec at the first comma: `^[when='@1,2']` becomes
   `^[when='@1']`.

**#52847 — make PropagationPolicy orderable** (merged 08-07)
9. Sorting parallel edges that differ in propagation policy raises `TypeError`, since plain
   `Enum` has no order.

**#52848 — print a blank before the abstract hash** (merged 08-10)
10. `str()` glues the abstract hash to the preceding token: `key=value /hash` prints as
    `key=value/hash` and re-parses with no hash at all.

**#52849 — print compiler flags in the order they are stored** (merged 08-10)
11. Flags print as non-propagating then propagating instead of storage order, so the str
    round-trip flips `cflags==-O2 cflags=-g`.

**#52851 — do not share arch and flags with the constraint** (merged 08-11)
12. `constrain` aliases the rhs compiler-flag list, so later constrains on the lhs mutate the
    rhs.
13. `constrain` aliases the rhs `ArchSpec`, so later constrains rewrite the rhs target.

**#52852 — apply the patch prefix rule to intersects too** (merged 08-11)
14. A patch sha that satisfies a prefix of itself does not intersect it. The same rule now
    applies in the constrain merge, which kept both shas as a two-element value.

**#52853 — a star means any value in intersects too** (merged 08-11)
15. `intersects` compares `key=*` as a literal string while `satisfies` reads it as any
    value, on either side.
16. A star on one arch attribute makes `satisfies` return early, excusing a mismatch on the
    others.
17. `constrain` compares the star literally too, so `os=*` constrained by a named value
    raises instead of taking the name.

**#52858 — keep flag propagation in constrain** (merged 08-11)
18. `FlagMap.constrain` demotes a propagating flag to non-propagating when the lhs has the
    plain one.

**#52859 — attach a ^dep only when its sub-dag is complete** (merged 08-10)
19. After a duplicate `^dep` the parser keeps targeting the discarded node, so a trailing `%`
    edge lands outside the DAG and is lost.

**#52860 — a transitive edge does not satisfy a direct edge** (merged 08-11)
20. The `direct` flag does not come back when a concrete spec is marked abstract again, so
    de-concretized specs stop satisfying `%` constraints.
21. At depth 1 the satisfies search takes any edge for a `%` constraint, so `^pkg-b`
    satisfies `%pkg-b`.

**#52861 — an anonymous spec is not inside a named one** (merged 08-10)
22. An anonymous spec satisfies any named spec, so satisfies is not transitive:
    `pkg-a ⊆ "" ⊆ pkg-b`.

**#52876 — make satisfies exhaustive** (merged 08-17)
23. `satisfies` gives up on the first node of a package name instead of backtracking across
    parallel same-name nodes.
24. At depth ≥ 2 `satisfies` traverses edges whose deptypes put the child outside the
    link/run-plus-direct reach of `^`.

**#52877 — fix shared mutable state of CompilerFlag** (merged 08-11)
25. `CompilerFlag` is a mutable str subclass and `constrain` copied the list but not the
    instances, so flags share propagation state across specs.

**#52894 — a namespace is a constraint to satisfies** (merged 08-13)
26. A spec without a namespace satisfies one that sets it, although it is less constrained.

**#52893 — duplicate ^dep clauses are parallel edges** (merged 08-18; includes the fix of the
closed #52908, whose lawful shape reduced to letting anonymous candidates through the
redundancy scans)
27. Two `^` clauses on one package name are reported disjoint or unsatisfiable although a DAG
    with two nodes satisfies both.
28. The parser merges duplicate `^dep` clauses into one node and rejects them when their
    constraints or dependency types conflict.
29. The meet of build‖link parallel edges with one of them invents a `build,link` edge that
    neither `copy()` nor the parser accepts back.
30. Constraining with an equal spec rewrites parallel deptype edges and claims a change, so
    x ∧ x ≠ x.
31. A conditional edge implied by an unconditional one to the same name is kept beside it
    instead of merging away.
32. Two conflicting `%[when=...]` deps under one unforced condition are reported disjoint,
    although any spec falsifying the condition satisfies both.
33. `constrain` raises on an anonymous dependency on the rhs only, so the meet depends on
    operand order and a spec with such an edge cannot constrain itself.
34. A `constrain` that assigns a name to an anonymous spec leaves the dependent edges of its
    children keyed by the anonymous name, so keyed lookups on the edge maps miss them.
35. A `constrain` with a concrete rhs copies it over the node with `_dup`, which prunes
    in-edges: right for a detached copy, wrong for a node still filed in its dependents'
    edge maps.

**#52905 — constraining an edge merges the propagation policy** (merged 08-17)
36. `DependencySpec._constrain` drops the rhs propagation policy, so a merge silently loses
    `%%`.
37. `%pkg-b` and `%%pkg-b` compare equal.

**#52906 — merge the abstract hash after the checks, report it as a change** (merged 08-18)
38. The changed flag misses a hash extension: `pkg-a` constrained by `pkg-a/abcdef` returns
    `False`.
39. A constraint rejected on name or version leaves its abstract hash behind on the lhs.

**#52907 — round-trip str of abstract spec with namespace** (merged 08-18)
40. The default format drops the namespace of an abstract spec, so the printed spec reads
    back as a strictly wider one.

**#52910 — edge queries distinguish name=None from name=""** (merged 08-18)
41. The name filter of the edge queries tests truthiness, so `""` returns every edge and
    there is no way to select edges to anonymous specs.

**#52856 — ArchSpec: fix satisfies, intersects, constrain** (merged 08-20)
42. `constrain` empties the target when only one side has one.
43. Constraining a target range by `*` replaces the range with the star.
44. Target `satisfies` is overlap instead of containment: `x86_64:` satisfies `haswell`.
45. `constrain` rewrites an already-contained target range and reports a change:
    `:icelake` constrained by `x86_64:` claims `True` and stores `x86_64:icelake`.
46. Incomparable target bounds are dropped instead of meeting as a union of ranges, so
    `cascadelake:` and `cannonlake:` read as disjoint.
47. Target ranges are not canonical: `:icelake` and `x86_64:icelake` denote one set but hash
    and serialize differently.
    (The PR also fixes the target slice of the constrain-atomicity bug, counted once as
    no. 48.)

## Left only in the umbrella #52801 (4 bugs)

Re-verified on 2026-08-17 on develop-shaped code, and no. 49 again on develop on 2026-08-20,
once every extraction PR had merged: still broken there.

48. `constrain` is not atomic: a failure in the dependency phase leaves the node dimensions
    already merged.
49. Node comparison on a virtual-name match drops the other dimensions:
    `^[virtuals=mpi] mpich+debug` satisfies `^mpi~debug`.
50. The merge copies in an edge whose `when` condition already cannot hold on the lhs.
51. A forced `when` condition with conflicting deps denotes the empty set but still
    intersects everything.

Bookkeeping against #52801's 19-bug list: 10 are covered by the merged extraction PRs' own
descriptions, 4 more fell to #52893 as verified side effects (nos. 29-32 above), one
(satisfies backtracking, no. 23) merged via #52876, and these 4 remain.

## Out of scope

Fixes from the same month that are spec-adjacent but not algebra/parsing/serialization:
package hash resolved by name instead of fullname (#52777), slots and GC-cycle fixes
(#52775), the cleared package hash of auto-spliced specs (#52862, open). Cleanups and perf:
#52778, #52782, #52785, #52835.
