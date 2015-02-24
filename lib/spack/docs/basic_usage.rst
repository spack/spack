.. _basic-usage:

Basic usage
=====================

Spack is implemented as a single command (``spack``) with many
*subcommands*.  Only a small subset of commands is needed for typical
usage.


Listing available packages
------------------------------

The first thing you likely want to do with spack is to install some
software.  Before that, you need to know what's available.  You can
see available package names either using the :ref:`package-list`, or
using the commands below.

.. _spack-list:

``spack list``
~~~~~~~~~~~~~~~~

The ``spack list`` command prints out a list of all of the packages
Spack can install:

.. command-output:: spack list

The packages are listed by name in alphabetical order.  You can also
do wildcats searches using ``*``:

.. command-output:: spack list m*

.. command-output:: spack list *util*

.. _spack-info:

``spack info``
~~~~~~~~~~~~~~~~

To get more information on a particular package from `spack list`, use
`spack info`.  Just supply the name of a package:

.. command-output:: spack info mpich

Most of the information is self-explanatory.  *Safe versions* are
versions that Spack has a checksum for, and Spack will use the
checksum to ensure they downloaded without any errors or malicious
attacks.  :ref:`Dependencies <sec-specs>` and :ref:`virtual
dependencies <sec-virtual-dependencies>`, are described in more detail
later.

.. _spack-versions:

``spack versions``
~~~~~~~~~~~~~~~~~~~~~~~~

To see *more* available versions of a package, run ``spack versions``,
for example:

.. command-output:: spack versions libelf

There are two sections in the output.  *Safe versions* are ones that
have already been checksummed.  Spack goes a step further, though, and
also shows you what versions are available out on the web---these are
*remote versions*.  Spack gets this information by scraping it
directly from web pages.  Depending on the package, Spack may or may
not be able to find any remote versions.


Installing and uninstalling
------------------------------

Now that you know how to list available packages and versions, you're
ready to start installing things.

.. _spack-install:

``spack install``
~~~~~~~~~~~~~~~~~~~~~

``spack install`` will install any package shown by ``spack list``.
To install the latest version of a package, along with all of its
dependencies, simply give it a package name:

.. code-block:: sh

   $ spack install mpileaks

If `mpileaks` depends on other packages, Spack will install those
first.  It then fetches the tarball for ``mpileaks``, expands it,
verifies that it was downloaded without errors, builds it, and
installs it in its own directory under ``$SPACK_HOME/opt``. You'll see
a number of messages from spack, a lot of build output, and a message
that the packages is installed:

.. code-block:: sh

   $ spack install mpileaks
   ==> Installing mpileaks
   ==> mpich is already installed in /home/gamblin2/spack/opt/chaos_5_x86_64_ib/gcc@4.4.7/mpich@3.0.4.
   ==> callpath is already installed in /home/gamblin2/spack/opt/chaos_5_x86_64_ib/gcc@4.4.7/callpath@1.0.2-5dce4318.
   ==> adept-utils is already installed in /home/gamblin2/spack/opt/chaos_5_x86_64_ib/gcc@4.4.7/adept-utils@1.0-5adef8da.
   ==> Trying to fetch from https://github.com/hpc/mpileaks/releases/download/v1.0/mpileaks-1.0.tar.gz
   ######################################################################## 100.0%
   ==> Staging archive: /home/gamblin2/spack/var/spack/stage/mpileaks@1.0%gcc@4.4.7=chaos_5_x86_64_ib-59f6ad23/mpileaks-1.0.tar.gz
   ==> Created stage in /home/gamblin2/spack/var/spack/stage/mpileaks@1.0%gcc@4.4.7=chaos_5_x86_64_ib-59f6ad23.
   ==> No patches needed for mpileaks.
   ==> Building mpileaks.

   ... build output ...

   ==> Successfully installed mpileaks.
     Fetch: 2.16s.  Build: 9.82s.  Total: 11.98s.
   [+] /home/gamblin2/spack/opt/chaos_5_x86_64_ib/gcc@4.4.7/mpileaks@1.0-59f6ad23

The last line, with the ``[+]``, indicates where the package is
installed.

