..
   Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. meta::
   :description lang=en:
      Learn how to control where Spack generates files and reads files, and how to effectively isolate a Spack installation.

.. _where_spack_writes_data:

Controlling where Spack writes data
===================================

A fresh checkout of Spack writes nothing into the ``$spack`` prefix; all data goes under the user's home directory in XDG-compliant locations.
A Spack instance that was installed before this layout — where data lived under ``$spack/opt``, ``$spack/var``, etc. — keeps using those legacy locations, so existing installs and environments are not disrupted.

Layout detection
----------------

Spack picks one of two *layout schemes* at startup:

* **new**: data under ``~/.local/share/spack``, state under ``~/.local/state/spack``, cache under ``~/.cache/spack``.
* **old**: installs in ``$spack/opt/spack``, environments in ``$spack/var/spack/environments``, license files in ``$spack/etc/spack/licenses``, etc. — i.e. the pre-1.2 layout.

The scheme is chosen by ``etc/spack/defaults/include.yaml`` using a ``when:`` clause that calls :func:`spack.paths.detect_layout`.
The new layout is defined by ``etc/spack/defaults/base/config.yaml``, which sets paths like ``config:install_tree:root`` to ``$data_home/installs``, ``environments_root`` to ``$data_home/environments``, etc.
The ``old-layout`` scope (``etc/spack/defaults/old/config.yaml``) overrides both the homes and the individual paths (install_tree, environments, etc.) to point back into ``$spack``.

**Unilateral override**: Setting any of the new-style environment variables (``SPACK_DATA_HOME``, ``SPACK_STATE_HOME``, or ``SPACK_CACHE_HOME``) forces the new layout even when legacy ``$spack`` data is present.
This ensures a partial override never produces a split layout.

**Config bypass**: If you set ``config::`` or ``include::`` entries directly (bypassing the defaults), the base config scope is omitted and the ``SPACK_*_HOME`` environment variables have no effect on locations.

How to override
---------------

In order of priority (highest first):

1. **Specific config keys** for individual paths — set ``config:install_tree:root``, ``config:environments_root``, ``config:license_dir``, ``config:source_cache``, ``config:gpg_path``, or ``config:gpg_keys_path`` in any user/site/system scope.

2. **Env vars** for individual homes — ``SPACK_DATA_HOME``, ``SPACK_STATE_HOME``, or ``SPACK_CACHE_HOME``.
   Any of these also *forces the new scheme* even when legacy ``$spack`` data is present, so a partial override never produces a split layout.

3. **Layout roots** — set ``config:locations:{data,state,cache}`` to redirect everything that uses the corresponding substitution.

Config locations themselves — ``user_config_path``, ``system_config_path``, the entry-point ``include.yaml`` — are NOT in config (they bootstrap config).
Override them with ``SPACK_USER_CONFIG_PATH``, ``SPACK_SYSTEM_CONFIG_PATH``, or ``SPACK_DISABLE_LOCAL_CONFIG``.

Path substitutions
------------------

Config values can reference these in any string field:

* ``$data_home``        — typically ``~/.local/share/spack`` (new) or ``$spack`` (old)
* ``$state_home``       — typically ``~/.local/state/spack`` (new) or ``~/.spack`` (old, if it exists)
* ``$cache_home``       — typically ``~/.cache/spack``
* ``$user_cache_path``  — alias for ``$state_home`` (legacy)
* ``$spack``            — the Spack instance's prefix
* ``$spack_instance_id`` — hash distinguishing co-installed Spack instances

Migrating user cache path and configs
--------------------------------------

If you have a ``~/.spack`` directory from before 1.2, each Spack command will print a warning until you run ``spack migrate``.
Spack will continue using ``~/.spack`` as ``$state_home`` (for backward compatibility) until you migrate.

If all Spack instances are upgrading to 1.2+, run::

    spack migrate --clear

to copy your config into ``~/.config/spack`` and move ``~/.spack`` to a backup at ``~/.spack.backup``.
This silences the warning.

Use ``spack migrate --restore`` to undo.

If you have older Spack instances that can't be upgraded and need ``~/.spack`` to stick around, see ``spack migrate --i-need-old-spack`` for how to silence the warning without migrating.

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
| modules        | x         |                    |            |                    |
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

References
----------

* :ref:`include.yaml <include-yaml>`
* :ref:`config.yaml <config-yaml>`
