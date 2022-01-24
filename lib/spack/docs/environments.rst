.. Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _environments:

============
Environments
============

Spack environments group independent sets of specs allowing them to
be processed together. They provide *virtual environments* similar to
those supported by other commonly used tools, such as `Python venv
<https://docs.python.org/3/library/venv.html>`_ and `Conda environments
<https://conda.io/docs/user-guide/tasks/manage-environments.html>`_.
However, Spack environments provide some distinctive features:

#. A spec installed "in" an environment is no different from the same
   spec installed anywhere else in Spack.  Environments are assembled
   simply by collecting together a set of specs.
#. Spack environments may contain more than one spec of the same
   package.
#. Multiple environments associated with a Spack instance seamlessly
   share the installed software.

Spack uses a "manifest and lock" model similar to `Bundler gemfiles
<https://bundler.io/man/gemfile.5.html>`_ and other package
managers. The user input file is named ``spack.yaml`` and the lock
file is named ``spack.lock``.

.. _environments-advantages:

-------------------
Uses and Advantages
-------------------

Environments facilitate software development and deployment in ways
that can include:

* An Environment is treated as a unit of operation.
  At the most basic level, environments allow for the separation
  of the steps for (a) choosing what to install, (b) determining
  which options apply, and (c) installing the software.
  All of the options for the specs are determined during concretization.
* Environments provide stability and repeatability.
  The separation of steps in the build process allows environments
  to remain stable and repeatable even if packages are upgraded.
  Specs are only re-concretized and installed when the user explicitly
  performs those operations.
* Environments provide a view of the installed software.
  An environment can be configured to maintain a filesystem view
  of its installed software, allowing that view to be loaded into
  the user environment at activation time.
* Environments support build reproduction.
  Environment files can be shared with others to `reproduce builds
  <https://spack-tutorial.readthedocs.io/en/latest/tutorial_environments.html#reproducing-builds>`_
  on the same or other systems.
* Environments enable building software on air-gapped networks.
  Environments can be used to create `mirrors
  <https://spack.readthedocs.io/en/latest/mirrors.html>`_ of
  software that would otherwise have to be downloaded from the
  internet.
* Environments enable reducing the load of recompiling software.
  Builds of an environment's software can be saved to a `binary cache
  <https://spack.readthedocs.io/en/latest/binary_caches.html>`_,
  allowing teams to avoid unnecessarily re-building software on
  the system.
* Environments provide the foundation for CI.
  Spack environments can be configured to generate CI `pipelines
  <https://spack.readthedocs.io/en/latest/pipelines.html>`_.
* Environments support common `developer workflows
  <https://spack-tutorial.readthedocs.io/en/latest/tutorial_developer_workflows.html#>`_.
  Teams can use environments to help manage their development of
  software across multiple packages.
* Environments can be used to create `container images
  <https://spack.readthedocs.io/en/latest/containers.html>`_.
* Environments can be used to manage large software deployments.
  Software deployments can be configured with `Spack stacks
  <https://spack-tutorial.readthedocs.io/en/latest/tutorial_stacks.html>`_.


.. _environments-types:

---------------------
Types of Environments
---------------------

Environments are either Spack-managed or independent. Both types
are defined by their ``spack.yaml`` and, once concretized, their
``spack.lock`` files.

^^^^^^^^^^^^^^^^^^^^
Managed Environments
^^^^^^^^^^^^^^^^^^^^

*Managed environments* are created using `spack env create env-name`,
where `env-name` is the name of the environment. Spack automatically
creates a subdirectory of the Spack instance's `var/spack/environments`
directory with the provided name. Since they are managed (and named),
you can reference them by their names.

^^^^^^^^^^^^^^^^^^^^^^^^
Independent Environments
^^^^^^^^^^^^^^^^^^^^^^^^

*Independent environments* live outside of the Spack instance's
`var/spack/environments` directory. They can be created using
`spack env create -d env-directory`, where `env-directory` is
the directory that is to contain the Spack environment files.
Or they can be "created" by placing the spack file(s) in any
directory (other than that used for managed environments).

Since they are not tied to a Spack instance, the environment
files can be versioned in a non-Spack repository making them
quite useful for project CI/CD and developer workflows. They
can also simply be shared for activities such as build reproduction.
Links to these options and more can be found 
:ref:`above <environments-advantages>`.


.. _environments-creating:

-----------------------
Creating an Environment
-----------------------

