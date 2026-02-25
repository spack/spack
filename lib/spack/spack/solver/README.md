# Spack Solver

This directory contains Spack's ASP-based concretizer. It uses the
[clingo](https://potassco.org/clingo/) solver to resolve package dependencies
and produce fully-concrete specs.

## Files

| File | Purpose |
|------|---------|
| `asp.py` | Main Python driver: generates facts, runs clingo, reconstructs specs |
| `core.py` | Low-level clingo helpers (`intermediate_repr`, `extract_args`, `NodeArgument`) |
| `concretize.lp` | Core ASP logic: node creation, versioning, variants, platform/OS/target, flags, conditions |
| `display.lp` | `#show` directives controlling which atoms appear in the answer set |
| `heuristic.lp` | Domain heuristics to guide search and speed up solving |
| `error_messages.lp` | Human-readable error message templates |
| `direct_dependency.lp` | Rules for direct-dependency constraints |
| `libc_compatibility.lp` | Linux libc compatibility rules |
| `os_compatibility.lp` | OS compatibility rules |
| `splices.lp` | ABI-splice rules: when a dependency of a reused spec can be swapped |
| `when_possible.lp` | "Reuse when possible" strategy rules |
| `requirements.py` | Translates `spack.yaml` `require:` directives into ASP facts |
| `reuse.py` | Identifies already-installed specs that can be reused |
| `runtimes.py` | Handles runtime dependencies (compilers, libc) |
| `versions.py` | Version weight and ordering fact generation |
| `input_analysis.py` | Analyses input specs to bound the set of packages considered |
| `splicing.py` | Python-side splice application after the solve |

---

## `attr` facts and spec reconstruction

### Overview

The concretizer expresses a concrete spec as a collection of `attr/N` atoms in
the answer set.  After solving, the Python side reads those atoms and calls
methods on `SpecBuilder` (`asp.py`) to reassemble `spack.spec.Spec` objects.
The pipeline is:

```
clingo answer set
      │
      │  display.lp: #show attr/2..6
      ▼
list of attr(Name, Arg1, ..., ArgN) atoms
      │
      │  extract_args(best_model, "attr")   [core.py]
      │  → [(Name, (Arg1, ..., ArgN)), ...]
      ▼
SpecBuilder.build_specs(function_tuples)   [asp.py]
      │
      │  getattr(self, Name)(*args)
      ▼
dict of NodeArgument → spack.spec.Spec
```

`extract_args` (`core.py:270`) filters the raw clingo symbols to those named
`"attr"` and converts each argument through `intermediate_repr`:

- A `node(ID, Package)` function becomes a `NodeArgument(id, pkg)` named tuple.
- A `node_flag(type, flag, group, source)` function becomes a `NodeFlag` named
  tuple.
- Everything else becomes a plain Python string.

`build_specs` then sorts the tuples by a priority key before dispatching:

| Priority | Attr name | Reason |
|----------|-----------|--------|
| −5 | `hash` | Inject full concrete specs from the reuse cache first |
| −4 | `node` | Create empty `Spec` objects before any attributes are set |
|  0 | *(all others)* | Set attributes on already-created nodes |
| +2 | `virtual_on_edge` | Update edge `virtuals` after all dependency edges exist |

After all atoms are dispatched, `build_specs` runs several post-processing
steps in order:

1. `reorder_flags()` — sort compiler flags topologically across the DAG.
2. `_inject_patches_variant()` — attach the `patches` pseudo-variant to roots.
3. `_ensure_external_path_if_external()` — resolve paths for external-module specs.
4. `_develop_specs_from_env()` — attach `dev_path` from the active environment.
5. `_specs_with_commits()` — resolve git commit SHAs into the `commit` variant.
6. `_finalize_concretization()` — mark specs concrete and compute DAG hashes.
7. Hash unification — deduplicate compiler/runtime nodes that appear in multiple
   subtrees.
8. Splice resolution — apply `splice_at_hash` operations collected during dispatch.

---

### `attr` facts that enter reconstruction

These atoms appear in the answer set and have a matching method on `SpecBuilder`.

| Fact | Arity | `SpecBuilder` method | Effect on `Spec` |
|------|:-----:|----------------------|-----------------|
| `attr("node", node(ID, Pkg))` | 2 | `node()` | Creates a new empty `Spec(Pkg)` in `_specs`, keyed by `NodeArgument(ID, Pkg)`. Every other attr for this package requires `"node"` to be processed first. |
| `attr("hash", node(ID, Pkg), Hash)` | 3 | `hash()` | Reuse path: looks up a pre-built concrete spec in `_hash_lookup` (populated by `reuse.py`) and stores it as-is. All subsequent attrs for that node are skipped, except `splice_at_hash`. |
| `attr("namespace", node(ID, Pkg), NS)` | 3 | `namespace()` | Sets `spec.namespace` (e.g. `"builtin"`). |
| `attr("version", node(ID, Pkg), Ver)` | 3 | `version()` | Sets `spec.versions` to the single chosen version. Exactly one version per node is required; violations produce a solver error. |
| `attr("node_platform", node(ID, Pkg), P)` | 3 | `node_platform()` | Sets `spec.architecture.platform`. |
| `attr("node_os", node(ID, Pkg), OS)` | 3 | `node_os()` | Sets `spec.architecture.os`. |
| `attr("node_target", node(ID, Pkg), T)` | 3 | `node_target()` | Sets `spec.architecture.target`. |
| `attr("node_flag", node(ID, Pkg), node_flag(Type, Flag, Group, Src))` | 3 | `node_flag()` | Appends one compiler flag to `spec.compiler_flags`. The structured `node_flag/4` term carries the flag type (e.g. `"cflags"`), the value, the flag group, and the source (e.g. `"compiler"`, `"literal"`, or a package name). Multiple atoms accumulate all flags; `reorder_flags()` sorts them into canonical order afterwards. |
| `attr("variant_selected", node(ID, Pkg), Name, Value, Type, VID)` | 6 | `variant_selected()` | Adds a variant value to the spec. Derived from `variant_value` plus variant metadata (`variant_type`, `node_has_variant`), providing the Python side with the type information (`"bool"`, `"single"`, `"multi"`) needed to instantiate the right `VariantValue` subclass. For multi-valued variants, one atom is emitted per value; the second and subsequent calls append to the existing variant. |
| `attr("depends_on", Parent, Child, Type)` | 4 | `depends_on()` | Adds a directed dependency edge with the given type (`"link"`, `"run"`, `"build"`, or `"test"`). The edge is added with `virtuals=()` as a placeholder; `virtual_on_edge` atoms fill in the actual virtual names afterwards. |
| `attr("virtual_on_edge", Parent, Provider, Virtual)` | 4 | `virtual_on_edge()` | Annotates an existing dependency edge with the virtual interface it satisfies. Processed last (priority +2) so that the edge already exists. |
| `attr("deprecated", node(ID, Pkg), Ver)` | 3 | `deprecated()` | Emits a `tty.warn` deprecation warning. Has no effect on the `Spec` object itself. |
| `attr("splice_at_hash", Parent, SpliceNode, ChildName, ChildHash)` | 5 | `splice_at_hash()` | Records that the dependency `ChildName`/`ChildHash` inside the reused spec at `Parent` should be replaced by `SpliceNode` (an ABI-compatible alternative). Stored in `_splices` and applied in a post-processing pass via `spack.solver.splicing._resolve_collected_splices()`. The only action called on nodes that already hold a concrete spec. |

---

### `attr` facts that do NOT enter reconstruction

These atoms appear in the answer set (because `display.lp` shows all `attr/N`)
but are filtered out by `SpecBuilder.ignored_attributes` before dispatch.
They are emitted to support error diagnosis, external tooling, or debugging.

The filter is a compiled regex matching the first argument of each `attr` atom:

- `^.*_set$`
- `^.*_satisfies$`
- `^.*_propagate$`
- `^closure$`
- `^compatible_libc$`
- `^dependency_holds$`
- `^package_hash$`
- `^reused_virtual_node$`
- `^root$`
- `^uses_virtual$`
- `^variant_default_value_from_cli$`
- `^variant_value$`
- `^virtual_node$`
- `^virtual_on_incoming_edges$`
- `^virtual_root$`

| Fact (pattern) | Purpose |
|----------------|---------|
| `attr("node_version_satisfies", node, Constraint)` | Witness that the chosen version satisfies `Constraint`. Used inside solver rules to check compatibility; carries no information beyond `version`. |
| `attr("node_target_satisfies", node, Constraint)` | Witness that the chosen target satisfies `Constraint`. Same role as `node_version_satisfies` for targets. |
| `attr(".*_propagate", ...)` | Records that a flag or variant value was introduced via propagation (the `==` constraint syntax). The propagated value itself already appears in the corresponding `node_flag` or `variant_value` atom. |
| `attr(".*_set", ...)` | Tracks which attributes were *explicitly constrained* rather than freely chosen. Examples: `variant_set`, `node_platform_set`, `node_os_set`, `node_target_set`, `node_flag_set`, `namespace_set`, `concrete_variant_set`, `provider_set`. |
| `attr("variant_value", node, Variant, Value)` | Raw variant value used pervasively in solver rules. `variant_selected` (which adds type and ID metadata) is the atom actually consumed for reconstruction. |
| `attr("closure", PackageNode, DepNode, "linkrun")` | Transitive link+run dependency closure of a node. Used when a package declares a `closure` condition requirement; not a direct spec attribute. |
| `attr("root", node)` | Marks the roots of the solve (specs directly requested by the user). Used to enforce unification-set constraints inside the solver. Not needed for reconstruction: `Result._compute_specs_from_answer_set()` identifies roots from the original `abstract_specs` list. |
| `attr("virtual_node", node)` | Marks a node as representing a virtual package (e.g. `mpi`, `blas`). Virtual packages do not become `Spec` objects; their provider does. |
| `attr("virtual_root", node)` | Marks a virtual package as a root of the solve. Same rationale as `virtual_node`. |
| `attr("virtual_on_incoming_edges", Provider, Virtual)` | Reverse-index counterpart of `virtual_on_edge`, recorded from the provider's perspective. Used in solver rules to detect missing virtual annotations. |
| `attr("reused_virtual_node", VirtualNode)` | Marks virtual nodes carried over from a reused concrete spec. Used by solver rules; the provider relationship is already encoded in `depends_on`/`virtual_on_edge`. |
| `attr("uses_virtual", node, Virtual)` | Records which virtual interfaces a node uses. The information is already captured by `virtual_on_edge`; this fact exists for use in solver rules. |
| `attr("compatible_libc", ...)` | Records that a node is compatible with the system libc under the rules in `libc_compatibility.lp`. Used within the solver; not a spec attribute. |
| `attr("dependency_holds", ...)` | Used by `splices.lp` to track that a dependency relationship has been preserved across a splice. Has no meaning outside the solver. |
| `attr("package_hash", ...)` | Records the hash of the `package.py` recipe for a given package version. Used to invalidate cached concretization results; not a property of a concrete spec. |
| `attr("variant_default_value_from_cli", ...)` | Records that a variant's default was overridden from the command line. Used to drive error messages; the actual value is already in `variant_value`. |
