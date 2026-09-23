# Shared Spack Configuration, Migration, and Isolation Use Cases

This document organizes the intended behavior of the shared-storage changes in this PR. The primary distinction is between configuring new locations, choosing new defaults, migrating resources created under older defaults, and isolating a Spack instance.

## Terminology

- **Generated artifacts** are resources Spack creates or manages, including installs, modules, environments, licenses, GPG data, bootstrap data, repositories, state, and caches. As of this PR, Spack does not maintain a default module root; module roots must be configured explicitly.
- **Old resources** are artifacts created by an older Spack layout under the Spack prefix, such as `$spack/opt/spack`, `$spack/var/spack/environments`, `$spack/opt/spack/gpg`, and `$spack/opt/spack/licenses`.
- **Layout scope** is `$spack/etc/spack/layout/`. Its existence records that old-resource evaluation or migration has completed for that Spack instance.
- **Isolate scope** is `$spack/etc/spack/isolate/`. It redirects newly created configuration and generated artifacts to an isolation target.
- **User-redirect scope** is the writable user configuration scope used by `spack isolate --self`.

The central safety rule is:

> Existing installs and modules are never moved, copied, or deleted. Existing portable resources are migrated only by normal startup when the migration rules below permit it. Isolation never relocates old resources.

# 1. Configuring Artifact Locations

The new `config:locations` settings provide a way to select where Spack-generated artifacts should be created. These settings are independent of automatic migration and isolation.

## 1.1 Data, state, and cache locations

The relevant settings are:

```yaml
config:
  locations:
    data: [...]
    state: [...]
    cache: [...]
```

A configuration may set these paths explicitly, for example:

```yaml
config:
  locations:
    data:
    - /shared/spack/data
    state:
    - /shared/spack/state
    cache:
    - /shared/spack/cache
```

When these settings are present, they are used as the location search paths for newly generated artifacts. In particular, configuring the data/state/cache locations is sufficient to relocate Spack-generated data without separately configuring every artifact category.

This includes, as applicable:

- install trees and associated installation state;
- modules generated for new installs;
- GPG data;
- licenses;
- managed environments;
- bootstrap data;
- repositories created or cloned without an explicit destination;
- Spack state and miscellaneous caches.

Explicit, resource-specific configuration still takes precedence. For example, an explicit `config:install_tree:root`, `config:environments_root`, `config:gpg_path`, license directory, repository destination, or bootstrap root remains authoritative rather than being replaced merely because `config:locations` is configured.

## 1.2 Location precedence

Location settings participate in normal Spack configuration scope precedence:

- user or user-redirect configuration can override layout defaults;
- layout configuration provides recorded old-resource paths and migration decisions;
- explicitly configured resource-specific paths remain user choices;
- command-line and active-environment configuration can override lower-priority generated configuration where applicable.

A location setting changes where future artifacts are created. It does not by itself move existing artifacts.

# 2. New Default Locations

A fresh Spack checkout with no old resources should use the new shared XDG-style defaults without performing migration.

## 2.1 Fresh Spack checkout

A completely new checkout has no old installs, modules, environments, licenses, or GPG data.

Expected behavior:

- No layout scope is generated.
- No migration state is written into the Spack prefix merely to mark initialization.
- New installs, modules, environments, licenses, GPG data, bootstrap data, repositories, state, and caches use the new defaults under the user’s shared locations.
- The first and later commands use those defaults consistently.

## 2.2 Existing installs at a custom location

A user may already have configured an install tree or another resource location explicitly.

Expected behavior:

- The explicit location is respected.
- Spack does not infer that it should replace or migrate that location.
- Existing artifacts remain untouched.
- Unrelated resources may still use the new defaults or undergo migration if their own configuration still points at an old default.

# 3. Automatic Migration of Old Default Artifacts

Normal Spack startup may evaluate old resources and migrate portable resources from old defaults to the new defaults. Migration is separate from choosing the new defaults and is never performed merely because a new location was configured.

The layout scope is the completion marker. Once `$spack/etc/spack/layout/` exists, later invocations must load its decisions and must not repeat automatic migration evaluation.

## 3.1 Existing installs and modules

If packages were previously installed under `$spack/opt/spack`:

- Existing installs are never moved, copied, or deleted.
- The old install tree remains authoritative for those installs.
- Modules associated with the old install tree remain at their original locations.
- The layout scope records the old install and module paths as needed.
- New installs use the new defaults unless an explicit install-tree configuration says otherwise.
- Spack does not maintain a default module root as of this PR. Module roots must be configured explicitly before generating new module files.