The first step in using a Spack environment is to create one.
The process and results are similar whether the environment
is managed or independent.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Creating a Managed Environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A managed environment is created by passing a name to the 
``spack env create`` command:

.. code-block:: console

   $ spack env create myenv

Spack then creates the directory ``var/spack/environments/myenv``
and, within it, the environment file ``spack.yaml`` and hidden
``.spack-env`` subdirectory.

Spack stores metadata in the ``.spack-env`` directory. User
interactions will occur through the ``spack.yaml`` file and the
Spack commands that affect it. When the environment is concretized,
Spack will create a file ``spack.lock`` with the concrete information
for the environment.

In addition to being the default location for the view associated
with an Environment, the ``.spack-env`` directory also contains
the following subdirectories:

  * ``repo``: A repo consisting of the Spack packages used in this
    environment.  This allows the environment to build the same, in
    theory, even on different versions of Spack with different
    packages!
  * ``logs``: A directory containing the build logs for the packages
    in this Environment.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Creating an Independent Environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As mentioned previously, independent environments are those
whose environment files do not reside within Spack's managed
environment directory. In other words, any directory can be
treated as an environment.

You can create a new independent environment in the current
directory using:

.. code-block:: console

   $ spack env create -d .

In this case Spack creates a ``spack.yaml`` file in the present
directory.

Alternatively, you can create an independent environment from an
existing ``spack.yaml`` manifest or a ``spack.lock`` lockfile.
In either case you can work in the directory where the files
reside or pass the full path to the files.

To create ``myenv`` from a ``spack.yaml`` manifest in the current
directory, enter:

.. code-block:: console

   $ spack env create myenv spack.yaml

.. note::

   A Spack environment created from a ``spack.yaml`` manifest
   is guaranteed to have the same root specs as the original
   environment, but may concretize differently.

If you want a more exact reproduction of the existing environment,
you can use the ``spack.lock`` lockfile by entering:

.. code-block:: console

   $ spack env create myenv spack.lock

.. note::

   A Spack environment created from a ``spack.lock`` lockfile
   is guaranteed to have the same concrete specs as the original
   environment.


.. _environments-activating:

--------------------------
Activating an Environment
--------------------------

Once the environment has been created, you will need to activate it
before you can use it.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Activating a Managed Environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To activate the managed environment, use the following command:

.. code-block:: console

   $ spack env activate myenv

or the shortcut alias

.. code-block:: console

   $ spacktivate myenv

By default, ``spack env activate`` will load the view associated
with the environment into the user environment. 

Options affecting the user environment are:

* ``-v, --with-view``:  ensures the environment view is loaded
* ``-V, --without-view``: activates the environment without changing
  the user environment variables

There is another handy option for those who like to modify their
prompts. The ``-p`` option changes the user's prompt to begin with
the environment name in brackets.

.. code-block:: console

   $ spack env activate -p myenv
   [myenv] $ ...

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Activating an Independent Environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Recall that independent environments are not managed by Spack or
accessed by name; rather, they are identified by their directory.
So, activating an independent environment simply requires the
``-d </path/to/myenv/directory>`` arguments.  For example:

.. code-block:: console

   $ spack env activate -d /path/to/myenv/directory

You can also use the ``-v`` and ``-V`` options described for
managed environments to affect the user environment.

.. _environments-deactivating:

----------------------------
Deactivating an Environment
----------------------------

When you are done using the environment you'll want to deactivate
it, especially if you are switching environments within a Spack
instance.

To deactivate either type of environment, enter:

.. code-block:: console

   $ spack env deactivate

or the shortcut alias

.. code-block:: console

   $ despacktivate

If the environment was activated with its view, deactivating the
environment will remove the view from the user environment.

.. _environments-using:

---------------------------
Using an Active Environment
---------------------------

All Spack commands that act on lists of installed specs are aware of,
or sensitive to, the associated specs **when the environment is active**.
For example, the ``find`` command shows only the specs in the environment.
The ``install`` and ``uninstall`` commands are similarly limited.

.. note::

   All environment-aware commands can also be called using the
   ``spack -e`` flag to specify the environment.

.. _environments-experiment:

^^^^^^^^^^
Experiment
^^^^^^^^^^

This section provides a simple experiment to illustrate the
affects of a few core commands when an environment is versus
is not active.

To see the affects of a few commands, you can experiment with
installing and creating a managed environment from a fresh Spack
clone. Enter the following commands:

.. code-block:: console

  $ spack find
  ==> 0 installed packages

  $ spack install zlib@1.2.11
  ==> Installing zlib-1.2.11-q6cqrdto4iktfg6qyqcc5u4vmfmwb7iv
  ==> No binary for zlib-1.2.11-q6cqrdto4iktfg6qyqcc5u4vmfmwb7iv found: installing from source
  ==> zlib: Executing phase: 'install'
  [+] ~/spack/opt/spack/linux-rhel7-broadwell/gcc-8.1.0/zlib-1.2.11-q6cqrdto4iktfg6qyqcc5u4vmfmwb7iv

  $ spack env create myenv
  ==> Updating view at ~/spack/var/spack/environments/myenv/.spack-env/view
  ==> Created environment 'myenv' in ~/spack/var/spack/environments/myenv
  ==> You can activate this environment with:
  ==>   spack env activate myenv

  $ spack env activate myenv

  $ spack find
  ==> In environment myenv
  ==> No root specs
  ==> 0 installed packages

  $ spack install zlib@1.2.8
  ==> Installing zlib-1.2.8-yfc7epf57nsfn2gn4notccaiyxha6z7x
  ==> No binary for zlib-1.2.8-yfc7epf57nsfn2gn4notccaiyxha6z7x found: installing from source
  ==> zlib: Executing phase: 'install'
  [+] ~/spack/opt/spack/linux-rhel7-broadwell/gcc-8.1.0/zlib-1.2.8-yfc7epf57nsfn2gn4notccaiyxha6z7x
  ==> Updating view at ~/spack/var/spack/environments/myenv/.spack-env/view

  $ spack find
  ==> In environment myenv
  ==> Root specs
  zlib@1.2.8

  ==> 1 installed package
  -- linux-rhel7-broadwell / gcc@8.1.0 ----------------------------
  zlib@1.2.8

  $ despacktivate

  $ spack find
  ==> 2 installed packages
  -- linux-rhel7-broadwell / gcc@8.1.0 ----------------------------
  zlib@1.2.8  zlib@1.2.11


Notice that when we installed the abstract spec ``zlib@1.2.8``, the
spec is retained as a root spec in the environment. The Spack instance,
however, has two versions of the package installed: ``zlib@1.2.8``
and ``zlib@1.2.11``.

.. note::

   All packages explicitly installed in an environment are considered
   root specs.

While this simple exercise shows how Spack tracks installed specs,
it *does not* represent the typical use of environments.

^^^^^^^^^^^^^^^^^^^^^
Adding Abstract Specs
^^^^^^^^^^^^^^^^^^^^^

Environments are meant to define a group of specs as a related
unit. That means the environment needs to be configured to contain
multiple specs. This is accomplished by adding abstract specs to
the environment's ``spack.yaml`` manifest.

Abstract specs can be added to the active environment through the
``spack add`` command or directly using an editor. For simplicity,
let's use the command:

.. code-block:: console

   $ spack env activate myenv
   $ spack add mpileaks

or

.. code-block:: console

   $ spack -e myenv add mpileaks

.. note::

   An *abstract spec* is the user-specified spec *before* Spack
   has applied any defaults or dependency information. Adding
   an abstract spec, therefore, does *not* affect the concrete
   specs in the ``spack.lock`` lockfile nor does it install the
   spec.

.. _environments_concretization:

^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Concretizing Abstract Specs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once an active environment has a list of abstract specs, those
specs need to be concretized -- the application of defaults and
dependencies -- before the software can be installed. There are
actually two ways specs can be concretized:

* concretize separately (default); and
* concretize together.

*Concretizing specs separately* -- one after the other -- is useful
for deploying a full software stack containing multiple configurations
of the same package to be installed alongside each other. This is
typically the preference for HPC centers and user support groups.

*Concretizing specs together* -- in a self-consistent way -- ensures
a single configuration is installed for each package in the environment.
Software developers tend to favor this approach for deployment.

We will defer discussion of how to configure the environment to choose
the non-default option to :ref:`environment-configuration`.

Entering the following command will ensure all of the root specs are
concretized according to the constraints prescribed in the configuration:

.. code-block:: console

   [myenv]$ spack concretize

Only the specs added and not yet concretized (concretizing separately)
are actually concretized. This guarantees that already concretized specs
are unchanged in the environment.

You can force the re-concretization of all of the environment's specs
using:

