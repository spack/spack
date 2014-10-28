.. _basic-usage:

Basic usage
=====================

Spack is implemented as a single command (``spack``) with many
*subcommands*, much like ``git``, ``svn``, ``yum``, or ``apt-get``.
Only a small subset of commands are needed for typical usage.

This section covers a small set of subcommands that should cover most
general use cases for Spack.


Listing available packages
------------------------------

The first thing you will likely want to do with spack is find out what
software is available to install.  There are a few relevant commands.

``spack list``
~~~~~~~~~~~~~~~~

The ``spack list`` command prints out a list of all of the packages
Spack can install:

.. command-output:: spack list

The packages are listed by name in alphabetical order.  You can also
do wildcard searches using ``*``:

.. command-output:: spack list m*

.. command-output:: spack list *util*


``spack info``
~~~~~~~~~~~~~~~~

To get information on a particular package from the full list, run
``spack info <package name>``.  For example, for ``mpich`` the output
looks like this:

.. command-output:: spack info mpich

This includes basic information about the package: where to download
it, its dependencies, virtual packages it provides (e.g. an MPI
implementation will provide the MPI interface), and a text
description, if one is available.  :ref:`Dependencies
<sec-specs>` and :ref:`virtual dependencies
<sec-virtual-dependencies>` are described in more detail later.

``spack versions``
~~~~~~~~~~~~~~~~~~~~~~~~

To see available versions of a package, run ``spack versions``, for
example:

.. command-output:: spack versions libelf

Since it has to manage many different software packages, Spack doesn't
place many restrictions on what a package version has to look like.
Packages like ``mpich`` use traditional version numbers like
``3.0.4``. Other packages, like ``libdwarf`` use date-stamp versions
like ``20130729``.  Versions can contain numbers, letters, dashes,
underscores, and periods.

Compiler Configuration
-----------------------------------

Spack has the ability to build packages with multiple compilers and
compiler versions. Spack searches for compilers on your machine
automatically the first time it is run. It does this by inspecting
your path.

``spack compilers``
~~~~~~~~~~~~~~~~~~~~~~~

You can see which compilers spack has found by running ``spack
compilers`` or ``spack compiler list``::

    $ spack compilers
    ==> Available compilers
    -- gcc ---------------------------------------------------------
        gcc@4.9.0  gcc@4.8.0  gcc@4.7.0  gcc@4.6.2  gcc@4.4.7
        gcc@4.8.2  gcc@4.7.1  gcc@4.6.3  gcc@4.6.1  gcc@4.1.2
    -- intel -------------------------------------------------------
        intel@15.0.0  intel@14.0.0  intel@13.0.0  intel@12.1.0  intel@10.0
        intel@14.0.3  intel@13.1.1  intel@12.1.5  intel@12.0.4  intel@9.1
        intel@14.0.2  intel@13.1.0  intel@12.1.3  intel@11.1
        intel@14.0.1  intel@13.0.1  intel@12.1.2  intel@10.1
    -- clang -------------------------------------------------------
        clang@3.4  clang@3.3  clang@3.2  clang@3.1
    -- pgi ---------------------------------------------------------
        pgi@14.3-0   pgi@13.2-0  pgi@12.1-0   pgi@10.9-0  pgi@8.0-1
        pgi@13.10-0  pgi@13.1-1  pgi@11.10-0  pgi@10.2-0  pgi@7.1-3
        pgi@13.6-0   pgi@12.8-0  pgi@11.1-0   pgi@9.0-4   pgi@7.0-6

Any of these compilers can be used to build Spack packages.  More on
how this is done is in :ref:`sec-specs`.

``spack compiler add``
~~~~~~~~~~~~~~~~~~~~~~~

If you do not see a compiler in this list, but you want to use it with
Spack, you can simply run ``spack compiler add`` with the path to
where the compiler is installed.  For example::

    $ spack compiler add /usr/local/tools/ic-13.0.079
    ==> Added 1 new compiler to /Users/gamblin2/.spackconfig
        intel@13.0.079

Or you can run ``spack compiler add`` with no arguments to force
autodetection.  This is useful if you do not know where compilers
live, but new compilers have been added to your ``PATH``.  For
example, using dotkit, you might do this::

    $ use gcc-4.9.0
    $ spack compiler add
    ==> Added 1 new compiler to /Users/gamblin2/.spackconfig
        gcc@4.9.0


