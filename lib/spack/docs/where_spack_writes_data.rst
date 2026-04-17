..
   Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. meta::
   :description lang=en:
      Learn how to control where Spack generates files and reads files, and how to effectively isolate a Spack installation.

.. _where_spack_writes_data:

Controlling where spack writes data
===================================

A fresh checkout of spack will not write anything into the ``$spack`` prefix; instead, all data is placed under the user's home directory.
You can control this in the following ways:

* Redirect everything with environment variables: set ``SPACK_HOME`` and one of ``SPACK_USER_CONFIG_PATH`` or ``SPACK_DISABLE_LOCAL_CONFIG=1``
* Or redirect everything with config:

  * set ``config:locations:home``
  * Update the ``user`` config scope with ``spack config --scope=spack edit include``
* Or redirect installs, environments, and cached downloads (everything that takes up significant space) by setting ``SPACK_DATA_HOME``
* Or use finer-grained configuration settings, for example:

  * ``config:install_tree:root`` to control where installs go
  * ``config:build_stage`` to control where builds are staged

In the absence of any Spack-specific settings, Spack will respect [XDG](https://specifications.freedesktop.org/basedir/latest/) environment variables controlling the home directory for specific types of data.

Spack's older layout, and pulling newer versions of Spack
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Spack previously stored many important pieces of data in the Spack prefix:

* Installs in ``$spack/opt/spack``
* Environments in ``$spack/var/spack/environments``
* GPG keys in ``$spack/opt/spack/gpg``

If Spack detects this old layout in use, it will continue to use it.
Targeted config settings like ``config:install_tree:root`` will override this, but not other environment variables or general configuration (i.e. anything described below this section).

.. _config-file-data-variables:

Spack-specific variables controlling data location
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Files generated and used by spack are organized roughly into four categories:

* Persistent, large quantities of data (e.g. installs and environments)
* Temporary (or assumed temporary) large quantities of data (e.g. stages for installs)
* Persistent caches/indices used by spack to speed up its commands (small quantities of data)
* The configuration files themselves

The corresponding variables that describe where this data is placed are:

* ``$data_home``
* ``$cache_home``
* ``$state_home`` (also known as ``$user_cache_path``)
* Config file locations are an exception: they can only be controlled with :ref:`environment variables <local-config-overrides>` or with :ref:`include.yaml <include-yaml>`

You can refer to these variables when configuring locations for stages, misc cache, etc.

The following table may help visualize where spack puts all the files it may generate:

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

.. [#wheretable-1] ``cache_home`` is used as a backup, but Spack prefers to write into the user's temp dir if it's available
.. [#wheretable-2] ``cache_home`` is modeled after `$XDG_CACHE_HOME <https://specifications.freedesktop.org/basedir/latest/>`_.
                   Spack assumes that ``$XDG_CACHE_HOME`` can be removed on user log-out.
                   Spack caches are intended to be longer-lived, so they live in ``state_home`` instead.
.. [#wheretable-3] as discussed elsewhere in this section, user-scope config is controlled with :ref:`environment variables <local-config-overrides>` or with :ref:`include.yaml <include-yaml>` to avoid recursion issues with configurable locations.
                   For the locations of other config scopes and how to write to them instead, see :ref:`configuration scopes <configuration-scopes>`.

Each of these variables are the *default* (fallback) for data in their category: more-specific data in that category may have config that overrides these defaults.
For example while build stages would reasonably be placed in ``$cache_home``, Spack's default configuration sets ``config:build_stage`` to the user's tempdir.
Any configuration controlling location that is more-specific than the above variables will always take precedence (e.g. ``config:install_tree:root``).

Each of these variables can be set with config or with environment variables.
For example ``$data_home`` evaluates to one of the following (highest-priority first):

#. ``SPACK_DATA_HOME`` env var if that is set
#. Under ``SPACK_HOME`` env var; for ``$data_home``, it is ``$SPACK_HOME/.local/share/spack``
#. ``config:locations:data``
#. Under ``config:locations:home``; for ``$data_home`` it is ``$spack_home/.local/share/spack``
#. ``XDG_DATA_HOME/spack`` if XDG_DATA_HOME is set
#. Under the default for ``XDG_DATA_HOME``: ``~/.local/share/spack``

``config:locations:home`` / ``SPACK_HOME`` can be used to control all 3 of ``data_home``, ``cache_home``, and ``state_home``.
They are placed relative to this directory (``$spack_home``):

* ``data_home`` is placed in ``$spack_home/.local/share/spack`` (as described above).
* ``state_home`` is placed in ``$spack_home/.local/state/spack``.
* ``cache_home`` is placed in ``$spack_home/.cache/spack``.

Location of installs and environments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Of particular interest is where the environments and installs are placed by Spack, because these can take up a lot of space.
These are controlled by ``$data_home``.
Older installs of spack placed these within ``$spack``, and fallback scheme in these cases is augmented to prefer these old locations if no data is detected in the corresponding new locations:

* ``$default_install_root``: the location where installs go by default.
  Overridden by ``config:install_tree:root``.
  Prefers ``$data_home/installs``, but if there are no installs there and there are installs in the old location ``$spack/opt/spack``, then the old location will be used.
* ``$default_envs_root``: the location where environments are managed by default.
  Overridden by ``config:environments_root``.
  Prefers ``$data_home/envs`` but if there are no envs there and there are envs in the old location ``$spack/var/spack/environments``, then the old location will be used.

References
^^^^^^^^^^

For more on this, see:

* :ref:`include.yaml <include-yaml>`
* :ref:`config.yaml <config-yaml>`
* :ref:`Environment variables controlling config scopes <local-config-overrides>`
