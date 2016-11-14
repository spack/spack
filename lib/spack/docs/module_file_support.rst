.. _modules:

=======
Modules
=======

The use of module systems to manage user environment in a controlled way
is a common practice at HPC centers that is often embraced also by individual
programmers on their development machines. To support this common practice
Spack provides integration with `Environment Modules
<http://modules.sourceforge.net/>`_ ,  `LMod
<http://lmod.readthedocs.io/en/latest/>`_ and `Dotkit <https://computing.llnl.gov/?set=jobs&page=dotkit>`_ by:

* generating module files after a successful installation
* providing commands that can leverage the spec syntax to manipulate modules

In the following you will see how to activate shell support for commands in Spack
that requires it, and discover what benefits this may bring with respect to deal
directly with automatically generated module files.

.. note::

   If your machine does not already have a module system installed,
   we advise you to use either Environment Modules or LMod. See :ref:`InstallEnvironmentModules`
   for more details.

.. _shell_support:

-------------
Shell support
-------------

You can enable shell support by sourcing the appropriate setup file
in the ``$SPACK_ROOT/share/spack`` directory.
For ``bash`` or ``ksh`` users:

.. code-block:: console

   $ . ${SPACK_ROOT}/share/spack/setup-env.sh

For ``csh`` and ``tcsh`` instead:

.. code-block:: console

   $ source $SPACK_ROOT/share/spack/setup-env.csh


.. note::
  You can put the source line in your ``.bashrc`` or ``.cshrc`` to
  have Spack's shell support available on the command line at any login.


----------------------------
Using module files via Spack
----------------------------

If you have shell support enabled you should be able to run either
``module avail`` or ``use -l spack`` to see what module/dotkit files have
been installed.  Here is sample output of those programs, showing lots
of installed packages.

.. code-block:: console

   $ module avail

   ------- /home/gamblin2/spack/share/spack/modules/linux-debian7-x86_64 --------
   adept-utils@1.0%gcc@4.4.7-5adef8da   libelf@0.8.13%gcc@4.4.7
   automaded@1.0%gcc@4.4.7-d9691bb0     libelf@0.8.13%intel@15.0.0
   boost@1.55.0%gcc@4.4.7               mpc@1.0.2%gcc@4.4.7-559607f5
   callpath@1.0.1%gcc@4.4.7-5dce4318    mpfr@3.1.2%gcc@4.4.7
   dyninst@8.1.2%gcc@4.4.7-b040c20e     mpich@3.0.4%gcc@4.4.7
   gcc@4.9.1%gcc@4.4.7-93ab98c5         mpich@3.0.4%gcc@4.9.0
   gmp@6.0.0a%gcc@4.4.7                 mrnet@4.1.0%gcc@4.4.7-72b7881d
   graphlib@2.0.0%gcc@4.4.7             netgauge@2.4.6%gcc@4.9.0-27912b7b
   launchmon@1.0.1%gcc@4.4.7            stat@2.1.0%gcc@4.4.7-51101207
   libNBC@1.1.1%gcc@4.9.0-27912b7b      sundials@2.5.0%gcc@4.9.0-27912b7b
   libdwarf@20130729%gcc@4.4.7-b52fac98

.. code-block:: console

   $ use -l spack

   spack ----------
     adept-utils@1.0%gcc@4.4.7-5adef8da - adept-utils @1.0
     automaded@1.0%gcc@4.4.7-d9691bb0 - automaded @1.0
     boost@1.55.0%gcc@4.4.7 - boost @1.55.0
     callpath@1.0.1%gcc@4.4.7-5dce4318 - callpath @1.0.1
     dyninst@8.1.2%gcc@4.4.7-b040c20e - dyninst @8.1.2
     gmp@6.0.0a%gcc@4.4.7 - gmp @6.0.0a
     libNBC@1.1.1%gcc@4.9.0-27912b7b - libNBC @1.1.1
     libdwarf@20130729%gcc@4.4.7-b52fac98 - libdwarf @20130729
     libelf@0.8.13%gcc@4.4.7 - libelf @0.8.13
     libelf@0.8.13%intel@15.0.0 - libelf @0.8.13
     mpc@1.0.2%gcc@4.4.7-559607f5 - mpc @1.0.2
     mpfr@3.1.2%gcc@4.4.7 - mpfr @3.1.2
     mpich@3.0.4%gcc@4.4.7 - mpich @3.0.4
     mpich@3.0.4%gcc@4.9.0 - mpich @3.0.4
     netgauge@2.4.6%gcc@4.9.0-27912b7b - netgauge @2.4.6
     sundials@2.5.0%gcc@4.9.0-27912b7b - sundials @2.5.0