``spack compiler info``
~~~~~~~~~~~~~~~~~~~~~~~

If you want to see specifics on a particular compiler, you can run
``spack compiler info`` on it::

    $ spack compiler info intel@12.1.3
    intel@12.1.3:
    cc  = /usr/local/bin/icc-12.1.293
    cxx = /usr/local/bin/icpc-12.1.293
    f77 = /usr/local/bin/ifort-12.1.293
    fc = /usr/local/bin/ifort-12.1.293

This shows which C, C++, and Fortran compilers were detected by Spack.


Manual configuration
~~~~~~~~~~~~~~~~~~~~~~~

If autodetection fails, you can manually conigure a compiler by
editing your ``~/.spackconfig`` file.  You can do this by running
``spack config edit``, which will open the file in your ``$EDITOR``.

Each compiler configuration in the file looks like this::

    ...
    [compiler "intel@15.0.0"]
        cc = /usr/local/bin/icc-15.0.024-beta
        cxx = /usr/local/bin/icpc-15.0.024-beta
        f77 = /usr/local/bin/ifort-15.0.024-beta
        fc = /usr/local/bin/ifort-15.0.024-beta
    ...

For compilers, like ``clang``, that do not support Fortran, you can simply
put ``None`` for ``f77`` and ``fc``::

    [compiler "clang@3.3svn"]
        cc = /usr/bin/clang
        cxx = /usr/bin/clang++
        f77 = None
        fc = None

Once you save the file, the configured compilers will show up in the
list displayed when you run ``spack compilers``.


Seeing installed packages -----------------------------------

``spack find``
~~~~~~~~~~~~~~~~~~~~~~

The second thing you're likely to want to do with Spack, and the first
thing users of your system will likely want to do, is to find what
software is already installed and ready to use.  You can do that with
``spack find``.

Running ``spack find`` with no arguments will list all the installed
packages:

.. code-block:: sh

   $ spack find
   == chaos_5_x86_64_ib ===========================================
   -- gcc@4.4.7 ---------------------------------------------------
       libdwarf@20130207-d9b909
       libdwarf@20130729-d9b909
       libdwarf@20130729-b52fac
       libelf@0.8.11
       libelf@0.8.12
       libelf@0.8.13

Packages are grouped by architecture, then by the compiler used to
build them, and then by their versions and options.  If a package has
dependencies, there will also be a hash at the end of the name
indicating the dependency configuration.  Packages with the same hash
have the same dependency configuration.  If you want ALL information
about dependencies, as well, then you can supply ``-l`` or ``--long``:

.. code-block:: sh

   $ spack find -l
   == chaos_5_x86_64_ib ===========================================
   -- gcc@4.4.7 ---------------------------------------------------
       libdwarf@20130207
           ^libelf@0.8.12
       libdwarf@20130729
           ^libelf@0.8.12
       libdwarf@20130729
           ^libelf@0.8.13
       libelf@0.8.11
       libelf@0.8.12
       libelf@0.8.13

Now you can see which versions of ``libelf`` each version of
``libdwarf`` was built with.

If you want to know the path where each of these packages is
installed, do ``spack find -p`` or ``--path``:

.. code-block:: sh

   $ spack find -p
   == chaos_5_x86_64_ib ===========================================
   -- gcc@4.4.7 ---------------------------------------------------
       libdwarf@20130207-d9b909  /g/g21/gamblin2/src/spack/opt/chaos_5_x86_64_ib/gcc@4.4.7/libdwarf@20130207-d9b909
       libdwarf@20130729-d9b909  /g/g21/gamblin2/src/spack/opt/chaos_5_x86_64_ib/gcc@4.4.7/libdwarf@20130729-d9b909
       libdwarf@20130729-b52fac  /g/g21/gamblin2/src/spack/opt/chaos_5_x86_64_ib/gcc@4.4.7/libdwarf@20130729-b52fac
       libelf@0.8.11             /g/g21/gamblin2/src/spack/opt/chaos_5_x86_64_ib/gcc@4.4.7/libelf@0.8.11
       libelf@0.8.12             /g/g21/gamblin2/src/spack/opt/chaos_5_x86_64_ib/gcc@4.4.7/libelf@0.8.12
       libelf@0.8.13             /g/g21/gamblin2/src/spack/opt/chaos_5_x86_64_ib/gcc@4.4.7/libelf@0.8.13


