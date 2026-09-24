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
- GPG data;
- licenses;
- managed environments;
- bootstrap data;
- repositories created or cloned without an explicit destination;
- Spack state and miscellaneous caches.

Module files are not included because Spack no longer maintains default module roots; module roots must be explicitly configured in `modules.yaml`.

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

A completely new checkout has no old installs, environments, licenses, or GPG data.

Expected behavior:

- No layout scope is generated.
- No migration state is written into the Spack prefix merely to mark initialization.
- New installs, environments, licenses, GPG data, bootstrap data, repositories, state, and caches use the new defaults under the user’s shared locations.
- Module files can be generated only after explicitly configuring module roots in `modules.yaml`.
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
- The layout scope records the old install tree path as needed.
- New installs use the new defaults unless an explicit install-tree configuration says otherwise.
- Spack does not maintain a default module root as of this PR. Module roots must be configured explicitly before generating new module files.

If the old install tree was configured explicitly at a custom location, that configuration is respected rather than treated as an old default to migrate.

## 3.2 Configuration migration and path rewriting

Migration copies resources from old to new locations, leaving old resources in place. The layout scope records old paths for resources that were not migrated: installs (never migrated), resources with custom configuration (skipped), and resources whose copy operation failed. Successfully copied resources with default configuration use the new default locations automatically (no layout entry needed).

Configuration migration must:

- preserve user-authored configuration and its scope precedence;
- rewrite paths only in generated or migration-owned configuration;
- record old paths in layout scope for resources that were not successfully copied to new defaults;
- avoid changing explicit custom paths;
- make the resulting configuration effective on the next Spack invocation.

The existence of the layout scope (or `.migration-done` marker) means that this evaluation has completed.

## 3.3 Licenses

- If `config:license_dir` uses the new default, Spack attempts to copy license entries to the shared default.
- Entries are processed in sorted (alphabetical) order for deterministic behavior across platforms.
- Entries are copied individually; old licenses remain in place.
- Migration stops at the first collision or failure; successfully copied entries before that point remain at both old and new locations.
- Migration does not use a destination lock because license files may be edited outside Spack.
- If migration is abandoned or incomplete, the old license directory is recorded in layout scope.
- If all licenses copy successfully, no layout entry is written (new location used by default).
- A custom configured license directory is left untouched.

## 3.4 Managed environments

- If `config:environments_root` is explicitly custom, Spack does not implicitly adopt or migrate environments from the old location.
- If it still uses the new default, Spack may copy old managed environments to the new shared root.
- Migration uses a lock shared with managed environment creation.
- Migration checks all destinations for conflicts upfront; if any destination already exists, no environments are copied.
- Views are excluded from the copy.
- Environments are processed in sorted (alphabetical) order.
- If a copy operation fails despite passing upfront checks and holding the lock, migration stops and leaves partial state for investigation rather than attempting cleanup.
- Old environments remain in place after copying.
- If all environments copy successfully, no layout entry is written (new location used by default).
- If migration fails or is abandoned, the old environments root is recorded in layout scope.

### Path rewriting in environment configs

After copying each environment directory, Spack rewrites paths in the environment's YAML files (`spack.yaml`, included configs) to work in the new location. This uses different rules than user config migration because environments are relocated as complete, self-contained units.

**Environment path rewriting rules:**

1. **Absolute path inside old env** → rewrite to new env location (e.g., view at `$old_env/view` becomes `$new_env/view`)
2. **Relative path pointing outside env** → make absolute to preserve the original target (e.g., `../../some/dir` becomes `/absolute/path/to/some/dir`)
3. **Relative path staying inside env** → keep relative (e.g., `./subdir` remains `./subdir`, will work in new location)
4. **Absolute path outside env** → unchanged (e.g., `/some/external/path` stays `/some/external/path`)

**Why environment rules differ from user config migration:**

User config migration (section 3.8) relocates only config files while other resources (repos, caches) may remain at the old location. Therefore, absolute paths into `~/.spack` only make sense to rewrite when they appear in `include:` sections (referencing other config files being moved).

Environment migration relocates the entire environment directory as a unit. Any path pointing inside the environment should be rewritten to the new location, regardless of context. Relative paths escaping the environment are made absolute to preserve their original targets, since the environment's position in the filesystem hierarchy changes.

## 3.5 GPG data

Spack migrates both the GPG keyring (`config:gpg_path`) and the GPG keys directory (`config:gpg_keys_path`) together. Both must succeed for migration to be considered successful.