.. code-block:: console

   [myenv]$ spack concretize -f

.. note::

   The ``concretize`` command does **not** install any packages.

Not sure what has and has not been concretized?

The ``spack find -c`` (or ``--concretized``) makes the distinction.

.. code-block:: console

  [myenv]$ spack add zlib
  [myenv]$ spack concretize
  [myenv]$ spack find -c
  ==> In environment myenv
  ==> Root specs
  zlib

  ==> Concretized roots
  -- linux-rhel7-x86_64 / gcc@4.9.3 -------------------------------
  zlib@1.2.11

  ==> 0 installed packages


.. _installing-environment:

^^^^^^^^^^^^^^^^^^^^^^^^^
Installing an Environment
^^^^^^^^^^^^^^^^^^^^^^^^^

The entire active environment can be installed without providing
any arguments to ``spack install``:

.. code-block:: console

   [myenv]$ spack install

Spack creates symbolic links in the environment's ``logs`` subdirectory,
allowing for easy inspection of build logs related to that environment.
The command also creates a Spack repo under the ``repos/`` subdirectory
that contains the ``package.py`` file used at install time.

.. note::

   If the environment's specs have not been concretized,
   ``spack install`` will do so before it installs them.

.. note::

   RESUME HERE

The ``--no-add`` option can be used in a concrete environment to tell
spack to install specs already present in the environment but not to
add any new root specs to the environment.  For root specs provided
to ``spack install`` on the command line, ``--no-add`` is the default,
while for dependency specs on the other hand, it is optional.  In other
words, if there is an unambiguous match in the active concrete environment
for a root spec provided to ``spack install`` on the command line, spack
does not require you to specify the ``--no-add`` option to prevent the spec
from being added again.  At the same time, a spec that already exists in the
environment, but only as a dependency, will be added to the environment as a
root spec without the ``--no-add`` option.

^^^^^^^^^^^^^^^^^^^^^^
Creating a Load Script
^^^^^^^^^^^^^^^^^^^^^^

You can create a load script for an installed environment to facilitate
setting up the user environment with the following command:

.. code-block:: console

   $ spack env loads -r

The file, called ``loads``, is written in the environment directory.

Sourcing the (``bash``) ``loads`` file will make the environment
available to the user and can be included in ``.bashrc`` files,
etc. The file may also be copied out of the environment, renamed,
etc.

.. _environment-configuration:

------------------------
Configuring Environments
------------------------

A variety of Spack behaviors are changed through Spack configuration
files, covered in more detail in the :ref:`configuration`
section.

Spack environments provide an additional level of configuration scope
between the custom scope and the user scope discussed in the
configuration documentation.

There are two ways to include configuration information in a Spack environment:

#. Inline in the ``spack.yaml`` file

#. Included in the ``spack.yaml`` file from another file.

Many Spack commands also affect configuration information in files
automatically. Those commands take a ``--scope`` argument, and the
environment can be specified by ``env:NAME`` (to affect environment
``foo``, set ``--scope env:foo``). These commands will automatically
manipulate configuration inline in the ``spack.yaml`` file.

^^^^^^^^^^^^^^^^^^^^^
Inline configurations
^^^^^^^^^^^^^^^^^^^^^

Inline Environment-scope configuration is done using the same yaml
format as standard Spack configuration scopes, covered in the
:ref:`configuration` section. Each section is contained under a
top-level yaml object with it's name. For example, a ``spack.yaml``
manifest file containing some package preference configuration (as in
a ``packages.yaml`` file) could contain:

.. code-block:: yaml

   spack:
     ...
     packages:
       all:
         compiler: [intel]
     ...

This configuration sets the default compiler for all packages to
``intel``.

^^^^^^^^^^^^^^^^^^^^^^^
Included configurations
^^^^^^^^^^^^^^^^^^^^^^^

Spack environments allow an ``include`` heading in their yaml
schema. This heading pulls in external configuration files and applies
them to the Environment.

.. code-block:: yaml

   spack:
     include:
     - relative/path/to/config.yaml
     - /absolute/path/to/packages.yaml

Environments can include files with either relative or absolute
paths. Inline configurations take precedence over included
configurations, so you don't have to change shared configuration files
to make small changes to an individual Environment. Included configs
listed earlier will have higher precedence, as the included configs are
applied in reverse order.

-------------------------------
Manually Editing the Specs List
-------------------------------

The list of abstract/root specs in the Environment is maintained in
the ``spack.yaml`` manifest under the heading ``specs``.