And, finally, you can restrict your search to a particular package
by supplying its name:

.. code-block:: sh

   $ spack find -p libelf
   == chaos_5_x86_64_ib ===========================================
   -- gcc@4.4.7 ---------------------------------------------------
       libelf@0.8.11  /g/g21/gamblin2/src/spack/opt/chaos_5_x86_64_ib/gcc@4.4.7/libelf@0.8.11
       libelf@0.8.12  /g/g21/gamblin2/src/spack/opt/chaos_5_x86_64_ib/gcc@4.4.7/libelf@0.8.12
       libelf@0.8.13  /g/g21/gamblin2/src/spack/opt/chaos_5_x86_64_ib/gcc@4.4.7/libelf@0.8.13


``spack find`` actually does a lot more than this.  You can use
*specs* to query for specific configurations and builds of each
package.  The full spec syntax is discussed in detail in
:ref:`sec-specs`.



Installing and uninstalling
------------------------------

``spack install``
~~~~~~~~~~~~~~~~~~~~~

``spack install`` will install any package that appears in the output
of ``spack list``.  To install the latest version of a pacakge and all
of its dependencies, simply run ``spack install <package>``:

.. code-block:: sh

   spack install mpileaks

Spack will fetch the tarball for ``mpileaks``, expand it, verify that
it was downloaded without errors, build it, and install it in its own
directory under ``$SPACK_HOME/opt``.  If the requested package depends
on other packages in order to build, Spack fetches them as well, and
installs them before it installs the requested package. Like the main
package, each dependency is also installed in its own directory.

Spack can also build *specific* configurations of a package.  For
example, to install something with a specific version, add ``@`` after
the package name, followed by a version string:

.. code-block:: sh

   spack install mpich@3.0.4

Any number of configurations of the same package can be installed at
once without interfering with each other.  This is good for multi-user
sites, as installing a version that one user needs will not disrupt
existing installations for other users.

In addition to version configuraitons, Spack can customize the
compiler, compile-time options (variants), and platform (for cross
compiles) of an installation.  Spack is unique in that it can also
configure the *dependencies* a package is built with.  For example,
two configurations of the same version of a package, one built with
boost 1.39.0, and the other version built with version 1.43.0, can
coexist.

This can all be done on the command line using special syntax.  Spack
calls the descriptor used to refer to a particular package
configuration a **spec**.  In the command lines above, both
``mpileaks`` and ``mpileaks@3.0.4`` are specs.  To customize
additional properties, simply add more attributes to the spec.  Specs
and their syntax are covered in more detail in :ref:`sec-specs`.


``spack uninstall``
~~~~~~~~~~~~~~~~~~~~~

To uninstall a package, type ``spack uninstall <package>``.  This will
completely remove the directory in which the package was installed.

.. code-block:: sh

   spack uninstall mpich

If there are still installed packages that depend on the package to be
uninstalled, spack will refuse to uninstall.  If you know what you're
doing, you can override this with ``spack uninstall -f <package>``.
However, running this risks breaking other installed packages. In
general, it is safer to remove dependent packages *before* removing
their dependencies.

A line like ``spack uninstall mpich`` may be ambiguous, if multiple
``mpich`` configurations are installed.  For example, if both
``mpich@3.0.2`` and ``mpich@3.1`` are installed, it could refer to
either one, and Spack cannot determine which one to uninstall.  Spack
will ask you to provide a version number to remove the ambiguity.  For
example, ``spack uninstall mpich@3.1`` is unambiguous in the above
scenario.


.. _sec-specs:

Specs & Dependencies
-------------------------

We now know that ``spack install`` and ``spack uninstall`` both take a
package name with an optional version specifier.  In Spack, that
descriptor is called a *spec*.  Spack uses specs to refer to a
particular build configuration (or configurations) of a package.
Specs are more than a package name and a version; you can use them to
specify the compiler, compiler version, architecture, compile options,
and dependency options for a build.  In this section, we'll go over
the full syntax of specs.

Here is an example of a much longer spec than we've seen thus far::

   mpileaks @1.2:1.4 %gcc@4.7.5 +debug -qt =bgqos_0 ^callpath @1.1 %gcc@4.7.2