Building a specific version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Spack can also build *specific versions* of a package.  To do this,
just add ``@`` after the package name, followed by a version:

.. code-block:: sh

   $ spack install mpich@3.0.4

Any number of versions of the same package can be installed at once
without interfering with each other.  This is good for multi-user
sites, as installing a version that one user needs will not disrupt
existing installations for other users.

In addition to different versions, Spack can customize the compiler,
compile-time options (variants), and platform (for cross compiles) of
an installation.  Spack is unique in that it can also configure the
*dependencies* a package is built with.  For example, two
configurations of the same version of a package, one built with boost
1.39.0, and the other version built with version 1.43.0, can coexist.

This can all be done on the command line using special syntax.  Spack
calls the descriptor used to refer to a particular package
configuration a **spec**.  In the command lines above, both
``mpileaks`` and ``mpileaks@3.0.4`` are specs.  Specs are described in
detail in :ref:`sec-specs`.

.. _spack-uninstall:

``spack uninstall``
~~~~~~~~~~~~~~~~~~~~~

To uninstall a package, type ``spack uninstall <package>``.  This will
completely remove the directory in which the package was installed.

.. code-block:: sh

   spack uninstall mpich

If there are still installed packages that depend on the package to be
uninstalled, spack will refuse to uninstall it. You can override this
behavior with ``spack uninstall -f <package>``, but you risk breaking
other installed packages. In general, it is safer to remove dependent
packages *before* removing their dependencies.

A line like ``spack uninstall mpich`` may be ambiguous, if multiple
``mpich`` configurations are installed.  For example, if both
``mpich@3.0.2`` and ``mpich@3.1`` are installed, ``mpich`` could refer
to either one. Because it cannot determine which one to uninstall,
Spack will ask you to provide a version number to remove the
ambiguity.  As an example, ``spack uninstall mpich@3.1`` is
unambiguous in this scenario.


Seeing installed packages
-----------------------------------

We know that ``spack list`` shows you the names of available packages,
but how do you figure out which are installed?

.. _spack-find:

``spack find``
~~~~~~~~~~~~~~~~~~~~~~

``spack find`` shows the *specs* of installed packages.  A spec is
like a name, but it has a version, compiler, architecture, and build
options associated with it.  In spack, you can have many installations
of the same package with different specs.

Running ``spack find`` with no arguments lists installed packages:

.. code-block:: sh

   $ spack find
   ==> 74 installed packages.
   -- chaos_5_x86_64_ib / gcc@4.4.7 --------------------------------
   ImageMagick@6.8.9-10  libdwarf@20130729  py-dateutil@2.4.0
   adept-utils@1.0       libdwarf@20130729  py-ipython@2.3.1
   atk@2.14.0            libelf@0.8.12      py-matplotlib@1.4.2
   boost@1.55.0          libelf@0.8.13      py-nose@1.3.4
   bzip2@1.0.6           libffi@3.1         py-numpy@1.9.1
   cairo@1.14.0          libmng@2.0.2       py-pygments@2.0.1
   callpath@1.0.2        libpng@1.6.16      py-pyparsing@2.0.3
   cmake@3.0.2           libtiff@4.0.3      py-pyside@1.2.2
   dbus@1.8.6            libtool@2.4.2      py-pytz@2014.10
   dbus@1.9.0            libxcb@1.11        py-setuptools@11.3.1
   dyninst@8.1.2         libxml2@2.9.2      py-six@1.9.0
   fontconfig@2.11.1     libxml2@2.9.2      python@2.7.8
   freetype@2.5.3        llvm@3.0           qhull@1.0
   gdk-pixbuf@2.31.2     memaxes@0.5        qt@4.8.6
   glib@2.42.1           mesa@8.0.5         qt@5.4.0
   graphlib@2.0.0        mpich@3.0.4        readline@6.3
   gtkplus@2.24.25       mpileaks@1.0       sqlite@3.8.5
   harfbuzz@0.9.37       mrnet@4.1.0        stat@2.1.0
   hdf5@1.8.13           ncurses@5.9        tcl@8.6.3
   icu@54.1              netcdf@4.3.3       tk@src
   jpeg@9a               openssl@1.0.1h     vtk@6.1.0
   launchmon@1.0.1       pango@1.36.8       xcb-proto@1.11
   lcms@2.6              pixman@0.32.6      xz@5.2.0
   libdrm@2.4.33         py-dateutil@2.4.0  zlib@1.2.8

   -- chaos_5_x86_64_ib / gcc@4.9.2 --------------------------------
   libelf@0.8.10  mpich@3.0.4