If the old install tree was configured explicitly at a custom location, that configuration is respected rather than treated as an old default to migrate.

## 3.2 Configuration migration and path rewriting

Migration may create or update generated configuration in the layout scope. This configuration records old paths when an old resource must remain in place and records new locations when a portable resource was successfully migrated.

Configuration migration must:

- preserve user-authored configuration and its scope precedence;
- rewrite paths only in generated or migration-owned configuration;
- retain old paths when migration is skipped, unsafe, or only partially successful;
- avoid changing explicit custom paths;
- make the resulting configuration effective on the next Spack invocation.

The existence of the layout scope means that this evaluation has completed, including cases where no portable resource needed to move.

## 3.3 Licenses

- If `config:license_dir` uses the new default, Spack attempts to copy license entries to the shared default.
- Entries are processed in sorted (alphabetical) order for deterministic behavior across platforms.
- Entries are copied individually and are not removed from the old location.
- Migration stops at the first collision or failure; successfully copied entries before that point remain.
- Migration does not use a destination lock because license files may be edited outside Spack.
- If migration is abandoned or incomplete, the old license directory remains configured in layout.
- A custom configured license directory is left untouched.

## 3.4 Managed environments

- If `config:environments_root` is explicitly custom, Spack does not implicitly adopt or migrate environments from the old location.
- If it still uses the new default, Spack may copy old managed environments to the new shared root.
- Migration uses a lock shared with managed environment creation.
- Migration checks all destinations for conflicts upfront; if any destination already exists, no environments are migrated.
- Views are excluded from the copy.
- Environments are processed in sorted (alphabetical) order.
- If a copy operation fails despite passing upfront checks and holding the lock, migration stops and leaves partial state for investigation rather than attempting cleanup.
- If migration is abandoned, the old environments root remains configured.

## 3.5 GPG data

Spack migrates both the GPG keyring (`config:gpg_path`) and the GPG keys directory (`config:gpg_keys_path`) together. Both must succeed for migration to be considered successful.

- `SPACK_GNUPGHOME` is authoritative when set.
- If it points to the old GPG keyring location, both paths are recorded in their old locations.
- If it points elsewhere, Spack does not add an automatic override.
- If it is unset and both configured GPG paths use the new defaults, Spack may migrate both directories.
- Destinations must not already exist; keyrings are never merged.
- Migration copies both directories to private sibling staging directories (keyring with mode `0700`), then atomically renames them into place.
- Failed staging is removed and sources are never modified.
- If either migration fails, both the old GPG keyring path and old GPG keys path are recorded in layout, keeping both in their original locations.
- Custom configured GPG paths are left untouched.

## 3.6 Partial failure and repeated commands

Migration preserves source data throughout. If a migration is incomplete or unsafe, generated configuration points to the old source so the resource remains usable.

After a normal migration attempt creates the layout scope:

- subsequent commands do not repeat migration evaluation;
- successful migrations are not copied again;
- failed or intentionally retained resources continue using their recorded old paths;
- the layout scope remains authoritative.

## 3.7 Undoing auto-migration

For resources that were actually migrated, `spack migrate --undo` can use migration backups to restore portable resources to their old locations, subject to conflict checks.

- Existing installs and modules need no physical restoration because they were never moved.
- Shared destinations are not removed automatically because other Spack instances may use them.
- Backups are removed only after restoration and layout updates succeed.
- Unsafe restoration preserves the backup and reports the conflict for later resolution.

# 4. Updated `spack isolate` Behavior

Isolation controls where newly generated artifacts are created for one Spack instance. It does not relocate old resources, even when old resources are present and automatic migration would otherwise be considered.

## 4.1 Fresh isolation

For a new Spack instance, a command such as:

```console
spack isolate --path x
```

needs to establish the isolation target as the default for new resources. The effective isolation configuration is therefore primarily:

```yaml
config:
  locations:
    data: [x]
    state: [x]
    cache: [x]
```

Expected behavior:

- New installs, modules, environments, licenses, GPG data, bootstrap data, repositories, state, and caches are created under `x` by default.
- The isolate scope writes the include override needed to select the isolated user scope and layout scope.
- For a fresh non-`--self` isolation, generated `config.yaml` belongs in `x`; the isolate scope need not contain generated bootstrap, repository, or configuration files.
- No layout scope is needed when no old resources exist.
- Isolation does not copy shared defaults or create references to nonexistent old resources.

For:

```console
spack isolate --self
```

`$spack/etc/spack/isolate` is both the isolate scope and the isolation target. User configuration additions go in its `user-redirect` subdirectory.