If provided to ``spack install``, this will install the ``mpileaks``
library at some version between ``1.2`` and ``1.4`` (inclusive),
built using ``gcc`` at version 4.7.5 for the Blue Gene/Q architecture,
with debug options enabled, and without Qt support.  Additionally, it
says to link it with the ``callpath`` library (which it depends on),
and to build callpath with ``gcc`` 4.7.2.  Most specs will not be as
complicated as this one, but this is a good example of what is
possible with specs.

More formally, a spec consists of the following pieces:

* Package name identifier (``mpileaks`` above)
* ``@`` Optional version specifier (``@1.2:1.4``)
* ``%`` Optional compiler specifier, with an optional compiler version
  (``gcc`` or ``gcc@4.7.3``)
* ``+`` or ``-`` or ``~`` Optional variant specifiers (``+debug``,
  ``-qt``, or ``~qt``)
* ``=`` Optional architecture specifier (``bgqos_0``)
* ``^`` Dependency specs (``^callpath@1.1``)

There are two things to notice here.  The first is that specs are
recursively defined.  That is, each dependency after ``^`` is a spec
itself.  The second is that everything is optional *except* for the
initial package name identifier.  Users can be as vague or as specific
as they want about the details of building packages, and this makes
spack good for beginners and experts alike.

To really understand what's going on above, we need to think about how
software is structured.  An executable or a library (these are
generally the artifacts produced by building software) depends on
other libraries in order to run.  We can represent the relationship
between a package and its dependencies as a graph.  Here is the full
dependency graph for ``mpileaks``:

.. graphviz::

   digraph {
       mpileaks -> mpich
       mpileaks -> callpath -> mpich
       callpath -> dyninst
       dyninst  -> libdwarf -> libelf
       dyninst  -> libelf
   }

Each box above is a package and each arrow represents a dependency on
some other package.  For example, we say that the package ``mpileaks``
*depends on* ``callpath`` and ``mpich``.  ``mpileaks`` also depends
*indirectly* on ``dyninst``, ``libdwarf``, and ``libelf``, in that
these libraries are dependencies of ``callpath``.  To install
``mpileaks``, Spack has to build all of these packages.  Dependency
graphs in Spack have to be acyclic, and the *depends on* relationship
is directional, so this is a *directed, acyclic graph* or *DAG*.

The package name identifier in the spec is the root of some dependency
DAG, and the DAG itself is implicit.  Spack knows the precise
dependencies among packages, but users do not need to know the full
DAG structure. Each ``^`` in the full spec refers to some dependency
of the root package. Spack will raise an error if you supply a name
after ``^`` that the root does not actually depend on (e.g. ``mpileaks
^emacs@23.3``).

Spack further simplifies things by only allowing one configuration of
each package within any single build.  Above, both ``mpileaks`` and
``callpath`` depend on ``mpich``, but ``mpich`` appears only once in
the DAG.  You cannot build an ``mpileaks`` version that depends on one
version of ``mpich`` *and* on a ``callpath`` version that depends on
some *other* version of ``mpich``.  In general, such a configuration
would likely behave unexpectedly at runtime, and Spack enforces this
to ensure a consistent runtime environment.


The point of specs is to abstract this full DAG from Spack users.  If
a user does not care about the DAG at all, she can refer to mpileaks
by simply writing ``mpileaks``.  If she knows that ``mpileaks``
indirectly uses ``dyninst`` and she wants a particular version of
``dyninst``, then she can refer to ``mpileaks ^dyninst@8.1``.  Spack
will fill in the rest when it parses the spec; the user only needs to
know package names and minimal details about their relationship.

When spack prints out specs, it sorts package names alphabetically to
normalize the way they are displayed, but users do not need to worry
about this when they write specs.  The only restriction on the order
of dependencies within a spec is that they appear *after* the root
package.  For example, these two specs represent exactly the same
configuration:

.. code-block:: sh

   mpileaks ^callpath@1.0 ^libelf@0.8.3
   mpileaks ^libelf@0.8.3 ^callpath@1.0

You can put all the same modifiers on dependency specs that you would
put on the root spec.  That is, you can specify their versions,
compilers, variants, and architectures just like any other spec.
Specifiers are associated with the nearest package name to their left.
For example, above, ``@1.1`` and ``%gcc@4.7.2`` associates with the
``callpath`` package, while ``@1.2:1.4``, ``%gcc@4.7.5``, ``+debug``,
``-qt``, and ``=bgqos_0`` all associate with the ``mpileaks`` package.

