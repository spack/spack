.. _advanced-packaging-tutorial:

============================
Advanced Topics in Packaging
============================

While you can quickly accomplish most common tasks with what
was covered in :ref:`packaging-tutorial`, there are times when such
knowledge won't suffice. Usually this happens for libraries that provide
more than one API and need to let dependents decide which one to use
or for packages that provide tools that are invoked at build-time,
or in other similar situations.

In the following we'll dig into some of the details of package
implementation that help us deal with these rare, but important,
occurrences. You can rest assured that in every case Spack remains faithful to
its philosophy: keep simple things simple, but be flexible enough when
complex requests arise!

----------------------
Setup for the tutorial
----------------------

The simplest way to follow along with this tutorial is to use our Docker image,
which comes with Spack and various packages pre-installed:

.. code-block:: console

  $ docker pull alalazo/spack:advanced_packaging_tutorial
  $ docker run --rm -h advanced-packaging-tutorial -it alalazo/spack:advanced_packaging_tutorial
  root@advanced-packaging-tutorial:/#
  root@advanced-packaging-tutorial:/# spack find
  ==> 20 installed packages.
  -- linux-ubuntu16.04-x86_64 / gcc@5.4.0 -------------------------
  arpack-ng@3.5.0  hdf5@1.10.1   libpciaccess@0.13.5  libtool@2.4.6  m4@1.4.18  ncurses@6.0          openblas@0.2.20  openssl@1.0.2k     superlu@5.2.1       xz@5.2.3
  cmake@3.9.4      hwloc@1.11.8  libsigsegv@2.11      libxml2@2.9.4  mpich@3.2  netlib-lapack@3.6.1  openmpi@3.0.0    pkg-config@0.29.2  util-macros@1.19.1  zlib@1.2.11

If you already started the image, you can set the ``EDITOR`` environment
variable to your preferred editor (``vi``, ``emacs``, and ``nano`` are included in the image)
and move directly to :ref:`specs_build_interface_tutorial`.

If you choose not to use the Docker image, you can clone the Spack repository
and build the necessary bits yourself:

.. code-block:: console

  $ git clone https://github.com/spack/spack.git
  Cloning into 'spack'...
  remote: Counting objects: 92731, done.
  remote: Compressing objects: 100% (1108/1108), done.
  remote: Total 92731 (delta 1964), reused 4186 (delta 1637), pack-reused 87932
  Receiving objects: 100% (92731/92731), 33.31 MiB | 64.00 KiB/s, done.
  Resolving deltas: 100% (43557/43557), done.
  Checking connectivity... done.

  $ cd spack
  $ git checkout tutorials/advanced_packaging
  Branch tutorials/advanced_packaging set up to track remote branch tutorials/advanced_packaging from origin.
  Switched to a new branch 'tutorials/advanced_packaging'

At this point you can install the software that will be used
during the rest of the tutorial (the output of the commands is omitted
for the sake of brevity):

.. code-block:: console

  $ spack install openblas
  $ spack install netlib-lapack
  $ spack install mpich
  $ spack install openmpi
  $ spack install --only=dependencies armadillo ^openblas
  $ spack install --only=dependencies netcdf
  $ spack install --only=dependencies elpa

Now, you are ready to set your preferred ``EDITOR`` and continue with
the rest of the tutorial.


.. _specs_build_interface_tutorial:

----------------------
Spec's build interface
----------------------

Spack is designed with an emphasis on assigning responsibilities
to the appropriate entities, as this results in a clearer and more intuitive interface
for the users.
When it comes to packaging, one of the most fundamental guideline that
emerged from this tenet is that:

  *It is a package's responsibility to know
  every software it directly depends on and to expose to others how to
  use the services it provides*.

Spec's build interface is a protocol-like implementation of this guideline
that allows packages to easily query their dependencies,
and prescribes how they should expose their own build information.

^^^^^^^^^^^^^^^^^^^^
A motivating example
^^^^^^^^^^^^^^^^^^^^

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
as a LAPACK provider:

.. code-block:: console

  root@advanced-packaging-tutorial:/# spack install armadillo ^openblas
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

If we try to build another version tied to ``netlib-lapack`` we'll
notice that this time the installation won't complete:

.. code-block:: console

  root@advanced-packaging-tutorial:/# spack install  armadillo ^netlib-lapack
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
    /usr/local/var/spack/stage/arpack-ng-3.5.0-bloz7cqirpdxj33pg7uj32zs5likz2un/arpack-ng-3.5.0/spack-build.out

