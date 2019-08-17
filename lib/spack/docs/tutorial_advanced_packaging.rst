.. Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _advanced-packaging-tutorial:

============================
Advanced Topics in Packaging
============================

Spack tries to automatically configure packages with information from
dependencies such that all you need to do is to list the dependencies
(i.e., with the ``depends_on`` directive) and the build system (for example
by deriving from :code:`CmakePackage`).

However, there are many special cases. Often you need to retrieve details
about dependencies to set package-specific configuration options, or to
define package-specific environment variables used by the package's build
system. This tutorial covers how to retrieve build information from
dependencies, and how you can automatically provide important information to
dependents in your package.

----------------------
Setup for the tutorial
----------------------

.. note::

  We do not recommend doing this section of the tutorial in a
  production Spack instance.

The tutorial uses custom package definitions with missing sections that
will be filled in during the tutorial. These package definitions are stored
in a separate package repository, which can be enabled with:

.. code-block:: console

  $ spack repo add --scope=site var/spack/repos/tutorial

This section of the tutorial may also require a newer version of
gcc. If you have not already installed gcc@7.2.0 and added it to your
configuration, you can do so with:

.. code-block:: console

  $ spack install gcc@7.2.0 %gcc@5.4.0
  $ spack compiler add --scope=site `spack location -i gcc@7.2.0 %gcc@5.4.0`

If you are using the tutorial docker image, all dependency packages
will have been installed. Otherwise, to install these packages you can use
the following commands:

.. code-block:: console

  $ spack install openblas
  $ spack install netlib-lapack
  $ spack install mpich

Now, you are ready to set your preferred ``EDITOR`` and continue with
the rest of the tutorial.

.. note::

  Several of these packages depend on an MPI implementation. You can use
  OpenMPI if you install it from scratch, but this is slow (>10 min.).
  A binary cache of MPICH may be provided, in which case you can force
  the package to use it and install quickly. All tutorial examples with
  packages that depend on MPICH include the spec syntax for building with it

.. _adv_pkg_tutorial_start:

---------------------------------------
Modifying a package's build environment
---------------------------------------

Spack sets up several environment variables like ``PATH`` by default to aid in
building a package, but many packages make use of environment variables which
convey specific information about their dependencies (e.g., ``MPICC``).
This section covers how to update your Spack packages so that package-specific
environment variables are defined at build-time.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Set environment variables in dependent packages at build-time
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies can set environment variables that are required when their
dependents build. For example, when a package depends on a python extension
like py-numpy, Spack's ``python`` package will add it to ``PYTHONPATH``
so it is available at build time; this is required because the default setup
that spack does is not sufficient for python to import modules.

To provide environment setup for a dependent, a package can implement the
:py:func:`setup_dependent_environment <spack.package.PackageBase.setup_dependent_environment>`
function. This function takes as a parameter a :py:class:`EnvironmentModifications <spack.util.environment.EnvironmentModifications>`
object which includes convenience methods to update the environment. For
example, an MPI implementation can set ``MPICC`` for packages that depend on it:

.. code-block:: python

  def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
      spack_env.set('MPICC', join_path(self.prefix.bin, 'mpicc'))

In this case packages that depend on ``mpi`` will have ``MPICC`` defined in
their environment when they build. This section is focused on modifying the
build-time environment represented by ``spack_env``, but it's worth noting that
modifications to ``run_env`` are included in Spack's automatically-generated
module files.

We can practice by editing the ``mpich`` package to set the ``MPICC``
environment variable in the build-time environment of dependent packages.

.. code-block:: console

  root@advanced-packaging-tutorial:/# spack edit mpich

Once you're finished, the method should look like this:

.. code-block:: python

  def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
      spack_env.set('MPICC',  join_path(self.prefix.bin, 'mpicc'))
      spack_env.set('MPICXX', join_path(self.prefix.bin, 'mpic++'))
      spack_env.set('MPIF77', join_path(self.prefix.bin, 'mpif77'))
      spack_env.set('MPIF90', join_path(self.prefix.bin, 'mpif90'))

      spack_env.set('MPICH_CC', spack_cc)
      spack_env.set('MPICH_CXX', spack_cxx)
      spack_env.set('MPICH_F77', spack_f77)
      spack_env.set('MPICH_F90', spack_fc)
      spack_env.set('MPICH_FC', spack_fc)