In the diagram above, ``mpileaks`` depends on ``mpich`` with an
unspecified version, but packages can depend on other packages with
*constraints* by adding more specifiers.  For example, ``mpileaks``
could depend on ``mpich@1.2:`` if it can only build with version
``1.2`` or higher of ``mpich``.

Below are more details about the specifiers that you can add to specs.

Version specifier
~~~~~~~~~~~~~~~~~~~~~~~

A version specifier comes somewhere after a package name and starts
with ``@``.  It can be a single version, e.g. ``@1.0``, ``@3``, or
``@1.2a7``.  Or, it can be a range of versions, such as ``@1.0:1.5``
(all versions between ``1.0`` and ``1.5``, inclusive).  Version ranges
can be open, e.g. ``:3`` means any version up to and including ``3``.
This would include ``3.4`` and ``3.4.2``.  ``4.2:`` means any version
above and including ``4.2``.  Finally, a version specifier can be a
set of arbitrary versions, such as ``@1.0,1.5,1.7`` (``1.0``, ``1.5``,
or ``1.7``).  When you supply such a specifier to ``spack install``,
it constrains the set of versions that Spack will install.

If the version spec is not provided, then Spack will choose one
according to policies set for the particular spack installation.  If
the spec is ambiguous, i.e. it could match multiple versions, Spack
will choose a version within the spec's constraints according to
policies set for the particular Spack installation.

Details about how versions are compared and how Spack determines if
one version is less than another are discussed in the developer guide.


Compiler specifier
~~~~~~~~~~~~~~~~~~~~~~~

A compiler specifier comes somewhere after a package name and starts
with ``%``.  It tells Spack what compiler(s) a particular package
should be built with.  After the ``%`` should come the name of some
registered Spack compiler.  This might include ``gcc``, or ``intel``,
but the specific compilers available depend on the site.  You can run
``spack compilers`` to get a list; more on this below.

The compiler spec can be followed by an optional *compiler version*.
A compiler version specifier looks exactly like a package version
specifier.  Version specifiers will associate with the nearest package
name or compiler specifier to their left in the spec.

If the compiler spec is omitted, Spack will choose a default compiler
based on site policies.


Variants
~~~~~~~~~~~~~~~~~~~~~~~

Variants are named options associated with a particular package, and
they can be turned on or off.  For example, above, supplying
``+debug`` causes ``mpileaks`` to be built with debug flags.  The
names of particular variants available for a package depend on what
was provided by the package author.  ``spack info <package>`` will
provide information on what build variants are available.

Depending on the package a variant may be on or off by default.  For
``mpileaks`` here, ``debug`` is off by default, and we turned it on
with ``+debug``.  If a package is on by default you can turn it off by
either adding ``-name`` or ``~name`` to the spec.

There are two syntaxes here because, depending on context, ``~`` and
``-`` may mean different things.  In most shells, the following will
result in the shell performing home directory substitution:

.. code-block:: sh

   mpileaks ~debug   # shell may try to substitute this!
   mpileaks~debug    # use this instead

If there is a user called ``debug``, the ``~`` will be incorrectly
expanded.  In this situation, you would want to write ``mpileaks
-debug``.  However, ``-`` can be ambiguous when included after a
package name without spaces:

.. code-block:: sh

   mpileaks-debug     # wrong!
   mpileaks -debug    # right

Spack allows the ``-`` character to be part of package names, so the
above will be interpreted as a request for the ``mpileaks-debug``
package, not a request for ``mpileaks`` built without ``debug``
options.  In this scenario, you should write ``mpileaks~debug`` to
avoid ambiguity.

When spack normalizes specs, it prints them out with no spaces and
uses only ``~`` for disabled variants.  We allow ``-`` and spaces on
the command line is provided for convenience and legibility.


Architecture specifier
~~~~~~~~~~~~~~~~~~~~~~~

The architecture specifier starts with a ``=`` and also comes after
some package name within a spec.  It allows a user to specify a
particular architecture for the package to be built.  This is mostly
used for architectures that need cross-compilation, and in most cases,
users will not need to specify the architecture when they install a
package.


.. _sec-virtual-dependencies:

Virtual dependencies
-------------------------