- `SPACK_GNUPGHOME` is authoritative when set.
- If it points to the old GPG keyring location, both paths are recorded in layout scope at their old locations.
- If it points elsewhere, Spack does not add an automatic override.
- If it is unset and both configured GPG paths use the new defaults, Spack may copy both directories to new locations.
- Destinations must not already exist; keyrings are never merged.
- Migration copies both directories to private sibling staging directories (keyring with mode `0700`), then atomically renames them into place.
- Failed staging is removed.
- Old GPG directories remain in place after successful copying.
- If both directories copy successfully, no layout entry is written (new locations used by default).
- If either copy fails, both the old GPG keyring path and old GPG keys path are recorded in layout scope.
- Custom configured GPG paths are left untouched.

## 3.6 Partial failure and repeated commands

Migration preserves old resources in place. If a migration is incomplete or unsafe, generated configuration (layout scope) points to the old locations so the resources remain usable.

After a migration attempt completes (marked by `.migration-done`):

- subsequent commands do not repeat migration evaluation;
- resources that successfully copied use new locations (no layout entry);
- resources that failed to copy or were intentionally retained continue using old paths (recorded in layout scope);
- the layout scope remains authoritative.

## 3.7 Undoing auto-migration

`spack migrate undo` updates the layout scope to point all resources back to their old locations.

- Old resources are already at their old locations (migration copied them, leaving originals in place).
- No file restoration is needed.
- Undo simply writes layout scope entries pointing to all old locations.
- New locations may be left in place for other Spack instances to use, or manually removed if desired.

## 3.8 Home directory migration

User configuration and package repositories in `~/.spack` are automatically migrated to the new XDG locations (`~/.config/spack` and `~/.local/state/spack/package_repos`) independently of `$spack` prefix migration.

This migration runs when:

- No isolate scope is active (`$spack/etc/spack/isolate/include.yaml` does not exist).
- The user scope in loaded configuration points to `~/.config/spack`.
- `~/.spack` exists and contains configuration files.
- `~/.config/spack` either does not exist or is empty.

For package repositories:

- The old location is `~/.spack/cache/repos` (now `~/.spack/package_repos` in recent Spack).
- The new location is `~/.local/state/spack/package_repos`.
- Migration only occurs if the new location is empty and Spack is using the default state location.

This allows users who:

- Pull a new Spack version into an existing checkout with old resources under `$spack`;
- Clone a fresh Spack instance with no old `$spack` resources; or
- Use a shared, read-only Spack prefix

to have their personal `~/.spack` configuration automatically migrated on first use.

The home directory migration runs on every Spack invocation (when conditions are met) and is independent of whether `$spack` prefix resources exist or whether the layout scope has been created. Configuration is reloaded after home directory migration completes to pick up the migrated user configuration.

`~/.spack` is retained after migration because older Spack instances may still reference it.

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

- New installs, environments, licenses, GPG data, bootstrap data, repositories, state, and caches are created under `x` by default.
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

Auto-migration is designed to be safe when multiple Spack instances run concurrently, whether on the same machine or accessing shared filesystems. Two distinct concurrency scenarios are handled:

1. **Multiple processes with the same `$spack` prefix**: For example, two users running commands against a shared Spack installation, or one user running multiple `spack` commands in parallel. These processes coordinate through a shared migration lock.

2. **Multiple different `$spack` prefixes each performing migration**: For example, a user with multiple Spack checkouts starting commands in each one simultaneously. Each prefix has its own independent migration lock, so they migrate in parallel without interfering.

## 6.1 Spack prefix migrations

Auto-migration of `$spack` prefix resources uses a per-prefix migration lock (`$spack/.migration-lock`) to coordinate concurrent Spack instances using that prefix:

- **Migration lock acquisition**: Each Spack process attempts to acquire the lock before migration. If the lock cannot be acquired (no write permissions or timeout), that process skips migration and proceeds with existing configuration.
  
- **Double-check after lock**: After acquiring the lock, the process re-checks `should_auto_migrate()` because another process may have completed migration while this one waited for the lock.

- **Migration completion marker**: The process that performs migration writes `$spack/.migration-done` as the final step. This marker is checked at config module load time and stored globally, allowing other processes to detect completed migration without re-evaluation.

- **Config reload decision**: A process reloads config if:
  - It performed migration itself (copied resources, wrote layout scope), OR
  - The marker didn't exist when config loaded but exists now (another process migrated while this one waited for the lock)
  
  This ensures all processes see the new layout scope configuration, whether they performed the migration or arrived while/after another process did.

- **Individual resource safety**:
  - Old resources remain in their original locations after migration. Migration copies resources to new locations without removing the originals.
  - Installs are never relocated.
  - GPG migration uses private atomic staging with atomic rename for the copy operation.
  - Environment migration locks the environments root (shared with `spack env create`), pre-checks all destinations, then copies.
  - License migration creates the destination directory and copies files individually; it reports partial success and stops on first conflict rather than claiming exclusive locking (since license files may be edited outside Spack).
  - Failed staging leaves no partially exposed destination at the new location.
  - Generated configuration (layout scope) points to old locations for resources that were not migrated: installs (never migrated), resources with custom configuration (skipped), and resources whose copy operation failed. Successfully copied resources use new default locations (no layout entry).