At this point we can, for instance, install ``netlib-scalapack`` with
``mpich``:

.. code-block:: console

  root@advanced-packaging-tutorial:/# spack install netlib-scalapack ^mpich
  ...
  ==> Created stage in /usr/local/var/spack/stage/netlib-scalapack-2.0.2-km7tsbgoyyywonyejkjoojskhc5knz3z
  ==> No patches needed for netlib-scalapack
  ==> Building netlib-scalapack [CMakePackage]
  ==> Executing phase: 'cmake'
  ==> Executing phase: 'build'
  ==> Executing phase: 'install'
  ==> Successfully installed netlib-scalapack
    Fetch: 0.01s.  Build: 3m 59.86s.  Total: 3m 59.87s.
  [+] /usr/local/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/netlib-scalapack-2.0.2-km7tsbgoyyywonyejkjoojskhc5knz3z


and double check the environment logs to verify that every variable was
set to the correct value.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Set environment variables in your own package
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Packages can modify their own build-time environment by implementing the
:py:func:`setup_environment <spack.package.PackageBase.setup_environment>` function.
For ``qt`` this looks like:

.. code-block:: python

    def setup_environment(self, spack_env, run_env):
        spack_env.set('MAKEFLAGS', '-j{0}'.format(make_jobs))
        run_env.set('QTDIR', self.prefix)

When ``qt`` builds, ``MAKEFLAGS`` will be defined in the environment.

To contrast with ``qt``'s :py:func:`setup_dependent_environment <spack.package.PackageBase.setup_dependent_environment>`
function:

.. code-block:: python

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.set('QTDIR', self.prefix)

Let's see how it works by completing the ``elpa`` package:

.. code-block:: console

  root@advanced-packaging-tutorial:/# spack edit elpa

In the end your method should look like:

.. code-block:: python

  def setup_environment(self, spack_env, run_env):
      spec = self.spec

      spack_env.set('CC', spec['mpi'].mpicc)
      spack_env.set('FC', spec['mpi'].mpifc)
      spack_env.set('CXX', spec['mpi'].mpicxx)
      spack_env.set('SCALAPACK_LDFLAGS', spec['scalapack'].libs.joined())

      spack_env.append_flags('LDFLAGS', spec['lapack'].libs.search_flags)
      spack_env.append_flags('LIBS', spec['lapack'].libs.link_flags)

At this point it's possible to proceed with the installation of ``elpa ^mpich``

------------------------------
Retrieving library information
------------------------------

Although Spack attempts to help packages locate their dependency libraries
automatically (e.g. by setting ``PKG_CONFIG_PATH`` and ``CMAKE_PREFIX_PATH``),
a package may have unique configuration options that are required to locate
libraries. When a package needs information about dependency libraries, the
general approach in Spack is to query the dependencies for the locations of
their libraries and set configuration options accordingly. By default most
Spack packages know how to automatically locate their libraries. This section
covers how to retrieve library information from dependencies and how to locate
libraries when the default logic doesn't work.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Accessing dependency libraries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you need to access the libraries of a dependency, you can do so
via the ``libs`` property of the spec, for example in the ``arpack-ng``
package:

.. code-block:: python

    def install(self, spec, prefix):
        lapack_libs = spec['lapack'].libs.joined(';')
        blas_libs = spec['blas'].libs.joined(';')

        cmake(*[
            '-DLAPACK_LIBRARIES={0}'.format(lapack_libs),
            '-DBLAS_LIBRARIES={0}'.format(blas_libs)
        ], '.')

Note that ``arpack-ng`` is querying virtual dependencies, which Spack
automatically resolves to the installed implementation (e.g. ``openblas``
for ``blas``).

We've started work on a package for ``armadillo``. You should open it,
read through the comment that starts with ``# TUTORIAL:`` and complete
the ``cmake_args`` section:

.. code-block:: console

  root@advanced-packaging-tutorial:/# spack edit armadillo

