..
   Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. meta::
   :description lang=en:
      Learn how to control where Spack generates files and reads files, and how to effectively isolate a Spack installation.

.. _where_spack_writes_data:

Controlling where Spack writes data
===================================

A fresh checkout of Spack writes nothing into the ``$spack`` prefix.
Persistent user data, state, and caches use XDG-compliant locations under the user's home directory by default, as described in :ref:`the location table <location-table>`; build stages prefer the system temporary directory, and module roots must be configured explicitly.
A Spack instance that was installed before this layout - where data lived under ``$spack/opt``, ``$spack/var``, etc. - keeps using the legacy install location but attempts to copy environments, GPG data, and licenses to the new default locations under ``$HOME``.
The original resources remain in place.

How to override
---------------

In order of priority (highest first):

1. Specific config keys for individual paths: set ``config:install_tree:root``, ``config:environments_root``, ``config:license_dir``, ``config:source_cache``, ``config:gpg_path``, or ``config:gpg_keys_path`` in any user/site/system scope.

2. Data-category config keys: set ``config:locations:{data,state,cache}`` to redirect everything that uses the corresponding substitution.
   See :ref:`locations config <locations_config>` for details.

3. Env vars for individual homes: - ``SPACK_DATA_HOME``, ``SPACK_STATE_HOME``, or ``SPACK_CACHE_HOME``.
   The default configuration allows these environment variables to influence the associated config variable.

Path substitutions
------------------

Config values can reference these in any string field:

* ``$data_home``         - ``config:locations:data``, defaults to ``~/.local/share/spack``.
* ``$state_home``        - ``config:locations:state``, defaults to ``~/.local/state/spack``.
* ``$cache_home``        - ``config:locations:cache``, defaults to ``~/.cache/spack``
* ``$user_cache_path``   - alias for ``$cache_home`` (legacy)
* ``$spack``             - the Spack instance's prefix
* ``$spack_instance_id`` - hash distinguishing individual Spack instances

Migration of ``$spack``-internal data for older instances
----------------------------------------------------------

If a user ``git pull``s into a pre-1.3 Spack instance, Spack will prompt to update where some artifacts are stored to match the new default layout.
The user must explicitly approve this migration, either interactively or by setting the ``SPACK_AUTOMIGRATE_YES`` environment variable to ``1`` or ``true`` (any other value does not approve).
``spack migrate undo`` restores use of the legacy locations by updating configuration; it does not remove files copied to the new locations.
The original resources are still available because migration leaves them in place.

The check runs at the start of every Spack command except ``spack isolate``, and it is skipped for ``spack --help`` and ``spack --version``.
It runs before configuration is loaded, so the copies go to the fixed default locations (``~/.local/share/spack``, or ``SPACK_DATA_HOME``/``XDG_DATA_HOME`` if set), regardless of ``config:locations`` or any resource-specific setting.

The prompt is written to and read from the controlling terminal (``/dev/tty``), not standard input or error, so it works when Spack's output is captured, e.g. by shell integration (``spack env activate``), ``$(spack ...)``, or ``2>&1 | tee log``.
It times out after 60 seconds, and an empty answer means "no".
A process without a controlling terminal (cron, CI, ``ssh -T``, a container without ``-t``) or running in the background declines automatically.
Declining is recorded as a decision: configuration is written that keeps using the legacy locations, Spack prints how to migrate later (``spack migrate use-new-layout``), and the prompt is not shown again.

The decision is recorded in the Spack prefix: ``$spack/.migration-done`` marks that a decision was made, ``$spack/.migration-lock`` serializes concurrent commands while one of them is deciding, and ``$spack/etc/spack/layout/`` holds a configuration scope that points at any resource that remains in its legacy location (installs always; environments, GPG data and licenses only when they could not be copied).
None of these files is created unless legacy resources exist in the prefix.
If the prefix is not writable and legacy resources are present, Spack stops with an error: the instance's administrator must run the migration (or ``spack migrate undo``) once.
A command that waits more than two minutes for another process to finish deciding stops with an error rather than guessing.

If ``SPACK_GNUPGHOME`` is set, the GPG keyring and keys directory are not copied: the variable is an explicit choice of keyring, and the layout scope keeps pointing ``config:gpg_path`` and ``config:gpg_keys_path`` at the legacy locations.

