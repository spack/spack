=================
Command Reference
=================

This is a reference for all commands in the Spack command line interface.
The same information is available through :ref:`spack-help`.

Commands that also have sections in the main documentation have a link to
"More documentation".

==================  =========================================================================
 Category            Commands 
==================  =========================================================================
Administration      | :ref:`deprecate <spack-deprecate>`,
                      :ref:`make-installer <spack-make-installer>`,
                      :ref:`mark <spack-mark>`,
                      :ref:`reindex <spack-reindex>`,
                      :ref:`test <spack-test>`,
                      :ref:`test-env <spack-test-env>`,
                      :ref:`verify <spack-verify>`
Query packages      | :ref:`dependencies <spack-dependencies>`,
                      :ref:`dependents <spack-dependents>`,
                      :ref:`diff <spack-diff>`,
                      :ref:`find <spack-find>`,
                      :ref:`graph <spack-graph>`,
                      :ref:`info <spack-info>`,
                      :ref:`list <spack-list>`,
                      :ref:`location <spack-location>`,
                    | :ref:`logs <spack-logs>`,
                      :ref:`providers <spack-providers>`,
                      :ref:`resource <spack-resource>`,
                      :ref:`tags <spack-tags>`
Build packages      | :ref:`build-env <spack-build-env>`,
                      :ref:`ci <spack-ci>`,
                      :ref:`clean <spack-clean>`,
                      :ref:`dev-build <spack-dev-build>`,
                      :ref:`fetch <spack-fetch>`,
                      :ref:`gc <spack-gc>`,
                      :ref:`install <spack-install>`,
                      :ref:`log-parse <spack-log-parse>`,
                    | :ref:`patch <spack-patch>`,
                      :ref:`restage <spack-restage>`,
                      :ref:`spec <spack-spec>`,
                      :ref:`stage <spack-stage>`,
                      :ref:`uninstall <spack-uninstall>`
Configuration       | :ref:`config <spack-config>`,
                      :ref:`external <spack-external>`,
                      :ref:`mirror <spack-mirror>`,
                      :ref:`repo <spack-repo>`,
                      :ref:`tutorial <spack-tutorial>`
Container           | :ref:`containerize <spack-containerize>`
Developer           | :ref:`blame <spack-blame>`,
                      :ref:`cd <spack-cd>`,
                      :ref:`commands <spack-commands>`,
                      :ref:`debug <spack-debug>`,
                      :ref:`license <spack-license>`,
                      :ref:`maintainers <spack-maintainers>`,
                      :ref:`pkg <spack-pkg>`,
                      :ref:`pydoc <spack-pydoc>`,
                    | :ref:`python <spack-python>`,
                      :ref:`solve <spack-solve>`,
                      :ref:`style <spack-style>`,
                      :ref:`unit-test <spack-unit-test>`,
                      :ref:`url <spack-url>`
Environments        | :ref:`add <spack-add>`,
                      :ref:`change <spack-change>`,
                      :ref:`concretize <spack-concretize>`,
                      :ref:`deconcretize <spack-deconcretize>`,
                      :ref:`develop <spack-develop>`,
                      :ref:`env <spack-env>`,
                      :ref:`remove <spack-remove>`,
                      :ref:`undevelop <spack-undevelop>`,
                    | :ref:`view <spack-view>`
Extensions          | :ref:`extensions <spack-extensions>`
More help           | :ref:`docs <spack-docs>`,
                      :ref:`help <spack-help>`
Create packages     | :ref:`buildcache <spack-buildcache>`,
                      :ref:`checksum <spack-checksum>`,
                      :ref:`create <spack-create>`,
                      :ref:`edit <spack-edit>`,
                      :ref:`gpg <spack-gpg>`,
                      :ref:`versions <spack-versions>`
System              | :ref:`arch <spack-arch>`,
                      :ref:`audit <spack-audit>`,
                      :ref:`bootstrap <spack-bootstrap>`,
                      :ref:`compiler <spack-compiler>`,
                      :ref:`compilers <spack-compilers>`
User environment    | :ref:`load <spack-load>`,
                      :ref:`module <spack-module>`,
                      :ref:`unload <spack-unload>`
==================  =========================================================================


----

.. _spack:

spack
-----

A flexible package manager that supports multiple versions,
configurations, platforms, and compilers.

.. code-block:: console

    spack [-hHdklLmbpvtV] [--color {always,never,auto}] [-c CONFIG_VARS] [-C DIR|ENV] [--timestamp] [--pdb]
      [-e ENV | -D DIR | -E] [--use-env-repo] [--sorted-profile STAT] [--lines LINES] [--stacktrace]
      [--print-shell-vars PRINT_SHELL_VARS]
      COMMAND ...


**Optional arguments**

``-h, --help``
  show this help message and exit

``-H, --all-help``
  show help for all commands (same as ``spack help --all``)

``--color {always,never,auto}``
  when to colorize output (default: auto)

``-c CONFIG_VARS, --config CONFIG_VARS``
  add one or more custom, one off config settings

``-C DIR|ENV, --config-scope DIR|ENV``
  add directory or environment as read-only configuration scope, without activating the environment.

``-d, --debug``
  write out debug messages

``--timestamp``
  add a timestamp to tty output

``--pdb``
  run spack under the pdb debugger

``-e ENV, --env ENV``
  run with a specific environment (see spack env)

``-D DIR, --env-dir DIR``
  run with an environment directory (ignore managed environments)

``-E, --no-env``
  run without any environments activated (see spack env)

``--use-env-repo``
  when running in an environment, use its package repository

``-k, --insecure``
  do not check ssl certificates when downloading

``-l, --enable-locks``
  use filesystem locking (default)

``-L, --disable-locks``
  do not use filesystem locking (unsafe)

``-m, --mock``
  use mock packages instead of real ones

``-b, --bootstrap``
  use bootstrap configuration (bootstrap store, config, externals)

``-p, --profile``
  profile execution using cProfile

``--sorted-profile STAT``
  profile and sort

``--lines LINES``
  lines of profile output or 'all' (default: 20)

``-v, --verbose``
  print additional output during builds

``--stacktrace``
  add stacktraces to all printed statements

``-t, --backtrace``
  always show backtraces for exceptions

``-V, --version``
  show version number and exit

``--print-shell-vars PRINT_SHELL_VARS``
  print info needed by setup-env.*sh


**Subcommands**

.. hlist::
   :columns: 4

   * :ref:`add <spack-add>`
   * :ref:`arch <spack-arch>`
   * :ref:`audit <spack-audit>`
   * :ref:`blame <spack-blame>`
   * :ref:`bootstrap <spack-bootstrap>`
   * :ref:`build-env <spack-build-env>`
   * :ref:`buildcache <spack-buildcache>`
   * :ref:`cd <spack-cd>`
   * :ref:`change <spack-change>`
   * :ref:`checksum <spack-checksum>`
   * :ref:`ci <spack-ci>`
   * :ref:`clean <spack-clean>`
   * :ref:`commands <spack-commands>`
   * :ref:`compiler <spack-compiler>`
   * :ref:`compilers <spack-compilers>`
   * :ref:`concretize <spack-concretize>`
   * :ref:`config <spack-config>`
   * :ref:`containerize <spack-containerize>`
   * :ref:`create <spack-create>`
   * :ref:`debug <spack-debug>`
   * :ref:`deconcretize <spack-deconcretize>`
   * :ref:`dependencies <spack-dependencies>`
   * :ref:`dependents <spack-dependents>`
   * :ref:`deprecate <spack-deprecate>`
   * :ref:`dev-build <spack-dev-build>`
   * :ref:`develop <spack-develop>`
   * :ref:`diff <spack-diff>`
   * :ref:`docs <spack-docs>`
   * :ref:`edit <spack-edit>`
   * :ref:`env <spack-env>`
   * :ref:`extensions <spack-extensions>`
   * :ref:`external <spack-external>`
   * :ref:`fetch <spack-fetch>`
   * :ref:`find <spack-find>`
   * :ref:`gc <spack-gc>`
   * :ref:`gpg <spack-gpg>`
   * :ref:`graph <spack-graph>`
   * :ref:`help <spack-help>`
   * :ref:`info <spack-info>`
   * :ref:`install <spack-install>`
   * :ref:`license <spack-license>`
   * :ref:`list <spack-list>`
   * :ref:`load <spack-load>`
   * :ref:`location <spack-location>`
   * :ref:`log-parse <spack-log-parse>`
   * :ref:`logs <spack-logs>`
   * :ref:`maintainers <spack-maintainers>`
   * :ref:`make-installer <spack-make-installer>`
   * :ref:`mark <spack-mark>`
   * :ref:`mirror <spack-mirror>`
   * :ref:`module <spack-module>`
   * :ref:`patch <spack-patch>`
   * :ref:`pkg <spack-pkg>`
   * :ref:`providers <spack-providers>`
   * :ref:`pydoc <spack-pydoc>`
   * :ref:`python <spack-python>`
   * :ref:`reindex <spack-reindex>`
   * :ref:`remove <spack-remove>`
   * :ref:`repo <spack-repo>`
   * :ref:`resource <spack-resource>`
   * :ref:`restage <spack-restage>`
   * :ref:`solve <spack-solve>`
   * :ref:`spec <spack-spec>`
   * :ref:`stage <spack-stage>`
   * :ref:`style <spack-style>`
   * :ref:`tags <spack-tags>`
   * :ref:`test <spack-test>`
   * :ref:`test-env <spack-test-env>`
   * :ref:`tutorial <spack-tutorial>`
   * :ref:`undevelop <spack-undevelop>`
   * :ref:`uninstall <spack-uninstall>`
   * :ref:`unit-test <spack-unit-test>`
   * :ref:`unload <spack-unload>`
   * :ref:`url <spack-url>`
   * :ref:`verify <spack-verify>`
   * :ref:`versions <spack-versions>`
   * :ref:`view <spack-view>`


----

.. _spack-add:

spack add
---------

add a spec to an environment

.. code-block:: console

    spack add [-h] [-l LIST_NAME] ...


**Positional arguments**

``specs``
  one or more package specs


**Optional arguments**

``-h, --help``
  show this help message and exit

``-l LIST_NAME, --list-name LIST_NAME``
  name of the list to add specs to


----

.. _spack-arch:

spack arch
----------

print architecture information about this machine

.. code-block:: console

    spack arch [-hg] [--known-targets] [--family | --generic] [-p | -o | -t] [-f | -b]


**Optional arguments**

``-h, --help``
  show this help message and exit

``-g, --generic-target``
  show the best generic target (deprecated)

``--known-targets``
  show a list of all known targets and exit

``--family``
  print generic ISA (x86_64, aarch64, ppc64le, ...)

``--generic``
  print feature level (x86_64_v3, armv8.4a, ...)

``-p, --platform``
  print only the platform

``-o, --operating-system``
  print only the operating system

``-t, --target``
  print only the target

``-f, --frontend``
  print frontend (DEPRECATED)

``-b, --backend``
  print backend (DEPRECATED)


----

.. _spack-audit:

spack audit
-----------

audit configuration files, packages, etc.

.. code-block:: console

    spack audit [-h] SUBCOMMAND ...


**Optional arguments**

``-h, --help``
  show this help message and exit


**Subcommands**

.. hlist::
   :columns: 4

   * :ref:`audit configs <spack-audit-configs>`
   * :ref:`audit externals <spack-audit-externals>`
   * :ref:`audit packages-https <spack-audit-packages-https>`
   * :ref:`audit packages <spack-audit-packages>`
   * :ref:`audit list <spack-audit-list>`


----

.. _spack-audit-configs:

spack audit configs
^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack audit configs [-h]


**Optional arguments**

``-h, --help``
  show this help message and exit


----

.. _spack-audit-externals:

spack audit externals
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack audit externals [-h] [--list] [PKG ...]


**Positional arguments**

``PKG``
  package to be analyzed (if none all packages will be processed)


**Optional arguments**

``-h, --help``
  show this help message and exit

``--list``
  if passed, list which packages have detection tests


----

.. _spack-audit-packages-https:

spack audit packages-https
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack audit packages-https [-h] [--all] [PKG ...]


**Positional arguments**

``PKG``
  package to be analyzed (if none all packages will be processed)


**Optional arguments**

``-h, --help``
  show this help message and exit

``--all``
  audit all packages


----

.. _spack-audit-packages:

spack audit packages
^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack audit packages [-h] [PKG ...]


**Positional arguments**

``PKG``
  package to be analyzed (if none all packages will be processed)


**Optional arguments**

``-h, --help``
  show this help message and exit


----

.. _spack-audit-list:

spack audit list
^^^^^^^^^^^^^^^^

.. code-block:: console

    spack audit list [-h]


**Optional arguments**

``-h, --help``
  show this help message and exit


----

.. _spack-blame:

spack blame
-----------

show contributors to packages

.. code-block:: console

    spack blame [-h] [-t | -p | -g] [--json] package_or_file


**Positional arguments**

``package_or_file``
  name of package to show contributions for, or path to a file in the spack repo


**Optional arguments**

``-h, --help``
  show this help message and exit

``-t, --time``
  sort by last modification date (default)

``-p, --percent``
  sort by percent of code

``-g, --git``
  show git blame output instead of summary

``--json``
  output blame as machine-readable json records


----

.. _spack-bootstrap:

spack bootstrap
---------------

manage bootstrap configuration

.. code-block:: console

    spack bootstrap [-h] SUBCOMMAND ...


**Optional arguments**

``-h, --help``
  show this help message and exit


**Subcommands**

.. hlist::
   :columns: 4

   * :ref:`bootstrap now <spack-bootstrap-now>`
   * :ref:`bootstrap status <spack-bootstrap-status>`
   * :ref:`bootstrap enable <spack-bootstrap-enable>`
   * :ref:`bootstrap disable <spack-bootstrap-disable>`
   * :ref:`bootstrap reset <spack-bootstrap-reset>`
   * :ref:`bootstrap root <spack-bootstrap-root>`
   * :ref:`bootstrap list <spack-bootstrap-list>`
   * :ref:`bootstrap add <spack-bootstrap-add>`
   * :ref:`bootstrap remove <spack-bootstrap-remove>`
   * :ref:`bootstrap mirror <spack-bootstrap-mirror>`


----

.. _spack-bootstrap-now:

spack bootstrap now
^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack bootstrap now [-h] [--dev]


**Optional arguments**

``-h, --help``
  show this help message and exit

``--dev``
  bootstrap dev dependencies too


----

.. _spack-bootstrap-status:

spack bootstrap status
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack bootstrap status [-h] [--optional] [--dev]


**Optional arguments**

``-h, --help``
  show this help message and exit

``--optional``
  show the status of rarely used optional dependencies

``--dev``
  show the status of dependencies needed to develop Spack


----

.. _spack-bootstrap-enable:

spack bootstrap enable
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack bootstrap enable [-h] [--scope {defaults,system,site,user,command_line} or env:ENVIRONMENT] [name]


**Positional arguments**

``name``
  name of the source to be enabled


**Optional arguments**

``-h, --help``
  show this help message and exit

``--scope {defaults,system,site,user,command_line} or env:ENVIRONMENT``
  configuration scope to read/modify


----

.. _spack-bootstrap-disable:

spack bootstrap disable
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack bootstrap disable [-h] [--scope {defaults,system,site,user,command_line} or env:ENVIRONMENT] [name]


**Positional arguments**

``name``
  name of the source to be disabled


**Optional arguments**

``-h, --help``
  show this help message and exit

``--scope {defaults,system,site,user,command_line} or env:ENVIRONMENT``
  configuration scope to read/modify


----

.. _spack-bootstrap-reset:

spack bootstrap reset
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack bootstrap reset [-hy]


**Optional arguments**

``-h, --help``
  show this help message and exit

``-y, --yes-to-all``
  assume "yes" is the answer to every confirmation request


----

.. _spack-bootstrap-root:

spack bootstrap root
^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack bootstrap root [-h] [--scope {defaults,system,site,user,command_line} or env:ENVIRONMENT] [path]


**Positional arguments**

``path``
  set the bootstrap directory to this value


**Optional arguments**

``-h, --help``
  show this help message and exit

``--scope {defaults,system,site,user,command_line} or env:ENVIRONMENT``
  configuration scope to read/modify


----

.. _spack-bootstrap-list:

spack bootstrap list
^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack bootstrap list [-h] [--scope {defaults,system,site,user,command_line} or env:ENVIRONMENT]


**Optional arguments**

``-h, --help``
  show this help message and exit

``--scope {defaults,system,site,user,command_line} or env:ENVIRONMENT``
  configuration scope to read/modify


----

.. _spack-bootstrap-add:

spack bootstrap add
^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack bootstrap add [-h] [--scope {defaults,system,site,user,command_line} or env:ENVIRONMENT] [--trust]
                    name metadata_dir


**Positional arguments**