Packages are divided into groups according to their architecture and
compiler.  Within each group, Spack tries to keep the view simple, and
only shows the version of installed packages.

In some cases, there may be different configurations of the *same*
version of a package installed.  For example, there are two
installations of of ``libdwarf@20130729`` above.  We can look at them
in more detail using ``spack find -d``, and by asking only to show
``libdwarf`` packages:

.. code-block:: sh

   $ spack find --deps libdwarf
   ==> 2 installed packages.
   -- chaos_5_x86_64_ib / gcc@4.4.7 --------------------------------
       libdwarf@20130729-d9b90962
           ^libelf@0.8.12
       libdwarf@20130729-b52fac98
           ^libelf@0.8.13

Now we see that the two instances of ``libdwarf`` depend on
*different* versions of ``libelf``: 0.8.12 and 0.8.13.  This view can
become complicated for packages with many dependencies.  If you just
want to know whether two packages' dependencies differ, you can use
``spack find -l``:

.. code-block:: sh

   $ spack find -l libdwarf
   ==> 2 installed packages.
   -- chaos_5_x86_64_ib / gcc@4.4.7 --------------------------------
   libdwarf@20130729-d9b90962  libdwarf@20130729-b52fac98

Now the ``libwarf`` installs have hashes after their names.  These are
hashes over all of the dependencies of each package.  If the hashes
are the same, then the packages have the same dependency configuration.

If you want to know the path where each package is installed, you can
use ``spack find -p``:

.. code-block:: sh

   $ spack find -p
   ==> 74 installed packages.
   -- chaos_5_x86_64_ib / gcc@4.4.7 --------------------------------
       ImageMagick@6.8.9-10  /home/gamblin2/spack/opt/chaos_5_x86_64_ib/gcc@4.4.7/ImageMagick@6.8.9-10-4df950dd
       adept-utils@1.0       /home/gamblin2/spack/opt/chaos_5_x86_64_ib/gcc@4.4.7/adept-utils@1.0-5adef8da
       atk@2.14.0            /home/gamblin2/spack/opt/chaos_5_x86_64_ib/gcc@4.4.7/atk@2.14.0-3d09ac09
       boost@1.55.0          /home/gamblin2/spack/opt/chaos_5_x86_64_ib/gcc@4.4.7/boost@1.55.0
       bzip2@1.0.6           /home/gamblin2/spack/opt/chaos_5_x86_64_ib/gcc@4.4.7/bzip2@1.0.6
       cairo@1.14.0          /home/gamblin2/spack/opt/chaos_5_x86_64_ib/gcc@4.4.7/cairo@1.14.0-fcc2ab44
       callpath@1.0.2        /home/gamblin2/spack/opt/chaos_5_x86_64_ib/gcc@4.4.7/callpath@1.0.2-5dce4318
   ...

And, finally, you can restrict your search to a particular package
by supplying its name:

.. code-block:: sh

   $ spack find -p libelf
   -- chaos_5_x86_64_ib / gcc@4.4.7 --------------------------------
       libelf@0.8.11  /home/gamblin2/spack/opt/chaos_5_x86_64_ib/gcc@4.4.7/libelf@0.8.11
       libelf@0.8.12  /home/gamblin2/spack/opt/chaos_5_x86_64_ib/gcc@4.4.7/libelf@0.8.12
       libelf@0.8.13  /home/gamblin2/spack/opt/chaos_5_x86_64_ib/gcc@4.4.7/libelf@0.8.13

``spack find`` actually does a lot more than this.  You can use
*specs* to query for specific configurations and builds of each
package. If you want to find only libelf versions greater than version
0.8.12, you could say:

.. code-block:: sh

   $ spack find libelf@0.8.12:
   -- chaos_5_x86_64_ib / gcc@4.4.7 --------------------------------
       libelf@0.8.12  libelf@0.8.13

Finding just the versions of libdwarf built with a particular version
of libelf would look like this:

.. code-block:: sh

   $ spack find -l libdwarf ^libelf@0.8.12
   ==> 1 installed packages.
   -- chaos_5_x86_64_ib / gcc@4.4.7 --------------------------------
   libdwarf@20130729-d9b90962

The full spec syntax is discussed in detail in :ref:`sec-specs`.


Compiler configuration
-----------------------------------

Spack has the ability to build packages with multiple compilers and
compiler versions. Spack searches for compilers on your machine
automatically the first time it is run. It does this by inspecting
your path.

.. _spack-compilers:

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

.. _spack-compiler-add:

``spack compiler add``
~~~~~~~~~~~~~~~~~~~~~~~

If you do not see a compiler in this list, but you want to use it with
Spack, you can simply run ``spack compiler add`` with the path to
where the compiler is installed.  For example::

    $ spack compiler add /usr/local/tools/ic-13.0.079
    ==> Added 1 new compiler to /Users/gamblin2/.spackconfig
        intel@13.0.079

Or you can run ``spack compiler add`` with no arguments to force
auto-detection.  This is useful if you do not know where compilers are
installed, but you know that new compilers have been added to your
``PATH``.  For example, using dotkit, you might do this::

    $ module load gcc-4.9.0
    $ spack compiler add
    ==> Added 1 new compiler to /Users/gamblin2/.spackconfig
        gcc@4.9.0

This loads the environment module for gcc-4.9.0 to get it into the
``PATH``, and then it adds the compiler to Spack.

.. _spack-compiler-info:

``spack compiler info``
~~~~~~~~~~~~~~~~~~~~~~~

If you want to see specifics on a particular compiler, you can run
``spack compiler info`` on it::

   $ spack compiler info intel@15
   intel@15.0.0:
           cc  = /usr/local/bin/icc-15.0.090
           cxx = /usr/local/bin/icpc-15.0.090
           f77 = /usr/local/bin/ifort-15.0.090
           fc  = /usr/local/bin/ifort-15.0.090

This shows which C, C++, and Fortran compilers were detected by Spack.
Notice also that we didn't have to be too specific about the
version. We just said ``intel@15``, and information about the only
matching Intel compiler was displayed.


Manual compiler configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If auto-detection fails, you can manually configure a compiler by
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

For compilers, like ``clang``, that do not support Fortran, put
``None`` for ``f77`` and ``fc``::

    [compiler "clang@3.3svn"]
        cc = /usr/bin/clang
        cxx = /usr/bin/clang++
        f77 = None
        fc = None

Once you save the file, the configured compilers will show up in the
list displayed by ``spack compilers``.


.. _sec-specs:

Specs & dependencies
-------------------------

We know that ``spack install``, ``spack uninstall``, and other
commands take a package name with an optional version specifier.  In
Spack, that descriptor is called a *spec*.  Spack uses specs to refer
to a particular build configuration (or configurations) of a package.
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

.. Note::

   Variants are not yet supported, but will be in the next Spack
   release (0.9), due in Q2 2015.

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

.. Note::

   Architecture specifiers are part of specs but are not yet
   functional. They will be in Spack version 1.0, due in Q3 2015.

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

.. _spack-providers:

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

Environment modules
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

     ------- /home/gamblin2/spack/share/spack/modules/chaos_5_x86_64_ib --------
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

.. _spack-module:

``spack module refresh``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Running ``spack module refresh`` will remove the
``share/spack/modules`` and ``share/spack/dotkit`` directories, then
regenerate all module and dotkit files from scratch:

.. code-block:: sh

   $ spack module refresh
   ==> Regenerating tcl module files.
   ==> Regenerating dotkit module files.


.. _extensions:

Extensions & Python support
------------------------------------