The dependence graph for ``mpileaks`` we saw above wasn't *quite*
accurate.  ``mpileaks`` uses MPI, which is an interface that has many
different implementations.  Above, we showed ``mpileaks`` and
``callpath`` depending on ``mpich``, which is one *particular*
implementation of MPI.  However, we could build either with another
implementation, such as ``openmpi`` or ``mvapich``.

Spack represents interfaces like this using *virtual dependencies*.
The real dependency DAG for ``mpileaks`` looks like this:

.. graphviz::

   digraph {
       mpi [color=red]
       mpileaks -> mpi
       mpileaks -> callpath -> mpi
       callpath -> dyninst
       dyninst  -> libdwarf -> libelf
       dyninst  -> libelf
   }

Notice that ``mpich`` has now been replaced with ``mpi``. There is no
*real* MPI package, but some packages *provide* the MPI interface, and
these packages can be substituted in for ``mpi`` when ``mpileaks`` is
built.

You can see what virtual packages a particular package provides by
getting info on it:

.. command-output:: spack info mpich

Spack is unique in that its virtual packages can be versioned, just
like regular packages.  A particular version of a package may provide
a particular version of a virtual package, and we can see above that
``mpich`` versions ``1`` and above provide all ``mpi`` interface
versions up to ``1``, and ``mpich`` versions ``3`` and above provide
``mpi`` versions up to ``3``.  A package can *depend on* a particular
version of a virtual package, e.g. if an application needs MPI-2
functions, it can depend on ``mpi@2:`` to indicate that it needs some
implementation that provides MPI-2 functions.


Constraining virtual packages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When installing a package that depends on a virtual package, you can
opt to specify the particular provider you want to use, or you can let
Spack pick.  For example, if you just type this::

   spack install mpileaks

Then spack will pick a provider for you according to site policies.
If you really want a particular version, say mpich, then you could
run this instead::

   spack install mpileaks ^mpich

This forces spack to use some version of ``mpich`` for its
implementation.  As always, you can be even more specific and require
a particular ``mpich`` version::

   spack install mpileaks ^mpich@3

The ``mpileaks`` package in particular only needs MPI-1 commands, so
any MPI implementation will do.  If another package depends on
``mpi@2`` and you try to give it an insufficient MPI implementation
(e.g., one that provides only ``mpi@:1``), then Spack will raise an
error.  Likewise, if you try to plug in some package that doesn't
provide MPI, Spack will raise an error.

``spack providers``
~~~~~~~~~~~~~~~~~~~~~~~~~~

You can see what packages provide a particular virtual package using
``spack providers``.  If you wanted to see what packages provide
``mpi``, you would just run:

.. command-output:: spack providers mpi

And if you *only* wanted to see packages that provide MPI-2, you would
add a version specifier to the spec:

.. command-output:: spack providers mpi@2

Notice that the package versions that provide insufficient MPI
versions are now filtered out.

.. _shell-support:

Environment Modules
-------------------------------

.. note::

   Environment module support is currently experimental and should not
   be considered a stable feature of Spack.  In particular, the
   interface and/or generated module names may change in future
   versions.

Spack provides some limited integration with environment module
systems to make it easier to use the packages it provides.

You can enable shell support by sourcing some files in the
``/share/spack`` directory.

For ``bash`` or ``ksh``, run:

.. code-block:: sh

   . $SPACK_ROOT/share/spack/setup-env.sh

For ``csh`` and ``tcsh`` run:

.. code-block:: csh

   setenv SPACK_ROOT /path/to/spack
   source $SPACK_ROOT/share/spack/setup-env.csh

You can put the above code in your ``.bashrc`` or ``.cshrc``, and
Spack's shell support will be available on the command line.


-------------------------------


When you install a package with Spack, it automatically generates an
environment module that lets you add the package to your environment.

Currently, Spack supports the generation of `TCL Modules
<http://wiki.tcl.tk/12999>`_ and `Dotkit
<https://computing.llnl.gov/?set=jobs&page=dotkit>`_.  Generated
module files for each of these systems can be found in these
directories:

  * ``$SPACK_ROOT/share/spack/modules``
  * ``$SPACK_ROOT/share/spack/dotkit``