``name``
  name of the new source of software

``metadata_dir``
  directory where to find metadata files


**Optional arguments**

``-h, --help``
  show this help message and exit

``--scope {defaults,system,site,user,command_line} or env:ENVIRONMENT``
  configuration scope to read/modify

``--trust``
  enable the source immediately upon addition


----

.. _spack-bootstrap-remove:

spack bootstrap remove
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack bootstrap remove [-h] name


**Positional arguments**

``name``
  name of the source to be removed


**Optional arguments**

``-h, --help``
  show this help message and exit


----

.. _spack-bootstrap-mirror:

spack bootstrap mirror
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack bootstrap mirror [-h] [--binary-packages] [--dev] DIRECTORY


**Positional arguments**

``DIRECTORY``
  root directory in which to create the mirror and metadata


**Optional arguments**

``-h, --help``
  show this help message and exit

``--binary-packages``
  download public binaries in the mirror

``--dev``
  download dev dependencies too


----

.. _spack-build-env:

spack build-env
---------------

run a command in a spec's install environment, or dump its environment to screen or file

.. code-block:: console

    spack build-env [-hfU] [--clean] [--dirty] [--reuse] [--fresh-roots] [--deprecated] [--dump FILE] [--pickle FILE] ...


**Positional arguments**

``spec [--] [cmd]...``
  specs of package environment to emulate


**Optional arguments**

``-h, --help``
  show this help message and exit

``--clean``
  unset harmful variables in the build environment (default)

``--dirty``
  preserve user environment in spack's build environment (danger!)

``-f, --force``
  allow changes to concretized specs in spack.lock (in an env)

``-U, --fresh``
  do not reuse installed deps; build newest configuration

``--reuse``
  reuse installed packages/buildcaches when possible

``--fresh-roots, --reuse-deps``
  concretize with fresh roots and reused dependencies

``--deprecated``
  allow concretizer to select deprecated versions

``--dump FILE``
  dump a source-able environment to FILE

``--pickle FILE``
  dump a pickled source-able environment to FILE


----

.. _spack-buildcache:

spack buildcache
----------------

create, download and install binary packages

.. code-block:: console

    spack buildcache [-h] SUBCOMMAND ...


**Optional arguments**

``-h, --help``
  show this help message and exit


**Subcommands**

.. hlist::
   :columns: 4

   * :ref:`buildcache push <spack-buildcache-push>`
   * :ref:`buildcache install <spack-buildcache-install>`
   * :ref:`buildcache list <spack-buildcache-list>`
   * :ref:`buildcache keys <spack-buildcache-keys>`
   * :ref:`buildcache check <spack-buildcache-check>`
   * :ref:`buildcache download <spack-buildcache-download>`
   * :ref:`buildcache prune <spack-buildcache-prune>`
   * :ref:`buildcache save-specfile <spack-buildcache-save-specfile>`
   * :ref:`buildcache sync <spack-buildcache-sync>`
   * :ref:`buildcache update-index <spack-buildcache-update-index>`
   * :ref:`buildcache migrate <spack-buildcache-migrate>`


----

.. _spack-buildcache-push:

spack buildcache push
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack buildcache push [-hf] [--unsigned | --signed | --key key] [--update-index] [--only {package,dependencies}]
                      [--with-build-dependencies | --without-build-dependencies] [--fail-fast]
                      [--base-image BASE_IMAGE] [--tag TAG] [--private] [-j JOBS]
                      mirror ...


**Positional arguments**

``mirror``
  mirror name, path, or URL

``specs``
  one or more package specs


**Optional arguments**

``-h, --help``
  show this help message and exit

``-f, --force``
  overwrite tarball if it exists

``--unsigned, -u``
  push unsigned buildcache tarballs

``--signed``
  push signed buildcache tarballs

``--key key, -k key``
  key for signing

``--update-index, --rebuild-index``
  regenerate buildcache index after building package(s)

``--only {package,dependencies}``
  select the buildcache mode. The default is to build a cache for the package along with all its dependencies. Alternatively, one can decide to build a cache for only the package or only the dependencies

``--with-build-dependencies``
  include build dependencies in the buildcache

``--without-build-dependencies``
  exclude build dependencies from the buildcache

``--fail-fast``
  stop pushing on first failure (default is best effort)

``--base-image BASE_IMAGE``
  specify the base image for the buildcache

``--tag TAG, -t TAG``
  when pushing to an OCI registry, tag an image containing all root specs and their runtime dependencies

``--private``
  for a private mirror, include non-redistributable packages

``-j JOBS, --jobs JOBS``
  explicitly set number of parallel jobs


----

.. _spack-buildcache-install:

spack buildcache install
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack buildcache install [-hfmuo] ...


**Positional arguments**

``specs``
  one or more package specs


**Optional arguments**

``-h, --help``
  show this help message and exit

``-f, --force``
  overwrite install directory if it exists

``-m, --multiple``
  allow all matching packages

``-u, --unsigned``
  install unsigned buildcache tarballs for testing

``-o, --otherarch``
  install specs from other architectures instead of default platform and OS


----

.. _spack-buildcache-list:

spack buildcache list
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack buildcache list [-hlLNva] ...


**Positional arguments**

``specs``
  one or more package specs


**Optional arguments**

``-h, --help``
  show this help message and exit

``-l, --long``
  show dependency hashes as well as versions

``-L, --very-long``
  show full dependency hashes as well as versions

``-N, --namespaces``
  show fully qualified package names

``-v, --variants``
  show variants in output (can be long)

``-a, --allarch``
  list specs for all available architectures instead of default platform and OS


----

.. _spack-buildcache-keys:

spack buildcache keys
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack buildcache keys [-hitf]


**Optional arguments**

``-h, --help``
  show this help message and exit

``-i, --install``
  install Keys pulled from mirror

``-t, --trust``
  trust all downloaded keys

``-f, --force``
  force new download of keys


----

.. _spack-buildcache-check:

spack buildcache check
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack buildcache check [-h] [-m MIRROR_URL] [-o OUTPUT_FILE]
                       [--scope {defaults,system,site,user,command_line} or env:ENVIRONMENT]
                       ...


**Positional arguments**

``specs``
  one or more package specs


**Optional arguments**

``-h, --help``
  show this help message and exit

``-m MIRROR_URL, --mirror-url MIRROR_URL``
  override any configured mirrors with this mirror URL

``-o OUTPUT_FILE, --output-file OUTPUT_FILE``
  file where rebuild info should be written

``--scope {defaults,system,site,user,command_line} or env:ENVIRONMENT``
  configuration scope containing mirrors to check


----

.. _spack-buildcache-download:

spack buildcache download
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack buildcache download [-h] [-s SPEC] -p PATH


**Optional arguments**

``-h, --help``
  show this help message and exit

``-s SPEC, --spec SPEC``
  download built tarball for spec from mirror

``-p PATH, --path PATH``
  path to directory where tarball should be downloaded


----

.. _spack-buildcache-prune:

spack buildcache prune
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack buildcache prune [-h] [--dry-run] mirror


**Positional arguments**

``mirror``
  mirror name, path, or URL


**Optional arguments**

``-h, --help``
  show this help message and exit

``--dry-run``
  do not actually delete anything from the buildcache, but log what would be deleted


----

.. _spack-buildcache-save-specfile:

spack buildcache save-specfile
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack buildcache save-specfile [-h] --root-spec ROOT_SPEC -s SPECS --specfile-dir SPECFILE_DIR


**Optional arguments**

``-h, --help``
  show this help message and exit

``--root-spec ROOT_SPEC``
  root spec of dependent spec

``-s SPECS, --specs SPECS``
  list of dependent specs for which saved yaml is desired

``--specfile-dir SPECFILE_DIR``
  path to directory where spec yamls should be saved


----

.. _spack-buildcache-sync:

spack buildcache sync
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack buildcache sync [-h] [--manifest-glob MANIFEST_GLOB] [source mirror] [destination mirror]


**Positional arguments**

``source mirror``
  source mirror name, path, or URL

``destination mirror``
  destination mirror name, path, or URL


**Optional arguments**

``-h, --help``
  show this help message and exit

``--manifest-glob MANIFEST_GLOB``
  a quoted glob pattern identifying CI rebuild manifest files


----

.. _spack-buildcache-update-index:

spack buildcache update-index
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack buildcache update-index [-hk] mirror


**Positional arguments**

``mirror``
  destination mirror name, path, or URL


**Optional arguments**

``-h, --help``
  show this help message and exit

``-k, --keys``
  if provided, key index will be updated as well as package index


----

.. _spack-buildcache-migrate:

spack buildcache migrate
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack buildcache migrate [-hudy] mirror


**Positional arguments**

``mirror``
  name of a configured mirror


**Optional arguments**

``-h, --help``
  show this help message and exit

``-u, --unsigned``
  Ignore signatures and do not resign, default is False

``-d, --delete-existing``
  Delete the previous layout, the default is to keep it.

``-y, --yes-to-all``
  assume "yes" is the answer to every confirmation request


----

.. _spack-cd:

spack cd
--------

cd to spack directories in the shell

.. code-block:: console

    spack cd [-h] [-m | -r | -i | -p | --repo [repo] | -s | -S | -c | -b | -e [name]] [--first] ...


**Positional arguments**

``spec``
  package spec


**Optional arguments**

``-h, --help``
  show this help message and exit

``-m, --module-dir``
  spack python module directory

``-r, --spack-root``
  spack installation root

``-i, --install-dir``
  install prefix for spec (spec need not be installed)

``-p, --package-dir``
  directory enclosing a spec's package.py file

``--repo [repo], --packages [repo], -P [repo]``
  package repository root (defaults to first configured repository)

``-s, --stage-dir``
  stage directory for a spec

``-S, --stages``
  top level stage directory

``-c, --source-dir``
  source directory for a spec (requires it to be staged first)

``-b, --build-dir``
  build directory for a spec (requires it to be staged first)

``-e [name], --env [name]``
  location of the named or current environment

``--first``
  use the first match if multiple packages match the spec


----

.. _spack-change:

spack change
------------

change an existing spec in an environment

.. code-block:: console

    spack change [-ha] [-l LIST_NAME] [--match-spec MATCH_SPEC] ...


**Positional arguments**

``specs``
  one or more package specs


**Optional arguments**

``-h, --help``
  show this help message and exit

``-l LIST_NAME, --list-name LIST_NAME``
  name of the list to remove specs from

``--match-spec MATCH_SPEC``
  if name is ambiguous, supply a spec to match

``-a, --all``
  change all matching specs (allow changing more than one spec)


----

.. _spack-checksum:

spack checksum
--------------

checksum available versions of a package

.. code-block:: console

    spack checksum [-h] [--keep-stage] [--batch] [--latest] [--preferred] [--add-to-package | --verify] [-j JOBS]
               package [versions ...]


**Positional arguments**

``package``
  name or spec (e.g. ``cmake`` or ``cmake@3.18``)

``versions``
  checksum these specific versions (if omitted, Spack searches for remote versions)


**Optional arguments**

``-h, --help``
  show this help message and exit

``--keep-stage``
  don't clean up staging area when command completes

``--batch, -b``
  don't ask which versions to checksum

``--latest, -l``
  checksum the latest available version

``--preferred, -p``
  checksum the known Spack preferred version

``--add-to-package, -a``
  add new versions to package

``--verify``
  verify known package checksums

``-j JOBS, --jobs JOBS``
  explicitly set number of parallel jobs


----

.. _spack-ci:

spack ci
--------

manage continuous integration pipelines

.. code-block:: console

    spack ci [-h] SUBCOMMAND ...


**Optional arguments**

``-h, --help``
  show this help message and exit


**Subcommands**

.. hlist::
   :columns: 4

   * :ref:`ci generate <spack-ci-generate>`
   * :ref:`ci rebuild-index <spack-ci-rebuild-index>`
   * :ref:`ci rebuild <spack-ci-rebuild>`
   * :ref:`ci reproduce-build <spack-ci-reproduce-build>`
   * :ref:`ci verify-versions <spack-ci-verify-versions>`


----

.. _spack-ci-generate:

spack ci generate
^^^^^^^^^^^^^^^^^

generate jobs file from a CI-aware spack file

if you want to report the results on CDash, you will need to set the SPACK_CDASH_AUTH_TOKEN
before invoking this command. the value must be the CDash authorization token needed to create
a build group and register all generated jobs under it


.. code-block:: console

    spack ci generate [-hfU] [--output-file OUTPUT_FILE] [--prune-dag | --no-prune-dag]
                  [--prune-unaffected | --no-prune-unaffected] [--prune-externals | --no-prune-externals]
                  [--check-index-only] [--artifacts-root ARTIFACTS_ROOT] [--forward-variable FORWARD_VARIABLE]
                  [--reuse] [--fresh-roots] [--deprecated] [-j JOBS]


**Optional arguments**

``-h, --help``
  show this help message and exit

``--output-file OUTPUT_FILE``
  pathname for the generated gitlab ci yaml file

``--prune-dag``
  skip up-to-date specs

``--no-prune-dag``
  process up-to-date specs

``--prune-unaffected``
  skip up-to-date specs

``--no-prune-unaffected``
  process up-to-date specs

``--prune-externals``
  skip external specs

``--no-prune-externals``
  process external specs

``--check-index-only``
  only check spec state from buildcache indices

``--artifacts-root ARTIFACTS_ROOT``
  path to the root of the artifacts directory

``--forward-variable FORWARD_VARIABLE``
  Environment variables to forward from the generate environment to the generated jobs.

``-f, --force``
  allow changes to concretized specs in spack.lock (in an env)

``-U, --fresh``
  do not reuse installed deps; build newest configuration

``--reuse``
  reuse installed packages/buildcaches when possible

``--fresh-roots, --reuse-deps``
  concretize with fresh roots and reused dependencies

``--deprecated``
  allow concretizer to select deprecated versions

``-j JOBS, --jobs JOBS``
  explicitly set number of parallel jobs


----

.. _spack-ci-rebuild-index:

spack ci rebuild-index
^^^^^^^^^^^^^^^^^^^^^^

rebuild the buildcache index for the remote mirror

use the active, gitlab-enabled environment to rebuild the buildcache index for the associated
mirror


.. code-block:: console

    spack ci rebuild-index [-h]


**Optional arguments**

``-h, --help``
  show this help message and exit


----

.. _spack-ci-rebuild:

spack ci rebuild
^^^^^^^^^^^^^^^^

rebuild a spec if it is not on the remote mirror

check a single spec against the remote mirror, and rebuild it from source if the mirror does
not contain the hash


.. code-block:: console

    spack ci rebuild [-ht] [--fail-fast] [--timeout TIMEOUT] [-j JOBS]


**Optional arguments**

``-h, --help``
  show this help message and exit

``-t, --tests``
  run stand-alone tests after the build

``--fail-fast``
  stop stand-alone tests after the first failure

``--timeout TIMEOUT``
  maximum time (in seconds) that tests are allowed to run

``-j JOBS, --jobs JOBS``
  explicitly set number of parallel jobs


----

.. _spack-ci-reproduce-build:

spack ci reproduce-build
^^^^^^^^^^^^^^^^^^^^^^^^

generate instructions for reproducing the spec rebuild job

artifacts of the provided gitlab pipeline rebuild job's URL will be used to derive
instructions for reproducing the build locally


.. code-block:: console

    spack ci reproduce-build [-hs] [--runtime {docker,podman}] [--working-dir WORKING_DIR] [--use-local-head]
                         [--gpg-file GPG_FILE | --gpg-url GPG_URL]
                         job_url


**Positional arguments**

``job_url``
  URL of GitLab job web page or artifact


**Optional arguments**

``-h, --help``
  show this help message and exit

``--runtime {docker,podman}``
  Container runtime to use.

``--working-dir WORKING_DIR``
  where to unpack artifacts

``-s, --autostart``
  Run docker reproducer automatically

``--use-local-head``
  Use the HEAD of the local Spack instead of reproducing a commit

``--gpg-file GPG_FILE``
  Path to public GPG key for validating binary cache installs

``--gpg-url GPG_URL``
  URL to public GPG key for validating binary cache installs


----

.. _spack-ci-verify-versions:

spack ci verify-versions
^^^^^^^^^^^^^^^^^^^^^^^^

validate version checksum & commits between git refs
This command takes a from_ref and to_ref arguments and
then parses the git diff between the two to determine which packages
have been modified verifies the new checksums inside of them.


.. code-block:: console

    spack ci verify-versions [-h] from_ref to_ref


**Positional arguments**

``from_ref``
  git ref from which start looking at changes

``to_ref``
  git ref to end looking at changes


**Optional arguments**

``-h, --help``
  show this help message and exit


----

.. _spack-clean:

spack clean
-----------

remove temporary build files and/or downloaded archives

.. code-block:: console

    spack clean [-hsdfmpba] ...


