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

Spack picks one of two *layout schemes* at startup:

* **xdg**: data under ``~/.local/share/spack``, state under ``~/.local/state/spack``, cache under ``~/.cache/spack``.
* **old**: installs in ``$spack/opt/spack``, environments in ``$spack/var/spack/environments``, license files in ``$spack/etc/spack/licenses``, etc. — i.e. the pre-1.2 layout.

The scheme is chosen by ``etc/spack/defaults/include.yaml`` using a ``when:`` clause that calls :func:`spack.paths.detect_layout`.
The included yaml — ``etc/spack/defaults/old/config.yaml`` or ``etc/spack/defaults/xdg/config.yaml`` — sets ``config:locations:*`` (and, for old, the install_tree/environments/etc. paths that don't share a single root).
Everything else flows through normal config: ``config:install_tree:root`` is ``$data_home/installs``, environments root is ``$data_home/environments``, gpg lives at ``$data_home/gpg``, and so on.

You can see the active scheme and where each path came from with::

    spack debug paths

Sample output::

    layout scheme: xdg (no legacy $spack-local data)

    homes:
      $data_home             /home/alice/.local/share/spack
        config:locations:data (scope: defaults:xdg)
      $state_home            /home/alice/.local/state/spack
        config:locations:state (scope: defaults:xdg)
      ...

    config-driven paths:
      config:install_tree:root /home/alice/.local/share/spack/installs
        $data_home/installs  [scope: defaults:base]
      ...

How to override
---------------

In order of priority (highest first):

1. **Env vars** for individual homes — ``SPACK_DATA_HOME``, ``SPACK_STATE_HOME``, ``SPACK_CACHE_HOME``, or ``SPACK_HOME`` (which sets all three via XDG-style subpaths). Any of these also *forces the xdg scheme* even when legacy ``$spack`` data is present, so a partial override never produces a split layout.

2. **Specific config keys** for individual paths — set ``config:install_tree:root``, ``config:environments_root``, ``config:license_dir``, ``config:source_cache``, ``config:gpg_path``, or ``config:gpg_keys_path`` in any user/site/system scope.

3. **Layout roots** — set ``config:locations:{home,data,state,cache}`` to redirect everything that uses the corresponding substitution.

Config locations themselves — ``user_config_path``, ``system_config_path``, the entry-point ``include.yaml`` — are NOT in config (they bootstrap config). Override them with ``SPACK_USER_CONFIG_PATH``, ``SPACK_SYSTEM_CONFIG_PATH``, or ``SPACK_DISABLE_LOCAL_CONFIG``.

Path substitutions
------------------

Config values can reference these in any string field:

* ``$data_home``        — typically ``~/.local/share/spack`` (xdg) or ``$spack`` (old)
* ``$state_home``       — typically ``~/.local/state/spack`` (xdg) or ``~/.spack`` (old)
* ``$cache_home``       — typically ``~/.cache/spack``
* ``$spack_home``       — base for spack's user-level data; defaults to ``~``
* ``$xdg_data_home``    — ``$XDG_DATA_HOME`` if set, else ``~/.local/share`` (no ``/spack`` suffix)
* ``$xdg_state_home``   — ``$XDG_STATE_HOME`` if set, else ``~/.local/state``
* ``$xdg_cache_home``   — ``$XDG_CACHE_HOME`` if set, else ``~/.cache``
* ``$user_cache_path``  — alias for ``$state_home`` (legacy)
* ``$spack``            — the Spack instance's prefix
* ``$spack_instance_id`` — hash distinguishing co-installed Spack instances

The ``$xdg_*_home`` substitutions are used by the xdg scheme yaml so the layout respects XDG env vars without baking that resolution into Python.

Migrating from the old layout
-----------------------------

If you have a ``~/.spack`` directory from before 1.2, you'll see a one-time warning. Run::

    spack migrate --clear

to copy your config into ``~/.config/spack`` and move ``~/.spack`` to a backup at ``~/.local/share/spack/dotspack_backup``. (The backup location is fixed; it does not move when you set ``SPACK_DATA_HOME``.) Use ``spack migrate --restore`` to undo.

If you have older Spack instances that can't be upgraded and need ``~/.spack`` to stick around, see ``spack migrate --i-need-old-spack``.

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
.. [#wheretable-2] ``cache_home`` is modeled after ``$XDG_CACHE_HOME``. Spack assumes that ``$XDG_CACHE_HOME`` can be removed on user log-out; misc cache is intended to be longer-lived, so it lives in ``state_home`` instead.
.. [#wheretable-3] User-scope config is controlled with :ref:`environment variables <local-config-overrides>` or with :ref:`include.yaml <include-yaml>` to avoid recursion issues with configurable locations.

References
----------

* :ref:`include.yaml <include-yaml>`
* :ref:`config.yaml <config-yaml>`
* :ref:`Environment variables controlling config scopes <local-config-overrides>`
