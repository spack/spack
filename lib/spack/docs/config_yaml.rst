.. _config-yaml:

====================================
Basic settings in ``config.yaml``
====================================

Spack's basic configuration options are set in ``config.yaml``.  You can
see the default settings by looking at
``etc/spack/defaults/config.yaml``:

.. literalinclude:: ../../../etc/spack/defaults/config.yaml
   :language: yaml

These settings can be overridden in ``etc/spack/config.yaml`` or
``~/.spack/config.yaml``.  See :ref:`configuration-scopes` for details.

.. _config-file-variables:

------------------------------
Config file variables
------------------------------

You may notice some variables prefixed with ``$`` in the settings above.
Spack understands several variables that can be used in values of
configuration parameters.  They are:

  * ``$spack``: path to the prefix of this spack installation
  * ``$tempdir``: default system temporary directory (as specified in
    Python's `tempfile.tempdir
    <https://docs.python.org/2/library/tempfile.html#tempfile.tempdir>`_
    variable.
  * ``$user``: name of the current user

Note that, as with shell variables, you can write these as ``$varname``
or with braces to distinguish the variable from surrounding characters:
``${varname}``.

--------------------
``install_tree``
--------------------

The location where Spack will install packages and their dependencies.
Default is ``$spack/opt/spack``.

--------------------
``module_roots``
--------------------

Controls where Spack installs generated module files.  You can customize
the location for each type of module.  e.g.:

.. code-block:: yaml

   module_roots:
     tcl:    $spack/share/spack/modules
     lmod:   $spack/share/spack/lmod
     dotkit: $spack/share/spack/dotkit

See :ref:`modules` for details.

--------------------
``build_stage``
--------------------

Spack is designed to run out of a user home directories, and on many
systems the home directory a (slow) network filesystem.  On most systems,
building in a temporary filesystem results in faster builds than building
in the home directory.  Usually, there is also more space available in
the temporary location than in the home directory. So, Spack tries to
create build stages in temporary space.

By default, Spack's ``build_stage`` is configured like this:

.. code-block:: yaml

   build_stage:
    - $tempdir
    - /nfs/tmp2/$user
    - $spack/var/spack/stage

This is an ordered list of paths that Spack should search when trying to
find a temporary directory for the build stage.  The list is searched in
order, and Spack will use the first directory to which it has write access.
See :ref:`config-file-variables` for more on ``$tempdir`` and ``$spack``.

When Spack builds a package, it creates a temporary directory within the
``build_stage``, and it creates a symbolic link to that directory in
``$spack/var/spack/stage``. This is used totrack the stage.

After a package is successfully installed, Spack deletes the temporary
directory it used to build.  Unsuccessful builds are not deleted, but you
can manually purge them with :ref:`spack purge --stage
<cmd-spack-purge>`.

.. note::

   The last item in the list is ``$spack/var/spack/stage``.  If this is the
   only writable directory in the ``build_stage`` list, Spack will build
   *directly* in ``$spack/var/spack/stage`` and will not link to temporary
   space.

--------------------
``source_cache``
--------------------

Location to cache downloaded tarballs and repositories.  By default these
are stored in ``$spack/var/spack/cache``.  These are stored indefinitely
by default. Can be purged with :ref:`spack purge --downloads
<cmd-spack-purge>`.

--------------------
``misc_cache``
--------------------

Temporary directory to store long-lived cache files, such as indices of
packages available in repositories.  Defaults to ``~/.spack/cache``.  Can
be purged with :ref:`spack purge --misc-cache <cmd-spack-purge>`.

--------------------
``verify_ssl``
--------------------

When set to ``true`` (default) Spack will verify certificates of remote
hosts when making ``ssl`` connections.  Set to ``false`` to disable, and
tools like ``curl`` will use their ``--insecure`` options.  Disabling
this can expose you to attacks.  Use at your own risk.

--------------------
``checksum``
--------------------

When set to ``true``, Spack verifies downloaded source code using a
checksum, and will refuse to build packages that it cannot verify.  Set
to ``false`` to disable these checks.  Disabling this can expose you to
attacks.  Use at your own risk.

--------------------
``dirty``
--------------------

By default, Spack unsets variables in your environment that can change
the way packages build. This includes ``LD_LIBRARY_PATH``, ``CPATH``,
``LIBRARY_PATH``, ``DYLD_LIBRARY_PATH``, and others.

By default, builds are ``clean``, but on some machines, compilers and
other tools may need custom ``LD_LIBRARY_PATH`` setings to run.  You can
set ``dirty`` to ``true`` to skip the cleaning step and make all builds
"dirty" by default.  Be aware that this will reduce the reproducibility
of builds.
