# ty Migration Log

This document records all changes made to migrate Spack from mypy to ty type checking.
`ty` version: 0.0.37

## Summary

Starting error count: **902 errors** across ~60+ files.
Final error count: **0 errors** — ty exits with code 0.
Remaining diagnostics (28): all warnings (`deprecated`, `possibly-missing-submodule`, etc.) — pre-existing, do not affect exit code.

Error breakdown:
- `unresolved-attribute`: 371
- `invalid-argument-type`: 303
- `invalid-assignment`: 63
- `unsupported-operator`: 48
- `no-matching-overload`: 24
- `call-non-callable`: 21
- `not-subscriptable`: 19
- `invalid-method-override`: 18
- `invalid-return-type`: 12
- `unresolved-import`: 11
- others: 12

## Key differences: mypy vs ty

- ty does **not** recognize mypy error codes in `# type: ignore[mypy-code]` comments.
  Lines with mypy-specific codes (e.g. `[import]`, `[union-attr]`, `[attr-defined]`) must be
  updated to use `# ty: ignore[ty-rule]` to suppress ty errors.
- ty is stricter about `None` narrowing — if a variable is typed `Optional[X]`, accessing
  attributes without a None-check raises `unresolved-attribute`.
- ty reports `warning[unused-type-ignore-comment]` for `# type: ignore` comments that suppress
  nothing — these will be cleaned up as well.

---

## Changes

### 1. pyproject.toml — Exclude docs, add unresolved import allowlist

**Rule**: `unresolved-import`
**Why**: `lib/spack/docs/conf.py` imports `sphinx.*` which is not installed in the type-check
environment. mypy's `files = ["lib/spack/spack/**/*.py"]` never included `lib/spack/docs/`.
`xdist` and `mpi4py` are optional test dependencies; `spack_repo.*` are mock packages used only
in tests and accessed via `# type: ignore[import]` in mypy.
**Changes**:
- Added `lib/spack/docs` to `[tool.ty.src] exclude`
- Added `sphinx`, `sphinx.*`, `xdist`, `mpi4py` to `[tool.ty.analysis] allowed-unresolved-imports`
- Added `spack_repo.*` to `[tool.ty.analysis] allowed-unresolved-imports`

---

### 2. lib/spack/spack/fetch_strategy.py — Type `self.stage`

**Rule**: `unresolved-attribute` (56 occurrences), `invalid-argument-type` (7 occurrences),
`no-matching-overload` (4 occurrences)
**Why**: `FetchStrategy.__init__` sets `self.stage = None` with no type annotation. ty infers the
type as `None`, so all subsequent attribute accesses on `self.stage` are flagged. The `@_needs_stage`
decorator ensures `self.stage is not None` at runtime before the decorated methods run, but ty
cannot see through this decorator. Fix: annotate `self.stage` as
`Optional[spack.stage.AbstractStage]`.
**Changes**:
- Added `TYPE_CHECKING` import and `AbstractStage` forward ref import
- Changed `self.stage = None` → `self.stage: Optional["spack.stage.AbstractStage"] = None`

---

### 3. lib/spack/spack/version/version_types.py — Add `isdevelop` to `VersionType`

**Rule**: `unresolved-attribute` (11 occurrences in `test/versions.py`)
**Why**: `isdevelop()` is defined on `StandardVersion` and `GitVersion` but not on the base
`VersionType`. The `ver()` function returns `VersionType`, so callers cannot call `.isdevelop()`.
The fix is to declare `isdevelop()` on the abstract base class with `raise NotImplementedError`,
mirroring the same pattern used for `intersection()`, `intersects()`, etc.
**Changes**:
- Added `isdevelop()` abstract method to `VersionType`

---

### 4. lib/spack/spack/config.py — Add `path` to `ConfigScope`

**Rule**: `unresolved-attribute` (7 occurrences)
**Why**: `ConfigScope` base class does not declare `path`, but both `DirectoryConfigScope` and
`SingleFileScope` define it. Code that holds a reference typed as `ConfigScope` then accesses
`.path`, which ty rejects. Fix: add `path: str` as an abstract property on `ConfigScope`.
**Changes**:
- Added `path: str` abstract property to `ConfigScope`

---

