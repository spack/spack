Application Developer Support
===============================

Three ways to use your Spack packages.

Setting up a User Environment
--------------------------------

Show how to build a script with a bunch of ``module loads`` commands.


Filesystem Views
-------------------------------

.. Maybe this is not the right location for this documentation.

The Spack installation area allows for many package installation trees
to coexist and gives the user choices as to what versions and variants
of packages to use.  To use them, the user must rely on a way to
aggregate a subset of those packages.  The section on Environment
Modules gives one good way to do that which relies on setting various
environment variables.  An alternative way to aggregate is through
**filesystem views**.

A filesystem view is a single directory tree which is the union of the
directory hierarchies of the individual package installation trees
that have been included.  The files of the view's installed packages
are brought into the view by symbolic or hard links back to their
location in the original Spack installation area.  As the view is
formed, any clashes due to a file having the exact same path in its
package installation tree are handled in a first-come-first-served
basis and a warning is printed.  Packages and their dependencies can
be both added and removed.  During removal, empty directories will be
purged.  These operations can be limited to pertain to just the
packages listed by the user or to exclude specific dependencies and
they allow for software installed outside of Spack to coexist inside
the filesystem view tree.

By its nature, a filesystem view represents a particular choice of one
set of packages among all the versions and variants that are available
in the Spack installation area.  It is thus equivalent to the
directory hiearchy that might exist under ``/usr/local``.  While this
limits a view to including only one version/variant of any package, it
provides the benefits of having a simpler and traditional layout which
may be used without any particular knowledge that its packages were
built by Spack.

Views can be used for a variety of purposes including:

- A central installation in a traditional layout, eg ``/usr/local`` maintained over time by the sysadmin.
- A self-contained installation area which may for the basis of a top-level atomic versioning scheme, eg ``/opt/pro`` vs ``/opt/dev``.
- Providing an atomic and monolithic binary distribution, eg for delivery as a single tarball.
- Producing ephemeral testing or developing environments.

Using Filesystem Views
~~~~~~~~~~~~~~~~~~~~~~

A filesystem view is created and packages are linked in by the ``spack
view`` command's ``symlink`` and ``hardlink`` sub-commands.  The
``spack view remove`` command can be used to unlink some or all of the
filesystem view.

The following example creates a filesystem view based
on an installed ``cmake`` package and then removes from the view the
files in the ``cmake`` package while retaining its dependencies.

.. code-block:: sh


    $ spack view -v symlink myview cmake@3.5.2
    ==> Linking package: "ncurses"
    ==> Linking package: "zlib"
    ==> Linking package: "openssl"
    ==> Linking package: "cmake"

    $ ls myview/
    bin  doc  etc  include  lib  share

    $ ls myview/bin/
    captoinfo  clear  cpack     ctest    infotocap        openssl  tabs  toe   tset
    ccmake     cmake  c_rehash  infocmp  ncurses6-config  reset    tic   tput

    $ spack view -v -d false rm myview cmake@3.5.2
    ==> Removing package: "cmake"

    $ ls myview/bin/
    captoinfo  c_rehash  infotocap        openssl  tabs  toe   tset
    clear      infocmp   ncurses6-config  reset    tic   tput


Limitations of Filesystem Views
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section describes some limitations that should be considered in
using filesystems views.

Filesystem views are merely organizational.  The binary executable
programs, shared libraries and other build products found in a view
are mere links into the "real" Spack installation area.  If a view is
built with symbolic links it requires the Spack-installed package to
be kept in place.  Building a view with hardlinks removes this
requirement but any internal paths (eg, rpath or ``#!`` interpreter
specifications) will still require the Spack-installed package files
to be in place.

.. FIXME: reference the relocation work of Hegner and Gartung.

As described above, when a view is built only a single instance of a
file may exist in the unified filesystem tree.  If more than one
package provides a file at the same path (relative to its own root)
then it is the first package added to the view that "wins".  A warning
is printed and it is up to the user to determine if the conflict
matters.

It is up to the user to assure a consistent view is produced.  In
particular if the user excludes packages, limits the following of
dependencies or removes packages the view may become inconsistent.  In
particular, if two packages require the same sub-tree of dependencies,
removing one package (recursively) will remove its dependencies and
leave the other package broken.