This is because ``netlib-lapack`` requires extra work, compared to ``openblas``,
to expose its build information to other packages. Let's edit it:

.. code-block:: console

  root@advanced-packaging-tutorial:/# spack edit netlib-lapack

and follow the instructions in the ``# TUTORIAL:`` comment as before.
What we need to implement is:

.. code-block:: python

  @property
  def lapack_libs(self):
      shared = True if '+shared' in self.spec else False
      return find_libraries(
          'liblapack', root=self.prefix, shared=shared, recurse=True
      )

i.e. a property that returns the correct list of libraries for the LAPACK interface.
Now we can finally install ``armadillo ^netlib-lapack``:

.. code-block:: console

  root@advanced-packaging-tutorial:/# spack install  armadillo ^netlib-lapack
  ...

  ==> Building armadillo [CMakePackage]
  ==> Executing phase: 'cmake'
  ==> Executing phase: 'build'
  ==> Executing phase: 'install'
  ==> Successfully installed armadillo
    Fetch: 0.01s.  Build: 3.75s.  Total: 3.76s.
  [+] /usr/local/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/armadillo-8.100.1-sxmpu5an4dshnhickh6ykchyfda7jpyn

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
What happens at subscript time?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The example above leaves us with a few questions. How could it be that the
attribute:

.. code-block:: python

  spec['lapack'].libs

stems from a property of the ``netlib-lapack`` package that has a different name?
How is it even computed for ``openblas``, given that in its package there's no code
that deals with finding libraries?
The answer is that ``libs`` is one of the few properties of specs that follow the
*build-interface protocol*. The others are currently ``command`` and ``headers``.
These properties exist only on concrete specs that have been retrieved via the
subscript notation.

What happens is that, whenever you retrieve a spec using subscripts:

.. code-block:: python

  lapack = spec['lapack']

the key that appears in the query (in this case ``'lapack'``) is attached to the
returned item. When, later on, you access any of the build-interface attributes, this
key is used to compute the result according to the following algorithm:

.. code-block:: none

  Given any pair of <query-key> and <build-attribute>:

    1. If <query-key> is the name of a virtual spec and the package
       providing it has an attribute named '<query-key>_<build-attribute>'
       return it

    2. Otherwise if the package has an attribute named '<build-attribute>'
       return that

    3. Otherwise use the default handler for <build-attribute>

Going back to our concrete case this means that, if the spec providing LAPACK
is ``netlib-lapack``, we are returning the value computed in the ``lapack_libs``
property. If it is ``openblas``, we are instead resorting to the default handler
for ``libs`` (which searches for the presence of ``libopenblas`` in the
installation prefix).

.. note::

  Types commonly returned by build-interface attributes
    Even though there's no enforcement on it, the type of the objects returned most often when
    asking for the ``libs`` attributes is :py:class:`LibraryList <llnl.util.filesystem.LibraryList>`.
    Similarly the usual type returned for ``headers`` is :py:class:`HeaderList <llnl.util.filesystem.HeaderList>`,
    while for ``command`` is :py:class:`Executable <spack.util.executable.Executable>`. You can refer to
    these objects' API documentation to discover more about them.

^^^^^^^^^^^^^^^^^^^^^^^
Extra query parameters
^^^^^^^^^^^^^^^^^^^^^^^

An advanced feature of the Spec's build-interface protocol is the support
for extra parameters after the subscript key. In fact, any of the keys used in the query
can be followed by a comma separated list of extra parameters which can be
inspected by the package receiving the request to fine-tune a response.

Let's look at an example and try to install ``netcdf``:

.. code-block:: console

  root@advanced-packaging-tutorial:/# spack install netcdf
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
    /usr/local/var/spack/stage/netcdf-4.4.1.1-gk2xxhbqijnrdwicawawcll4t3c7dvoj/netcdf-4.4.1.1/spack-build.out

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

where we highlighted the line retrieving  the extra parameters. Now we can successfully
complete the installation of ``netcdf``:

.. code-block:: console

  root@advanced-packaging-tutorial:/# spack install netcdf
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


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Single package providing multiple virtual specs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