The names here should look familiar, they're the same ones from
``spack find``.  You *can* use the names here directly.  For example,
you could type either of these commands to load the callpath module:

.. code-block:: console

   $ use callpath@1.0.1%gcc@4.4.7-5dce4318

.. code-block:: console

   $ module load callpath@1.0.1%gcc@4.4.7-5dce4318

.. _cmd-spack-load:

^^^^^^^^^^^^^^^^^^^^^^^
``spack load / unload``
^^^^^^^^^^^^^^^^^^^^^^^

Neither of these is particularly pretty, easy to remember, or
easy to type.  Luckily, Spack has its own interface for using modules
and dotkits.  You can use the same spec syntax you're used to:

=========================  ==========================
Environment Modules        Dotkit
=========================  ==========================
``spack load <spec>``      ``spack use <spec>``
``spack unload <spec>``    ``spack unuse <spec>``
=========================  ==========================

And you can use the same shortened names you use everywhere else in
Spack.  For example, this will add the ``mpich`` package built with
``gcc`` to your path:

.. code-block:: console

   $ spack install mpich %gcc@4.4.7

   # ... wait for install ...

   $ spack use mpich %gcc@4.4.7
   Prepending: mpich@3.0.4%gcc@4.4.7 (ok)
   $ which mpicc
   ~/src/spack/opt/linux-debian7-x86_64/gcc@4.4.7/mpich@3.0.4/bin/mpicc

Or, similarly with modules, you could type:

.. code-block:: console

   $ spack load mpich %gcc@4.4.7

These commands will add appropriate directories to your ``PATH``,
``MANPATH``, ``CPATH``, and ``LD_LIBRARY_PATH``.  When you no longer
want to use a package, you can type unload or unuse similarly:

.. code-block:: console

   $ spack unload mpich %gcc@4.4.7  # modules
   $ spack unuse  mpich %gcc@4.4.7  # dotkit

.. note::

   These ``use``, ``unuse``, ``load``, and ``unload`` subcommands are
   only available if you have enabled Spack's shell support *and* you
   have dotkit or modules installed on your machine.

^^^^^^^^^^^^^^^^^^^^^^
Ambiguous module names
^^^^^^^^^^^^^^^^^^^^^^

If a spec used with load/unload or use/unuse is ambiguous (i.e. more
than one installed package matches it), then Spack will warn you:

.. code-block:: console

   $ spack load libelf
   ==> Error: Multiple matches for spec libelf.  Choose one:
   libelf@0.8.13%gcc@4.4.7 arch=linux-debian7-x86_64
   libelf@0.8.13%intel@15.0.0 arch=linux-debian7-x86_64

You can either type the ``spack load`` command again with a fully
qualified argument, or you can add just enough extra constraints to
identify one package.  For example, above, the key differentiator is
that one ``libelf`` is built with the Intel compiler, while the other
used ``gcc``.  You could therefore just type:

.. code-block:: console

   $ spack load libelf %intel

To identify just the one built with the Intel compiler.

.. _extensions:

.. _cmd-spack-module-loads:

^^^^^^^^^^^^^^^^^^^^^^
``spack module loads``
^^^^^^^^^^^^^^^^^^^^^^

In some cases, it is desirable to load not just a module, but also all
the modules it depends on.  This is not required for most modules
because Spack builds binaries with RPATH support.  However, not all
packages use RPATH to find their dependencies: this can be true in
particular for Python extensions, which are currently *not* built with
RPATH.

Scripts to load modules recursively may be made with the command:

.. code-block:: console

    $ spack module loads --dependencies <spec>

An equivalent alternative is:

.. code-block :: console

    $ source <( spack module loads --dependencies <spec> )

.. warning::

    The ``spack load`` command does not currently accept the
    ``--dependencies`` flag.  Use ``spack module loads`` instead, for
    now.