Build System Configuration Support
----------------------------------

Imagine a developer creating a CMake-based (or Autotools) project in a local
directory, which depends on libraries A-Z.  Once Spack has installed
those dependencies, one would like to run ``cmake`` with appropriate
command line and environment so CMake can find them.  The ``spack
setup`` command does this conveniently, producing a CMake
configuration that is essentially the same as how Spack *would have*
configured the project.  This can be demonstrated with a usage
example:

.. code-block:: bash

   cd myproject
    spack setup myproject@local
    mkdir build; cd build
    ../spconfig.py ..
    make
    make install

Notes:
  * Spack must have ``myproject/package.py`` in its repository for
    this to work.
  * ``spack setup`` produces the executable script ``spconfig.py`` in
    the local directory, and also creates the module file for the
    package.  ``spconfig.py`` is normally run from the user's
    out-of-source build directory.
  * The version number given to ``spack setup`` is arbitrary, just
    like ``spack diy``.  ``myproject/package.py`` does not need to
    have any valid downloadable versions listed (typical when a
    project is new).
  * spconfig.py produces a CMake configuration that *does not* use the
    Spack wrappers.  Any resulting binaries *will not* use RPATH,
    unless the user has enabled it.  This is recommended for
    development purposes, not production.
  * ``spconfig.py`` is human readable, and can serve as a developer
    reference of what dependencies are being used.
  * ``make install`` installs the package into the Spack repository,
    where it may be used by other Spack packages.
  * CMake-generated makefiles re-run CMake in some circumstances.  Use
    of ``spconfig.py`` breaks this behavior, requiring the developer
    to manually re-run ``spconfig.py`` when a ``CMakeLists.txt`` file
    has changed.

CMakePackage
~~~~~~~~~~~~

In order ot enable ``spack setup`` functionality, the author of
``myproject/package.py`` must subclass from ``CMakePackage`` instead
of the standard ``Package`` superclass.  Because CMake is
standardized, the packager does not need to tell Spack how to run
``cmake; make; make install``.  Instead the packager only needs to
create (optional) methods ``configure_args()`` and ``configure_env()``, which
provide the arguments (as a list) and extra environment variables (as
a dict) to provide to the ``cmake`` command.  Usually, these will
translate variant flags into CMake definitions.  For example:

.. code-block:: python

    def configure_args(self):
        spec = self.spec
        return [
            '-DUSE_EVERYTRACE=%s' % ('YES' if '+everytrace' in spec else 'NO'),
            '-DBUILD_PYTHON=%s' % ('YES' if '+python' in spec else 'NO'),
            '-DBUILD_GRIDGEN=%s' % ('YES' if '+gridgen' in spec else 'NO'),
            '-DBUILD_COUPLER=%s' % ('YES' if '+coupler' in spec else 'NO'),
            '-DUSE_PISM=%s' % ('YES' if '+pism' in spec else 'NO')]

If needed, a packager may also override methods defined in
``StagedPackage`` (see below).


StagedPackage
~~~~~~~~~~~~~

``CMakePackage`` is implemented by subclassing the ``StagedPackage``
superclass, which breaks down the standard ``Package.install()``
method into several sub-stages: ``setup``, ``configure``, ``build``
and ``install``.  Details:

* Instead of implementing the standard ``install()`` method, package
  authors implement the methods for the sub-stages
  ``install_setup()``, ``install_configure()``,
  ``install_build()``, and ``install_install()``.

* The ``spack install`` command runs the sub-stages ``configure``,
  ``build`` and ``install`` in order.  (The ``setup`` stage is
  not run by default; see below).
* The ``spack setup`` command runs the sub-stages ``setup``
  and a dummy install (to create the module file).
* The sub-stage install methods take no arguments (other than
  ``self``).  The arguments ``spec`` and ``prefix`` to the standard
  ``install()`` method may be accessed via ``self.spec`` and
  ``self.prefix``.

GNU Autotools
~~~~~~~~~~~~~

The ``setup`` functionality is currently only available for
CMake-based packages.  Extending this functionality to GNU
Autotools-based packages would be easy (and should be done by a
developer who actively uses Autotools).  Packages that use
non-standard build systems can gain ``setup`` functionality by
subclassing ``StagedPackage`` directly.