- **Layout scope**: The layout scope directory (`$spack/etc/spack/layout/`) inherits permissions from its parent directory (`$spack/etc/spack/`), ensuring proper access in shared installations where multiple users need to read and write the layout scope.

## 6.2 Home directory migrations

User config and package repositories are migrated from `~/.spack` independently of `$spack` prefix resources:

- **User config** (`~/.spack` → `~/.config/spack`):
  - Uses a sibling lock (`.spack-user-config-migration.lock` in `~/.config/`) to serialize concurrent migrations.
  - Stages all config files to `.spack-config-staging` before atomically renaming to `spack`.
  - Another Spack instance will never see partial config files; the directory appears atomically.

- **Package repositories** (`~/.spack/package_repos` → `~/.local/state/spack/package_repos`):
  - Uses a sibling lock (`.spack-package-repos-migration-lock`) to serialize concurrent migrations.
  - Stages the entire tree to `.package-repos-migration` before atomically renaming.
  - Another Spack instance will never see a partial repository tree.

Both home directory migrations can run safely alongside any number of other Spack instances, whether they're using the old locations, the new locations, or attempting concurrent migrations.

# 7. Auto-Migration Algorithm Details

**NOTE: This section was human-generated. Take special care to ask before modifying it.**

This section provides implementation-level details of the locking algorithm and auto-migration logic.

## 7.1 Algorithm steps

0. If no old resources are present, then all auto-migration logic is skipped
1. Else, Spack holds a global `$spack/.migration-lock` before doing auto-migration
2. Destinations for individual components are locked while migrating those components (e.g. envs)
3. Spack copies old resources to where new defaults expect. Even if the copy is successful, the old resources are kept in place.
4. Layout scope is updated to point at old locations for: installs (never migrated), resources with custom configuration (skipped), or resources whose copy operation fails (e.g. gpg keys already exist at destination)
5. Migration writes a `$spack/.migration-done` file
6. The config.py module checks for `$spack/.migration-done` when it loads
7. `spack isolate` writes `$spack/.migration-done` for Spack instances with old resources

## 7.2 Rationale and invariants

### Checking for old resources and leaving them in place

There are two scenarios where we know migration is complete:
- `$spack/.migration-done` exists
- There are no old spack resources (in which case there was never a migration, because right now, migration means copying those resources into new destinations and pointing config to them)

### Locking both destinations and spack prefix

- **Destination locks are required** to coordinate between different spack prefixes simultaneously migrating into `$HOME`. GPG and environments acquire these locks.

- **The global `$spack/.migration-lock` is semi-redundant** given the combination of (a) fault-tolerance mechanisms (hash-based markers that distinguish "our prior migration" from "another instance's migration") and (b) destination locking. Two processes from the same spack prefix could safely race through migration - they'd serialize at each destination lock, and the second would find markers indicating that resource was already migrated.

- **However, the global lock is kept for practical benefits:**
  - **Reduces contention**: Only one process performs migration work; others wait and see `.migration-done` marker
  - **More efficient**: No wasted work from multiple processes all attempting the same migrations
  - **Simpler reasoning**: One process handles the entire migration atomically
  - **Covers licenses**: License migration currently has no destination lock (relies on hash comparison), so the global lock prevents races there

### Fault tolerance for interrupted migrations

If a migration process succeeds in copying a resource but crashes before writing `$spack/.migration-done`, the next process needs to distinguish "our prior successful copy" from "another spack instance's copy." This is handled per-resource-type:

- **GPG keys**: A marker file `.migration-<hash>` (where hash identifies the spack prefix) is added to the staging directory and moved atomically with the GPG data. If the destination exists with our marker, it's our prior copy (success). If it exists without our marker, it's a collision (failure).

- **Environments**: Each environment directory gets a `.migration-<hash>` marker after copying. If an environment with the same name exists at the destination with our marker, it's our prior copy (skip it). Without our marker, it's a collision (stop migration).

- **Licenses**: File content hashes are compared. If a license file exists at the destination with matching hash, it's either our prior copy or an identical file (both fine, continue). If the hash differs, it's a collision (stop migration).

### The migration-done marker

- If that file already exists before it loads any config, then config doesn't need to be reloaded
- Otherwise, spack may have been doing a migration while the config was loading
- We want to load config before making auto-migration decisions, because (a) if we are running `spack isolate`, then we don't want to auto-migrate (and config aliases determine whether we are doing that) and (b) if config sets `config:environments_root` to something non-default, we also don't want to write it