.. code-block:: yaml

   spack:
       specs:
         - ncview
         - netcdf
         - nco
         - py-sphinx

Appending to this list in the yaml is identical to using the ``spack
add`` command from the command line. However, there is more power
available from the yaml file.

^^^^^^^^^^^^^^^^^^^
Spec concretization
^^^^^^^^^^^^^^^^^^^

Specs can be concretized separately or together, as already
explained in :ref:`environments_concretization`. The behavior active
under any environment is determined by the ``concretization`` property:

.. code-block:: yaml

   spack:
       specs:
         - ncview
         - netcdf
         - nco
         - py-sphinx
       concretization: together

which can currently take either one of the two allowed values ``together`` or ``separately``
(the default).

.. admonition:: Re-concretization of user specs

   When concretizing specs together the entire set of specs will be
   re-concretized after any addition of new user specs, to ensure that
   the environment remains consistent. When instead the specs are concretized
   separately only the new specs will be re-concretized after any addition.

^^^^^^^^^^^^^
Spec Matrices
^^^^^^^^^^^^^

Entries in the ``specs`` list can be individual abstract specs or a
spec matrix.

A spec matrix is a yaml object containing multiple lists of specs, and
evaluates to the cross-product of those specs. Spec matrices also
contain an ``excludes`` directive, which eliminates certain
combinations from the evaluated result.

The following two Environment manifests are identical:

.. code-block:: yaml

   spack:
     specs:
       - zlib %gcc@7.1.0
       - zlib %gcc@4.9.3
       - libelf %gcc@7.1.0
       - libelf %gcc@4.9.3
       - libdwarf %gcc@7.1.0
       - cmake

   spack:
     specs:
       - matrix:
           - [zlib, libelf, libdwarf]
           - ['%gcc@7.1.0', '%gcc@4.9.3']
         exclude:
           - libdwarf%gcc@4.9.3
       - cmake

Spec matrices can be used to install swaths of software across various
toolchains.

The concretization logic for spec matrices differs slightly from the
rest of Spack. If a variant or dependency constraint from a matrix is
invalid, Spack will reject the constraint and try again without
it. For example, the following two Environment manifests will produce
the same specs:

.. code-block:: yaml

   spack:
     specs:
       - matrix:
           - [zlib, libelf, hdf5+mpi]
           - [^mvapich2@2.2, ^openmpi@3.1.0]

   spack:
     specs:
       - zlib
       - libelf
       - hdf5+mpi ^mvapich2@2.2
       - hdf5+mpi ^openmpi@3.1.0

This allows one to create toolchains out of combinations of
constraints and apply them somewhat indiscriminately to packages,
without regard for the applicability of the constraint.

^^^^^^^^^^^^^^^^^^^^
Spec List References
^^^^^^^^^^^^^^^^^^^^

The last type of possible entry in the specs list is a reference.

The Spack environment manifest yaml schema contains an additional
heading ``definitions``. Under definitions is an array of yaml
objects. Each object has one or two fields. The one required field is
a name, and the optional field is a ``when`` clause.

The named field is a spec list. The spec list uses the same syntax as
the ``specs`` entry. Each entry in the spec list can be a spec, a spec
matrix, or a reference to an earlier named list. References are
specified using the ``$`` sigil, and are "splatted" into place
(i.e. the elements of the referent are at the same level as the
elements listed separately). As an example, the following two manifest
files are identical.

.. code-block:: yaml

   spack:
     definitions:
       - first: [libelf, libdwarf]
       - compilers: ['%gcc', '%intel']
       - second:
           - $first
           - matrix:
               - [zlib]
               - [$compilers]
     specs:
       - $second
       - cmake

   spack:
     specs:
       - libelf
       - libdwarf
       - zlib%gcc
       - zlib%intel
       - cmake

.. note::

   Named spec lists in the definitions section may only refer
   to a named list defined above itself. Order matters.

In short files like the example, it may be easier to simply list the
included specs. However for more complicated examples involving many
packages across many toolchains, separately factored lists make
Environments substantially more manageable.

Additionally, the ``-l`` option to the ``spack add`` command allows
one to add to named lists in the definitions section of the manifest
file directly from the command line.