### 5. lib/spack/spack/llnl/util/tty/log.py — Type `_out`/`_err` ColorStream fields

**Rule**: `unresolved-attribute` (13 occurrences), `unsupported-operator` (3), others
**Why**: The `log_output` context manager class stores `_out`/`_err`/`_active` as `None` initially
with no annotations. ty infers them as `None`. Fix: add proper `Optional[ColorStream]` annotations.
**Changes**:
- Added `Optional[ColorStream]` annotations to `_out`, `_err`, `_active` instance variables in
  the `log_output` classes

---

### 6. lib/spack/spack/spec.py — `Spec._hash` and `Spec | None` attribute guards

**Rule**: `unresolved-attribute` (19+ occurrences)
**Why**: `Spec._hash` is a cached hash attribute not declared in class body. Also, many places
access attributes on `Optional[Spec]` without None-checks. Fix: declare `_hash` in class body;
add `assert` or guard checks where needed.
**Changes**:
- See per-line entries below

---

### 7. lib/spack/spack/util/spack_yaml.py — `syaml_str` dynamic attributes

**Rule**: `unresolved-attribute` (8 occurrences)
**Why**: `syaml_str` is a `str` subclass that has `override`, `prepend`, and `append` attributes
set dynamically. ty does not see these. Fix: declare them in the class body with
`Optional[bool]` types.
**Changes**:
- Added `override`, `prepend`, `append` to `syaml_str` class body

---

### 8. lib/spack/spack/package_base.py — `stop_before_phase`/`last_phase` on `PackageBase`

**Rule**: `unresolved-attribute` (8 occurrences)
**Why**: `stop_before_phase` and `last_phase` are set at runtime on `PackageBase` subclasses
by the installer, but are not declared in the class body. Fix: declare them as `Optional[str]`
class attributes.
**Changes**:
- Added `stop_before_phase: Optional[str]` and `last_phase: Optional[str]` to `PackageBase`

---

### 9. lib/spack/spack/graph.py — Graph color stream types

**Rule**: `unresolved-attribute` (17), `not-subscriptable` (3), `unsupported-operator` (4),
`invalid-argument-type` (7), `invalid-return-type` (1)
**Why**: `graph.py` declares class members as `None` without type annotations and then later
accesses attributes on them. Multiple patterns here.
**Changes**:
- See per-line entries below

---

### 10. Inline `# type: ignore` → `# ty: ignore` conversions

**Rule**: Various
**Why**: ty does not recognize mypy's error codes (e.g. `[union-attr]`, `[attr-defined]`,
`[arg-type]`). Lines that previously had mypy `# type: ignore[X]` comments need the code
changed to ty's equivalent, or the comment changed to a blanket `# ty: ignore`.
**Changes**:
- See per-file entries below for each converted comment

---

### Session 3 — Systematic file-by-file cleanup (0 errors remaining)

**Files fixed** (with patterns applied):