The directories are automatically added to your ``MODULEPATH`` and
``DK_NODE`` environment variables when you enable Spack's `shell
support <shell-support_>`_.

Using Modules & Dotkits
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have shell support enabled you should be able to run either
``module avail`` or ``use -l spack`` to see what modules/dotkits have
been installed.  Here is sample output of those programs, showing lots
of installed packages.

  .. code-block:: sh

     $ module avail

     ------- /g/g21/gamblin2/src/spack/share/spack/modules/chaos_5_x86_64_ib --------
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

  .. code-block:: sh

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
you could type either of these commands to load the callpath module
(assuming dotkit and modules are installed):

.. code-block:: sh

   use callpath@1.0.1%gcc@4.4.7-5dce4318

.. code-block:: sh

   module load callpath@1.0.1%gcc@4.4.7-5dce4318

Neither of these is particularly pretty, easy to remember, or
easy to type.  Luckily, Spack has its own interface for using modules
and dotkits.  You can use the same spec syntax you're used to:

  =========================  ==========================
  Modules                    Dotkit
  =========================  ==========================
  ``spack load <spec>``      ``spack use <spec>``
  ``spack unload <spec>``    ``spack unuse <spec>``
  =========================  ==========================

And you can use the same shortened names you use everywhere else in
Spack.  For example, this will add the ``mpich`` package built with
``gcc`` to your path:

.. code-block:: sh

   $ spack install mpich %gcc@4.4.7

   # ... wait for install ...

   $ spack use mpich %gcc@4.4.7
   Prepending: mpich@3.0.4%gcc@4.4.7 (ok)
   $ which mpicc
   ~/src/spack/opt/chaos_5_x86_64_ib/gcc@4.4.7/mpich@3.0.4/bin/mpicc

Or, similarly with modules, you could type:

.. code-block:: sh

   $ spack load mpich %gcc@4.4.7

These commands will add appropriate directories to your ``PATH``,
``MANPATH``, and ``LD_LIBRARY_PATH``.  When you no longer want to use
a package, you can type unload or unuse similarly:

.. code-block:: sh

   $ spack unload mpich %gcc@4.4.7    # modules
   $ spack unuse mpich %gcc@4.4.7     # dotkit

.. note::

   These ``use``, ``unuse``, ``load``, and ``unload`` subcommands are
   only available if you have enabled Spack's shell support *and* you
   have dotkit or modules installed on your machine.

Ambiguous module names
~~~~~~~~~~~~~~~~~~~~~~~~

If a spec used with load/unload or use/unuse is ambiguous (i.e. more
than one installed package matches it), then Spack will warn you:

.. code-block:: sh

   $ spack load libelf
   ==> Error: Multiple matches for spec libelf.  Choose one:
   libelf@0.8.13%gcc@4.4.7=chaos_5_x86_64_ib
   libelf@0.8.13%intel@15.0.0=chaos_5_x86_64_ib

You can either type the ``spack load`` command again with a fully
qualified argument, or you can add just enough extra constraints to
identify one package.  For example, above, the key differentiator is
that one ``libelf`` is built with the Intel compiler, while the other
used ``gcc``.  You could therefore just type:

.. code-block:: sh

   $ spack load libelf %intel

To identify just the one built with the Intel compiler.


Regenerating Module files
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Module and dotkit files are generated when packages are installed, and
are placed in the following directories under the Spack root:

  * ``$SPACK_ROOT/share/spack/modules``
  * ``$SPACK_ROOT/share/spack/dotkit``

Sometimes you may need to regenerate the modules files.  For example,
if newer, fancier module support is added to Spack at some later date,
you may want to regenerate all the modules to take advantage of these
new features.

``spack module refresh``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Running ``spack module refresh`` will remove the
``share/spack/modules`` and ``share/spack/dotkit`` directories, then
regenerate all module and dotkit files from scratch:

.. code-block:: sh

   $ spack module refresh
   ==> Regenerating tcl module files.
   ==> Regenerating dotkit module files.

Getting Help
-----------------------

``spack help``
~~~~~~~~~~~~~~~~~~~~~~

If you don't find what you need here, the ``help`` subcommand will
print out out a list of *all* of ``spack``'s options and subcommands:

.. command-output:: spack help

Adding an argument, e.g. ``spack help <subcommand>``, will print out
usage information for a particular subcommand:

.. command-output:: spack help install

Alternately, you can use ``spack -h`` in place of ``spack help``, or
``spack <subcommand> -h`` to get help on a particular subcommand.