**Positional arguments**

``specs``
  one or more package specs


**Optional arguments**

``-h, --help``
  show this help message and exit

``-s, --stage``
  remove all temporary build stages (default)

``-d, --downloads``
  remove cached downloads

``-f, --failures``
  force removal of all install failure tracking markers

``-m, --misc-cache``
  remove long-lived caches, like the virtual package index

``-p, --python-cache``
  remove .pyc, .pyo files and __pycache__ folders

``-b, --bootstrap``
  remove software and configuration needed to bootstrap Spack

``-a, --all``
  equivalent to ``-sdfmp`` (does not include ``--bootstrap``)


----

.. _spack-commands:

spack commands
--------------

list available spack commands

.. code-block:: console

    spack commands [-ha] [--update-completion] [--format {subcommands,rst,names,bash,fish}] [--header FILE]
               [--update FILE]
               ...


**Positional arguments**

``rst_files``
  list of rst files to search for `_cmd-spack-<cmd>` cross-refs


**Optional arguments**

``-h, --help``
  show this help message and exit

``--update-completion``
  regenerate spack's tab completion scripts

``-a, --aliases``
  include command aliases

``--format {subcommands,rst,names,bash,fish}``
  format to be used to print the output (default: names)

``--header FILE``
  prepend contents of FILE to the output (useful for rst format)

``--update FILE``
  write output to the specified file, if any command is newer


----

.. _spack-compiler:

spack compiler
--------------

manage compilers

.. code-block:: console

    spack compiler [-h] SUBCOMMAND ...


**Optional arguments**

``-h, --help``
  show this help message and exit


**Subcommands**

.. hlist::
   :columns: 4

   * :ref:`compiler find <spack-compiler-find>`
   * :ref:`compiler remove <spack-compiler-remove>`
   * :ref:`compiler list <spack-compiler-list>`
   * :ref:`compiler info <spack-compiler-info>`


----

.. _spack-compiler-find:

spack compiler find
^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack compiler find [-h] [--mixed-toolchain | --no-mixed-toolchain]
                    [--scope {defaults,system,site,user,command_line} or env:ENVIRONMENT] [-j JOBS]
                    ...


**Positional arguments**

``add_paths``
  


**Optional arguments**

``-h, --help``
  show this help message and exit

``--mixed-toolchain``
  (DEPRECATED) Allow mixed toolchains (for example: clang, clang++, gfortran)

``--no-mixed-toolchain``
  (DEPRECATED) Do not allow mixed toolchains (for example: clang, clang++, gfortran)

``--scope {defaults,system,site,user,command_line} or env:ENVIRONMENT``
  configuration scope to modify

``-j JOBS, --jobs JOBS``
  explicitly set number of parallel jobs


----

.. _spack-compiler-remove:

spack compiler remove
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack compiler remove [-ha] [--scope {defaults,system,site,user,command_line} or env:ENVIRONMENT] compiler_spec


**Positional arguments**

``compiler_spec``
  


**Optional arguments**

``-h, --help``
  show this help message and exit

``-a, --all``
  remove ALL compilers that match spec

``--scope {defaults,system,site,user,command_line} or env:ENVIRONMENT``
  configuration scope to modify


----

.. _spack-compiler-list:

spack compiler list
^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack compiler list [-h] [--scope {defaults,system,site,user,command_line} or env:ENVIRONMENT] [--remote]


**Optional arguments**

``-h, --help``
  show this help message and exit

``--scope {defaults,system,site,user,command_line} or env:ENVIRONMENT``
  configuration scope to read from

``--remote``
  list also compilers from registered buildcaches


----

.. _spack-compiler-info:

spack compiler info
^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack compiler info [-h] [--scope {defaults,system,site,user,command_line} or env:ENVIRONMENT] compiler_spec


**Positional arguments**

``compiler_spec``
  


**Optional arguments**

``-h, --help``
  show this help message and exit

``--scope {defaults,system,site,user,command_line} or env:ENVIRONMENT``
  configuration scope to read from


----

.. _spack-compilers:

spack compilers
---------------

list available compilers

.. code-block:: console

    spack compilers [-h] [--scope {defaults,system,site,user,command_line} or env:ENVIRONMENT] [--remote]


**Optional arguments**

``-h, --help``
  show this help message and exit

``--scope {defaults,system,site,user,command_line} or env:ENVIRONMENT``
  configuration scope to read/modify

``--remote``
  list also compilers from registered buildcaches


----

.. _spack-concretize:

spack concretize
----------------

concretize an environment and write a lockfile

.. code-block:: console

    spack concretize [-hqfU] [--test {root,all}] [--reuse] [--fresh-roots] [--deprecated] [-j JOBS]


**Optional arguments**

``-h, --help``
  show this help message and exit

``--test {root,all}``
  concretize with test dependencies of only root packages or all packages

``-q, --quiet``
  don't print concretized specs

``-f, --force``
  allow changes to concretized specs in spack.lock (in an env)

``-U, --fresh``
  do not reuse installed deps; build newest configuration

``--reuse``
  reuse installed packages/buildcaches when possible

``--fresh-roots, --reuse-deps``
  concretize with fresh roots and reused dependencies

``--deprecated``
  allow concretizer to select deprecated versions

``-j JOBS, --jobs JOBS``
  explicitly set number of parallel jobs


----

.. _spack-config:

spack config
------------

get and set configuration options

.. code-block:: console

    spack config [-h] [--scope {defaults,system,site,user,command_line} or env:ENVIRONMENT] SUBCOMMAND ...


**Optional arguments**

``-h, --help``
  show this help message and exit

``--scope {defaults,system,site,user,command_line} or env:ENVIRONMENT``
  configuration scope to read/modify


**Subcommands**

.. hlist::
   :columns: 4

   * :ref:`config get <spack-config-get>`
   * :ref:`config blame <spack-config-blame>`
   * :ref:`config edit <spack-config-edit>`
   * :ref:`config list <spack-config-list>`
   * :ref:`config scopes <spack-config-scopes>`
   * :ref:`config add <spack-config-add>`
   * :ref:`config change <spack-config-change>`
   * :ref:`config prefer-upstream <spack-config-prefer-upstream>`
   * :ref:`config remove <spack-config-remove>`
   * :ref:`config update <spack-config-update>`
   * :ref:`config revert <spack-config-revert>`


----

.. _spack-config-get:

spack config get
^^^^^^^^^^^^^^^^

.. code-block:: console

    spack config get [-h] [section]


**Positional arguments**

``section``
  configuration section to print


**Optional arguments**

``-h, --help``
  show this help message and exit


----

.. _spack-config-blame:

spack config blame
^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack config blame [-h] [section]


**Positional arguments**

``section``
  configuration section to print


**Optional arguments**

``-h, --help``
  show this help message and exit


----

.. _spack-config-edit:

spack config edit
^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack config edit [-h] [--print-file] [section]


**Positional arguments**

``section``
  configuration section to edit


**Optional arguments**

``-h, --help``
  show this help message and exit

``--print-file``
  print the file name that would be edited


----

.. _spack-config-list:

spack config list
^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack config list [-h]


**Optional arguments**

``-h, --help``
  show this help message and exit


----

.. _spack-config-scopes:

spack config scopes
^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack config scopes [-hp] [-t scope-type [scope-type ...]] [section]


**Positional arguments**

``section``
  tailor scope path information to the specified section (implies ``--paths``)


**Optional arguments**

``-h, --help``
  show this help message and exit

``-p, --paths``
  show associated paths for appropriate scopes

``-t scope-type [scope-type ...], --type scope-type [scope-type ...]``
  list only scopes of the specified type(s)


----

.. _spack-config-add:

spack config add
^^^^^^^^^^^^^^^^

.. code-block:: console

    spack config add [-h] [-f FILE] [path]


**Positional arguments**

``path``
  colon-separated path to config that should be added, e.g. 'config:default:true'


**Optional arguments**

``-h, --help``
  show this help message and exit

``-f FILE, --file FILE``
  file from which to set all config values


----

.. _spack-config-change:

spack config change
^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack config change [-h] [--match-spec MATCH_SPEC] path


**Positional arguments**

``path``
  colon-separated path to config section with specs


**Optional arguments**

``-h, --help``
  show this help message and exit

``--match-spec MATCH_SPEC``
  only change constraints that match this


----

.. _spack-config-prefer-upstream:

spack config prefer-upstream
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack config prefer-upstream [-h] [--local]


**Optional arguments**

``-h, --help``
  show this help message and exit

``--local``
  set packages preferences based on local installs, rather than upstream


----

.. _spack-config-remove:

spack config remove
^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack config remove [-h] path


**Positional arguments**

``path``
  colon-separated path to config that should be removed, e.g. 'config:default:true'


**Optional arguments**

``-h, --help``
  show this help message and exit


----

.. _spack-config-update:

spack config update
^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack config update [-hy] section


**Positional arguments**

``section``
  section to update


**Optional arguments**

``-h, --help``
  show this help message and exit

``-y, --yes-to-all``
  assume "yes" is the answer to every confirmation request


----

.. _spack-config-revert:

spack config revert
^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack config revert [-hy] section


**Positional arguments**

``section``
  section to update


**Optional arguments**

``-h, --help``
  show this help message and exit

``-y, --yes-to-all``
  assume "yes" is the answer to every confirmation request


----

.. _spack-containerize:

spack containerize
------------------

creates recipes to build images for different container runtimes

.. code-block:: console

    spack containerize [-h] [--list-os] [--last-stage {bootstrap,build,final}]


**Optional arguments**

``-h, --help``
  show this help message and exit

``--list-os``
  list all the OS that can be used in the bootstrap phase and exit

``--last-stage {bootstrap,build,final}``
  last stage in the container recipe


----

.. _spack-create:

spack create
------------

create a new package file

.. code-block:: console

    spack create [-hfb] [--keep-stage] [-n NAME] [-t TEMPLATE] [-r REPO] [-N NAMESPACE] [--skip-editor] [url]


**Positional arguments**

``url``
  url of package archive


**Optional arguments**

``-h, --help``
  show this help message and exit

``--keep-stage``
  don't clean up staging area when command completes

``-n NAME, --name NAME``
  name of the package to create

``-t TEMPLATE, --template TEMPLATE``
  build system template to use

``-r REPO, --repo REPO``
  path to a repository where the package should be created

``-N NAMESPACE, --namespace NAMESPACE``
  specify a namespace for the package

``-f, --force``
  overwrite any existing package file with the same name

``--skip-editor``
  skip the edit session for the package (e.g., automation)

``-b, --batch``
  don't ask which versions to checksum


----

.. _spack-debug:

spack debug
-----------

debugging commands for troubleshooting Spack

.. code-block:: console

    spack debug [-h] SUBCOMMAND ...


**Optional arguments**

``-h, --help``
  show this help message and exit


**Subcommands**

.. hlist::
   :columns: 4

   * :ref:`debug report <spack-debug-report>`


----

.. _spack-debug-report:

spack debug report
^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack debug report [-h]


**Optional arguments**

``-h, --help``
  show this help message and exit


----

.. _spack-deconcretize:

spack deconcretize
------------------

remove specs from the concretized lockfile of an environment

.. code-block:: console

    spack deconcretize [-hya] [--root] ...


**Positional arguments**

``specs``
  one or more package specs


**Optional arguments**

``-h, --help``
  show this help message and exit

``--root``
  deconcretize only specific environment roots

``-y, --yes-to-all``
  assume "yes" is the answer to every confirmation request

``-a, --all``
  deconcretize ALL specs that match each supplied spec


----

.. _spack-dependencies:

spack dependencies
------------------

show dependencies of a package

.. code-block:: console

    spack dependencies [-hitV] [--deptype DEPTYPE] ...


**Positional arguments**

``spec``
  package spec


**Optional arguments**

``-h, --help``
  show this help message and exit

``-i, --installed``
  list installed dependencies of an installed spec instead of possible dependencies of a package

``-t, --transitive``
  show all transitive dependencies

``--deptype DEPTYPE``
  comma-separated list of deptypes to traverse (default=build,link,run,test)

``-V, --no-expand-virtuals``
  do not expand virtual dependencies


----

.. _spack-dependents:

spack dependents
----------------

show packages that depend on another

.. code-block:: console

    spack dependents [-hit] ...


**Positional arguments**

``spec``
  package spec


**Optional arguments**

``-h, --help``
  show this help message and exit

``-i, --installed``
  list installed dependents of an installed spec instead of possible dependents of a package

``-t, --transitive``
  show all transitive dependents


----

.. _spack-deprecate:

spack deprecate
---------------

replace one package with another via symlinks

.. code-block:: console

    spack deprecate [-hy] [-d | -D] [-i | -I] [-l {soft,hard}] ...


**Positional arguments**

``specs``
  spec to deprecate and spec to use as deprecator


**Optional arguments**

``-h, --help``
  show this help message and exit

``-y, --yes-to-all``
  assume "yes" is the answer to every confirmation request

``-d, --dependencies``
  deprecate dependencies (default)

``-D, --no-dependencies``
  do not deprecate dependencies

``-i, --install-deprecator``
  concretize and install deprecator spec

``-I, --no-install-deprecator``
  deprecator spec must already be installed (default)

``-l {soft,hard}, --link-type {soft,hard}``
  (deprecated)


----

.. _spack-dev-build:

spack dev-build
---------------

developer build: build from code in current working directory

.. code-block:: console

    spack dev-build [-hniqfU] [-j JOBS] [-d SOURCE_PATH] [--keep-prefix] [--skip-patch] [--drop-in SHELL]
                [--test {root,all}] [-b BEFORE | -u UNTIL] [--clean | --dirty] [--reuse] [--fresh-roots]
                [--deprecated]
                ...


**Positional arguments**

``spec``
  package spec


**Optional arguments**

``-h, --help``
  show this help message and exit

``-j JOBS, --jobs JOBS``
  explicitly set number of parallel jobs

``-n, --no-checksum``
  do not use checksums to verify downloaded files (unsafe)

``-d SOURCE_PATH, --source-path SOURCE_PATH``
  path to source directory (defaults to the current directory)

``-i, --ignore-dependencies``
  do not try to install dependencies of requested packages

``--keep-prefix``
  do not remove the install prefix if installation fails

``--skip-patch``
  skip patching for the developer build

``-q, --quiet``
  do not display verbose build output while installing

``--drop-in SHELL``
  drop into a build environment in a new shell, e.g., bash

``--test {root,all}``
  run tests on only root packages or all packages

``-b BEFORE, --before BEFORE``
  phase to stop before when installing (default None)

``-u UNTIL, --until UNTIL``
  phase to stop after when installing (default None)

``--clean``
  unset harmful variables in the build environment (default)

``--dirty``
  preserve user environment in spack's build environment (danger!)

``-f, --force``
  allow changes to concretized specs in spack.lock (in an env)

``-U, --fresh``
  do not reuse installed deps; build newest configuration

``--reuse``
  reuse installed packages/buildcaches when possible

``--fresh-roots, --reuse-deps``
  concretize with fresh roots and reused dependencies

``--deprecated``
  allow concretizer to select deprecated versions


----

.. _spack-develop:

spack develop
-------------

add a spec to an environment's dev-build information

.. code-block:: console

    spack develop [-hr] [-p PATH] [-b BUILD_DIRECTORY] [--no-clone | --clone] [-f FORCE] ...


**Positional arguments**

``spec``
  package spec


**Optional arguments**

``-h, --help``
  show this help message and exit

``-p PATH, --path PATH``
  source location of package

``-b BUILD_DIRECTORY, --build-directory BUILD_DIRECTORY``
  build directory for the package

``--no-clone``
  do not clone, the package already exists at the source path

``--clone``
  (default) clone the package unless the path already exists, use ``--force`` to overwrite

``-f FORCE, --force FORCE``
  remove any files or directories that block cloning source code

``-r, --recursive``
  traverse nodes of the graph to mark everything up to the root as a develop spec


----

.. _spack-diff:

spack diff
----------

compare two specs

.. code-block:: console

    spack diff [-h] [--json] [--first] [-a ATTRIBUTE] [--ignore IGNORE] ...


**Positional arguments**

``specs``
  one or more package specs


**Optional arguments**

``-h, --help``
  show this help message and exit

``--json``
  dump json output instead of pretty printing

``--first``
  load the first match if multiple packages match the spec

``-a ATTRIBUTE, --attribute ATTRIBUTE``
  select the attributes to show (defaults to all)

``--ignore IGNORE``
  omit diffs related to these dependencies


----

.. _spack-docs:

spack docs
----------

open spack documentation in a web browser

.. code-block:: console

    spack docs [-h]


**Optional arguments**

``-h, --help``
  show this help message and exit


----

.. _spack-edit:

spack edit
----------

open package files in ``$EDITOR``

.. code-block:: console

    spack edit [-h] [-b | -c | -d | -t | -m] [-r REPO] [-N NAMESPACE] [package ...]