#### Source files
- `cmd/common/arguments.py`: `# ty: ignore[invalid-method-override]` on 4 `__call__` overrides
- `cmd/blame.py`: `invalid-argument-type` (pathlib.Path), `unsupported-operator` (`/` on Optional)
- `cmd/compiler.py`: `invalid-argument-type` on multiple `colify(reversed(...))` calls
- `cmd/config.py`: `invalid-argument-type` (default_modify_scope, editor), `no-matching-overload` (dirname), `unresolved-attribute` (setup_parser.add_parser)
- `cmd/edit.py`: `unresolved-attribute` on `None | Repo` paths
- `cmd/env.py`: `invalid-argument-type` (MakefileModel.from_env), `unresolved-attribute` (env.user_specs)
- `cmd/find.py`: `invalid-assignment` (datetime into dict), `invalid-argument-type` (hashes set)
- `cmd/location.py`: `unresolved-attribute` on Optional types, `no-matching-overload` (os.path.join)
- `cmd/mirror.py`: `invalid-argument-type` on `colify` and `comma_or` with generators/iterators
- `cmd/patch.py`, `cmd/stage.py`: `invalid-argument-type` (env passed to helper expecting non-None)
- `cmd/solve.py`: `invalid-argument-type` (out=IOBase, tty.msg)
- `reporters/cdash.py`: `invalid-method-override` on 3 methods, `invalid-argument-type` (Content-Length str)
- `bootstrap/core.py`: `invalid-assignment` (empty dict not assignable to QueryInfo)
- `bootstrap/environment.py`: `unresolved-reference` (_current_python_dict not in scope)
- `builder.py`: `invalid-return-type` on individual return statements
- `ci/common.py`: `invalid-argument-type` (win_quote, Request headers)
- `cray_manifest.py`: `unresolved-attribute` (_hashes_final, origin on Spec)
- `detection/common.py`: `no-matching-overload` on `filter(regex.match, ...)`
- `detection/path.py`: `invalid-argument-type` (dedupe_paths), `invalid-assignment` + `unresolved-attribute` (compiled regex list)
- `directives.py`: `call-top-callable`, `no-matching-overload` (setdefault)
- `externals.py`: `invalid-assignment` (architecture.target assignment)
- `modules/lmod.py`: `too-many-positional-arguments` (Spec), `unresolved-attribute` (unlocked_paths)
- `multimethod.py`: `unresolved-attribute` (__name__ on Self@__call__)
- `operating_systems/windows_os.py`: `no-matching-overload` (subprocess.check_output)
- `patch.py`: `unresolved-attribute` (cls.module.__file__)
- `provider_index.py`: `invalid-argument-type` (sjson.dump)
- `relocate.py`: `invalid-argument-type` (re.escape with Sized)
- `report.py`: `invalid-method-override` (succeed)
- `sandbox.py`: `unresolved-attribute` (os.O_PATH)
- `schema/__init__.py`: `invalid-return-type` (boolean expression)
- `stage.py`: `unresolved-attribute` (tempfile._get_candidate_names, mirror_layout.path)
- `subprocess_context.py`: `unresolved-attribute` (urlopen._instance)
- `tokenize.py`: `unsupported-operator` (`+=` on mixed list)
- `traverse.py`: `invalid-argument-type` (deque.append, queue.append)
- `util/cpus.py`: `unresolved-attribute` (os.sched_getaffinity)
- `util/elf.py`: `not-subscriptable` + `invalid-argument-type` (rpaths list)
- `util/gcs.py`: `unresolved-attribute` (self.bucket methods on Optional)
- `util/package_hash.py`: `invalid-assignment` (str to bytes | None)
- `util/path.py`: `unresolved-attribute` (env.path, syaml_str._start_mark)
- `util/prefix.py`: `invalid-method-override` (join returns Prefix not str)
- `util/unparse/unparser.py`: `invalid-return-type` (ast.Str.s is str|bytes|int|...)
- `variant.py`: `call-non-callable` (values(v)), `invalid-argument-type` (tuple[None])
- Various cmd/* single-error files: `cmd/__init__.py`, `cmd/checksum.py`, `cmd/commands.py`, `cmd/create.py`, `cmd/extensions.py`, `cmd/gpg.py`, `cmd/log_parse.py`, `cmd/maintainers.py`, `cmd/pkg.py`, `cmd/resource.py`, `cmd/unit_test.py`

#### Test files (all suppressed with # ty: ignore)
- `test/installer_tui.py` (51): BuildStatus.add_build, BuildInfo.__init__, unresolved-attribute
- `test/spec_syntax.py` (39): unresolved-attribute, unsupported-operator, not-subscriptable, invalid-argument-type
- `test/versions.py` (17): unsupported-operator, unresolved-attribute, invalid-assignment, invalid-argument-type
- `test/binary_distribution.py` (16): invalid-argument-type
- `test/spec_semantics.py` (12): unresolved-attribute, unsupported-operator
- `test/directives.py` (12): invalid-assignment, invalid-argument-type
- `test/cmd/checksum.py` (12): invalid-argument-type, unresolved-attribute
- `test/concretization/core.py` (11): unresolved-attribute, invalid-argument-type, invalid-assignment
- `test/new_installer.py` (10): invalid-argument-type
- `test/cmd/uninstall.py` (10): unresolved-attribute, invalid-argument-type, not-subscriptable, unsupported-operator
- `test/cmd/env.py` (10): no-matching-overload, unresolved-attribute
- `test/installer.py` (9): unresolved-import, invalid-argument-type, unresolved-attribute, call-non-callable
- Many smaller test files (1-4 errors each): all patterns suppressed inline

---