Spack's installation model assumes that each package will live in its
own install prefix.  However, certain packages are typically installed
*within* the directory hierarchy of other packages.  For example,
modules in interpreted languages like `Python
<https://www.python.org>`_ are typically installed in the
``$prefix/lib/python-2.7/site-packages`` directory.

Spack has support for this type of installation as well.  In Spack,
a package that can live inside the prefix of another package is called
an *extension*.  Suppose you have Python installed like so:

.. code-block:: sh

   $ spack find python
   ==> 1 installed packages.
   -- chaos_5_x86_64_ib / gcc@4.4.7 --------------------------------
   python@2.7.8

.. _spack-extensions:

``spack extensions``
~~~~~~~~~~~~~~~~~~~~~~~

You can find extensions for your Python installation like this:

.. code-block:: sh

   $ spack extensions python
   ==> python@2.7.8%gcc@4.4.7=chaos_5_x86_64_ib-703c7a96
   ==> 36 extensions:
   geos          py-ipython     py-pexpect    py-pyside            py-sip
   py-basemap    py-libxml2     py-pil        py-pytz              py-six
   py-biopython  py-mako        py-pmw        py-rpy2              py-sympy
   py-cython     py-matplotlib  py-pychecker  py-scientificpython  py-virtualenv
   py-dateutil   py-mpi4py      py-pygments   py-scikit-learn
   py-epydoc     py-mx          py-pylint     py-scipy
   py-gnuplot    py-nose        py-pyparsing  py-setuptools
   py-h5py       py-numpy       py-pyqt       py-shiboken

   ==> 12 installed:
   -- chaos_5_x86_64_ib / gcc@4.4.7 --------------------------------
   py-dateutil@2.4.0    py-nose@1.3.4       py-pyside@1.2.2
   py-dateutil@2.4.0    py-numpy@1.9.1      py-pytz@2014.10
   py-ipython@2.3.1     py-pygments@2.0.1   py-setuptools@11.3.1
   py-matplotlib@1.4.2  py-pyparsing@2.0.3  py-six@1.9.0

   ==> None activated.

The extensions are a subset of what's returned by ``spack list``, and
they are packages like any other.  They are installed into their own
prefixes, and you can see this with ``spack find -p``:

.. code-block:: sh

   $ spack find -p py-numpy
   ==> 1 installed packages.
   -- chaos_5_x86_64_ib / gcc@4.4.7 --------------------------------
       py-numpy@1.9.1  /g/g21/gamblin2/src/spack/opt/chaos_5_x86_64_ib/gcc@4.4.7/py-numpy@1.9.1-66733244

However, even though this package is installed, you cannot use it
directly when you run ``python``:

.. code-block:: sh

   $ spack load python
   $ python
   Python 2.7.8 (default, Feb 17 2015, 01:35:25)
   [GCC 4.4.7 20120313 (Red Hat 4.4.7-11)] on linux2
   Type "help", "copyright", "credits" or "license" for more information.
   >>> import numpy
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   ImportError: No module named numpy
   >>>

Extensions & Environment Modules
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are two ways to get ``numpy`` working in Python.  The first is
to use :ref:`shell-support`.  You can simply ``use`` or ``load`` the
module for the extension, and it will be added to the ``PYTHONPATH``
in your current shell.

For tcl modules:

.. code-block:: sh

   $ spack load python
   $ spack load py-numpy

or, for dotkit:

.. code-block:: sh

   $ spack use python
   $ spack use py-numpy

Now ``import numpy`` will succeed for as long as you keep your current
session open.


Activating Extensions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is often desirable to have certain packages *always* available as
part of a Python installation.  Spack offers a more permanent solution
for this case.  Instead of requiring users to load particular
environment modules, you can *activate* the package within the Python
installation:

.. _spack-activate:

``spack activate``
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: sh

   $ spack activate py-numpy
   ==> Activated extension py-setuptools@11.3.1%gcc@4.4.7=chaos_5_x86_64_ib-3c74eb69 for python@2.7.8%gcc@4.4.7.
   ==> Activated extension py-nose@1.3.4%gcc@4.4.7=chaos_5_x86_64_ib-5f70f816 for python@2.7.8%gcc@4.4.7.
   ==> Activated extension py-numpy@1.9.1%gcc@4.4.7=chaos_5_x86_64_ib-66733244 for python@2.7.8%gcc@4.4.7.