How each resource is copied
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Every copy is staged next to its destination and renamed into place, so another Spack instance never sees a half-copied resource.
A resource whose legacy directory is itself a symbolic link (``$spack/etc/spack/licenses -> /site/licenses``) is migrated by re-creating the link at the new location; its content is not copied.

**GPG data.**
The keys directory (``$spack/var/spack/gpg``, public keys imported by ``spack gpg init``) is copied first, then the keyring (``$spack/opt/spack/gpg``).
Both must succeed, or both stay in the legacy locations.
A destination that already exists is never merged with: if another Spack instance already put a keyring at ``$data_home/gpg``, this instance keeps its own in ``$spack``.
GnuPG's transient files (agent sockets, ``*.lock``, ``random_seed``, keyring backups ``*~``) are not copied.

**Licenses.**
The entries of ``$spack/etc/spack/licenses`` are copied one by one, in alphabetical order, into ``$data_home/licenses``, which may already hold licenses from another instance.
An entry that already exists at the destination with the same content is accepted; symbolic links are copied as links.
At the first entry that exists with different content (a subdirectory is compared as a whole), the copy stops with a warning that names the difference, the entries copied so far are left at the destination, and the legacy directory stays configured.
Resolve the difference by hand and run ``spack migrate use-new-layout``.

**Environments.**
See :ref:`migrated-environments`.

Spack also independently (without prompting) copies user configuration from ``~/.spack`` to ``~/.config/spack`` and package repositories from ``~/.spack/package_repos`` to ``~/.local/share/spack/package_repos`` when the old locations contain data and the new destinations are available.
This home-directory migration can occur for a fresh checkout and does not create migration state in the Spack prefix, so each user of a shared Spack instance gets it the first time they run that instance.
The old files remain in place for use by older Spack instances.

.. _home-migration:

Migration of ``~/.spack``
-------------------------

**User configuration.**
Only the configuration files (``*.yaml``, ``*.yml``, and symbolic links) under ``~/.spack`` are copied to ``~/.config/spack``, keeping their relative layout (``~/.spack/linux/packages.yaml`` becomes ``~/.config/spack/linux/packages.yaml``).
A directory that holds an environment (``spack.yaml`` or ``spack.lock``) or a package repository (``repo.yaml``) is data rather than configuration and is not descended into.
A file that cannot be parsed or read is skipped with a warning.
Everything else in ``~/.spack`` is either regenerable (caches, the bootstrap store, package repository clones) or data that the configuration refers to by path, and keeps working where it is.

Two kinds of values are rewritten in the copies, so that the configuration means the same thing in its new location:

* An absolute path that spells out the Spack 1.2 default for its own setting (``bootstrap:root: ~/.spack/bootstrap``, ``config:misc_cache: ~/.spack/cache``, ``config:test_stage: ~/.spack/test``, ``~/.spack/stage`` in ``config:build_stage``, as written by ``spack bootstrap root --set`` or ``spack config add``) is replaced by the new default (``$state_home/bootstrap``, ``$cache_home/$spack_instance_id/cache``, ...).
* A relative path in ``repos``, ``mirrors``, ``include``, ``config:environments_root`` or ``config:license_dir`` is made absolute against ``~/.spack``, where the data still is, since relative paths resolve against the directory of the file they are written in.

Any other string is left as it is: an absolute path into ``~/.spack`` under some other setting is a choice that still names what it did.

The copy is skipped when the user scope has been pointed elsewhere with :envvar:`SPACK_CONFIG_HOME` or ``SPACK_USER_CONFIG_PATH``, or disabled with :envvar:`SPACK_DISABLE_LOCAL_CONFIG`; it goes to ``$XDG_CONFIG_HOME/spack`` if that variable is set.
A ``~/.config/spack`` that already exists and is not empty is left alone: nothing is merged into it.
If ``~/.spack`` is itself a symbolic link (to a dotfiles checkout, say), ``~/.config/spack`` is created as a link to the same target and nothing is rewritten; Spack instead prints the values that still spell out 1.2 defaults, once, for you to update.

**Package repositories.**
Each clone under ``~/.spack/package_repos`` is copied to the same name under ``$data_home/package_repos``, unless a clone of that name is already there (the name is a hash of the remote URL, so it is the same repository).
A clone that cannot be copied is named in a warning and Spack clones it afresh at the new location when needed; to keep using the old clone, point ``repos:<name>:destination`` at it.