If you followed the instructions in the package, when you are finished your
``cmake_args`` method should look like:

.. code-block:: python

  def cmake_args(self):
        spec = self.spec

        return [
            # ARPACK support
            '-DARPACK_LIBRARY={0}'.format(spec['arpack-ng'].libs.joined(";")),
            # BLAS support
            '-DBLAS_LIBRARY={0}'.format(spec['blas'].libs.joined(";")),
            # LAPACK support
            '-DLAPACK_LIBRARY={0}'.format(spec['lapack'].libs.joined(";")),
            # SuperLU support
            '-DSuperLU_INCLUDE_DIR={0}'.format(spec['superlu'].prefix.include),
            '-DSuperLU_LIBRARY={0}'.format(spec['superlu'].libs.joined(";")),
            # HDF5 support
            '-DDETECT_HDF5={0}'.format('ON' if '+hdf5' in spec else 'OFF')
        ]

As you can see, getting the list of libraries that your dependencies provide
is as easy as accessing the their ``libs`` attribute. Furthermore, the interface
remains the same whether you are querying regular or virtual dependencies.

At this point you can complete the installation of ``armadillo`` using ``openblas``
as a LAPACK provider (``armadillo ^openblas ^mpich``):

.. code-block:: console

  root@advanced-packaging-tutorial:/# spack install armadillo ^openblas ^mpich
  ==> pkg-config is already installed in /usr/local/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/pkg-config-0.29.2-ae2hwm7q57byfbxtymts55xppqwk7ecj
  ...
  ==> superlu is already installed in /usr/local/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/superlu-5.2.1-q2mbtw2wo4kpzis2e2n227ip2fquxrno
  ==> Installing armadillo
  ==> Using cached archive: /usr/local/var/spack/cache/armadillo/armadillo-8.100.1.tar.xz
  ==> Staging archive: /usr/local/var/spack/stage/armadillo-8.100.1-n2eojtazxbku6g4l5izucwwgnpwz77r4/armadillo-8.100.1.tar.xz
  ==> Created stage in /usr/local/var/spack/stage/armadillo-8.100.1-n2eojtazxbku6g4l5izucwwgnpwz77r4
  ==> Applied patch undef_linux.patch
  ==> Building armadillo [CMakePackage]
  ==> Executing phase: 'cmake'
  ==> Executing phase: 'build'
  ==> Executing phase: 'install'
  ==> Successfully installed armadillo
    Fetch: 0.01s.  Build: 3.96s.  Total: 3.98s.
  [+] /usr/local/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/armadillo-8.100.1-n2eojtazxbku6g4l5izucwwgnpwz77r4

Hopefully the installation went fine and the code we added expanded to the right list
of semicolon separated libraries (you are encouraged to open ``armadillo``'s
build logs to double check).

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Providing libraries to dependents
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Spack provides a default implementation for ``libs`` which often works
out of the box. A user can write a package definition without having to
implement a ``libs`` property and dependents can retrieve its libraries
as shown in the above section. However, the default implementation assumes that
libraries follow the naming scheme ``lib<package name>.so`` (or e.g.
``lib<package name>.a`` for static libraries). Packages which don't
follow this naming scheme must implement this function themselves, e.g.
``opencv``:

.. code-block:: python

    @property
    def libs(self):
        shared = "+shared" in self.spec
        return find_libraries(
            "libopencv_*", root=self.prefix, shared=shared, recurse=True
        )

This issue is common for packages which implement an interface (i.e.
virtual package providers in Spack). If we try to build another version of
``armadillo`` tied to ``netlib-lapack`` (``armadillo ^netlib-lapack ^mpich``)
we'll notice that this time the installation won't complete:

.. code-block:: console

  root@advanced-packaging-tutorial:/# spack install  armadillo ^netlib-lapack ^mpich
  ==> pkg-config is already installed in /usr/local/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/pkg-config-0.29.2-ae2hwm7q57byfbxtymts55xppqwk7ecj
  ...
  ==> openmpi is already installed in /usr/local/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/openmpi-3.0.0-yo5qkfvumpmgmvlbalqcadu46j5bd52f
  ==> Installing arpack-ng
  ==> Using cached archive: /usr/local/var/spack/cache/arpack-ng/arpack-ng-3.5.0.tar.gz
  ==> Already staged arpack-ng-3.5.0-bloz7cqirpdxj33pg7uj32zs5likz2un in /usr/local/var/spack/stage/arpack-ng-3.5.0-bloz7cqirpdxj33pg7uj32zs5likz2un
  ==> No patches needed for arpack-ng
  ==> Building arpack-ng [Package]
  ==> Executing phase: 'install'
  ==> Error: RuntimeError: Unable to recursively locate netlib-lapack libraries in /usr/local/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/netlib-lapack-3.6.1-jjfe23wgt7nkjnp2adeklhseg3ftpx6z
  RuntimeError: RuntimeError: Unable to recursively locate netlib-lapack libraries in /usr/local/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/netlib-lapack-3.6.1-jjfe23wgt7nkjnp2adeklhseg3ftpx6z

  /usr/local/var/spack/repos/builtin/packages/arpack-ng/package.py:105, in install:
       5             options.append('-DCMAKE_INSTALL_NAME_DIR:PATH=%s/lib' % prefix)
       6
       7             # Make sure we use Spack's blas/lapack:
    >> 8             lapack_libs = spec['lapack'].libs.joined(';')
       9             blas_libs = spec['blas'].libs.joined(';')
       10
       11            options.extend([

  See build log for details:
    /usr/local/var/spack/stage/arpack-ng-3.5.0-bloz7cqirpdxj33pg7uj32zs5likz2un/arpack-ng-3.5.0/spack-build-out.txt

Unlike ``openblas`` which provides a library named ``libopenblas.so``,
``netlib-lapack`` provides ``liblapack.so``, so it needs to implement
customized library search logic. Let's edit it:

.. code-block:: console

  root@advanced-packaging-tutorial:/# spack edit netlib-lapack

and follow the instructions in the ``# TUTORIAL:`` comment as before.
What we need to implement is:

.. code-block:: python

  @property
  def lapack_libs(self):
      shared = True if '+shared' in self.spec else False
      return find_libraries(
          'liblapack', root=self.prefix, shared=shared, recursive=True
      )

i.e., a property that returns the correct list of libraries for the LAPACK interface.

We use the name ``lapack_libs`` rather than ``libs`` because
``netlib-lapack`` can also provide ``blas``, and when it does it is provided
as a separate library file. Using this name ensures that when
dependents ask for ``lapack`` libraries, ``netlib-lapack`` will retrieve only
the libraries associated with the ``lapack`` interface. Now we can finally
install ``armadillo ^netlib-lapack ^mpich``:

.. code-block:: console

  root@advanced-packaging-tutorial:/# spack install  armadillo ^netlib-lapack ^mpich
  ...

  ==> Building armadillo [CMakePackage]
  ==> Executing phase: 'cmake'
  ==> Executing phase: 'build'
  ==> Executing phase: 'install'
  ==> Successfully installed armadillo
    Fetch: 0.01s.  Build: 3.75s.  Total: 3.76s.
  [+] /usr/local/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/armadillo-8.100.1-sxmpu5an4dshnhickh6ykchyfda7jpyn

Since each implementation of a virtual package is responsible for locating the
libraries associated with the interfaces it provides, dependents do not need
to include special-case logic for different implementations and for example
need only ask for :code:`spec['blas'].libs`.

----------------------
Other Packaging Topics
----------------------

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Attach attributes to other packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Build tools usually also provide a set of executables that can be used
when another package is being installed. Spack gives you the opportunity
to monkey-patch dependent modules and attach attributes to them. This
helps make the packager experience as similar as possible to what would
have been the manual installation of the same package.

An example here is the ``automake`` package, which overrides
:py:func:`setup_dependent_package <spack.package.PackageBase.setup_dependent_package>`:

.. code-block:: python

  def setup_dependent_package(self, module, dependent_spec):
      # Automake is very likely to be a build dependency,
      # so we add the tools it provides to the dependent module
      executables = ['aclocal', 'automake']
      for name in executables:
          setattr(module, name, self._make_executable(name))

so that every other package that depends on it can use directly ``aclocal``
and ``automake`` with the usual function call syntax of :py:class:`Executable <spack.util.executable.Executable>`:

.. code-block:: python

  aclocal('--force')

^^^^^^^^^^^^^^^^^^^^^^^
Extra query parameters
^^^^^^^^^^^^^^^^^^^^^^^

An advanced feature of the Spec's build-interface protocol is the support
for extra parameters after the subscript key. In fact, any of the keys used in the query
can be followed by a comma-separated list of extra parameters which can be
inspected by the package receiving the request to fine-tune a response.

Let's look at an example and try to install ``netcdf ^mpich``:

.. code-block:: console

  root@advanced-packaging-tutorial:/# spack install netcdf ^mpich
  ==> libsigsegv is already installed in /usr/local/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/libsigsegv-2.11-fypapcprssrj3nstp6njprskeyynsgaz
  ==> m4 is already installed in /usr/local/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/m4-1.4.18-r5envx3kqctwwflhd4qax4ahqtt6x43a
  ...
  ==> Error: AttributeError: 'list' object has no attribute 'search_flags'
  AttributeError: AttributeError: 'list' object has no attribute 'search_flags'

  /usr/local/var/spack/repos/builtin/packages/netcdf/package.py:207, in configure_args:
       50            # used instead.
       51            hdf5_hl = self.spec['hdf5:hl']
       52            CPPFLAGS.append(hdf5_hl.headers.cpp_flags)
    >> 53            LDFLAGS.append(hdf5_hl.libs.search_flags)
       54
       55            if '+parallel-netcdf' in self.spec:
       56                config_args.append('--enable-pnetcdf')

  See build log for details:
    /usr/local/var/spack/stage/netcdf-4.4.1.1-gk2xxhbqijnrdwicawawcll4t3c7dvoj/netcdf-4.4.1.1/spack-build-out.txt

We can see from the error that ``netcdf`` needs to know how to link the *high-level interface*
of ``hdf5``, and thus passes the extra parameter ``hl`` after the request to retrieve it.
Clearly the implementation in the ``hdf5`` package is not complete, and we need to fix it:

.. code-block:: console

  root@advanced-packaging-tutorial:/# spack edit hdf5

If you followed the instructions correctly, the code added to the
``lib`` property should be similar to:

.. code-block:: python
  :emphasize-lines: 1

  query_parameters = self.spec.last_query.extra_parameters
  key = tuple(sorted(query_parameters))
  libraries = query2libraries[key]
  shared = '+shared' in self.spec
  return find_libraries(
      libraries, root=self.prefix, shared=shared, recurse=True
  )

where we highlighted the line retrieving the extra parameters. Now we can successfully
complete the installation of ``netcdf ^mpich``:

.. code-block:: console

  root@advanced-packaging-tutorial:/# spack install netcdf ^mpich
  ==> libsigsegv is already installed in /usr/local/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/libsigsegv-2.11-fypapcprssrj3nstp6njprskeyynsgaz
  ==> m4 is already installed in /usr/local/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/m4-1.4.18-r5envx3kqctwwflhd4qax4ahqtt6x43a
  ...
  ==> Installing netcdf
  ==> Using cached archive: /usr/local/var/spack/cache/netcdf/netcdf-4.4.1.1.tar.gz
  ==> Already staged netcdf-4.4.1.1-gk2xxhbqijnrdwicawawcll4t3c7dvoj in /usr/local/var/spack/stage/netcdf-4.4.1.1-gk2xxhbqijnrdwicawawcll4t3c7dvoj
  ==> Already patched netcdf
  ==> Building netcdf [AutotoolsPackage]
  ==> Executing phase: 'autoreconf'
  ==> Executing phase: 'configure'
  ==> Executing phase: 'build'
  ==> Executing phase: 'install'
  ==> Successfully installed netcdf
    Fetch: 0.01s.  Build: 24.61s.  Total: 24.62s.
  [+] /usr/local/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/netcdf-4.4.1.1-gk2xxhbqijnrdwicawawcll4t3c7dvoj