Several things have happened here.  The user requested that
``py-numpy`` be activated in the ``python`` installation it was built
with.  Spack knows that ``py-numpy`` depends on ``py-nose`` and
``py-setuptools``, so it activated those packages first.  Finally,
once all dependencies were activated in the ``python`` installation,
``py-numpy`` was activated as well.

If we run ``spack extensions`` again, we now see the three new
packages listed as activated:

.. code-block:: sh

   $ spack extensions python
   ==> python@2.7.8%gcc@4.4.7=chaos_5_x86_64_ib-703c7a96
   ==> 36 extensions:
   geos          py-ipython     py-pexpect    py-pyside            py-sip
   py-basemap    py-libxml2     py-pil        py-pytz              py-six
   py-biopython  py-mako        py-pmw        py-rpy2              py-sympy
   py-cython     py-matplotlib  py-pychecker  py-scientificpython  py-virtualenv
   py-dateutil   py-mpi4py      py-pygments   py-scikit-learn
   py-epydoc     py-mx          py-pylint     py-scipy
   py-gnuplot    py-nose        py-pyparsing  py-setuptools
   py-h5py       py-numpy       py-pyqt       py-shiboken

   ==> 12 installed:
   -- chaos_5_x86_64_ib / gcc@4.4.7 --------------------------------
   py-dateutil@2.4.0    py-nose@1.3.4       py-pyside@1.2.2
   py-dateutil@2.4.0    py-numpy@1.9.1      py-pytz@2014.10
   py-ipython@2.3.1     py-pygments@2.0.1   py-setuptools@11.3.1
   py-matplotlib@1.4.2  py-pyparsing@2.0.3  py-six@1.9.0

   ==> 3 currently activated:
   -- chaos_5_x86_64_ib / gcc@4.4.7 --------------------------------
   py-nose@1.3.4  py-numpy@1.9.1  py-setuptools@11.3.1


Now, when a user runs python, ``numpy`` will be available for import
*without* the user having to explicitly loaded.  ``python@2.7.8`` now
acts like a system Python installation with ``numpy`` installed inside
of it.

Spack accomplishes this by symbolically linking the *entire* prefix of
the ``py-numpy`` into the prefix of the ``python`` package.  To the
python interpreter, it looks like ``numpy`` is installed in the
``site-packages`` directory.

The only limitation of activation is that you can only have a *single*
version of an extension activated at a time.  This is because multiple
versions of the same extension would conflict if symbolically linked
into the same prefix.  Users who want a different version of a package
can still get it by using environment modules, but they will have to
explicitly load their preferred version.

``spack activate -f``
^^^^^^^^^^^^^^^^^^^^^^^^^
If, for some reason, you want to activate a package *without* its
dependencies, you can use ``spack activate -f``:

.. code-block:: sh

   $ spack activate -f py-numpy
   ==> Activated extension py-numpy@1.9.1%gcc@4.4.7=chaos_5_x86_64_ib-66733244 for python@2.7.8%gcc@4.4.7.

.. _spack-deactivate:

``spack deactivate``
^^^^^^^^^^^^^^^^^^^^^^^^^

We've seen how activating an extension can be used to set up a default
version of a Python module.  Obviously, you may want to change that at
some point.  ``spack deactivate`` is the command for this.  There are
several variants:

  * ``spack deactivate <extension>`` will deactivate a single
    extension.  If another activated extension depends on this one,
    Spack will warn you and exit with an error.
  * ``spack deactivate -f <extension>`` deactivates an extension
    regardless of packages that depend on it.
  * ``spack deactivate -a <extension>`` deactivates an extension and
    all of its dependencies.  Use ``-f`` to disregard dependents.
  * ``spack deactivate -a <extendee>`` deactivates *all* activated
    extensions of a package.  For example, to deactivate *all* python
    extensions, use::

       spack deactivate -a python


Getting Help
-----------------------

.. _spack-help:

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