.. See #1662


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Module Commands for Shell Scripts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Although Spack is flexible, the ``module`` command is much faster.
This could become an issue when emitting a series of ``spack load``
commands inside a shell script.  By adding the ``--shell`` flag,
``spack module find`` may also be used to generate code that can be
cut-and-pasted into a shell script.  For example:

.. code-block:: console

    $ spack module loads --dependencies py-numpy git
    # bzip2@1.0.6%gcc@4.9.3=linux-x86_64
    module load bzip2-1.0.6-gcc-4.9.3-ktnrhkrmbbtlvnagfatrarzjojmkvzsx
    # ncurses@6.0%gcc@4.9.3=linux-x86_64
    module load ncurses-6.0-gcc-4.9.3-kaazyneh3bjkfnalunchyqtygoe2mncv
    # zlib@1.2.8%gcc@4.9.3=linux-x86_64
    module load zlib-1.2.8-gcc-4.9.3-v3ufwaahjnviyvgjcelo36nywx2ufj7z
    # sqlite@3.8.5%gcc@4.9.3=linux-x86_64
    module load sqlite-3.8.5-gcc-4.9.3-a3eediswgd5f3rmto7g3szoew5nhehbr
    # readline@6.3%gcc@4.9.3=linux-x86_64
    module load readline-6.3-gcc-4.9.3-se6r3lsycrwxyhreg4lqirp6xixxejh3
    # python@3.5.1%gcc@4.9.3=linux-x86_64
    module load python-3.5.1-gcc-4.9.3-5q5rsrtjld4u6jiicuvtnx52m7tfhegi
    # py-setuptools@20.5%gcc@4.9.3=linux-x86_64
    module load py-setuptools-20.5-gcc-4.9.3-4qr2suj6p6glepnedmwhl4f62x64wxw2
    # py-nose@1.3.7%gcc@4.9.3=linux-x86_64
    module load py-nose-1.3.7-gcc-4.9.3-pwhtjw2dvdvfzjwuuztkzr7b4l6zepli
    # openblas@0.2.17%gcc@4.9.3+shared=linux-x86_64
    module load openblas-0.2.17-gcc-4.9.3-pw6rmlom7apfsnjtzfttyayzc7nx5e7y
    # py-numpy@1.11.0%gcc@4.9.3+blas+lapack=linux-x86_64
    module load py-numpy-1.11.0-gcc-4.9.3-mulodttw5pcyjufva4htsktwty4qd52r
    # curl@7.47.1%gcc@4.9.3=linux-x86_64
    module load curl-7.47.1-gcc-4.9.3-ohz3fwsepm3b462p5lnaquv7op7naqbi
    # autoconf@2.69%gcc@4.9.3=linux-x86_64
    module load autoconf-2.69-gcc-4.9.3-bkibjqhgqm5e3o423ogfv2y3o6h2uoq4
    # cmake@3.5.0%gcc@4.9.3~doc+ncurses+openssl~qt=linux-x86_64
    module load cmake-3.5.0-gcc-4.9.3-x7xnsklmgwla3ubfgzppamtbqk5rwn7t
    # expat@2.1.0%gcc@4.9.3=linux-x86_64
    module load expat-2.1.0-gcc-4.9.3-6pkz2ucnk2e62imwakejjvbv6egncppd
    # git@2.8.0-rc2%gcc@4.9.3+curl+expat=linux-x86_64
    module load git-2.8.0-rc2-gcc-4.9.3-3bib4hqtnv5xjjoq5ugt3inblt4xrgkd

The script may be further edited by removing unnecessary modules.


^^^^^^^^^^^^^^^
Module Prefixes
^^^^^^^^^^^^^^^

On some systems, modules are automatically prefixed with a certain
string; ``spack module loads`` needs to know about that prefix when it
issues ``module load`` commands.  Add the ``--prefix`` option to your
``spack module loads`` commands if this is necessary.

For example, consider the following on one system:

.. code-block:: console

    $ module avail
    linux-SuSE11-x86_64/antlr-2.7.7-gcc-5.3.0-bdpl46y

    $ spack module loads antlr    # WRONG!
    # antlr@2.7.7%gcc@5.3.0~csharp+cxx~java~python arch=linux-SuSE11-x86_64
    module load antlr-2.7.7-gcc-5.3.0-bdpl46y

    $ spack module loads --prefix linux-SuSE11-x86_64/ antlr
    # antlr@2.7.7%gcc@5.3.0~csharp+cxx~java~python arch=linux-SuSE11-x86_64
    module load linux-SuSE11-x86_64/antlr-2.7.7-gcc-5.3.0-bdpl46y

----------------------------
Auto-generating Module Files
----------------------------

Module files are generated by post-install hooks after the successful
installation of a package. The following table summarizes the essential
information associated with the different file formats
that can be generated by Spack:

  +-----------------------------+--------------------+-------------------------------+----------------------+
  |                             | **Hook name**      |  **Default root directory**   | **Compatible tools** |
  +=============================+====================+===============================+======================+
  |  **Dotkit**                 | ``dotkit``         |   share/spack/dotkit          |  DotKit              |
  +-----------------------------+--------------------+-------------------------------+----------------------+
  |  **TCL - Non-Hierarchical** | ``tcl``            |  share/spack/modules          | Env. Modules/LMod    |
  +-----------------------------+--------------------+-------------------------------+----------------------+
  |  **Lua - Hierarchical**     | ``lmod``           |   share/spack/lmod            | LMod                 |
  +-----------------------------+--------------------+-------------------------------+----------------------+


Though Spack ships with sensible defaults for the generation of module files,
one can customize many aspects of it to accommodate package or site specific needs.
These customizations are enabled by either:

 1. overriding certain callback APIs in the Python packages
 2. writing specific rules in the ``modules.yaml`` configuration file

The former method fits best cases that are site independent, e.g. injecting variables
from language interpreters into their extensions. The latter instead permits to
fine tune the content, naming and creation of module files to meet site specific conventions.

^^^^^^^^^^^^^^^^^^^^
``Package`` file API
^^^^^^^^^^^^^^^^^^^^

There are two methods that can be overridden in any ``package.py`` to affect the
content of generated module files. The first one is:

.. code-block:: python

   def setup_environment(self, spack_env, run_env):
       """Set up the compile and runtime environments for a package."""
       pass

and can alter the content of *the same package where it is overridden*
by adding actions to ``run_env``. The second method is:

.. code-block:: python

   def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
       """Set up the environment of packages that depend on this one"""
       pass

and has similar effects on module file of dependees. Even in this case
``run_env`` must be filled with the desired list of environment modifications.

.. note::
 The ``R`` package and callback APIs
  A typical example in which overriding both methods prove to be useful
  is given by the ``R`` package. This package installs libraries and headers
  in non-standard locations and it is possible to prepend the appropriate directory
  to the corresponding environment variables:

  ================== =================================
   LIBRARY_PATH       ``self.prefix/rlib/R/lib``
   LD_LIBRARY_PATH    ``self.prefix/rlib/R/lib``
   CPATH              ``self.prefix/rlib/R/include``
  ================== =================================

  with the following snippet:

  .. literalinclude:: ../../../var/spack/repos/builtin/packages/R/package.py
     :pyobject: R.setup_environment

  The ``R`` package also knows which environment variable should be modified
  to make language extensions provided by other packages available, and modifies
  it appropriately in the override of the second method:

  .. literalinclude:: ../../../var/spack/repos/builtin/packages/R/package.py
     :lines: 128-129,146-151

.. _modules-yaml:

---------------------------------
Configuration in ``modules.yaml``
---------------------------------

The name of the configuration file that controls module generation behavior
is ``modules.yaml``. The default configuration:

.. literalinclude:: ../../../etc/spack/defaults/modules.yaml
   :language: yaml

activates generation for ``tcl`` and ``dotkit`` module files and inspects
the installation folder of each package for the presence of a set of subdirectories
(``bin``, ``man``, ``share/man``, etc.). If any is found its full path is prepended
to the environment variables listed below the folder name.

^^^^^^^^^^^^^^^^^^^^^^^^^^^
Activation of other systems
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Any other module file generator shipped with Spack can be activated adding it to the
list under the ``enable`` key in the module file. Currently the only generator that
is not activated by default is ``lmod``, which produces hierarchical lua module files.
For each module system that can be enabled a finer configuration is possible.