At the close of this tutorial's subsection, it may be useful to see where the
build-interface protocol shines the most i.e. when it comes to manage packages
that provide more than one virtual spec. An example of a package of this kind is
``intel-parallel-studio``, and due to its complexity we'll limit our discussion
here to just a few considerations (without any hands-on). You can open
the related ``package.py`` in the usual way:

.. code-block:: console

  root@advanced-packaging-tutorial:/# spack edit intel-parallel-studio

As you can see this package provides a lot of virtual specs, and thus it has
more than one function that enters into the build-interface protocol. These
functions will be invoked for *exactly the same spec* according to the key used
by its dependents in the subscript query.

So, for instance, the ``blas_libs`` property will be returned when
``intel-parallel-studio`` is the BLAS provider in the current DAG and
is retrieved by a dependent with:

.. code-block:: python

  blas = self.spec['blas']
  blas_libs = blas.libs

Within the property we inspect various aspects of the current spec:

.. code-block:: python

  @property
  def blas_libs(self):
     spec = self.spec
     prefix = self.prefix
     shared = '+shared' in spec

     if '+ilp64' in spec:
         mkl_integer = ['libmkl_intel_ilp64']
     else:
         mkl_integer = ['libmkl_intel_lp64']
     ...

and construct the list of library we need to return accordingly.

What we achieved is that the complexity of dealing with ``intel-parallel-studio``
is now gathered in the package itself, instead of being spread
all over its possible dependents.
Thus, a package that uses MPI or LAPACK doesn't care which implementation it uses,
as each virtual dependency has
*a uniform interface* to ask for libraries or headers and manipulate them.
The packages that provide this virtual spec, on the other hand, have a clear
way to differentiate their answer to the query [#uniforminterface]_.

.. [#uniforminterface] Before this interface was added, each package that
   depended on MPI or LAPACK had dozens of lines of code copied from other
   packages telling it where to find the libraries and what they are called.
   With the addition of this interface, the virtual dependency itself tells
   other packages that depend on it where it can find its libraries.

---------------------------
Package's build environment
---------------------------

Besides Spec's build interface, Spack provides means to set environment
variables, either for yourself or for your dependent packages, and to
attach attributes to your dependents. We'll see them next with the help
of a few real use cases.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Set variables at build-time for yourself
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Spack provides a way to manipulate a package's build time and
run time environments using the
:py:func:`setup_environment <spack.package.PackageBase.setup_environment>` function.
Let's try to see how it works by completing the ``elpa`` package:

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

The two arguments, ``spack_env`` and ``run_env``, are both instances of
:py:class:`EnvironmentModifications <spack.environment.EnvironmentModifications>` and
permit you to register modifications to either the build-time or the run-time
environment of the package, respectively.
At this point it's possible to proceed with the installation of ``elpa``:

.. code-block:: console

  root@advanced-packaging-tutorial:/# spack install elpa
  ==> pkg-config is already installed in /usr/local/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/pkg-config-0.29.2-ae2hwm7q57byfbxtymts55xppqwk7ecj
  ==> ncurses is already installed in /usr/local/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/ncurses-6.0-ukq4tccptm2rxd56d2bumqthnpcjzlez
  ...
  ==> Executing phase: 'build'
  ==> Executing phase: 'install'
  ==> Successfully installed elpa
    Fetch: 3.94s.  Build: 41.93s.  Total: 45.87s.
  [+] /usr/local/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/elpa-2016.05.004-sdbfhwcexg7s2zqf52vssb762ocvklbu

If you had modifications to ``run_env``, those would have appeared e.g. in the module files
generated for the package.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Set variables in dependencies at build-time
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Another common occurrence, particularly for packages like ``r`` and ``python``
that support extensions and for packages that provide build tools,
is to require *their dependents* to have some environment variables set.

The mechanism is similar to what we just saw, except that we override the
:py:func:`setup_dependent_environment <spack.package.PackageBase.setup_dependent_environment>`
function, which takes one additional argument, i.e. the dependent spec that needs the modified
environment. Let's practice completing the ``mpich`` package:

.. code-block:: console

  root@advanced-packaging-tutorial:/# spack edit mpich

Once you're finished the method should look like this:

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

At this point we can, for instance, install ``netlib-scalapack``:

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
set to the correct value. More complicated examples of the use of this function
may be found in the ``r`` and ``python`` package.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Attach attributes to other packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Build tools usually also provide a set of executables that can be used
when another package is being installed. Spack gives the opportunity
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