**Positional arguments**

``package``
  package name


**Optional arguments**

``-h, --help``
  show this help message and exit

``-b, --build-system``
  edit the build system with the supplied name or fullname

``-c, --command``
  edit the command with the supplied name

``-d, --docs``
  edit the docs with the supplied name

``-t, --test``
  edit the test with the supplied name

``-m, --module``
  edit the main spack module with the supplied name

``-r REPO, --repo REPO``
  path to repo to edit package or build system in

``-N NAMESPACE, --namespace NAMESPACE``
  namespace of package or build system to edit


----

.. _spack-env:

spack env
---------

manage virtual environments

.. code-block:: console

    spack env [-h] SUBCOMMAND ...


**Optional arguments**

``-h, --help``
  show this help message and exit


**Subcommands**

.. hlist::
   :columns: 4

   * :ref:`env activate <spack-env-activate>`
   * :ref:`env deactivate <spack-env-deactivate>`
   * :ref:`env create <spack-env-create>`
   * :ref:`env remove <spack-env-remove>`
   * :ref:`env rename <spack-env-rename>`
   * :ref:`env list <spack-env-list>`
   * :ref:`env status <spack-env-status>`
   * :ref:`env loads <spack-env-loads>`
   * :ref:`env view <spack-env-view>`
   * :ref:`env update <spack-env-update>`
   * :ref:`env revert <spack-env-revert>`
   * :ref:`env depfile <spack-env-depfile>`
   * :ref:`env track <spack-env-track>`
   * :ref:`env untrack <spack-env-untrack>`


----

.. _spack-env-activate:

spack env activate
^^^^^^^^^^^^^^^^^^

set the active environment

.. code-block:: console

    spack env activate [-hpd] [--sh | --csh | --fish | --bat | --pwsh] [-v name | -V] [--temp] [--create]
                   [--envfile [ENVFILE]] [--keep-relative]
                   [env]


**Positional arguments**

``env``
  name or directory of the environment being activated


**Optional arguments**

``-h, --help``
  show this help message and exit

``--sh``
  print sh commands to activate the environment

``--csh``
  print csh commands to activate the environment

``--fish``
  print fish commands to activate the environment

``--bat``
  print bat commands to activate the environment

``--pwsh``
  print powershell commands to activate environment

``-v name, --with-view name``
  set runtime environment variables for the named view

``-V, --without-view``
  do not set runtime environment variables for any view

``-p, --prompt``
  add the active environment to the command line prompt

``--temp``
  create and activate in a temporary directory

``--create``
  create and activate the environment if it doesn't exist

``--envfile [ENVFILE]``
  manifest or lock file (ends with '.json' or '.lock')

``--keep-relative``
  copy envfile's relative develop paths verbatim when create

``-d, --dir``
  activate environment based on the directory supplied


----

.. _spack-env-deactivate:

spack env deactivate
^^^^^^^^^^^^^^^^^^^^

deactivate the active environment

.. code-block:: console

    spack env deactivate [-h] [--sh | --csh | --fish | --bat | --pwsh]


**Optional arguments**

``-h, --help``
  show this help message and exit

``--sh``
  print sh commands to deactivate the environment

``--csh``
  print csh commands to deactivate the environment

``--fish``
  print fish commands to activate the environment

``--bat``
  print bat commands to activate the environment

``--pwsh``
  print pwsh commands to activate the environment


----

.. _spack-env-create:

spack env create
^^^^^^^^^^^^^^^^

create a new environment

    create a new environment or, optionally, copy an existing environment

    a manifest file results in a new abstract environment while a lock file
    creates a new concrete environment
    

.. code-block:: console

    spack env create [-hd] [--keep-relative] [--without-view | --with-view WITH_VIEW]
                 [--include-concrete INCLUDE_CONCRETE]
                 env [envfile]


**Positional arguments**

``env``
  name or directory of the new environment

``envfile``
  manifest or lock file (ends with '.json' or '.lock')


**Optional arguments**

``-h, --help``
  show this help message and exit

``-d, --dir``
  create an environment in a specific directory

``--keep-relative``
  copy envfile's relative develop paths verbatim

``--without-view``
  do not maintain a view for this environment