Directives that are aimed at driving the generation of a particular type of module files
should be listed under a top level key that corresponds to the generator being
customized:

.. code-block:: yaml

   modules:
     enable:
       - tcl
       - dotkit
       - lmod
     tcl:
       # contains environment modules specific customizations
     dotkit:
       # contains dotkit specific customizations
     lmod:
       # contains lmod specific customizations

All these module sections allow for both:

1. global directives that usually affect the whole layout of modules or the naming scheme
2. directives that affect only a set of packages and modify their content

For the latter point in particular it is possible to use anonymous specs
to select an appropriate set of packages on which the modifications should be applied.

.. _anonymous_specs:

^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Selection by anonymous specs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The procedure to select packages using anonymous specs is a natural
extension of using them to install packages, the only difference being
that specs in this case **are not required to have a root package**.
Consider for instance this snippet:

.. code-block:: yaml

   modules:
     tcl:
       # The keyword `all` selects every package
       all:
         environment:
           set:
             BAR: 'bar'
       # This anonymous spec selects any package that
       # depends on openmpi. The double colon at the
       # end clears the set of rules that matched so far.
       ^openmpi::
         environment:
           set:
             BAR: 'baz'
       # Selects any zlib package
       zlib:
         environment:
           prepend_path:
             LD_LIBRARY_PATH: 'foo'
       # Selects zlib compiled with gcc@4.8
       zlib%gcc@4.8:
         environment:
           unset:
           - FOOBAR

During module file generation, the configuration above will instruct
Spack to set the environment variable ``BAR=bar`` for every module,
unless the associated spec satisfies ``^openmpi`` in which case ``BAR=baz``.
In addition in any spec that satisfies ``zlib`` the value ``foo`` will be
prepended to ``LD_LIBRARY_PATH`` and in any spec that satisfies ``zlib%gcc@4.8``
the variable ``FOOBAR`` will be unset.

.. note::
   Order does matter
     The modifications associated with the ``all`` keyword are always evaluated
     first, no matter where they appear in the configuration file. All the other
     spec constraints are instead evaluated top to bottom.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Blacklist or whitelist the generation of specific module files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Anonymous specs are also used to prevent module files from being written or
to force them to be written. A common case for that at HPC centers is to hide
from users all of the software that needs to be built with system compilers.
Suppose for instance to have ``gcc@4.4.7`` provided by your system. Then
with a configuration file like this one:

.. code-block:: yaml

   modules:
     tcl:
       whitelist: ['gcc', 'llvm']  # Whitelist will have precedence over blacklist
       blacklist: ['%gcc@4.4.7']   # Assuming gcc@4.4.7 is the system compiler

you will skip the generation of module files for any package that
is compiled with ``gcc@4.4.7``, with the exception of any ``gcc``
or any ``llvm`` installation.

^^^^^^^^^^^^^^^^^^^^^^^^^^^
Customize the naming scheme
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The names of environment modules generated by spack are not always easy to
fully comprehend due to the long hash in the name. There are two module
configuration options to help with that. The first is a global setting to
adjust the hash length. It can be set anywhere from 0 to 32 and has a default
length of 7. This is the representation of the hash in the module file name and
does not affect the size of the package hash. Be aware that the smaller the
hash length the more likely naming conflicts will occur. The following snippet
shows how to set hash length in the module file names:

.. code-block:: yaml

   modules:
     tcl:
       hash_length: 7

To help make module names more readable, and to help alleviate name conflicts
with a short hash, one can use the ``suffixes`` option in the modules
configuration file. This option will add strings to modules that match a spec.
For instance, the following config options,

.. code-block:: yaml

   modules:
     tcl:
       all:
         suffixes:
           ^python@2.7.12: 'python-2.7.12'
           ^openblas: 'openblas'

will add a ``python-2.7.12`` version string to any packages compiled with
python matching the spec, ``python@2.7.12``. This is useful to know which
version of python a set of python extensions is associated with. Likewise, the
``openblas`` string is attached to any program that has openblas in the spec,
most likely via the ``+blas`` variant specification.