The ``when`` directive can be used to conditionally add specs to a
named list. The ``when`` directive takes a string of Python code
referring to a restricted set of variables, and evaluates to a
boolean. The specs listed are appended to the named list if the
``when`` string evaluates to ``True``. In the following snippet, the
named list ``compilers`` is ``['%gcc', '%clang', '%intel']`` on
``x86_64`` systems and ``['%gcc', '%clang']`` on all other systems.

.. code-block:: yaml

   spack:
     definitions:
       - compilers: ['%gcc', '%clang']
       - when: arch.satisfies('x86_64:')
         compilers: ['%intel']

.. note::

   Any definitions with the same named list with true ``when``
   clauses (or absent ``when`` clauses) will be appended together

The valid variables for a ``when`` clause are:

#. ``platform``. The platform string of the default Spack
   architecture on the system.

#. ``os``. The os string of the default Spack architecture on
   the system.

#. ``target``. The target string of the default Spack
   architecture on the system.

#. ``architecture`` or ``arch``. A Spack spec satisfying the default Spack
   architecture on the system. This supports querying via the ``satisfies``
   method, as shown above.

#. ``arch_str``. The architecture string of the default Spack architecture
   on the system.

#. ``re``. The standard regex module in Python.

#. ``env``. The user environment (usually ``os.environ`` in Python).

#. ``hostname``. The hostname of the system (if ``hostname`` is an
   executable in the user's PATH).

^^^^^^^^^^^^^^^^^^^^^^^^
SpecLists as Constraints
^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies and compilers in Spack can be both packages in an
environment and constraints on other packages. References to SpecLists
allow a shorthand to treat packages in a list as either a compiler or
a dependency using the ``$%`` or ``$^`` syntax respectively.

For example, the following environment has three root packages:
``gcc@8.1.0``, ``mvapich2@2.3.1 %gcc@8.1.0``, and ``hdf5+mpi
%gcc@8.1.0 ^mvapich2@2.3.1``.

.. code-block:: yaml

   spack:
     definitions:
     - compilers: [gcc@8.1.0]
     - mpis: [mvapich2@2.3.1]
     - packages: [hdf5+mpi]

     specs:
     - $compilers
     - matrix:
       - [$mpis]
       - [$%compilers]
     - matrix:
       - [$packages]
       - [$^mpis]
       - [$%compilers]

This allows for a much-needed reduction in redundancy between packages
and constraints.

----------------
Filesystem Views
----------------

Spack environments can define filesystem views, which provide a direct access point
for software similar to the directory hierarchy that might exist under ``/usr/local``.
Filesystem views are updated every time the environment is written out to the lock
file ``spack.lock``, so the concrete environment and the view are always compatible.
The files of the view's installed packages are brought into the view by symbolic or
hard links, referencing the original Spack installation, or by copy.

.. _configuring_environment_views:

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Configuration in ``spack.yaml``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Spack Environment manifest file has a top-level keyword
``view``. Each entry under that heading is a **view descriptor**, headed
by a name. Any number of views may be defined under the ``view`` heading.
The view descriptor contains the root of the view, and
optionally the projections for the view, ``select`` and
``exclude`` lists for the view and link information via ``link`` and
``link_type``.

For example, in the following manifest
file snippet we define a view named ``mpis``, rooted at
``/path/to/view`` in which all projections use the package name,
version, and compiler name to determine the path for a given
package. This view selects all packages that depend on MPI, and
excludes those built with the PGI compiler at version 18.5.
The root specs with their (transitive) link and run type dependencies
will be put in the view due to the  ``link: all`` option,
and the files in the view will be symlinks to the spack install
directories.

.. code-block:: yaml

   spack:
     ...
     view:
       mpis:
         root: /path/to/view
         select: [^mpi]
         exclude: ['%pgi@18.5']
         projections:
           all: {name}/{version}-{compiler.name}
         link: all
         link_type: symlink

The default for the ``select`` and
``exclude`` values is to select everything and exclude nothing. The
default projection is the default view projection (``{}``). The ``link``
attribute allows the following values:

#. ``link: all`` include root specs with their transitive run and link type
   dependencies (default);
#. ``link: run`` include root specs with their transitive run type dependencies;
#. ``link: roots`` include root specs without their dependencies.

The ``link_type`` defaults to ``symlink`` but can also take the value
of ``hardlink`` or ``copy``.

.. tip::

   The option ``link: run`` can be used to create small environment views for
   Python packages. Python will be able to import packages *inside* of the view even
   when the environment is not activated, and linked libraries will be located
   *outside* of the view thanks to rpaths.


