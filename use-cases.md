# Shared Spack Migration and Isolation Use Cases

This document describes the intended high-level behavior for shared Spack migration and isolation. It is derived from the branch implementation, the existing migration summary, and the design discussion for `features/shared-spack-7`.

## Terminology

- **Old resources** are data created by an older Spack layout under the Spack prefix, including installs, modules, environments, licenses, and GPG keys.
- **Layout scope** is the generated `$spack/etc/spack/layout/` scope. Its existence means that old-resource evaluation or migration has completed for that Spack instance.
- **Isolate scope** is `$spack/etc/spack/isolate/`. It redirects newly created user, bootstrap, repository, data, state, and cache content to the isolation target.
- **Normal startup** may relocate portable resources when the configured destination is the new default and the operation is safe.
- **Isolation** never relocates old resources. It records old-resource paths and directs only new data to the isolation target.

## 1. Existing Spack with Installs

### 1.1 Existing installs at the old default

A user pulls this change into a Spack instance that previously installed packages into `$spack/opt/spack`.

Expected behavior:

- Existing installs are never moved, copied, or deleted.
- A normal startup records `$spack/opt/spack` as the install tree in the layout scope.
- Modules associated with that install tree remain at their old locations and are recorded as needed.
- New resources use the new shared defaults where no old-resource override is required.
- A later command sees the layout scope and does not re-evaluate auto-migration.

### 1.2 Existing installs at a custom location

A user previously configured `config:install_tree:root` to a custom path and has installed packages there.

Expected behavior:

- The custom install tree is respected.
- Spack does not infer that it should move or replace the user’s configured install tree.
- Existing installs remain untouched.
- Auto-migration of unrelated portable resources may still occur when their own configured paths use the new defaults.

## 2. Existing Spack with Other Old Resources

A normal startup finds old resources under the Spack prefix.

### Licenses

- If `config:license_dir` is the new default, Spack attempts to copy license entries to the shared default.
- Licenses are copied one at a time; they are not removed from the old location.
- Spack does not lock the license destination because Spack does not normally create license files and cannot exclude manual user edits.
- If an entry collides or copying fails, successfully copied entries remain in the shared destination.
- The operation warns which entries were copied, explains that migration is being abandoned for licenses, and keeps the old license directory configured for this Spack instance.
- If the user configured a custom license directory, Spack leaves it untouched and does not add an automatic override merely because an old license directory exists.

### Environments

- If the user explicitly configured `config:environments_root` to any custom path, Spack respects that configuration and does not relocate environments found in the old Spack location. Those old environments are treated as potentially abandoned rather than implicitly adopted.
- Only when `config:environments_root` is the new default does Spack attempt to copy old managed environments to the shared default.
- Environment migration uses a lock in the environments root shared with managed environment creation.
- Views are excluded because they can contain generated or linked content that should not be copied as part of environment relocation.
- Environments are copied individually.
- If migration fails after creating destination environments, Spack removes only environments created by that migration attempt while holding the lock. Pre-existing destination environments are never removed.
- If migration is abandoned, the old environments root remains configured.
- If the user configured a custom environments root, Spack respects it and does not auto-migrate from the old location. The old environments are not automatically added to the configured root or copied there.

### GPG keys

- If `SPACK_GNUPGHOME` is set, it is authoritative and Spack does not auto-relocate keys.
- If it explicitly points to the old GPG location, that old path is recorded in layout.
- If it points elsewhere, Spack does not add a layout override.
- If it is unset and the configured GPG path is the new default, Spack may migrate the old keyring.
- The final GPG destination must not already exist. Keyrings are databases and must never be merged.
- Spack copies the complete old keyring into a sibling staging directory with `0700` permissions, then atomically renames the staging directory into the final destination.
- Failed staging is removed; the source is never chmodded or modified.
- If migration cannot complete, the old GPG path is recorded in layout.
- If the configured GPG path is custom, Spack leaves it untouched and writes no automatic override.

## 3. Fresh Spack Checkout

A completely new Spack checkout has no old installs, modules, environments, licenses, or GPG keys.

Expected behavior:

- No layout scope is generated.
- No auto-migration is performed.
- New installs, modules, environments, licenses, GPG data, bootstrap data, state, and cache use the new shared XDG-style defaults under `$HOME`.
- Nothing is written into the Spack prefix merely to establish migration state.

## 4. Fresh Checkout Followed by Isolation

A user runs:

```console
spack isolate --path x
```

before creating resources.

Expected behavior:

- The isolate scope redirects new user/config data and bootstrap/repository data to the isolation target.
- `config:locations:data`, `state`, and `cache` point to `x`.
- New installs, modules, environments, licenses, and GPG data are therefore created under `x` by default.
- No layout scope is needed when no old resources exist.
- Isolation does not copy shared defaults or create pointers to nonexistent old resources.