.. note::
   TCL module files
     A modification that is specific to ``tcl`` module files is the possibility
     to change the naming scheme of modules.

     .. code-block:: yaml

       modules:
         tcl:
           naming_scheme: '${PACKAGE}/${VERSION}-${COMPILERNAME}-${COMPILERVER}'
           all:
             conflict: ['${PACKAGE}', 'intel/14.0.1']

     will create module files that will conflict with ``intel/14.0.1`` and with the
     base directory of the same module, effectively preventing the possibility to
     load two or more versions of the same software at the same time. The tokens
     that are available for use in this directive are the same understood by
     the ``Spec.format`` method.


.. note::
   LMod hierarchical module files
     When ``lmod`` is activated Spack will generate a set of hierarchical lua module
     files that are understood by LMod. The generated hierarchy always contains the
     three layers ``Core`` / ``Compiler`` / ``MPI`` but can be further extended to
     any other virtual dependency present in Spack. A case that could be useful in
     practice is for instance:

     .. code-block:: yaml

       modules:
         enable:
           - lmod
         lmod:
           core_compilers: ['gcc@4.8']
           hierarchical_scheme: ['lapack']

     that will generate a hierarchy in which the ``lapack`` layer is treated as the ``mpi``
     one. This allows a site to build the same libraries or applications against different
     implementations of ``mpi`` and ``lapack``, and let LMod switch safely from one to the
     other.

.. warning::
  Deep hierarchies and ``lmod spider``
   For hierarchies that are deeper than three layers ``lmod spider`` may have some issues.
   See `this discussion on the LMod project <https://github.com/TACC/Lmod/issues/114>`_.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Filter out environment modifications
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Modifications to certain environment variables in module files are generated by
default, for instance by prefix inspections in the default configuration file.
There are cases though where some of these modifications are unwanted.
Suppose you need to avoid having ``CPATH`` and ``LIBRARY_PATH``
modified by your ``dotkit`` modules:

.. code-block:: yaml

   modules:
     dotkit:
       all:
         filter:
           # Exclude changes to any of these variables
           environment_blacklist: ['CPATH', 'LIBRARY_PATH']

The configuration above will generate dotkit module files that will not contain
modifications to either ``CPATH`` or ``LIBRARY_PATH`` and environment module
files that instead will contain these modifications.

^^^^^^^^^^^^^^^^^^^^^
Autoload dependencies
^^^^^^^^^^^^^^^^^^^^^

In some cases it can be useful to have module files directly autoload
their dependencies.  This may be the case for Python extensions, if not
activated using ``spack activate``:

.. code-block:: yaml

   modules:
     tcl:
       ^python:
         autoload: 'direct'

The configuration file above will produce module files that will
automatically load their direct dependencies. The allowed values for the
``autoload`` statement are either ``none``, ``direct`` or ``all``.

.. note::
  TCL prerequisites
     In the ``tcl`` section of the configuration file it is possible to use
     the ``prerequisites`` directive that accepts the same values as
     ``autoload``. It will produce module files that have a ``prereq``
     statement instead of automatically loading other modules.

------------------------
Maintaining Module Files
------------------------

Spack not only provides great flexibility in the generation of module files
and in the customization of both their layout and content, but also ships with
a tool to ease the burden of their maintenance in production environments.
This tool is the ``spack module`` command:

.. command-output:: spack module --help

.. _cmd-spack-module-refresh:

^^^^^^^^^^^^^^^^^^^^^^^^
``spack module refresh``
^^^^^^^^^^^^^^^^^^^^^^^^

The command that regenerates module files to update their content or
their layout is ``module refresh``:

.. command-output:: spack module refresh --help

A set of packages can be selected using anonymous specs for the optional
``constraint`` positional argument. The argument ``--module-type`` identifies
the type of module files to refresh. Optionally the entire tree can be deleted
before regeneration if the change in layout is radical.

.. _cmd-spack-module-rm:

^^^^^^^^^^^^^^^^^^^
``spack module rm``
^^^^^^^^^^^^^^^^^^^

If instead what you need is just to delete a few module files, then the right
command is ``module rm``:

.. command-output:: spack module rm --help

.. note::
  We care about your module files!
   Every modification done on modules
   that are already existing will ask for a confirmation by default. If
   the command is used in a script it is possible though to pass the
   ``-y`` argument, that will skip this safety measure.