## 4.2 Isolation immediately after updating an existing Spack

A particularly important case is:

1. an older Spack instance has installs under `$spack/opt/spack` and possibly other old resources;
2. the user updates the checkout to this new logic;
3. the first command they run is `spack isolate`.

In this case:

- isolation must not move, copy, or delete old installs, modules, environments, licenses, or GPG data;
- isolation does not establish or maintain a default module root; new module roots must be configured explicitly;
- old resources remain at their original locations;
- old-resource paths are recorded in configuration alongside the new data/state/cache defaults;
- for a fresh isolation target, both isolation locations and old-resource paths are written to the target's `config.yaml`;
- for `--reuse-old` with an existing target `config.yaml`, isolation locations and old-resource paths are written to the layout scope instead to avoid overwriting the preserved configuration;
- the isolate scope's `include.yaml` includes the layout scope, making old-resource redirects available when needed;
- the resulting configuration uses the isolate scope and gives user or user-redirect configuration higher precedence than layout fallback values.

## 4.3 Reusing an old isolation target after pulling

Older isolation changed the tracked `$spack/etc/spack/include.yaml`. Before pulling the new checkout, users must resolve that modification:

- `spack isolate --undo` using the old Spack removes the old isolation, including the old self-isolation target and its contents; or
- `git checkout etc/spack/include.yaml` restores the tracked file while preserving the old target and its contents.

The second option is required when the user wants to reuse an old target with the new:

```console
spack isolate --reuse-old
```

This is especially important for old `spack isolate --self`, where `$spack/etc/spack/isolate` was both the isolate scope and target. Running the old undo command first would remove the configuration that `--reuse-old` is intended to preserve.

Expected `--reuse-old` behavior:

- old target files such as `config.yaml`, `repos.yaml`, and `bootstrap.yaml` remain byte-for-byte intact;
- the current isolate include behavior is established without restoring the old tracked-file modification;
- the defining isolate scope remains effective, so preserved old configuration continues to contribute values;
- `user-redirect` is used for new user configuration when applicable;
- layout remains available for old-resource redirects and generated location settings;
- explicit old repository destinations remain unchanged;
- new repositories without explicit destinations use the isolated location defaults.

`--reuse-old --overwrite` is rejected because preserving and replacing the same target are contradictory operations.

## 4.4 Isolation and the layout scope

The isolate include uses an override so external user, site, and system scopes are not implicitly reintroduced. The replacement include must explicitly retain the layout scope because layout contains old-resource redirects and migration decisions.

The intended effective precedence is:

1. isolated user or user-redirect scope;
2. the defining isolate scope, including preserved old target configuration when applicable;
3. layout scope;
4. built-in defaults.

The defining scope is not removed merely because it defines `include::`; inherited include scopes are replaced, but the scope containing the override remains active without recursively including its own directory.

## 4.5 Updating command completion while isolated

When developing an isolated Spack instance, command completion should be regenerated using the normal, non-isolated scope graph and without an active environment. This prevents the generated completion files from incorporating isolated or environment-specific configuration scopes.

Run:

```console
SPACK_DISABLE_ISOLATION=1 spack -E commands --update-completion
```

`SPACK_DISABLE_ISOLATION` causes the top-level include to skip the isolate scope for this invocation. `-E` tells Spack not to activate an environment. Neither setting changes the persistent isolation configuration; they only affect this command invocation.

## 4.6 Isolation undo

The current `spack isolate --undo` removes the current isolate scope. It does not restore or delete old resources. For old self-isolation data, whether the target remains available depends on whether the user performed the old undo before pulling or restored the tracked include file to preserve it.

# 5. Non-writable Prefixes and Custom Configuration

If the Spack prefix is not writable:

- Spack cannot create a layout or isolate scope there;
- it must not claim that migration completed;
- it must not write migration state into the prefix;
- existing readable configuration remains in effect;
- commands proceed using locations that can be read and configured.

Migration and isolation decisions use the fully resolved configuration, including active environments and command-line configuration where applicable. A custom path for one resource does not prevent safe default migration of an unrelated resource.

# 6. Concurrency and Safety Invariants

- Existing source data is preserved throughout all migration operations.
- Installs and modules are never relocated.
- GPG migration locks the destination parent and uses private atomic staging.
- Environment migration locks the environments root, shared with managed environment creation.
- License migration reports partial success rather than pretending to provide exclusive locking.
- Failed GPG staging leaves no partially exposed destination.
- Generated configuration points to old sources whenever migration is incomplete or unsafe.
- A layout scope prevents repeated automatic migration evaluation.