.. _spack-migrate-command:

The ``spack migrate`` command
-----------------------------

``spack migrate`` manages the state left behind by the migration described above. It has three actions:

``spack migrate undo``
  Point all resources back at their legacy locations under ``$spack`` by updating the layout scope.
  Nothing is moved or deleted; copies made in the new locations are left in place.

``spack migrate use-new-layout``
  Remove the layout scope and re-run the migration of ``$spack``-internal resources, for example after declining the prompt on the first run.

Both actions hold the migration lock, so a Spack command started meanwhile waits for them to finish (up to two minutes) and then uses the result; they stop if another process changed the migration state while they were waiting for the lock.

``spack migrate cleanup-old``
  Permanently delete ``~/.spack``.
  Before deleting, Spack prints what the directory contains, which values in the *active* configuration still refer to it, and asks for confirmation.
  Pass ``--yes`` to skip the prompt (required when there is no terminal) and ``--dry-run`` to print the report without deleting.

  Only the active configuration is inspected.
  Inactive environments, conditional configuration scopes, other Spack instances, and anything outside Spack's configuration are not checked; it is up to you to make sure nothing else depends on the directory.

  If ``config:install_tree:root`` resolves to a directory under ``~/.spack``, or the active ``user`` configuration scope is under ``~/.spack``, ``cleanup-old`` refuses to proceed **even with** ``--yes``, because deleting the directory would delete your installed packages (and the next ``spack install`` would silently recreate the store there) or the configuration Spack is running with.
  Uninstalling the packages does not lift this restriction: the configured install tree must be moved out of ``~/.spack`` first, or the directory removed by hand.
  It also refuses to act on a ``~/.spack`` that is a symbolic link.

  Every other reference is only reported: any configuration value that resolves to a path under ``~/.spack`` (a mirror, a repository, a license directory, ...), ``config:locations`` and ``SPACK_GNUPGHOME``.
  The report is the safety net and you make the call; if unsure, keep the directory.

Using ``spack isolate`` to avoid migration prompts
---------------------------------------------------

If the first spack command you run after a ``git pull`` is ``spack isolate``, spack will not prompt for migration of any resources that are in legacy locations (e.g. will not attempt to move environments out of ``$spack/var/spack/environments``).

.. _location-table:

The location table
------------------

+----------------------+-----------+------------+------------+--------------------+
|                      | data_home | state_home | cache_home | somewhere_else     |
+======================+===========+============+============+====================+
| installs             | x         |            |            |                    |
+----------------------+-----------+------------+------------+--------------------+
| bootstrap artifacts  |           | x          |            |                    |
+----------------------+-----------+------------+------------+--------------------+
| build stages         |           | x          |            | x [#wheretable-1]_ |
+----------------------+-----------+------------+------------+--------------------+
| download cache       | x         |            |            |                    |
+----------------------+-----------+------------+------------+--------------------+
| gpg keys             | x         |            |            |                    |
+----------------------+-----------+------------+------------+--------------------+
| modules              |           |            |            | x [#wheretable-2]_ |
+----------------------+-----------+------------+------------+--------------------+
| environments         | x         |            |            |                    |
+----------------------+-----------+------------+------------+--------------------+
| misc cache           |           |            | x          |                    |
+----------------------+-----------+------------+------------+--------------------+
| test stages          |           | x          |            |                    |
+----------------------+-----------+------------+------------+--------------------+
| licenses             | x         |            |            |                    |
+----------------------+-----------+------------+------------+--------------------+
| config files         |           |            |            | x [#wheretable-3]_ |
+----------------------+-----------+------------+------------+--------------------+
| package repos        | x         |            |            |                    |
+----------------------+-----------+------------+------------+--------------------+

.. [#wheretable-1] ``state_home`` is used as a backup, but Spack prefers to write into the user's temp dir if it's available.
.. [#wheretable-2] Spack does not provide a default module root; module roots must be configured explicitly in ``modules.yaml``.
.. [#wheretable-3] User-scope config is controlled with :ref:`environment variables <local-config-overrides>` or with :ref:`include.yaml <include-yaml>` to avoid recursion issues with configurable locations.

References
----------

* :ref:`include.yaml <include-yaml>`
* :ref:`config.yaml <config-yaml>`