There are two shorthands for environments with a single view. If the
environment at ``/path/to/env`` has a single view, with a root at
``/path/to/env/.spack-env/view``, with default selection and exclusion
and the default projection, we can put ``view: True`` in the
environment manifest. Similarly, if the environment has a view with a
different root, but default selection, exclusion, and projections, the
manifest can say ``view: /path/to/view``. These views are
automatically named ``default``, so that

.. code-block:: yaml

   spack:
     ...
     view: True

is equivalent to

.. code-block:: yaml

   spack:
     ...
     view:
       default:
         root: .spack-env/view

and

.. code-block:: yaml

   spack:
     ...
     view: /path/to/view

is equivalent to

.. code-block:: yaml

   spack:
     ...
     view:
       default:
         root: /path/to/view

By default, Spack environments are configured with ``view: True`` in
the manifest. Environments can be configured without views using
``view: False``. For backwards compatibility reasons, environments
with no ``view`` key are treated the same as ``view: True``.

From the command line, the ``spack env create`` command takes an
argument ``--with-view [PATH]`` that sets the path for a single, default
view. If no path is specified, the default path is used (``view:
True``). The argument ``--without-view`` can be used to create an
environment without any view configured.

The ``spack env view`` command can be used to change the manage views
of an Environment. The subcommand ``spack env view enable`` will add a
view named ``default`` to an environment. It takes an optional
argument to specify the path for the new default view. The subcommand
``spack env view disable`` will remove the view named ``default`` from
an environment if one exists. The subcommand ``spack env view
regenerate`` will regenerate the views for the environment. This will
apply any updates in the environment configuration that have not yet
been applied.

.. _view_projections:

""""""""""""""""
View Projections
""""""""""""""""
The default projection into a view is to link every package into the
root of the view. The projections attribute is a mapping of partial specs to
spec format strings, defined by the :meth:`~spack.spec.Spec.format`
function, as shown in the example below:

.. code-block:: yaml

   projections:
     zlib: {name}-{version}
     ^mpi: {name}-{version}/{^mpi.name}-{^mpi.version}-{compiler.name}-{compiler.version}
     all: {name}-{version}/{compiler.name}-{compiler.version}

The entries in the projections configuration file must all be either
specs or the keyword ``all``. For each spec, the projection used will
be the first non-``all`` entry that the spec satisfies, or ``all`` if
there is an entry for ``all`` and no other entry is satisfied by the
spec. Where the keyword ``all`` appears in the file does not
matter.

Given the example above, the spec ``zlib@1.2.8``
will be linked into ``/my/view/zlib-1.2.8/``, the spec
``hdf5@1.8.10+mpi %gcc@4.9.3 ^mvapich2@2.2`` will be linked into
``/my/view/hdf5-1.8.10/mvapich2-2.2-gcc-4.9.3``, and the spec
``hdf5@1.8.10~mpi %gcc@4.9.3`` will be linked into
``/my/view/hdf5-1.8.10/gcc-4.9.3``.

If the keyword ``all`` does not appear in the projections
configuration file, any spec that does not satisfy any entry in the
file will be linked into the root of the view as in a single-prefix
view. Any entries that appear below the keyword ``all`` in the
projections configuration file will not be used, as all specs will use
the projection under ``all`` before reaching those entries.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Activating environment views
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``spack env activate`` command will put the default view for the
environment into the user's path, in addition to activating the
environment for Spack commands. The arguments ``-v,--with-view`` and
``-V,--without-view`` can be used to tune this behavior. The default
behavior is to activate with the environment view if there is one.

The environment variables affected by the ``spack env activate``
command and the paths that are used to update them are determined by
the :ref:`prefix inspections <customize-env-modifications>` defined in
your modules configuration; the defaults are summarized in the following
table.

=================== =========
Variable            Paths
=================== =========
PATH                bin
MANPATH             man, share/man
ACLOCAL_PATH        share/aclocal
LD_LIBRARY_PATH     lib, lib64
LIBRARY_PATH        lib, lib64
CPATH               include
PKG_CONFIG_PATH     lib/pkgconfig, lib64/pkgconfig, share/pkgconfig
CMAKE_PREFIX_PATH   .
=================== =========

Each of these paths are appended to the view root, and added to the
relevant variable if the path exists. For this reason, it is not
recommended to use non-default projections with the default view of an
environment.

The ``spack env deactivate`` command will remove the default view of
the environment from the user's path.