For `spack isolate --self`, the isolation target is the Spack isolate directory and user additions use its `user-redirect` subdirectory.

## 5. Isolation of an Existing Spack

A user runs `spack isolate --path x` on an instance that already has old resources.

Expected behavior:

- Isolation never migrates, copies, or moves old installs, modules, environments, licenses, or GPG keys.
- Old installs and modules remain at their original paths.
- Existing old environments, licenses, and GPG keys are explicitly pointed to from the generated layout configuration.
- New data, state, cache, bootstrap data, and repositories are directed to `x`.
- If the target did not previously contain `config.yaml`, generated isolation configuration is written to `x/config.yaml`.
- If the target already contained `config.yaml`, it is preserved; generated old-resource overrides are written to the layout scope.
- If no old resource exists for a category, no override is emitted for that category. The isolation location defaults handle future data.
- The layout scope becomes the marker that resource evaluation has completed.

## 6. Pulling After a Previous Isolation

A Spack instance was isolated in the past. The user then updates the checkout and may restore the tracked `etc/spack/include.yaml` with `git checkout etc/spack/include.yaml` to undo older SCM-monitored isolation changes. The user immediately runs `spack isolate` again.

Expected behavior:

- The new isolation command establishes the current isolate scope without requiring tracked-file modifications.
- If the old isolation left a layout scope, the layout scope remains authoritative for old-resource paths and prevents normal auto-migration from running again.
- Re-isolation does not relocate old resources.
- With `--overwrite`, the old isolation destination/scope is replaced according to the command’s normal overwrite behavior, while unrelated files outside the destination remain untouched.
- The new target receives the new isolation location configuration.

## 7. Second and Later Spack Commands

After either:

- a normal auto-migration attempt created the layout scope; or
- `spack isolate` evaluated old resources and created the layout scope,

the next Spack command must not repeat auto-migration evaluation.

Expected behavior:

- The existence of the layout scope is the completion marker.
- Existing layout decisions are loaded and respected.
- Portable resources are not copied again.
- Failed or intentionally retained resources continue to use the explicitly recorded old paths.

## 8. Spack Prefix Is Not Writable

If Spack cannot write its configuration scopes:

- Spack cannot create a layout or isolate scope in the prefix.
- It must not attempt to write migration state there.
- Existing configuration remains in effect.
- The command should proceed using the configuration that can be read, with no claim that migration completed.

## 9. Custom Configuration and Active Environments

Migration decisions use the fully resolved configuration, including active environment and command-line configuration where applicable.

Expected behavior:

- A custom resource path is respected even if it is empty or does not yet exist.
- Spack does not treat a custom path as permission to migrate data into the new default.
- A custom path for one resource does not prevent safe migration of another resource whose path still uses the new default.
- Configuration written by an active environment takes precedence over generated layout decisions where the configuration model gives it higher priority.

## 10. Undoing Auto-Migration

A user runs:

```console
spack migrate --undo
```

(or the supported `spack migrate undo` form, depending on command-line parsing).

Expected behavior:

- The Spack instance is made to use its old resource locations again by writing redirected configuration into the layout scope.
- The undo operation discovers what was auto-migrated by inspecting `$spack/.migration-backup/`.
- Backed-up licenses and environments are restored to their old in-Spack locations, subject to conflict checks.
- GPG data that was auto-migrated is restored from its migration backup when such a backup exists; GPG restoration must not merge keyrings or overwrite an unrelated destination.
- Existing installs and modules were never relocated, so they need no restore operation; layout configuration points back to their old locations.
- The shared destination is not removed automatically because it may be used by other Spack instances.
- The migration backup is removed only after restoration and layout updates succeed.
- If restoration cannot be completed safely, the operation reports the conflict and preserves the backup so the user can resolve it and retry.

The layout scope is stored under the Spack prefix, independently of the isolate target. However, because the isolate scope uses an `include::` override, the isolate scope must explicitly include the layout scope if isolated commands are expected to consume layout settings. Isolation intentionally does not re-include site and system scopes, but it must retain the layout scope in its replacement include list. Once included, the layout scope can be updated by `spack migrate undo` as long as the Spack configuration area is writable. If isolation was performed on a writable instance with old resources, isolation creates the layout scope while recording those resources. If a fresh isolated instance had no old resources, no layout scope is needed; undo has no old-resource migration to reverse until a later normal migration creates one.

## 11. Concurrency and Partial Failure

Migration must account for multiple Spack instances sharing destinations.

- GPG migration locks the destination parent while atomically creating the final keyring directory.
- Environment migration locks the environments root, and managed environment creation uses the same lock.
- License migration does not claim to exclude manual edits; it reports partial success explicitly.
- Old source data is preserved throughout migration.
- Generated configuration points to the old source whenever a resource migration is incomplete or unsafe.
- A partially exposed GPG destination must never be left behind; failed staging is removed before migration reports failure.
