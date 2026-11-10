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
The user must explicitly approve this migration, either interactively or by setting the ``SPACK_AUTOMIGRATE_YES`` environment variable to ``1`` or ``true``.
``spack migrate undo`` restores use of the legacy locations by updating configuration; it does not remove files copied to the new locations.
The original resources are still available because migration leaves them in place.

Spack also independently (without prompting) copies user configuration from ``~/.spack`` to ``~/.config/spack`` and package repositories from ``~/.spack/package_repos`` to ``~/.local/share/spack/package_repos`` when the old locations contain data and the new destinations are available.
This home-directory migration can occur for a fresh checkout and does not create migration state in the Spack prefix.
The old files remain in place for use by older Spack instances.

.. _spack-migrate-command:

The ``spack migrate`` command
-----------------------------

``spack migrate`` manages the state left behind by the migration described above. It has three actions:

``spack migrate undo``
  Point all resources back at their legacy locations under ``$spack`` by updating the layout scope.
  Nothing is moved or deleted; copies made in the new locations are left in place.

``spack migrate use-new-layout``
  Remove the layout scope and re-run the migration of ``$spack``-internal resources, for example after declining the prompt on the first run.

``spack migrate cleanup-old``
  Permanently delete ``~/.spack``.
  Before deleting, Spack prints what the directory contains, which values in the *active* configuration still refer to it, and asks for confirmation.
  Pass ``--yes`` to skip the prompt (required when there is no terminal) and ``--dry-run`` to print the report without deleting.

  Only the active configuration is inspected.
  Inactive environments, conditional configuration scopes, other Spack instances, and anything outside Spack's configuration are not checked; it is up to you to make sure nothing else depends on the directory.

  If ``config:install_tree:root`` resolves to a directory under ``~/.spack``, ``cleanup-old`` refuses to proceed **even with** ``--yes``, because deleting the directory would delete your installed packages and the next ``spack install`` would silently recreate the store there.
  Uninstalling the packages does not lift this restriction: the configured install tree must be moved out of ``~/.spack`` first, or the directory removed by hand.

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