``--with-view WITH_VIEW``
  maintain view at WITH_VIEW (vs. environment's directory)

``--include-concrete INCLUDE_CONCRETE``
  copy concrete specs from INCLUDE_CONCRETE's environment


----

.. _spack-env-remove:

spack env remove
^^^^^^^^^^^^^^^^

remove managed environment(s)

    remove existing environment(s) managed by Spack

    directory environments and manifests embedded in repositories must be
    removed manually
    

.. code-block:: console

    spack env remove [-hyf] env [env ...]


**Positional arguments**

``env``
  name(s) of the environment(s) being removed


**Optional arguments**

``-h, --help``
  show this help message and exit

``-y, --yes-to-all``
  assume "yes" is the answer to every confirmation request

``-f, --force``
  force removal even when included in other environment(s)


----

.. _spack-env-rename:

spack env rename
^^^^^^^^^^^^^^^^

rename an existing environment

    rename a managed environment or move an independent/directory environment

    operation cannot be performed to or from an active environment
    

.. code-block:: console

    spack env rename [-hdf] from to


**Positional arguments**

``from``
  current name or directory of the environment

``to``
  new name or directory for the environment


**Optional arguments**

``-h, --help``
  show this help message and exit

``-d, --dir``
  positional arguments are environment directory paths

``-f, --force``
  force renaming even if overwriting an existing environment


----

.. _spack-env-list:

spack env list
^^^^^^^^^^^^^^

list all managed environments

.. code-block:: console

    spack env list [-h]


**Optional arguments**

``-h, --help``
  show this help message and exit


----

.. _spack-env-status:

spack env status
^^^^^^^^^^^^^^^^

print active environment status

.. code-block:: console

    spack env status [-h]


**Optional arguments**

``-h, --help``
  show this help message and exit


----

.. _spack-env-loads:

spack env loads
^^^^^^^^^^^^^^^

list modules for an installed environment '(see spack module loads)'

.. code-block:: console

    spack env loads [-hr] [-n MODULE_SET_NAME] [-m {tcl,lmod}] [--input-only] [-p PREFIX] [-x EXCLUDE]


**Optional arguments**

``-h, --help``
  show this help message and exit

``-n MODULE_SET_NAME, --module-set-name MODULE_SET_NAME``
  module set for which to generate load operations

``-m {tcl,lmod}, --module-type {tcl,lmod}``
  type of module system to generate loads for

``--input-only``
  generate input for module command (instead of a shell script)

``-p PREFIX, --prefix PREFIX``
  prepend to module names when issuing module load commands

``-x EXCLUDE, --exclude EXCLUDE``
  exclude package from output; may be specified multiple times

``-r, --dependencies``
  recursively traverse spec dependencies


----

.. _spack-env-view:

spack env view
^^^^^^^^^^^^^^

manage the environment's view

    provide the path when enabling a view with a non-default path
    

.. code-block:: console

    spack env view [-h] {regenerate,enable,disable} [view_path]


**Positional arguments**

``{regenerate,enable,disable}``
  action to take for the environment's view

``view_path``
  view's non-default path when enabling it


**Optional arguments**

``-h, --help``
  show this help message and exit


----

.. _spack-env-update:

spack env update
^^^^^^^^^^^^^^^^

update the environment manifest to the latest schema format

    update the environment to the latest schema format, which may not be
    readable by older versions of spack

    a backup copy of the manifest is retained in case there is a need to revert
    this operation
    

.. code-block:: console

    spack env update [-hy] env


**Positional arguments**

``env``
  name or directory of the environment


**Optional arguments**

``-h, --help``
  show this help message and exit

``-y, --yes-to-all``
  assume "yes" is the answer to every confirmation request


----

.. _spack-env-revert:

spack env revert
^^^^^^^^^^^^^^^^

restore the environment manifest to its previous format

    revert the environment's manifest to the schema format from its last
    'spack env update'

    the current manifest will be overwritten by the backup copy and the backup
    copy will be removed
    

.. code-block:: console

    spack env revert [-hy] env


**Positional arguments**

``env``
  name or directory of the environment


**Optional arguments**

``-h, --help``
  show this help message and exit

``-y, --yes-to-all``
  assume "yes" is the answer to every confirmation request


----

.. _spack-env-depfile:

spack env depfile
^^^^^^^^^^^^^^^^^

generate a depfile to exploit parallel builds across specs

    requires the active environment to be concrete
    

.. code-block:: console

    spack env depfile [-h] [--make-prefix TARGET] [--make-disable-jobserver]
                  [--use-buildcache [{auto,only,never},][package:{auto,only,never},][dependencies:{auto,only,never}]]
                  [-o FILE] [-G {make}]
                  ...


**Positional arguments**

``specs``
  limit the generated file to matching specs


**Optional arguments**

``-h, --help``
  show this help message and exit

``--make-prefix TARGET, --make-target-prefix TARGET``
  prefix Makefile targets/variables with <TARGET>/<name>,

``--make-disable-jobserver``
  disable POSIX jobserver support

``--use-buildcache [{auto,only,never},][package:{auto,only,never},][dependencies:{auto,only,never}]``
  use `only` to prune redundant build dependencies

``-o FILE, --output FILE``
  write the depfile to FILE rather than to stdout

``-G {make}, --generator {make}``
  specify the depfile type (only supports `make`)


----

.. _spack-env-track:

spack env track
^^^^^^^^^^^^^^^

track an environment from a directory in Spack

.. code-block:: console

    spack env track [-hy] [-n NAME] dir


**Positional arguments**

``dir``
  path to environment


**Optional arguments**

``-h, --help``
  show this help message and exit

``-n NAME, --name NAME``
  custom environment name

``-y, --yes-to-all``
  assume "yes" is the answer to every confirmation request


----

.. _spack-env-untrack:

spack env untrack
^^^^^^^^^^^^^^^^^

track an environment from a directory in Spack

.. code-block:: console

    spack env untrack [-hfy] env [env ...]


**Positional arguments**

``env``
  tracked environment name


**Optional arguments**

``-h, --help``
  show this help message and exit

``-f, --force``
  force unlink even when environment is active

``-y, --yes-to-all``
  assume "yes" is the answer to every confirmation request


----

.. _spack-extensions:

spack extensions
----------------

list extensions for package

.. code-block:: console

    spack extensions [-hlLdp] [-s {packages,installed,all}] ...


**Positional arguments**

``extendable``
  spec of package to list extensions for


**Optional arguments**

``-h, --help``
  show this help message and exit

``-l, --long``
  show dependency hashes as well as versions

``-L, --very-long``
  show full dependency hashes as well as versions

``-d, --deps``
  output dependencies along with found specs

``-p, --paths``
  show paths to package install directories

``-s {packages,installed,all}, --show {packages,installed,all}``
  show only part of output


----

.. _spack-external:

spack external
--------------

manage external packages in Spack configuration

.. code-block:: console

    spack external [-h] SUBCOMMAND ...


**Optional arguments**

``-h, --help``
  show this help message and exit


**Subcommands**

.. hlist::
   :columns: 4

   * :ref:`external find <spack-external-find>`
   * :ref:`external list <spack-external-list>`
   * :ref:`external read-cray-manifest <spack-external-read-cray-manifest>`


----

.. _spack-external-find:

spack external find
^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack external find [-h] [--not-buildable] [--exclude EXCLUDE] [-p PATH]
                    [--scope {defaults,system,site,user,command_line} or env:ENVIRONMENT] [--all] [-t TAG] [-j JOBS]
                    ...


**Positional arguments**

``packages``
  


**Optional arguments**

``-h, --help``
  show this help message and exit

``--not-buildable``
  packages with detected externals won't be built with Spack

``--exclude EXCLUDE``
  packages to exclude from search

``-p PATH, --path PATH``
  one or more alternative search paths for finding externals

``--scope {defaults,system,site,user,command_line} or env:ENVIRONMENT``
  configuration scope to modify

``--all``
  search for all packages that Spack knows about

``-t TAG, --tag TAG``
  filter a package query by tag (multiple use allowed)

``-j JOBS, --jobs JOBS``
  explicitly set number of parallel jobs


----

.. _spack-external-list:

spack external list
^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack external list [-h]


**Optional arguments**

``-h, --help``
  show this help message and exit


----

.. _spack-external-read-cray-manifest:

spack external read-cray-manifest
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack external read-cray-manifest [-h] [--file FILE] [--directory DIRECTORY] [--ignore-default-dir] [--dry-run]
                                  [--fail-on-error]


**Optional arguments**

``-h, --help``
  show this help message and exit

``--file FILE``
  specify a location other than the default

``--directory DIRECTORY``
  specify a directory storing a group of manifest files

``--ignore-default-dir``
  ignore the default directory of manifest files

``--dry-run``
  don't modify DB with files that are read

``--fail-on-error``
  if a manifest file cannot be parsed, fail and report the full stack trace


----

.. _spack-fetch:

spack fetch
-----------

fetch archives for packages

.. code-block:: console

    spack fetch [-hnmDfU] [--reuse] [--fresh-roots] [--deprecated] ...


**Positional arguments**

``specs``
  one or more package specs


**Optional arguments**

``-h, --help``
  show this help message and exit

``-n, --no-checksum``
  do not use checksums to verify downloaded files (unsafe)

``-m, --missing``
  fetch only missing (not yet installed) dependencies

``-D, --dependencies``
  also fetch all dependencies

``-f, --force``
  allow changes to concretized specs in spack.lock (in an env)

``-U, --fresh``
  do not reuse installed deps; build newest configuration

``--reuse``
  reuse installed packages/buildcaches when possible

``--fresh-roots, --reuse-deps``
  concretize with fresh roots and reused dependencies

``--deprecated``
  allow concretizer to select deprecated versions


----

.. _spack-find:

spack find
----------

list and search installed packages

.. code-block:: console

    spack find [-hIdplLNrcfumv] [--format FORMAT | -H | --json] [--specfile-format] [--groups] [--no-groups] [-t TAG]
           [--show-full-compiler] [-x | -X] [--loaded] [-M | --only-deprecated] [--deprecated]
           [--install-tree INSTALL_TREE] [--start-date START_DATE] [--end-date END_DATE]
           ...


**Positional arguments**

``installed_specs``
  constraint to select a subset of installed packages


**Optional arguments**

``-h, --help``
  show this help message and exit

``--format FORMAT``
  output specs with the specified format string

``-H, --hashes``
  same as ``--format {/hash}``; use with ``xargs`` or ``$()``

``--json``
  output specs as machine-readable json records

``-I, --install-status``
  show install status of packages

``--specfile-format``
  show the specfile format for installed deps 

``-d, --deps``
  output dependencies along with found specs

``-p, --paths``
  show paths to package install directories

``--groups``
  display specs in arch/compiler groups (default on)

``--no-groups``
  do not group specs by arch/compiler

``-l, --long``
  show dependency hashes as well as versions

``-L, --very-long``
  show full dependency hashes as well as versions

``-t TAG, --tag TAG``
  filter a package query by tag (multiple use allowed)

``-N, --namespaces``
  show fully qualified package names

``-r, --only-roots``
  don't show full list of installed specs in an environment

``-c, --show-concretized``
  show concretized specs in an environment

``-f, --show-flags``
  show spec compiler flags

``--show-full-compiler``
  (DEPRECATED) show full compiler specs. Currently it's a no-op

``-x, --explicit``
  show only specs that were installed explicitly

``-X, --implicit``
  show only specs that were installed as dependencies

``-u, --unknown``
  show only specs Spack does not have a package for

``-m, --missing``
  show missing dependencies as well as installed specs

``-v, --variants``
  show variants in output (can be long)

``--loaded``
  show only packages loaded in the user environment

``-M, --only-missing``
  show only missing dependencies

``--only-deprecated``
  show only deprecated packages

``--deprecated``
  show deprecated packages as well as installed specs

``--install-tree INSTALL_TREE``
  Install trees to query: 'all' (default), 'local', 'upstream', upstream name or path

``--start-date START_DATE``
  earliest date of installation [YYYY-MM-DD]

``--end-date END_DATE``
  latest date of installation [YYYY-MM-DD]


----

.. _spack-gc:

spack gc
--------

remove specs that are now no longer needed

.. code-block:: console

    spack gc [-hEby] [-e ENV] ...


**Positional arguments**

``installed_specs``
  constraint to select a subset of installed packages


**Optional arguments**

``-h, --help``
  show this help message and exit

``-E, --except-any-environment``
  remove everything unless needed by an environment

``-e ENV, --except-environment ENV``
  remove everything unless needed by specified environment

``-b, --keep-build-dependencies``
  do not remove installed build-only dependencies of roots

``-y, --yes-to-all``
  assume "yes" is the answer to every confirmation request


----

.. _spack-gpg:

spack gpg
---------

handle GPG actions for spack

.. code-block:: console

    spack gpg [-h] SUBCOMMAND ...


**Optional arguments**

``-h, --help``
  show this help message and exit


**Subcommands**

.. hlist::
   :columns: 4

   * :ref:`gpg verify <spack-gpg-verify>`
   * :ref:`gpg trust <spack-gpg-trust>`
   * :ref:`gpg untrust <spack-gpg-untrust>`
   * :ref:`gpg sign <spack-gpg-sign>`
   * :ref:`gpg create <spack-gpg-create>`
   * :ref:`gpg list <spack-gpg-list>`
   * :ref:`gpg init <spack-gpg-init>`
   * :ref:`gpg export <spack-gpg-export>`
   * :ref:`gpg publish <spack-gpg-publish>`


----

.. _spack-gpg-verify:

spack gpg verify
^^^^^^^^^^^^^^^^

.. code-block:: console

    spack gpg verify [-h] ... [signature]


**Positional arguments**

``installed_spec``
  installed package spec

``signature``
  the signature file


**Optional arguments**

``-h, --help``
  show this help message and exit


----

.. _spack-gpg-trust:

spack gpg trust
^^^^^^^^^^^^^^^

.. code-block:: console

    spack gpg trust [-h] keyfile


**Positional arguments**

``keyfile``
  add a key to the trust store


**Optional arguments**

``-h, --help``
  show this help message and exit


----

.. _spack-gpg-untrust:

spack gpg untrust
^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack gpg untrust [-h] [--signing] keys [keys ...]


**Positional arguments**

``keys``
  remove keys from the trust store


**Optional arguments**

``-h, --help``
  show this help message and exit

``--signing``
  allow untrusting signing keys


----

.. _spack-gpg-sign:

spack gpg sign
^^^^^^^^^^^^^^

.. code-block:: console

    spack gpg sign [-h] [--output DEST] [--key KEY] [--clearsign] ...


**Positional arguments**

``installed_spec``
  installed package spec


**Optional arguments**

``-h, --help``
  show this help message and exit

``--output DEST``
  the directory to place signatures

``--key KEY``
  the key to use for signing

``--clearsign``
  if specified, create a clearsign signature


----

.. _spack-gpg-create:

spack gpg create
^^^^^^^^^^^^^^^^

.. code-block:: console

    spack gpg create [-h] [--comment COMMENT] [--expires EXPIRATION] [--export DEST] [--export-secret DEST] name email


**Positional arguments**

``name``
  the name to use for the new key

``email``
  the email address to use for the new key


**Optional arguments**

``-h, --help``
  show this help message and exit

``--comment COMMENT``
  a description for the intended use of the key

``--expires EXPIRATION``
  when the key should expire

``--export DEST``
  export the public key to a file

``--export-secret DEST``
  export the private key to a file


----

.. _spack-gpg-list:

spack gpg list
^^^^^^^^^^^^^^

.. code-block:: console

    spack gpg list [-h] [--trusted] [--signing]


**Optional arguments**

``-h, --help``
  show this help message and exit

``--trusted``
  list trusted keys

``--signing``
  list keys which may be used for signing


----

.. _spack-gpg-init:

spack gpg init
^^^^^^^^^^^^^^

.. code-block:: console

    spack gpg init [-h]


**Optional arguments**

``-h, --help``
  show this help message and exit

``--from DIR``
  


----

.. _spack-gpg-export:

spack gpg export
^^^^^^^^^^^^^^^^

.. code-block:: console

    spack gpg export [-h] [--secret] location [keys ...]


**Positional arguments**

``location``
  where to export keys

``keys``
  the keys to export (all public keys if unspecified)


**Optional arguments**

``-h, --help``
  show this help message and exit

``--secret``
  export secret keys


----

.. _spack-gpg-publish:

spack gpg publish
^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack gpg publish [-h] (-d directory | -m mirror-name | --mirror-url mirror-url) [--update-index] [keys ...]


**Positional arguments**

``keys``
  keys to publish (all public keys if unspecified)


**Optional arguments**

``-h, --help``
  show this help message and exit

``-d directory, --directory directory``
  local directory where keys will be published

``-m mirror-name, --mirror-name mirror-name``
  name of the mirror where keys will be published

``--mirror-url mirror-url``
  URL of the mirror where keys will be published

``--update-index, --rebuild-index``
  regenerate buildcache key index after publishing key(s)


----

.. _spack-graph:

spack graph
-----------

generate graphs of package dependency relationships

.. code-block:: console

    spack graph [-hsci] [-a | -d] [--deptype DEPTYPE] ...


**Positional arguments**

``specs``
  one or more package specs


**Optional arguments**

``-h, --help``
  show this help message and exit

``-a, --ascii``
  draw graph as ascii to stdout (default)

``-d, --dot``
  generate graph in dot format and print to stdout

``-s, --static``
  graph static (possible) deps, don't concretize (implies ``--dot``)

``-c, --color``
  use different colors for different dependency types

``-i, --installed``
  graph specs from the DB

``--deptype DEPTYPE``
  comma-separated list of deptypes to traverse (default=build,link,run,test)


----

.. _spack-help:

spack help
----------

get help on spack and its commands

.. code-block:: console

    spack help [-ha] [--spec help_command]


**Positional arguments**

``help_command``
  command to get help on


**Optional arguments**

``-h, --help``
  show this help message and exit

``-a, --all``
  list all available commands and options

``--spec``
  help on the package specification syntax


----

.. _spack-info:

spack info
----------

get detailed information on a particular package

.. code-block:: console

    spack info [-ha] [--detectable] [--maintainers] [--namespace] [--no-dependencies] [--no-variants] [--no-versions]
           [--phases] [--tags] [--tests] [--virtuals] [--variants-by-name]
           package


**Positional arguments**

``package``
  package name


**Optional arguments**

``-h, --help``
  show this help message and exit

``-a, --all``
  output all package information

``--detectable``
  output information on external detection

``--maintainers``
  output package maintainers

``--namespace``
  output package namespace

``--no-dependencies``
  do not output build, link, and run package dependencies

``--no-variants``
  do not output variants

``--no-versions``
  do not output versions

``--phases``
  output installation phases

``--tags``
  output package tags

``--tests``
  output relevant build-time and stand-alone tests

``--virtuals``
  output virtual packages

``--variants-by-name``
  list variants in strict name order; don't group by condition


----

.. _spack-install:

spack install
-------------

build and install packages

.. code-block:: console

    spack install [-hnvyfU] [--only {package,dependencies}] [-u UNTIL] [-p CONCURRENT_PACKAGES] [-j JOBS] [--overwrite]
              [--fail-fast] [--keep-prefix] [--keep-stage] [--dont-restage]
              [--use-cache | --no-cache | --cache-only | --use-buildcache [{auto,only,never},][package:{auto,only,never},][dependencies:{auto,only,never}]]
              [--include-build-deps] [--no-check-signature] [--show-log-on-error] [--source] [--fake]
              [--only-concrete] [--add | --no-add] [--clean | --dirty] [--test {root,all}]
              [--log-format {junit,cdash}] [--log-file LOG_FILE] [--help-cdash] [--reuse] [--fresh-roots]
              [--deprecated]
              ...


**Positional arguments**

``spec``
  package spec


**Optional arguments**

``-h, --help``
  show this help message and exit

``--only {package,dependencies}``
  select the mode of installation

``-u UNTIL, --until UNTIL``
  phase to stop after when installing (default None)

``-p CONCURRENT_PACKAGES, --concurrent-packages CONCURRENT_PACKAGES``
  maximum number of packages to build concurrently

``-j JOBS, --jobs JOBS``
  explicitly set number of parallel jobs

``--overwrite``
  reinstall an existing spec, even if it has dependents

``--fail-fast``
  stop all builds if any build fails (default is best effort)

``--keep-prefix``
  don't remove the install prefix if installation fails

``--keep-stage``
  don't remove the build stage if installation succeeds

``--dont-restage``
  if a partial install is detected, don't delete prior state

``--use-cache``
  check for pre-built Spack packages in mirrors (default)

``--no-cache``
  do not check for pre-built Spack packages in mirrors

``--cache-only``
  only install package from binary mirrors

``--use-buildcache [{auto,only,never},][package:{auto,only,never},][dependencies:{auto,only,never}]``
  select the mode of buildcache for the 'package' and 'dependencies'

``--include-build-deps``
  include build deps when installing from cache, useful for CI pipeline troubleshooting

``--no-check-signature``
  do not check signatures of binary packages (override mirror config)

``--show-log-on-error``
  print full build log to stderr if build fails

``--source``
  install source files in prefix

``-n, --no-checksum``
  do not use checksums to verify downloaded files (unsafe)

``-v, --verbose``
  display verbose build output while installing

``--fake``
  fake install for debug purposes

``--only-concrete``
  (with environment) only install already concretized specs

``--add``
  (with environment) add spec to the environment as a root

``--no-add``
  (with environment) do not add spec to the environment as a root

``--clean``
  unset harmful variables in the build environment (default)

``--dirty``
  preserve user environment in spack's build environment (danger!)

``--test {root,all}``
  run tests on only root packages or all packages

``--log-format {junit,cdash}``
  format to be used for log files

``--log-file LOG_FILE``
  filename for the log file

``--help-cdash``
  show usage instructions for CDash reporting

``--cdash-upload-url CDASH_UPLOAD_URL``
  

``--cdash-build CDASH_BUILD``
  

``--cdash-site CDASH_SITE``
  

``--cdash-track CDASH_TRACK``
  

``--cdash-buildstamp CDASH_BUILDSTAMP``
  

``-y, --yes-to-all``
  assume "yes" is the answer to every confirmation request

``-f, --force``
  allow changes to concretized specs in spack.lock (in an env)

``-U, --fresh``
  do not reuse installed deps; build newest configuration

``--reuse``
  reuse installed packages/buildcaches when possible

``--fresh-roots, --reuse-deps``
  concretize with fresh roots and reused dependencies

``--deprecated``
  allow concretizer to select deprecated versions


----

.. _spack-license:

spack license
-------------

list and check license headers on files in spack

.. code-block:: console

    spack license [-h] [--root ROOT] SUBCOMMAND ...


**Optional arguments**

``-h, --help``
  show this help message and exit

``--root ROOT``
  scan a different prefix for license issues


**Subcommands**

.. hlist::
   :columns: 4

   * :ref:`license list-files <spack-license-list-files>`
   * :ref:`license verify <spack-license-verify>`


----

.. _spack-license-list-files:

spack license list-files
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack license list-files [-h]


**Optional arguments**

``-h, --help``
  show this help message and exit


----

.. _spack-license-verify:

spack license verify
^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack license verify [-h]


**Optional arguments**

``-h, --help``
  show this help message and exit


----

.. _spack-list:

spack list
----------

list and search available packages

.. code-block:: console

    spack list [-hdv] [-r REPOS] [--format {name_only,version_json,html}] [-t TAG] [--count | --update FILE] ...


**Positional arguments**

``filter``
  optional case-insensitive glob patterns to filter results


**Optional arguments**

``-h, --help``
  show this help message and exit

``-r REPOS, --repo REPOS, -N REPOS, --namespace REPOS``
  only list packages from the specified repo/namespace

``-d, --search-description``
  filtering will also search the description for a match

``--format {name_only,version_json,html}``
  format to be used to print the output [default: name_only]

``-v, --virtuals``
  include virtual packages in list

``-t TAG, --tag TAG``
  filter a package query by tag (multiple use allowed)

``--count``
  display the number of packages that would be listed

``--update FILE``
  write output to the specified file, if any package is newer


----

.. _spack-load:

spack load
----------

add package to the user environment

.. code-block:: console

    spack load [-h] [--sh | --csh | --fish | --bat | --pwsh] [--first] [--list] ...


**Positional arguments**

``installed_specs``
  constraint to select a subset of installed packages


**Optional arguments**

``-h, --help``
  show this help message and exit

``--sh``
  print sh commands to load the package

``--csh``
  print csh commands to load the package

``--fish``
  print fish commands to load the package

``--bat``
  print bat commands to load the package

``--pwsh``
  print pwsh commands to load the package

``--first``
  load the first match if multiple packages match the spec

``--list``
  show loaded packages: same as ``spack find --loaded``


----

.. _spack-location:

spack location
--------------

print out locations of packages and spack directories

.. code-block:: console

    spack location [-h] [-m | -r | -i | -p | --repo [repo] | -s | -S | -c | -b | -e [name]] [--first] ...


**Positional arguments**

``spec``
  package spec


**Optional arguments**

``-h, --help``
  show this help message and exit

``-m, --module-dir``
  spack python module directory

``-r, --spack-root``
  spack installation root

``-i, --install-dir``
  install prefix for spec (spec need not be installed)

``-p, --package-dir``
  directory enclosing a spec's package.py file

``--repo [repo], --packages [repo], -P [repo]``
  package repository root (defaults to first configured repository)

``-s, --stage-dir``
  stage directory for a spec

``-S, --stages``
  top level stage directory

``-c, --source-dir``
  source directory for a spec (requires it to be staged first)

``-b, --build-dir``
  build directory for a spec (requires it to be staged first)

``-e [name], --env [name]``
  location of the named or current environment

``--first``
  use the first match if multiple packages match the spec


----

.. _spack-log-parse:

spack log-parse
---------------

filter errors and warnings from build logs

.. code-block:: console

    spack log-parse [-hp] [--show SHOW] [-c CONTEXT] [-w WIDTH] [-j JOBS] file


**Positional arguments**

``file``
  a log file containing build output, or - for stdin


**Optional arguments**

``-h, --help``
  show this help message and exit

``--show SHOW``
  comma-separated list of what to show; options: errors, warnings

``-c CONTEXT, --context CONTEXT``
  lines of context to show around lines of interest

``-p, --profile``
  print out a profile of time spent in regexes during parse

``-w WIDTH, --width WIDTH``
  wrap width: auto-size to terminal by default; 0 for no wrap

``-j JOBS, --jobs JOBS``
  number of jobs to parse log file (default: 1 for short logs, ncpus for long logs)


----

.. _spack-logs:

spack logs
----------

print out logs for packages

.. code-block:: console

    spack logs [-h] ...


**Positional arguments**

``spec``
  package spec


**Optional arguments**

``-h, --help``
  show this help message and exit


----

.. _spack-maintainers:

spack maintainers
-----------------

get information about package maintainers

.. code-block:: console

    spack maintainers [-ha] [--maintained | --unmaintained] [--by-user] ...


**Positional arguments**

``package_or_user``
  names of packages or users to get info for


**Optional arguments**

``-h, --help``
  show this help message and exit

``--maintained``
  show names of maintained packages

``--unmaintained``
  show names of unmaintained packages

``-a, --all``
  show maintainers for all packages

``--by-user``
  show packages for users instead of users for packages


----

.. _spack-make-installer:

spack make-installer
--------------------

generate Windows installer

.. code-block:: console

    spack make-installer [-h] (-v SPACK_VERSION | -s SPACK_SOURCE) [-g {SILENT,VERYSILENT}] output_dir


**Positional arguments**

``output_dir``
  output directory


**Optional arguments**

``-h, --help``
  show this help message and exit

``-v SPACK_VERSION, --spack-version SPACK_VERSION``
  download given spack version

``-s SPACK_SOURCE, --spack-source SPACK_SOURCE``
  full path to spack source

``-g {SILENT,VERYSILENT}, --git-installer-verbosity {SILENT,VERYSILENT}``
  level of verbosity provided by bundled git installer (default is fully verbose)


----

.. _spack-mark:

spack mark
----------

mark packages as explicitly or implicitly installed

.. code-block:: console

    spack mark [-ha] (-e | -i) ...


**Positional arguments**

``installed_specs``
  one or more installed package specs


**Optional arguments**

``-h, --help``
  show this help message and exit

``-a, --all``
  mark ALL installed packages that match each supplied spec

``-e, --explicit``
  mark packages as explicitly installed

``-i, --implicit``
  mark packages as implicitly installed


----

.. _spack-mirror:

spack mirror
------------

manage mirrors (source and binary)

.. code-block:: console

    spack mirror [-hn] SUBCOMMAND ...


**Optional arguments**

``-h, --help``
  show this help message and exit

``-n, --no-checksum``
  do not use checksums to verify downloaded files (unsafe)


**Subcommands**

.. hlist::
   :columns: 4

   * :ref:`mirror create <spack-mirror-create>`
   * :ref:`mirror destroy <spack-mirror-destroy>`
   * :ref:`mirror add <spack-mirror-add>`
   * :ref:`mirror remove <spack-mirror-remove>`
   * :ref:`mirror set-url <spack-mirror-set-url>`
   * :ref:`mirror set <spack-mirror-set>`
   * :ref:`mirror list <spack-mirror-list>`


----

.. _spack-mirror-create:

spack mirror create
^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack mirror create [-haDfU] [-d DIRECTORY] [--file FILE] [--exclude-file EXCLUDE_FILE]
                    [--exclude-specs EXCLUDE_SPECS] [--skip-unstable-versions] [-n VERSIONS_PER_SPEC] [--private]
                    [--reuse] [--fresh-roots] [--deprecated]
                    ...


**Positional arguments**

``specs``
  one or more package specs


**Optional arguments**

``-h, --help``
  show this help message and exit

``-d DIRECTORY, --directory DIRECTORY``
  directory in which to create mirror

``-a, --all``
  mirror all versions of all packages in Spack, or all packages in the current environment if there is an active environment (this requires significant time and space)

``--file FILE``
  file with specs of packages to put in mirror

``--exclude-file EXCLUDE_FILE``
  specs which Spack should not try to add to a mirror (listed in a file, one per line)

``--exclude-specs EXCLUDE_SPECS``
  specs which Spack should not try to add to a mirror (specified on command line)

``--skip-unstable-versions``
  don't cache versions unless they identify a stable (unchanging) source code

``-D, --dependencies``
  also fetch all dependencies

``-n VERSIONS_PER_SPEC, --versions-per-spec VERSIONS_PER_SPEC``
  the number of versions to fetch for each spec, choose 'all' to retrieve all versions of each package

``--private``
  for a private mirror, include non-redistributable packages

``-f, --force``
  allow changes to concretized specs in spack.lock (in an env)

``-U, --fresh``
  do not reuse installed deps; build newest configuration

``--reuse``
  reuse installed packages/buildcaches when possible

``--fresh-roots, --reuse-deps``
  concretize with fresh roots and reused dependencies

``--deprecated``
  allow concretizer to select deprecated versions


----

.. _spack-mirror-destroy:

spack mirror destroy
^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack mirror destroy [-h] (-m mirror_name | --mirror-url mirror_url)


**Optional arguments**

``-h, --help``
  show this help message and exit

``-m mirror_name, --mirror-name mirror_name``
  find mirror to destroy by name

``--mirror-url mirror_url``
  find mirror to destroy by url


----

.. _spack-mirror-add:

spack mirror add
^^^^^^^^^^^^^^^^

.. code-block:: console

    spack mirror add [-h] [--scope {defaults,system,site,user,command_line} or env:ENVIRONMENT] [--type {binary,source}]
                 [--autopush] [--unsigned | --signed]
                 [--s3-access-key-id S3_ACCESS_KEY_ID | --s3-access-key-id-variable S3_ACCESS_KEY_ID_VARIABLE]
                 [--s3-access-key-secret S3_ACCESS_KEY_SECRET | --s3-access-key-secret-variable S3_ACCESS_KEY_SECRET_VARIABLE]
                 [--s3-access-token S3_ACCESS_TOKEN | --s3-access-token-variable S3_ACCESS_TOKEN_VARIABLE]
                 [--s3-profile S3_PROFILE] [--s3-endpoint-url S3_ENDPOINT_URL]
                 [--oci-username OCI_USERNAME | --oci-username-variable OCI_USERNAME_VARIABLE]
                 [--oci-password OCI_PASSWORD | --oci-password-variable OCI_PASSWORD_VARIABLE]
                 mirror url


**Positional arguments**

``mirror``
  mnemonic name for mirror

``url``
  url of mirror directory from 'spack mirror create'


**Optional arguments**

``-h, --help``
  show this help message and exit

``--scope {defaults,system,site,user,command_line} or env:ENVIRONMENT``
  configuration scope to modify

``--type {binary,source}``
  specify the mirror type: for both binary and source use ``--type binary --type source`` (default)

``--autopush``
  set mirror to push automatically after installation

``--unsigned``
  do not require signing and signature verification when pushing and installing from this build cache

``--signed``
  require signing and signature verification when pushing and installing from this build cache

``--s3-access-key-id S3_ACCESS_KEY_ID``
  ID string to use to connect to this S3 mirror

``--s3-access-key-id-variable S3_ACCESS_KEY_ID_VARIABLE``
  environment variable containing ID string to use to connect to this S3 mirror

``--s3-access-key-secret S3_ACCESS_KEY_SECRET``
  secret string to use to connect to this S3 mirror

``--s3-access-key-secret-variable S3_ACCESS_KEY_SECRET_VARIABLE``
  environment variable containing secret string to use to connect to this S3 mirror

``--s3-access-token S3_ACCESS_TOKEN``
  access token to use to connect to this S3 mirror

``--s3-access-token-variable S3_ACCESS_TOKEN_VARIABLE``
  environment variable containing access token to use to connect to this S3 mirror

``--s3-profile S3_PROFILE``
  S3 profile name to use to connect to this S3 mirror

``--s3-endpoint-url S3_ENDPOINT_URL``
  endpoint URL to use to connect to this S3 mirror

``--oci-username OCI_USERNAME``
  username to use to connect to this OCI mirror

``--oci-username-variable OCI_USERNAME_VARIABLE``
  environment variable containing username to use to connect to this OCI mirror

``--oci-password OCI_PASSWORD``
  password to use to connect to this OCI mirror

``--oci-password-variable OCI_PASSWORD_VARIABLE``
  environment variable containing password to use to connect to this OCI mirror


----

.. _spack-mirror-remove:

spack mirror remove
^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack mirror remove [-h] [--scope {defaults,system,site,user,command_line} or env:ENVIRONMENT] mirror


**Positional arguments**

``mirror``
  mnemonic name for mirror


**Optional arguments**

``-h, --help``
  show this help message and exit

``--scope {defaults,system,site,user,command_line} or env:ENVIRONMENT``
  configuration scope to modify


----

.. _spack-mirror-set-url:

spack mirror set-url
^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack mirror set-url [-h] [--push | --fetch] [--scope {defaults,system,site,user,command_line} or env:ENVIRONMENT]
                     [--s3-access-key-id S3_ACCESS_KEY_ID | --s3-access-key-id-variable S3_ACCESS_KEY_ID_VARIABLE]
                     [--s3-access-key-secret S3_ACCESS_KEY_SECRET | --s3-access-key-secret-variable S3_ACCESS_KEY_SECRET_VARIABLE]
                     [--s3-access-token S3_ACCESS_TOKEN | --s3-access-token-variable S3_ACCESS_TOKEN_VARIABLE]
                     [--s3-profile S3_PROFILE] [--s3-endpoint-url S3_ENDPOINT_URL]
                     [--oci-username OCI_USERNAME | --oci-username-variable OCI_USERNAME_VARIABLE]
                     [--oci-password OCI_PASSWORD | --oci-password-variable OCI_PASSWORD_VARIABLE]
                     mirror url


**Positional arguments**

``mirror``
  mnemonic name for mirror

``url``
  url of mirror directory from 'spack mirror create'


**Optional arguments**

``-h, --help``
  show this help message and exit

``--push``
  set only the URL used for uploading

``--fetch``
  set only the URL used for downloading

``--scope {defaults,system,site,user,command_line} or env:ENVIRONMENT``
  configuration scope to modify

``--s3-access-key-id S3_ACCESS_KEY_ID``
  ID string to use to connect to this S3 mirror

``--s3-access-key-id-variable S3_ACCESS_KEY_ID_VARIABLE``
  environment variable containing ID string to use to connect to this S3 mirror

``--s3-access-key-secret S3_ACCESS_KEY_SECRET``
  secret string to use to connect to this S3 mirror

``--s3-access-key-secret-variable S3_ACCESS_KEY_SECRET_VARIABLE``
  environment variable containing secret string to use to connect to this S3 mirror

``--s3-access-token S3_ACCESS_TOKEN``
  access token to use to connect to this S3 mirror

``--s3-access-token-variable S3_ACCESS_TOKEN_VARIABLE``
  environment variable containing access token to use to connect to this S3 mirror

``--s3-profile S3_PROFILE``
  S3 profile name to use to connect to this S3 mirror

``--s3-endpoint-url S3_ENDPOINT_URL``
  endpoint URL to use to connect to this S3 mirror

``--oci-username OCI_USERNAME``
  username to use to connect to this OCI mirror

``--oci-username-variable OCI_USERNAME_VARIABLE``
  environment variable containing username to use to connect to this OCI mirror

``--oci-password OCI_PASSWORD``
  password to use to connect to this OCI mirror

``--oci-password-variable OCI_PASSWORD_VARIABLE``
  environment variable containing password to use to connect to this OCI mirror


----

.. _spack-mirror-set:

spack mirror set
^^^^^^^^^^^^^^^^

.. code-block:: console

    spack mirror set [-h] [--push | --fetch] [--type {binary,source}] [--url URL] [--autopush | --no-autopush]
                 [--unsigned | --signed] [--scope {defaults,system,site,user,command_line} or env:ENVIRONMENT]
                 [--s3-access-key-id S3_ACCESS_KEY_ID | --s3-access-key-id-variable S3_ACCESS_KEY_ID_VARIABLE]
                 [--s3-access-key-secret S3_ACCESS_KEY_SECRET | --s3-access-key-secret-variable S3_ACCESS_KEY_SECRET_VARIABLE]
                 [--s3-access-token S3_ACCESS_TOKEN | --s3-access-token-variable S3_ACCESS_TOKEN_VARIABLE]
                 [--s3-profile S3_PROFILE] [--s3-endpoint-url S3_ENDPOINT_URL]
                 [--oci-username OCI_USERNAME | --oci-username-variable OCI_USERNAME_VARIABLE]
                 [--oci-password OCI_PASSWORD | --oci-password-variable OCI_PASSWORD_VARIABLE]
                 mirror


**Positional arguments**

``mirror``
  mnemonic name for mirror


**Optional arguments**

``-h, --help``
  show this help message and exit

``--push``
  modify just the push connection details

``--fetch``
  modify just the fetch connection details

``--type {binary,source}``
  specify the mirror type: for both binary and source use ``--type binary --type source``

``--url URL``
  url of mirror directory from 'spack mirror create'

``--autopush``
  set mirror to push automatically after installation

``--no-autopush``
  set mirror to not push automatically after installation

``--unsigned``
  do not require signing and signature verification when pushing and installing from this build cache

``--signed``
  require signing and signature verification when pushing and installing from this build cache

``--scope {defaults,system,site,user,command_line} or env:ENVIRONMENT``
  configuration scope to modify

``--s3-access-key-id S3_ACCESS_KEY_ID``
  ID string to use to connect to this S3 mirror

``--s3-access-key-id-variable S3_ACCESS_KEY_ID_VARIABLE``
  environment variable containing ID string to use to connect to this S3 mirror

``--s3-access-key-secret S3_ACCESS_KEY_SECRET``
  secret string to use to connect to this S3 mirror

``--s3-access-key-secret-variable S3_ACCESS_KEY_SECRET_VARIABLE``
  environment variable containing secret string to use to connect to this S3 mirror

``--s3-access-token S3_ACCESS_TOKEN``
  access token to use to connect to this S3 mirror

``--s3-access-token-variable S3_ACCESS_TOKEN_VARIABLE``
  environment variable containing access token to use to connect to this S3 mirror

``--s3-profile S3_PROFILE``
  S3 profile name to use to connect to this S3 mirror

``--s3-endpoint-url S3_ENDPOINT_URL``
  endpoint URL to use to connect to this S3 mirror

``--oci-username OCI_USERNAME``
  username to use to connect to this OCI mirror

``--oci-username-variable OCI_USERNAME_VARIABLE``
  environment variable containing username to use to connect to this OCI mirror

``--oci-password OCI_PASSWORD``
  password to use to connect to this OCI mirror

``--oci-password-variable OCI_PASSWORD_VARIABLE``
  environment variable containing password to use to connect to this OCI mirror


----

.. _spack-mirror-list:

spack mirror list
^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack mirror list [-h] [--scope {defaults,system,site,user,command_line} or env:ENVIRONMENT]


**Optional arguments**

``-h, --help``
  show this help message and exit

``--scope {defaults,system,site,user,command_line} or env:ENVIRONMENT``
  configuration scope to read from


----

.. _spack-module:

spack module
------------

generate/manage module files

.. code-block:: console

    spack module [-h] SUBCOMMAND ...


**Optional arguments**

``-h, --help``
  show this help message and exit


**Subcommands**

.. hlist::
   :columns: 4

   * :ref:`module lmod <spack-module-lmod>`
   * :ref:`module tcl <spack-module-tcl>`


----

.. _spack-module-lmod:

spack module lmod
^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack module lmod [-h] [-n MODULE_SET_NAME] SUBCOMMAND ...


**Optional arguments**

``-h, --help``
  show this help message and exit

``-n MODULE_SET_NAME, --name MODULE_SET_NAME``
  named module set to use from modules configuration


**Subcommands**

.. hlist::
   :columns: 4

   * :ref:`module lmod refresh <spack-module-lmod-refresh>`
   * :ref:`module lmod find <spack-module-lmod-find>`
   * :ref:`module lmod rm <spack-module-lmod-rm>`
   * :ref:`module lmod loads <spack-module-lmod-loads>`
   * :ref:`module lmod setdefault <spack-module-lmod-setdefault>`


----

.. _spack-module-lmod-refresh:

spack module lmod refresh
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: console

    spack module lmod refresh [-hy] [--delete-tree] [--upstream-modules] ...


**Positional arguments**

``installed_specs``
  constraint to select a subset of installed packages


**Optional arguments**

``-h, --help``
  show this help message and exit

``--delete-tree``
  delete the module file tree before refresh

``--upstream-modules``
  generate modules for packages installed upstream

``-y, --yes-to-all``
  assume "yes" is the answer to every confirmation request


----

.. _spack-module-lmod-find:

spack module lmod find
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: console

    spack module lmod find [-hr] [--full-path] ...


**Positional arguments**

``installed_specs``
  constraint to select a subset of installed packages


**Optional arguments**

``-h, --help``
  show this help message and exit

``--full-path``
  display full path to module file

``-r, --dependencies``
  recursively traverse spec dependencies


----

.. _spack-module-lmod-rm:

spack module lmod rm
~~~~~~~~~~~~~~~~~~~~

.. code-block:: console

    spack module lmod rm [-hy] ...


**Positional arguments**

``installed_specs``
  constraint to select a subset of installed packages


**Optional arguments**

``-h, --help``
  show this help message and exit

``-y, --yes-to-all``
  assume "yes" is the answer to every confirmation request


----

.. _spack-module-lmod-loads:

spack module lmod loads
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: console

    spack module lmod loads [-hr] [--input-only] [-p PREFIX] [-x EXCLUDE] ...


**Positional arguments**

``installed_specs``
  constraint to select a subset of installed packages


**Optional arguments**

``-h, --help``
  show this help message and exit

``--input-only``
  generate input for module command (instead of a shell script)

``-p PREFIX, --prefix PREFIX``
  prepend to module names when issuing module load commands

``-x EXCLUDE, --exclude EXCLUDE``
  exclude package from output; may be specified multiple times

``-r, --dependencies``
  recursively traverse spec dependencies


----

.. _spack-module-lmod-setdefault:

spack module lmod setdefault
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: console

    spack module lmod setdefault [-h] ...


**Positional arguments**

``installed_specs``
  constraint to select a subset of installed packages


**Optional arguments**

``-h, --help``
  show this help message and exit


----

.. _spack-module-tcl:

spack module tcl
^^^^^^^^^^^^^^^^

.. code-block:: console

    spack module tcl [-h] [-n MODULE_SET_NAME] SUBCOMMAND ...


**Optional arguments**

``-h, --help``
  show this help message and exit

``-n MODULE_SET_NAME, --name MODULE_SET_NAME``
  named module set to use from modules configuration


**Subcommands**

.. hlist::
   :columns: 4

   * :ref:`module tcl refresh <spack-module-tcl-refresh>`
   * :ref:`module tcl find <spack-module-tcl-find>`
   * :ref:`module tcl rm <spack-module-tcl-rm>`
   * :ref:`module tcl loads <spack-module-tcl-loads>`
   * :ref:`module tcl setdefault <spack-module-tcl-setdefault>`


----

.. _spack-module-tcl-refresh:

spack module tcl refresh
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: console

    spack module tcl refresh [-hy] [--delete-tree] [--upstream-modules] ...


**Positional arguments**

``installed_specs``
  constraint to select a subset of installed packages


**Optional arguments**

``-h, --help``
  show this help message and exit

``--delete-tree``
  delete the module file tree before refresh

``--upstream-modules``
  generate modules for packages installed upstream

``-y, --yes-to-all``
  assume "yes" is the answer to every confirmation request


----

.. _spack-module-tcl-find:

spack module tcl find
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: console

    spack module tcl find [-hr] [--full-path] ...


**Positional arguments**

``installed_specs``
  constraint to select a subset of installed packages


**Optional arguments**

``-h, --help``
  show this help message and exit

``--full-path``
  display full path to module file

``-r, --dependencies``
  recursively traverse spec dependencies


----

.. _spack-module-tcl-rm:

spack module tcl rm
~~~~~~~~~~~~~~~~~~~

.. code-block:: console

    spack module tcl rm [-hy] ...


**Positional arguments**

``installed_specs``
  constraint to select a subset of installed packages


**Optional arguments**

``-h, --help``
  show this help message and exit

``-y, --yes-to-all``
  assume "yes" is the answer to every confirmation request


----

.. _spack-module-tcl-loads:

spack module tcl loads
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: console

    spack module tcl loads [-hr] [--input-only] [-p PREFIX] [-x EXCLUDE] ...


**Positional arguments**

``installed_specs``
  constraint to select a subset of installed packages


**Optional arguments**

``-h, --help``
  show this help message and exit

``--input-only``
  generate input for module command (instead of a shell script)

``-p PREFIX, --prefix PREFIX``
  prepend to module names when issuing module load commands

``-x EXCLUDE, --exclude EXCLUDE``
  exclude package from output; may be specified multiple times

``-r, --dependencies``
  recursively traverse spec dependencies


----

.. _spack-module-tcl-setdefault:

spack module tcl setdefault
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: console

    spack module tcl setdefault [-h] ...


**Positional arguments**

``installed_specs``
  constraint to select a subset of installed packages


**Optional arguments**

``-h, --help``
  show this help message and exit


----

.. _spack-patch:

spack patch
-----------

patch expanded archive sources in preparation for install

.. code-block:: console

    spack patch [-hnfU] [--reuse] [--fresh-roots] [--deprecated] ...


**Positional arguments**

``specs``
  one or more package specs


**Optional arguments**

``-h, --help``
  show this help message and exit

``-n, --no-checksum``
  do not use checksums to verify downloaded files (unsafe)

``-f, --force``
  allow changes to concretized specs in spack.lock (in an env)

``-U, --fresh``
  do not reuse installed deps; build newest configuration

``--reuse``
  reuse installed packages/buildcaches when possible

``--fresh-roots, --reuse-deps``
  concretize with fresh roots and reused dependencies

``--deprecated``
  allow concretizer to select deprecated versions


----

.. _spack-pkg:

spack pkg
---------

query packages associated with particular git revisions

.. code-block:: console

    spack pkg [-h] SUBCOMMAND ...


**Optional arguments**

``-h, --help``
  show this help message and exit


**Subcommands**

.. hlist::
   :columns: 4

   * :ref:`pkg add <spack-pkg-add>`
   * :ref:`pkg list <spack-pkg-list>`
   * :ref:`pkg diff <spack-pkg-diff>`
   * :ref:`pkg added <spack-pkg-added>`
   * :ref:`pkg changed <spack-pkg-changed>`
   * :ref:`pkg removed <spack-pkg-removed>`
   * :ref:`pkg grep <spack-pkg-grep>`
   * :ref:`pkg source <spack-pkg-source>`
   * :ref:`pkg hash <spack-pkg-hash>`


----

.. _spack-pkg-add:

spack pkg add
^^^^^^^^^^^^^

.. code-block:: console

    spack pkg add [-h] package [package ...]


**Positional arguments**

``package``
  one or more package names


**Optional arguments**

``-h, --help``
  show this help message and exit


----

.. _spack-pkg-list:

spack pkg list
^^^^^^^^^^^^^^

.. code-block:: console

    spack pkg list [-h] [rev]


**Positional arguments**

``rev``
  revision to list packages for


**Optional arguments**

``-h, --help``
  show this help message and exit


----

.. _spack-pkg-diff:

spack pkg diff
^^^^^^^^^^^^^^

.. code-block:: console

    spack pkg diff [-h] [rev1] [rev2]


**Positional arguments**

``rev1``
  revision to compare against

``rev2``
  revision to compare to rev1 (default is HEAD)


**Optional arguments**

``-h, --help``
  show this help message and exit


----

.. _spack-pkg-added:

spack pkg added
^^^^^^^^^^^^^^^

.. code-block:: console

    spack pkg added [-h] [rev1] [rev2]


**Positional arguments**

``rev1``
  revision to compare against

``rev2``
  revision to compare to rev1 (default is HEAD)


**Optional arguments**

``-h, --help``
  show this help message and exit


----

.. _spack-pkg-changed:

spack pkg changed
^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack pkg changed [-h] [-t TYPE] [rev1] [rev2]


**Positional arguments**

``rev1``
  revision to compare against

``rev2``
  revision to compare to rev1 (default is HEAD)


**Optional arguments**

``-h, --help``
  show this help message and exit

``-t TYPE, --type TYPE``
  types of changes to show (A: added, R: removed, C: changed); default is 'C'


----

.. _spack-pkg-removed:

spack pkg removed
^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack pkg removed [-h] [rev1] [rev2]


**Positional arguments**

``rev1``
  revision to compare against

``rev2``
  revision to compare to rev1 (default is HEAD)


**Optional arguments**

``-h, --help``
  show this help message and exit


----

.. _spack-pkg-grep:

spack pkg grep
^^^^^^^^^^^^^^

.. code-block:: console

    spack pkg grep [--help] ...


**Positional arguments**

``grep_args``
  arguments for grep


**Optional arguments**

``--help``
  show this help message and exit


----

.. _spack-pkg-source:

spack pkg source
^^^^^^^^^^^^^^^^

.. code-block:: console

    spack pkg source [-hc] ...


**Positional arguments**

``spec``
  package spec


**Optional arguments**

``-h, --help``
  show this help message and exit

``-c, --canonical``
  dump canonical source as used by package hash


----

.. _spack-pkg-hash:

spack pkg hash
^^^^^^^^^^^^^^

.. code-block:: console

    spack pkg hash [-h] ...


**Positional arguments**

``spec``
  package spec


**Optional arguments**

``-h, --help``
  show this help message and exit


----

.. _spack-providers:

spack providers
---------------

list packages that provide a particular virtual package

.. code-block:: console

    spack providers [-h] [virtual_package ...]


**Positional arguments**

``virtual_package``
  find packages that provide this virtual package


**Optional arguments**

``-h, --help``
  show this help message and exit


----

.. _spack-pydoc:

spack pydoc
-----------

run pydoc from within spack

.. code-block:: console

    spack pydoc [-h] entity


**Positional arguments**

``entity``
  run pydoc help on entity


**Optional arguments**

``-h, --help``
  show this help message and exit


----

.. _spack-python:

spack python
------------

launch an interpreter as spack would launch a command

.. code-block:: console

    spack python [-hVu] [-c PYTHON_COMMAND] [-i {python,ipython}] [-m MODULE] [--path] ...


**Positional arguments**

``python_args``
  file to run plus arguments


**Optional arguments**

``-h, --help``
  show this help message and exit

``-V, --version``
  print the Python version number and exit

``-c PYTHON_COMMAND``
  command to execute

``-u``
  for compatibility with xdist, do not use without adding -u to the interpreter

``-i {python,ipython}``
  python interpreter

``-m MODULE``
  run library module as a script

``--path``
  show path to python interpreter that spack uses


----

.. _spack-reindex:

spack reindex
-------------

rebuild Spack's package database

.. code-block:: console

    spack reindex [-h]


**Optional arguments**

``-h, --help``
  show this help message and exit


----

.. _spack-remove:

spack remove
------------

remove specs from an environment

.. code-block:: console

    spack remove [-haf] [-l LIST_NAME] ...


**Positional arguments**

``specs``
  one or more package specs


**Optional arguments**

``-h, --help``
  show this help message and exit

``-a, --all``
  remove all specs from (clear) the environment

``-l LIST_NAME, --list-name LIST_NAME``
  name of the list to remove specs from

``-f, --force``
  remove concretized spec (if any) immediately


----

.. _spack-repo:

spack repo
----------

manage package source repositories

.. code-block:: console

    spack repo [-h] SUBCOMMAND ...


**Optional arguments**

``-h, --help``
  show this help message and exit


**Subcommands**

.. hlist::
   :columns: 4

   * :ref:`repo create <spack-repo-create>`
   * :ref:`repo list <spack-repo-list>`
   * :ref:`repo add <spack-repo-add>`
   * :ref:`repo set <spack-repo-set>`
   * :ref:`repo remove <spack-repo-remove>`
   * :ref:`repo migrate <spack-repo-migrate>`
   * :ref:`repo update <spack-repo-update>`


----

.. _spack-repo-create:

spack repo create
^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack repo create [-h] [-d SUBDIR] directory namespace


**Positional arguments**

``directory``
  directory to create the repo in

``namespace``
  name or namespace to identify packages in the repository


**Optional arguments**

``-h, --help``
  show this help message and exit

``-d SUBDIR, --subdirectory SUBDIR``
  subdirectory to store packages in the repository


----

.. _spack-repo-list:

spack repo list
^^^^^^^^^^^^^^^

.. code-block:: console

    spack repo list [-h] [--scope {defaults,system,site,user,command_line} or env:ENVIRONMENT] [--names | --namespaces]


**Optional arguments**

``-h, --help``
  show this help message and exit

``--scope {defaults,system,site,user,command_line} or env:ENVIRONMENT``
  configuration scope to read from

``--names``
  show configuration names only

``--namespaces``
  show repository namespaces only


----

.. _spack-repo-add:

spack repo add
^^^^^^^^^^^^^^

.. code-block:: console

    spack repo add [-h] [--name NAME] [--path PATH] [--scope {defaults,system,site,user,command_line} or env:ENVIRONMENT]
               path_or_repo [destination]


**Positional arguments**

``path_or_repo``
  path or git repository of a Spack package repository

``destination``
  destination to clone git repository into (defaults to cache directory)


**Optional arguments**

``-h, --help``
  show this help message and exit

``--name NAME``
  config name for the package repository, defaults to the namespace of the repository

``--path PATH``
  relative path to the Spack package repository inside a git repository. Can be repeated to add multiple package repositories in case of a monorepo

``--scope {defaults,system,site,user,command_line} or env:ENVIRONMENT``
  configuration scope to modify


----

.. _spack-repo-set:

spack repo set
^^^^^^^^^^^^^^

.. code-block:: console

    spack repo set [-h] [--destination DESTINATION] [--path PATH]
               [--scope {defaults,system,site,user,command_line} or env:ENVIRONMENT]
               namespace


**Positional arguments**

``namespace``
  namespace of a Spack package repository


**Optional arguments**

``-h, --help``
  show this help message and exit

``--destination DESTINATION``
  destination to clone git repository into

``--path PATH``
  relative path to the Spack package repository inside a git repository. Can be repeated to add multiple package repositories in case of a monorepo

``--scope {defaults,system,site,user,command_line} or env:ENVIRONMENT``
  configuration scope to modify


----

.. _spack-repo-remove:

spack repo remove
^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack repo remove [-h] [--scope {defaults,system,site,user,command_line} or env:ENVIRONMENT] namespace_or_path


**Positional arguments**

``namespace_or_path``
  namespace or path of a Spack package repository


**Optional arguments**

``-h, --help``
  show this help message and exit

``--scope {defaults,system,site,user,command_line} or env:ENVIRONMENT``
  configuration scope to modify


----

.. _spack-repo-migrate:

spack repo migrate
^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack repo migrate [-h] (--dry-run | --fix) namespace_or_path


**Positional arguments**

``namespace_or_path``
  path to a Spack package repository directory


**Optional arguments**

``-h, --help``
  show this help message and exit

``--dry-run``
  do not modify the repository, but dump a patch file

``--fix``
  automatically migrate the repository to the latest Package API


----

.. _spack-repo-update:

spack repo update
^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack repo update [-h] [--remote [REMOTE]] [--scope {defaults,system,site,user,command_line} or env:ENVIRONMENT]
                  [--branch [BRANCH]] [--tag [TAG] | --commit [COMMIT]]
                  [names ...]


**Positional arguments**

``names``
  repositories to update


**Optional arguments**

``-h, --help``
  show this help message and exit

``--remote [REMOTE], -r [REMOTE]``
  name of remote to check for branches, tags, or commits

``--scope {defaults,system,site,user,command_line} or env:ENVIRONMENT``
  configuration scope to modify

``--branch [BRANCH], -b [BRANCH]``
  name of a branch to change to

``--tag [TAG], -t [TAG]``
  name of a tag to change to

``--commit [COMMIT], -c [COMMIT]``
  name of a commit to change to


----

.. _spack-resource:

spack resource
--------------

list downloadable resources (tarballs, repos, patches, etc.)

.. code-block:: console

    spack resource [-h] SUBCOMMAND ...


**Optional arguments**

``-h, --help``
  show this help message and exit


**Subcommands**

.. hlist::
   :columns: 4

   * :ref:`resource list <spack-resource-list>`
   * :ref:`resource show <spack-resource-show>`


----

.. _spack-resource-list:

spack resource list
^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack resource list [-h] [--only-hashes]


**Optional arguments**

``-h, --help``
  show this help message and exit

``--only-hashes``
  only print sha256 hashes of resources


----

.. _spack-resource-show:

spack resource show
^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack resource show [-h] hash


**Positional arguments**

``hash``
  


**Optional arguments**

``-h, --help``
  show this help message and exit


----

.. _spack-restage:

spack restage
-------------

revert checked out package source code

.. code-block:: console

    spack restage [-h] ...


**Positional arguments**

``specs``
  one or more package specs


**Optional arguments**

``-h, --help``
  show this help message and exit


----

.. _spack-solve:

spack solve
-----------

concretize a specs using an ASP solver

.. code-block:: console

    spack solve [-hlLNtfU] [--show SHOW] [--timers] [--stats] [-I | --no-install-status] [-y | -j | --format FORMAT]
            [-c {nodes,edges,paths}] [--reuse] [--fresh-roots] [--deprecated]
            ...


**Positional arguments**

``specs``
  one or more package specs


**Optional arguments**

``-h, --help``
  show this help message and exit

``--show SHOW``
  select outputs

``--timers``
  print out timers for different solve phases

``--stats``
  print out statistics from clingo

``-l, --long``
  show dependency hashes as well as versions

``-L, --very-long``
  show full dependency hashes as well as versions

``-N, --namespaces``
  show fully qualified package names

``-I, --install-status``
  show install status of packages

``--no-install-status``
  do not show install status annotations

``-y, --yaml``
  print concrete spec as YAML

``-j, --json``
  print concrete spec as JSON

``--format FORMAT``
  print concrete spec with the specified format string

``-c {nodes,edges,paths}, --cover {nodes,edges,paths}``
  how extensively to traverse the DAG (default: nodes)

``-t, --types``
  show dependency types

``-f, --force``
  allow changes to concretized specs in spack.lock (in an env)

``-U, --fresh``
  do not reuse installed deps; build newest configuration

``--reuse``
  reuse installed packages/buildcaches when possible

``--fresh-roots, --reuse-deps``
  concretize with fresh roots and reused dependencies

``--deprecated``
  allow concretizer to select deprecated versions


----

.. _spack-spec:

spack spec
----------

show what would be installed, given a spec

.. code-block:: console

    spack spec [-hlLNtfU] [-I | --no-install-status] [-y | -j | --format FORMAT] [-c {nodes,edges,paths}] [--reuse]
           [--fresh-roots] [--deprecated]
           ...


**Positional arguments**

``specs``
  one or more package specs


**Optional arguments**

``-h, --help``
  show this help message and exit

``-l, --long``
  show dependency hashes as well as versions

``-L, --very-long``
  show full dependency hashes as well as versions

``-N, --namespaces``
  show fully qualified package names

``-I, --install-status``
  show install status of packages

``--no-install-status``
  do not show install status annotations

``-y, --yaml``
  print concrete spec as YAML

``-j, --json``
  print concrete spec as JSON

``--format FORMAT``
  print concrete spec with the specified format string

``-c {nodes,edges,paths}, --cover {nodes,edges,paths}``
  how extensively to traverse the DAG (default: nodes)

``-t, --types``
  show dependency types

``-f, --force``
  allow changes to concretized specs in spack.lock (in an env)

``-U, --fresh``
  do not reuse installed deps; build newest configuration

``--reuse``
  reuse installed packages/buildcaches when possible

``--fresh-roots, --reuse-deps``
  concretize with fresh roots and reused dependencies

``--deprecated``
  allow concretizer to select deprecated versions


----

.. _spack-stage:

spack stage
-----------

expand downloaded archive in preparation for install

.. code-block:: console

    spack stage [-hnsfU] [-p PATH] [-e EXCLUDE] [--reuse] [--fresh-roots] [--deprecated] ...


**Positional arguments**

``specs``
  one or more package specs


**Optional arguments**

``-h, --help``
  show this help message and exit

``-n, --no-checksum``
  do not use checksums to verify downloaded files (unsafe)

``-p PATH, --path PATH``
  path to stage package, does not add to spack tree

``-e EXCLUDE, --exclude EXCLUDE``
  exclude packages that satisfy the specified specs

``-s, --skip-installed``
  dont restage already installed specs

``-f, --force``
  allow changes to concretized specs in spack.lock (in an env)

``-U, --fresh``
  do not reuse installed deps; build newest configuration

``--reuse``
  reuse installed packages/buildcaches when possible

``--fresh-roots, --reuse-deps``
  concretize with fresh roots and reused dependencies

``--deprecated``
  allow concretizer to select deprecated versions


----

.. _spack-style:

spack style
-----------

runs source code style checks on spack

.. code-block:: console

    spack style [-harUf] [-b BASE] [--root ROOT] [-t TOOL | -s TOOL] [--spec-strings] ...


**Positional arguments**

``files``
  specific files to check


**Optional arguments**

``-h, --help``
  show this help message and exit

``-b BASE, --base BASE``
  branch to compare against to determine changed files (default: develop)

``-a, --all``
  check all files, not just changed files

``-r, --root-relative``
  print root-relative paths (default: cwd-relative)

``-U, --no-untracked``
  exclude untracked files from checks

``-f, --fix``
  format automatically if possible (e.g., with isort, black)

``--root ROOT``
  style check a different spack instance

``-t TOOL, --tool TOOL``
  specify which tools to run (default: import, isort, black, flake8, mypy)

``-s TOOL, --skip TOOL``
  specify tools to skip (choose from import, isort, black, flake8, mypy)

``--spec-strings``
  upgrade spec strings in Python, JSON and YAML files for compatibility with Spack v1.0 and v0.x. Example: spack style ``--spec-strings $(git ls-files)``. Note: must be used only on specs from spack v0.X.


----

.. _spack-tags:

spack tags
----------

show package tags and associated packages

.. code-block:: console

    spack tags [-hia] [tag ...]


**Positional arguments**

``tag``
  show packages with the specified tag


**Optional arguments**

``-h, --help``
  show this help message and exit

``-i, --installed``
  show information for installed packages only

``-a, --all``
  show packages for all available tags


----

.. _spack-test:

spack test
----------

run spack's tests for an install

.. code-block:: console

    spack test [-h] SUBCOMMAND ...


**Optional arguments**

``-h, --help``
  show this help message and exit


**Subcommands**

.. hlist::
   :columns: 4

   * :ref:`test run <spack-test-run>`
   * :ref:`test list <spack-test-list>`
   * :ref:`test find <spack-test-find>`
   * :ref:`test status <spack-test-status>`
   * :ref:`test results <spack-test-results>`
   * :ref:`test remove <spack-test-remove>`


----

.. _spack-test-run:

spack test run
^^^^^^^^^^^^^^

run tests for the specified installed packages

    if no specs are listed, run tests for all packages in the current
    environment or all installed packages if there is no active environment
    

.. code-block:: console

    spack test run [-hx] [--alias ALIAS] [--fail-fast] [--fail-first] [--externals] [--keep-stage]
               [--log-format {junit,cdash}] [--log-file LOG_FILE] [--help-cdash] [--timeout TIMEOUT]
               [--clean | --dirty]
               ...


**Positional arguments**

``installed_specs``
  one or more installed package specs


**Optional arguments**

``-h, --help``
  show this help message and exit

``--alias ALIAS``
  provide an alias for this test-suite for subsequent access

``--fail-fast``
  stop tests for each package after the first failure

``--fail-first``
  stop after the first failed package

``--externals``
  test packages that are externally installed

``-x, --explicit``
  only test packages that are explicitly installed

``--keep-stage``
  keep testing directory for debugging

``--log-format {junit,cdash}``
  format to be used for log files

``--log-file LOG_FILE``
  filename for the log file

``--cdash-upload-url CDASH_UPLOAD_URL``
  

``--cdash-build CDASH_BUILD``
  

``--cdash-site CDASH_SITE``
  

``--cdash-track CDASH_TRACK``
  

``--cdash-buildstamp CDASH_BUILDSTAMP``
  

``--help-cdash``
  show usage instructions for CDash reporting

``--timeout TIMEOUT``
  maximum time (in seconds) that tests are allowed to run

``--clean``
  unset harmful variables in the build environment (default)

``--dirty``
  preserve user environment in spack's build environment (danger!)


----

.. _spack-test-list:

spack test list
^^^^^^^^^^^^^^^

list installed packages with available tests

.. code-block:: console

    spack test list [-ha] [tag ...]


**Positional arguments**

``tag``
  limit packages to those with all listed tags


**Optional arguments**

``-h, --help``
  show this help message and exit

``-a, --all``
  list all packages with tests (not just installed)


----

.. _spack-test-find:

spack test find
^^^^^^^^^^^^^^^

find tests that are running or have available results

    displays aliases for tests that have them, otherwise test suite content hashes
    

.. code-block:: console

    spack test find [-h] ...


**Positional arguments**

``filter``
  optional case-insensitive glob patterns to filter results


**Optional arguments**

``-h, --help``
  show this help message and exit


----

.. _spack-test-status:

spack test status
^^^^^^^^^^^^^^^^^

get the current status for the specified Spack test suite(s)

.. code-block:: console

    spack test status [-h] ...


**Positional arguments**

``names``
  test suites for which to print status


**Optional arguments**

``-h, --help``
  show this help message and exit


----

.. _spack-test-results:

spack test results
^^^^^^^^^^^^^^^^^^

get the results from Spack test suite(s) (default all)

.. code-block:: console

    spack test results [-hlf] ...


**Positional arguments**

``[name(s)] [-- installed_specs]...``
  suite names and installed package constraints


**Optional arguments**

``-h, --help``
  show this help message and exit

``-l, --logs``
  print the test log for each matching package

``-f, --failed``
  only show results for failed tests of matching packages


----

.. _spack-test-remove:

spack test remove
^^^^^^^^^^^^^^^^^

remove results from Spack test suite(s) (default all)

    if no test suite is listed, remove results for all suites.

    removed tests can no longer be accessed for results or status, and will not
    appear in ``spack test list`` results
    

.. code-block:: console

    spack test remove [-hy] ...


**Positional arguments**

``names``
  test suites to remove from test stage


**Optional arguments**

``-h, --help``
  show this help message and exit

``-y, --yes-to-all``
  assume "yes" is the answer to every confirmation request


----

.. _spack-test-env:

spack test-env
--------------

run a command in a spec's test environment, or dump its environment to screen or file

.. code-block:: console

    spack test-env [-hfU] [--clean] [--dirty] [--reuse] [--fresh-roots] [--deprecated] [--dump FILE] [--pickle FILE] ...


**Positional arguments**

``spec [--] [cmd]...``
  specs of package environment to emulate


**Optional arguments**

``-h, --help``
  show this help message and exit

``--clean``
  unset harmful variables in the build environment (default)

``--dirty``
  preserve user environment in spack's build environment (danger!)

``-f, --force``
  allow changes to concretized specs in spack.lock (in an env)

``-U, --fresh``
  do not reuse installed deps; build newest configuration

``--reuse``
  reuse installed packages/buildcaches when possible

``--fresh-roots, --reuse-deps``
  concretize with fresh roots and reused dependencies

``--deprecated``
  allow concretizer to select deprecated versions

``--dump FILE``
  dump a source-able environment to FILE

``--pickle FILE``
  dump a pickled source-able environment to FILE


----

.. _spack-tutorial:

spack tutorial
--------------

set up spack for our tutorial (WARNING: modifies config!)

.. code-block:: console

    spack tutorial [-hy]


**Optional arguments**

``-h, --help``
  show this help message and exit

``-y, --yes-to-all``
  assume "yes" is the answer to every confirmation request


----

.. _spack-undevelop:

spack undevelop
---------------

remove specs from an environment

.. code-block:: console

    spack undevelop [-ha] ...


**Positional arguments**

``specs``
  one or more package specs


**Optional arguments**

``-h, --help``
  show this help message and exit

``-a, --all``
  remove all specs from (clear) the environment


----

.. _spack-uninstall:

spack uninstall
---------------

remove installed packages

.. code-block:: console

    spack uninstall [-hfRya] [--remove] [--origin ORIGIN] ...


**Positional arguments**

``installed_specs``
  one or more installed package specs


**Optional arguments**

``-h, --help``
  show this help message and exit

``-f, --force``
  remove regardless of whether other packages or environments depend on this one

``--remove``
  if in an environment, then the spec should also be removed from the environment description

``-R, --dependents``
  also uninstall any packages that depend on the ones given via command line

``-y, --yes-to-all``
  assume "yes" is the answer to every confirmation request

``-a, --all``
  remove ALL installed packages that match each supplied spec

``--origin ORIGIN``
  only remove DB records with the specified origin


----

.. _spack-unit-test:

spack unit-test
---------------

run spack's unit tests (wrapper around pytest)

.. code-block:: console

    spack unit-test [-hHs] [-n NUMPROCESSES] [-l | -L | -N] [--extension EXTENSION] [-k EXPRESSION] [--showlocals] ...


**Positional arguments**

``pytest_args``
  arguments for pytest


**Optional arguments**

``-h, --help``
  show this help message and exit

``-H, --pytest-help``
  show full pytest help, with advanced options

``-n NUMPROCESSES, --numprocesses NUMPROCESSES``
  run tests in parallel up to this wide, default 1 for sequential

``-l, --list``
  list test filenames

``-L, --list-long``
  list all test functions

``-N, --list-names``
  list full names of all tests

``--extension EXTENSION``
  run test for a given spack extension

``-s``
  print output while tests run (disable capture)

``-k EXPRESSION``
  filter tests by keyword (can also use w/list options)

``--showlocals``
  show local variable values in tracebacks


----

.. _spack-unload:

spack unload
------------

remove package from the user environment

.. code-block:: console

    spack unload [-ha] [--sh | --csh | --fish | --bat | --pwsh] ...


**Positional arguments**

``installed_specs``
  one or more installed package specs


**Optional arguments**

``-h, --help``
  show this help message and exit

``--sh``
  print sh commands to activate the environment

``--csh``
  print csh commands to activate the environment

``--fish``
  print fish commands to load the package

``--bat``
  print bat commands to load the package

``--pwsh``
  print pwsh commands to load the package

``-a, --all``
  unload all loaded Spack packages


----

.. _spack-url:

spack url
---------

debugging tool for url parsing

.. code-block:: console

    spack url [-h] SUBCOMMAND ...


**Optional arguments**

``-h, --help``
  show this help message and exit


**Subcommands**

.. hlist::
   :columns: 4

   * :ref:`url parse <spack-url-parse>`
   * :ref:`url list <spack-url-list>`
   * :ref:`url summary <spack-url-summary>`
   * :ref:`url stats <spack-url-stats>`


----

.. _spack-url-parse:

spack url parse
^^^^^^^^^^^^^^^

.. code-block:: console

    spack url parse [-hs] url


**Positional arguments**

``url``
  url to parse


**Optional arguments**

``-h, --help``
  show this help message and exit

``-s, --spider``
  spider the source page for versions


----

.. _spack-url-list:

spack url list
^^^^^^^^^^^^^^

.. code-block:: console

    spack url list [-hce] [-n | -N | -v | -V]


**Optional arguments**

``-h, --help``
  show this help message and exit

``-c, --color``
  color the parsed version and name in the urls shown (versions will be cyan, name red)

``-e, --extrapolation``
  color the versions used for extrapolation as well (additional versions will be green, names magenta)

``-n, --incorrect-name``
  only list urls for which the name was incorrectly parsed

``-N, --correct-name``
  only list urls for which the name was correctly parsed

``-v, --incorrect-version``
  only list urls for which the version was incorrectly parsed

``-V, --correct-version``
  only list urls for which the version was correctly parsed


----

.. _spack-url-summary:

spack url summary
^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack url summary [-h]


**Optional arguments**

``-h, --help``
  show this help message and exit


----

.. _spack-url-stats:

spack url stats
^^^^^^^^^^^^^^^

.. code-block:: console

    spack url stats [-h] [--show-issues]


**Optional arguments**

``-h, --help``
  show this help message and exit

``--show-issues``
  show packages with issues (md5 hashes, http urls)


----

.. _spack-verify:

spack verify
------------

verify spack installations on disk

.. code-block:: console

    spack verify [-h] SUBCOMMAND ...


**Optional arguments**

``-h, --help``
  show this help message and exit


**Subcommands**

.. hlist::
   :columns: 4

   * :ref:`verify manifest <spack-verify-manifest>`
   * :ref:`verify libraries <spack-verify-libraries>`


----

.. _spack-verify-manifest:

spack verify manifest
^^^^^^^^^^^^^^^^^^^^^

verify that install directories have not been modified since installation

.. code-block:: console

    spack verify manifest [-hlja] [-s | -f] ...


**Positional arguments**

``specs_or_files``
  specs or files to verify


**Optional arguments**

``-h, --help``
  show this help message and exit

``-l, --local``
  verify only locally installed packages

``-j, --json``
  ouptut json-formatted errors

``-a, --all``
  verify all packages

``-s, --specs``
  treat entries as specs (default)

``-f, --files``
  treat entries as absolute filenames


----

.. _spack-verify-libraries:

spack verify libraries
^^^^^^^^^^^^^^^^^^^^^^

verify that shared libraries of install packages can be located in rpaths (Linux only)

.. code-block:: console

    spack verify libraries [-h] ...


**Positional arguments**

``installed_specs``
  constraint to select a subset of installed packages


**Optional arguments**

``-h, --help``
  show this help message and exit


----

.. _spack-versions:

spack versions
--------------

list available versions of a package

.. code-block:: console

    spack versions [-h] [-s | -r | -n] [-j JOBS] package


**Positional arguments**

``package``
  package name


**Optional arguments**

``-h, --help``
  show this help message and exit

``-s, --safe``
  only list safe versions of the package

``-r, --remote``
  only list remote versions of the package

``-n, --new``
  only list remote versions newer than the latest checksummed version

``-j JOBS, --jobs JOBS``
  explicitly set number of parallel jobs


----

.. _spack-view:

spack view
----------

project packages to a compact naming scheme on the filesystem

.. code-block:: console

    spack view [-hv] [-e EXCLUDE] [-d {true,false,yes,no}] ACTION ...


**Optional arguments**

``-h, --help``
  show this help message and exit

``-v, --verbose``
  if not verbose only warnings/errors will be printed

``-e EXCLUDE, --exclude EXCLUDE``
  exclude packages with names matching the given regex pattern

``-d {true,false,yes,no}, --dependencies {true,false,yes,no}``
  link/remove/list dependencies


**Subcommands**

.. hlist::
   :columns: 4

   * :ref:`view symlink <spack-view-symlink>`
   * :ref:`view hardlink <spack-view-hardlink>`
   * :ref:`view copy <spack-view-copy>`
   * :ref:`view remove <spack-view-remove>`
   * :ref:`view statlink <spack-view-statlink>`


----

.. _spack-view-symlink:

spack view symlink
^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack view symlink [-hi] [--projection-file PROJECTION_FILE] path spec [spec ...]


**Positional arguments**

``path``
  path to file system view directory

``spec``
  seed specs of the packages to view


**Optional arguments**

``-h, --help``
  show this help message and exit

``--projection-file PROJECTION_FILE``
  initialize view using projections from file

``-i, --ignore-conflicts``
  


----

.. _spack-view-hardlink:

spack view hardlink
^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack view hardlink [-hi] [--projection-file PROJECTION_FILE] path spec [spec ...]


**Positional arguments**

``path``
  path to file system view directory

``spec``
  seed specs of the packages to view


**Optional arguments**

``-h, --help``
  show this help message and exit

``--projection-file PROJECTION_FILE``
  initialize view using projections from file

``-i, --ignore-conflicts``
  


----

.. _spack-view-copy:

spack view copy
^^^^^^^^^^^^^^^

.. code-block:: console

    spack view copy [-hi] [--projection-file PROJECTION_FILE] path spec [spec ...]


**Positional arguments**

``path``
  path to file system view directory

``spec``
  seed specs of the packages to view


**Optional arguments**

``-h, --help``
  show this help message and exit

``--projection-file PROJECTION_FILE``
  initialize view using projections from file

``-i, --ignore-conflicts``
  


----

.. _spack-view-remove:

spack view remove
^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack view remove [-ha] [--no-remove-dependents] path [spec ...]


**Positional arguments**

``path``
  path to file system view directory

``spec``
  seed specs of the packages to view


**Optional arguments**

``-h, --help``
  show this help message and exit

``--no-remove-dependents``
  do not remove dependents of specified specs

``-a, --all``
  act on all specs in view


----

.. _spack-view-statlink:

spack view statlink
^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    spack view statlink [-h] path [spec ...]


**Positional arguments**

``path``
  path to file system view directory

``spec``
  seed specs of the packages to view


**Optional arguments**

``-h, --help``
  show this help message and exit

