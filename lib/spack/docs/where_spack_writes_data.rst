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
A Spack instance that was installed before this layout — where data lived under ``$spack/opt``, ``$spack/var``, etc. — keeps using the legacy install location but attempts to copy environments, GPG data, and licenses to the new default locations under ``$HOME``.
The original resources remain in place.

How to override
---------------

In order of priority (highest first):

1. **Specific config keys** for individual paths — set ``config:install_tree:root``, ``config:environments_root``, ``config:license_dir``, ``config:source_cache``, ``config:gpg_path``, or ``config:gpg_keys_path`` in any user/site/system scope.

2. **Layout roots** — set ``config:locations:{data,state,cache}`` to redirect everything that uses the corresponding substitution.

3. **Env vars** for individual homes — ``SPACK_DATA_HOME``, ``SPACK_STATE_HOME``, or ``SPACK_CACHE_HOME``.
   The default configuration allows these environment variables to influence the associated config variable.

Config locations themselves — ``user_config_path``, ``system_config_path``, the entry-point ``include.yaml`` — are NOT in config (they bootstrap config).
Override them with ``SPACK_USER_CONFIG_PATH``, ``SPACK_SYSTEM_CONFIG_PATH``, or ``SPACK_DISABLE_LOCAL_CONFIG``.

Path substitutions
------------------

Config values can reference these in any string field:

* ``$data_home``        — ``config:locations:data``, defaults to ``~/.local/share/spack``.
* ``$state_home``       — ``config:locations:state``, defaults to ``~/.local/state/spack``.
* ``$cache_home``       — ``config:locations:cache``, defaults to ``~/.cache/spack``
* ``$user_cache_path``  — alias for ``$state_home`` (legacy)
* ``$spack``            — the Spack instance's prefix
* ``$spack_instance_id`` — hash distinguishing co-installed Spack instances

Migration of ``$spack``-internal data for older instances
----------------------------------------------------------

If a user ``git pull``s into a pre-1.3 Spack instance, Spack will prompt to update where some artifacts are stored to match the new default layout.
The user must explicitly approve this migration, either interactively or by setting the ``SPACK_AUTOMIGRATE_YES`` environment variable.
``spack migrate undo`` restores use of the legacy locations by updating configuration; it does not remove files copied to the new locations.
The original resources are still available because migration leaves them in place.

Spack also independently (without prompting) copies user configuration from ``~/.spack`` to ``~/.config/spack`` and package repositories from ``~/.spack/package_repos`` to ``~/.local/state/spack/package_repos`` when the old locations contain data and the new destinations are available.
This home-directory migration can occur for a fresh checkout and does not create migration state in the Spack prefix.
The old files remain in place for use by older Spack instances.

Using ``spack isolate`` to avoid migration prompts
---------------------------------------------------

If the first spack command you run after a ``git pull`` is ``spack isolate``, spack will not prompt for migration of any resources that are in legacy locations (e.g. will not attempt to move environments out of ``$spack/var/spack/environments``).



.. _location-table:

The location table
------------------

+----------------+-----------+--------------------+------------+--------------------+
|                | data_home | state_home         | cache_home | somewhere_else     |
+================+===========+====================+============+====================+
| installs       | x         |                    |            |                    |
+----------------+-----------+--------------------+------------+--------------------+
| build stages   |           |                    |            | x [#wheretable-1]_ |
+----------------+-----------+--------------------+------------+--------------------+
| download cache | x         |                    |            |                    |
+----------------+-----------+--------------------+------------+--------------------+
| gpg keys       | x         |                    |            |                    |
+----------------+-----------+--------------------+------------+--------------------+
| modules        |           |                    |            | x [#wheretable-4]_ |
+----------------+-----------+--------------------+------------+--------------------+
| environments   | x         |                    |            |                    |
+----------------+-----------+--------------------+------------+--------------------+
| misc cache     |           | x [#wheretable-2]_ |            |                    |
+----------------+-----------+--------------------+------------+--------------------+
| test stages    |           | x                  |            |                    |
+----------------+-----------+--------------------+------------+--------------------+
| licenses       | x         |                    |            |                    |
+----------------+-----------+--------------------+------------+--------------------+
| config files   |           |                    |            | x [#wheretable-3]_ |
+----------------+-----------+--------------------+------------+--------------------+

.. [#wheretable-1] ``cache_home`` is used as a backup, but Spack prefers to write into the user's temp dir if it's available.
.. [#wheretable-2] ``cache_home`` is modeled after ``$XDG_CACHE_HOME``.
                   Spack assumes that ``$XDG_CACHE_HOME`` can be removed on user log-out; misc cache is intended to be longer-lived, so it lives in ``state_home`` instead.
.. [#wheretable-3] User-scope config is controlled with :ref:`environment variables <local-config-overrides>` or with :ref:`include.yaml <include-yaml>` to avoid recursion issues with configurable locations.
.. [#wheretable-4] Spack does not provide a default module root; module roots must be configured explicitly in ``modules.yaml``.

References
----------

* :ref:`include.yaml <include-yaml>`
* :ref:`config.yaml <config-yaml>`
