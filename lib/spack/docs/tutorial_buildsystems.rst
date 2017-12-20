.. _build-systems-tutorial:

==============================
Spack Package Build Systems
==============================

You may begin to notice after writing a couple of package template files a
pattern emerge for some packages. For example, you may find yourself writing
an :code:`install()` method that invokes: :code:`configure`, :code:`cmake`,
:code:`make`, :code:`make install`. You may also find yourself writing
:code:`"prefix=" + prefix` as an argument to :code:`configure` or :code:`cmake`.
Rather than having you repeat these lines for all packages, Spack has
classes that can take care of these patterns. In addition,
these package files allow for finer grained control of these build systems.
In this section, we will describe each build system and give examples on
how these can be manipulated to install a package.

-----------------------
Package Class Hierarchy
-----------------------

.. graphviz::

    digraph G {

        node [
            shape = "record"
        ]
        edge [
            arrowhead = "empty"
        ]

        PackageBase -> Package [dir=back]
        PackageBase -> MakefilePackage [dir=back]
        PackageBase -> AutotoolsPackage [dir=back]
        PackageBase -> CMakePackage [dir=back]
        PackageBase -> PythonPackage [dir=back]
    }

The above diagram gives a high level view of the class hierarchy and how each
package relates. Each subclass inherits from the :code:`PackageBaseClass`
super class. The bulk of the work is done in this super class which includes
fetching, extracting to a staging directory and installing. Each subclass
then adds additional build-system-specific functionality. In the following
sections, we will go over examples of how to utilize each subclass and to see
how powerful these abstractions are when packaging.

-----------------
Package
-----------------

We've already seen examples of a :code:`Package` class in our walkthrough for writing
package files, so we won't be spending much time with them here. Briefly,
the Package class allows for abitrary control over the build process, whereas
subclasses rely on certain patterns (e.g. :code:`configure` :code:`make`
:code:`make install`) to be useful. :code:`Package` classes are particularly useful
for packages that have a non-conventional way of being built since the packager
can utilize some of Spack's helper functions to customize the building and
installing of a package.

-------------------
Autotools
-------------------

As we have seen earlier, packages using :code:`Autotools` use :code:`configure`,
:code:`make` and :code:`make install` commands to execute the build and
install process. In our :code:`Package` class, your typical build incantation will
consist of the following:

.. code-block:: python

    def install(self, spec, prefix):
        configure("--prefix=" + prefix)
        make()
        make("install")

You'll see that this looks similar to what we wrote in our packaging tutorial.

The :code:`Autotools` subclass aims to simplify writing package files and provides
convenience methods to manipulate each of the different phases for a :code:`Autotools`
build system.

:code:`Autotools` packages consist of four phases:

1. :code:`autoreconf()`
2. :code:`configure()`
3. :code:`build()`
4. :code:`install()`


Each of these phases have sensible defaults. Let's take a quick look at some
the internals of the :code:`Autotools` class:

.. code-block:: console

    $ spack edit --build-system autotools


This will open the :code:`AutotoolsPackage` file in your text editor.

.. note::
    The examples showing code for these classes is abridged to avoid having
    long examples. We only show what is relevant to the packager.


.. literalinclude:: ../../../lib/spack/spack/build_systems/autotools.py
    :language: python
    :emphasize-lines: 42,45,62
    :lines: 40-95,259-267
    :linenos:


Important to note are the highlighted lines. These properties allow the
packager to set what build targets and install targets they want for their
package. If, for example, we wanted to add as our build target :code:`foo`
then we can append to our :code:`build_targets` property:

.. code-block:: python

    build_targets = ["foo"]

Which is similiar to invoking make in our Package

.. code-block:: python

     make("foo")

This is useful if we have packages that ignore environment variables and need
a command-line argument.

Another thing to take note of is in the :code:`configure()` method.
Here we see that the :code:`prefix` argument is already included since it is a
common pattern amongst packages using :code:`Autotools`. We then only have to
override :code:`configure_args()`, which will then return it's output to
to :code:`configure()`. Then, :code:`configure()` will append the common
arguments

Packagers also have the option to run :code:`autoreconf` in case a package
needs to update the build system and generate a new :code:`configure`. Though,
for the most part this will be unnecessary.

Let's look at the :code:`mpileaks` package.py file that we worked on earlier:

.. code-block:: console

    $ spack edit mpileaks

Notice that mpileaks is a :code:`Package` class but uses the :code:`Autotools`
build system. Although this package is acceptable let's make this into an
:code:`AutotoolsPackage` class and simplify it further.

.. literalinclude:: tutorial/examples/Autotools/0.package.py
   :language: python
   :emphasize-lines: 28
   :linenos:

We first inherit from the :code:`AutotoolsPackage` class.


Although we could keep the :code:`install()` method, most of it can be handled
by the :code:`AutotoolsPackage` base class. In fact, the only thing that needs
to be overridden is :code:`configure_args()`.

.. literalinclude:: tutorial/examples/Autotools/1.package.py
   :language: python
   :emphasize-lines: 42,43
   :linenos:

Since Spack takes care of setting the prefix for us we can exclude that as
an argument to :code:`configure`. Our packages look simpler, and the packager
does not need to worry about whether they have properly included :code:`configure`
and :code:`make`.

This version of the :code:`mpileaks` package installs the same as the previous,
but the :code:`AutotoolsPackage` class lets us do it with a cleaner looking
package file.

-----------------
Makefile
-----------------

Packages that utilize :code:`Make` or a :code:`Makefile` usually require you
to edit a :code:`Makefile` to set up platform and compiler specific variables.
These packages are handled by the :code:`Makefile` subclass which provides
convenience methods to help write these types of packages.

A :code:`MakefilePackage` class has three phases that can be overridden. These include:

    1. :code:`edit()`
    2. :code:`build()`
    3. :code:`install()`

Packagers then have the ability to control how a :code:`Makefile` is edited, and
what targets to include for the build phase or install phase.

Let's also take a look inside the :code:`MakefilePackage` class:

.. code-block:: console

    $ spack edit --build-system makefile

Take note of the following:


.. literalinclude:: ../../../lib/spack/spack/build_systems/makefile.py
   :language: python
   :lines: 33-79,89-107
   :emphasize-lines: 48,54,61
   :linenos:

Similar to :code:`Autotools`, :code:`MakefilePackage` class has properties
that can be set by the packager. We can also override the different
methods highlighted.


Let's try to recreate the Bowtie_ package:

.. _Bowtie: http://bowtie-bio.sourceforge.net/index.shtml


.. code-block:: console

    $ spack create -f https://downloads.sourceforge.net/project/bowtie-bio/bowtie/1.2.1.1/bowtie-1.2.1.1-src.zip
    ==> This looks like a URL for bowtie
    ==> Found 1 version of bowtie:

    1.2.1.1  https://downloads.sourceforge.net/project/bowtie-bio/bowtie/1.2.1.1/bowtie-1.2.1.1-src.zip

    ==> How many would you like to checksum? (default is 1, q to abort) 1
    ==> Downloading...
    ==> Fetching https://downloads.sourceforge.net/project/bowtie-bio/bowtie/1.2.1.1/bowtie-1.2.1.1-src.zip
    ######################################################################## 100.0%
    ==> Checksummed 1 version of bowtie
    ==> This package looks like it uses the makefile build system
    ==> Created template for bowtie package
    ==> Created package file: /Users/mamelara/spack/var/spack/repos/builtin/packages/bowtie/package.py

Once the fetching is completed, Spack will open up your text editor in the
usual fashion and create a template of a :code:`MakefilePackage` package.py.

.. literalinclude:: tutorial/examples/Makefile/0.package.py
   :language: python
   :linenos:

Spack was successfully able to detect that :code:`Bowtie` uses :code:`Make`.
Let's add in the rest of our details for our package:

.. literalinclude:: tutorial/examples/Makefile/1.package.py
   :language: python
   :emphasize-lines: 29,30,32,33,37,39
   :linenos:

As we mentioned earlier, most packages using a :code:`Makefile` have hard-coded
variables that must be edited. These variables are fine if you happen to not
care about setup or types of compilers used but Spack is designed to work with
any compiler. The :code:`MakefilePackage` subclass makes it easy to edit
these :code:`Makefiles` by having an :code:`edit()` method that
can be overridden.

Let's take a look at the default :code:`Makefile` that :code:`Bowtie` provides.
If we look inside, we see that :code:`CC` and :code:`CXX` point to our GNU
compiler:

.. code-block:: console

    $ spack stage bowtie

.. note::
    As usual make sure you have shell support activated with spack:
        :code:`source /path/to/spack_root/spack/share/spack/setup-env.sh`

.. code-block:: console

    $ spack cd -s bowtie
    $ cd bowtie-1.2
    $ vim Makefile


.. code-block:: make

    CPP = g++ -w
    CXX = $(CPP)
    CC = gcc
    LIBS = $(LDFLAGS) -lz
    HEADERS = $(wildcard *.h)

To fix this, we need to use the :code:`edit()` method to write our custom
:code:`Makefile`.

.. literalinclude:: tutorial/examples/Makefile/2.package.py
   :language: python
   :emphasize-lines: 42,43,44
   :linenos:

Here we use a :code:`FileFilter` object to edit our :code:`Makefile`. It takes
in a regular expression and then replaces :code:`CC` and :code:`CXX` to whatever
Spack sets :code:`CC` and :code:`CXX` environment variables to. This allows us to
build :code:`Bowtie` with whatever compiler we specify through Spack's
:code:`spec` syntax.

Let's change the build and install phases of our package:

.. literalinclude:: tutorial/examples/Makefile/3.package.py
   :language: python
   :emphasize-lines: 46, 52
   :linenos:

Here demonstrate another strategy that we can use to manipulate our package
We can provide command-line arguments to :code:`make()`. Since :code:`Bowtie`
can use :code:`tbb` we can either add :code:`NO_TBB=1` as a argument to prevent
:code:`tbb` support or we can just invoke :code:`make` with no arguments.

:code:`Bowtie` requires our :code:`install_target` to provide a path to
the install directory. We can do this by providing :code:`prefix=` as a command
line argument to :code:`make()`.

Let's look at a couple of other examples and go through them:

.. code-block:: console

    $ spack edit cbench

Some packages allow environment variables to be set and will honor them.
Packages that use :code:`?=` for assignment in their :code:`Makefile`
can be set using environment variables. In our :code:`cbench` example we
set two environment variables in our :code:`edit()` method:

.. code-block:: python

    def edit(self, spec, prefix):
        # The location of the Cbench source tree
        env['CBENCHHOME'] = self.stage.source_path

        # The location that will contain all your tests and your results
        env['CBENCHTEST'] = prefix

        # ... more code

As you may have noticed, we didn't really write anything to the :code:`Makefile`
but rather we set environment variables that will override variables set in
the :code:`Makefile`.

Some packages include a configuration file that sets certain compiler variables,
platform specific variables, and the location of dependencies or libraries.
If the file is simple and only requires a couple of changes, we can overwrite
those entries with our :code:`FileFilter` object. If the configuration involves
complex changes, we can write a new configuration file from scratch.

Let's look at an example of this in the :code:`elk` package:

.. code-block:: console

    $ spack edit elk

.. code-block:: python

        def edit(self, spec, prefix):
        # Dictionary of configuration options
            config = {
                'MAKE': 'make',
                'AR':   'ar'
            }

            # Compiler-specific flags
            flags = ''
            if self.compiler.name == 'intel':
                flags = '-O3 -ip -unroll -no-prec-div'
            elif self.compiler.name == 'gcc':
                flags = '-O3 -ffast-math -funroll-loops'
            elif self.compiler.name == 'pgi':
                flags = '-O3 -lpthread'
            elif self.compiler.name == 'g95':
                flags = '-O3 -fno-second-underscore'
            elif self.compiler.name == 'nag':
                flags = '-O4 -kind=byte -dusty -dcfuns'
            elif self.compiler.name == 'xl':
                flags = '-O3'
            config['F90_OPTS'] = flags
            config['F77_OPTS'] = flags

            # BLAS/LAPACK support
            # Note: BLAS/LAPACK must be compiled with OpenMP support
            # if the +openmp variant is chosen
            blas = 'blas.a'
            lapack = 'lapack.a'
            if '+blas' in spec:
                blas = spec['blas'].libs.joined()
            if '+lapack' in spec:
                lapack = spec['lapack'].libs.joined()
            # lapack must come before blas
            config['LIB_LPK'] = ' '.join([lapack, blas])

            # FFT support
            if '+fft' in spec:
                config['LIB_FFT'] = join_path(spec['fftw'].prefix.lib,
                                            'libfftw3.so')
                config['SRC_FFT'] = 'zfftifc_fftw.f90'
            else:
                config['LIB_FFT'] = 'fftlib.a'
                config['SRC_FFT'] = 'zfftifc.f90'

            # MPI support
            if '+mpi' in spec:
                config['F90'] = spec['mpi'].mpifc
                config['F77'] = spec['mpi'].mpif77
            else:
                config['F90'] = spack_fc
                config['F77'] = spack_f77
                config['SRC_MPI'] = 'mpi_stub.f90'

            # OpenMP support
            if '+openmp' in spec:
                config['F90_OPTS'] += ' ' + self.compiler.openmp_flag
                config['F77_OPTS'] += ' ' + self.compiler.openmp_flag
            else:
                config['SRC_OMP'] = 'omp_stub.f90'

            # Libxc support
            if '+libxc' in spec:
                config['LIB_libxc'] = ' '.join([
                    join_path(spec['libxc'].prefix.lib, 'libxcf90.so'),
                    join_path(spec['libxc'].prefix.lib, 'libxc.so')
                ])
                config['SRC_libxc'] = ' '.join([
                    'libxc_funcs.f90',
                    'libxc.f90',
                    'libxcifc.f90'
                ])
            else:
                config['SRC_libxc'] = 'libxcifc_stub.f90'

            # Write configuration options to include file
            with open('make.inc', 'w') as inc:
                for key in config:
                    inc.write('{0} = {1}\n'.format(key, config[key]))

:code:`config` is just a dictionary that we can add key-value pairs to. By the
end of the :code:`edit()` method we write the contents of our dictionary to
:code:`make.inc`.

---------------
CMake
---------------

CMake_ is another common build system that has been gaining popularity. It works
in a similar manner to :code:`Autotools` but with differences in variable names,
the number of configuration options available, and the handling of shared libraries.
Typical build incantations look like this:

.. _CMake: https://cmake.org

.. code-block:: python

    def install(self, spec, prefix):
        cmake("-DCMAKE_INSTALL_PREFIX:PATH=/path/to/install_dir ..")
        make()
        make("install")

As you can see from the example above, it's very similar to invoking
:code:`configure` and :code:`make` in an :code:`Autotools` build system. However,
the variable names and options differ. Most options in CMake are prefixed
with a :code:`'-D'` flag to indicate a configuration setting.

In the :code:`CMakePackage` class we can override the following phases:

1. :code:`cmake()`
2. :code:`build()`
3. :code:`install()`

The :code:`CMakePackage` class also provides sensible defaults so we only need to
override :code:`cmake_args()`.

Let's look at these defaults in the :code:`CMakePackage` class:

.. code-block:: console

    $ spack edit --build-system cmake


And go into a bit of detail on the highlighted sections:


.. literalinclude:: ../../../lib/spack/spack/build_systems/cmake.py
   :language: python
   :lines: 37-92, 94-155, 174-211
   :emphasize-lines: 57,68,86,94,96,99,100,101,102,111,117,135,136
   :linenos:

Some :code:`CMake` packages use different generators. Spack is able to support
Unix-Makefile_ generators as well as Ninja_ generators.

.. _Unix-Makefile: https://cmake.org/cmake/help/v3.4/generator/Unix%20Makefiles.html
.. _Ninja: https://cmake.org/cmake/help/v3.4/generator/Ninja.html

Default generator is :code:`Unix Makefile`.

Next we setup the build type. In :code:`CMake` you can specify the build type
that you want. Options include:

1. empty
2. Debug
3. Release
4. RelWithDebInfo
5. MinSizeRel

With these options you can specify whether you want your executable to have
the debug version only, release version or the release with debug information.
Release executables tend to be more optimized than Debug. In Spack, we set
the default as RelWithDebInfo unless otherwise specified through a variant.

Spack then automatically sets up the :code:`-DCMAKE_INSTALL_PREFIX` path,
appends the build type (RelDebInfo default), and then specifies a verbose
:code:`Makefile`.

Next we add the :code:`rpaths` to :code:`-DCMAKE_INSTALL_RPATH:STRING`.


Finally we add to :code:`-DCMAKE_PREFIX_PATH:STRING` the locations of all our
dependencies so that :code:`CMake` can find them.

In the end our :code:`cmake` line will look like this (example is :code:`xrootd`):

.. code-block:: console

    $ cmake $HOME/spack/var/spack/stage/xrootd-4.6.0-4ydm74kbrp4xmcgda5upn33co5pwddyk/xrootd-4.6.0 -G Unix Makefiles -DCMAKE_INSTALL_PREFIX:PATH=$HOME/spack/opt/spack/darwin-sierra-x86_64/clang-9.0.0-apple/xrootd-4.6.0-4ydm74kbrp4xmcgda5upn33co5pwddyk -DCMAKE_BUILD_TYPE:STRING=RelWithDebInfo -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON -DCMAKE_FIND_FRAMEWORK:STRING=LAST -DCMAKE_INSTALL_RPATH_USE_LINK_PATH:BOOL=FALSE -DCMAKE_INSTALL_RPATH:STRING=$HOME/spack/opt/spack/darwin-sierra-x86_64/clang-9.0.0-apple/xrootd-4.6.0-4ydm74kbrp4xmcgda5upn33co5pwddyk/lib:$HOME/spack/opt/spack/darwin-sierra-x86_64/clang-9.0.0-apple/xrootd-4.6.0-4ydm74kbrp4xmcgda5upn33co5pwddyk/lib64 -DCMAKE_PREFIX_PATH:STRING=$HOME/spack/opt/spack/darwin-sierra-x86_64/clang-9.0.0-apple/cmake-3.9.4-hally3vnbzydiwl3skxcxcbzsscaasx5


Saves a lot of typing doesn't it?


Let's try to recreate callpath_:

.. _callpath: https://github.com/LLNL/callpath.git

.. code-block:: console

    $ spack create -f https://github.com/llnl/callpath/archive/v1.0.3.tar.gz
    ==> This looks like a URL for callpath
    ==> Found 4 versions of callpath:

    1.0.3  https://github.com/LLNL/callpath/archive/v1.0.3.tar.gz
    1.0.2  https://github.com/LLNL/callpath/archive/v1.0.2.tar.gz
    1.0.1  https://github.com/LLNL/callpath/archive/v1.0.1.tar.gz
    1.0    https://github.com/LLNL/callpath/archive/v1.0.tar.gz

    ==> How many would you like to checksum? (default is 1, q to abort) 1
    ==> Downloading...
    ==> Fetching https://github.com/LLNL/callpath/archive/v1.0.3.tar.gz
    ######################################################################## 100.0%
    ==> Checksummed 1 version of callpath
    ==> This package looks like it uses the cmake build system
    ==> Created template for callpath package
    ==> Created package file: /Users/mamelara/spack/var/spack/repos/builtin/packages/callpath/package.py


which then produces the following template:

.. literalinclude:: tutorial/examples/Cmake/0.package.py
   :language: python
   :linenos:

Again we fill in the details:

.. literalinclude:: tutorial/examples/Cmake/1.package.py
   :language: python
   :linenos:
   :emphasize-lines: 28,32,33,37,38,39,40,41,42

As mentioned earlier, Spack will use sensible defaults to prevent repeated code
and to make writing :code:`CMake` package files simpler.

In callpath, we want to add options to :code:`CALLPATH_WALKER` as well as add
compiler flags. We add the following options like so:

.. literalinclude:: tutorial/examples/Cmake/2.package.py
   :language: python
   :linenos:
   :emphasize-lines: 45,49,50

Now we can control our build options using :code:`cmake_args()`. If defaults are
sufficient enough for the package, we can leave this method out.

:code:`CMakePackage` classes allow for control of other features in the
build system. For example, you can specify the path to the "out of source"
build directory and also point to the root of the :code:`CMakeLists.txt` file if it
is placed in a non-standard location.

A good example of a package that has its :code:`CMakeLists.txt` file located at a
different location is found in :code:`spades`.

.. code-block:: console

    $ spack edit spade

.. code-block:: python

    root_cmakelists_dir = "src"

Here :code:`root_cmakelists_dir` will tell Spack where to find the location
of :code:`CMakeLists.txt`. In this example, it is located a directory level below in
the :code:`src` directory.

Some :code:`CMake` packages also require the :code:`install` phase to be
overridden. For example, let's take a look at :code:`sniffles`.

.. code-block:: console

    $ spack edit sniffles

In the :code:`install()` method, we have to manually install our targets
so we override the :code:`install()` method to do it for us:

.. code-block:: python

    # the build process doesn't actually install anything, do it by hand
    def install(self, spec, prefix):
        mkdir(prefix.bin)
        src = "bin/sniffles-core-{0}".format(spec.version.dotted)
        binaries = ['sniffles', 'sniffles-debug']
        for b in binaries:
            install(join_path(src, b), join_path(prefix.bin, b))


--------------
PythonPackage
--------------

Python extensions and modules are built differently from source than most
applications. Python uses a :code:`setup.py` script to install Python modules.
The script consists of a call to :code:`setup()` which provides the information
required to build a module to Distutils. If you're familiar with pip or
easy_install, setup.py does the same thing.

These modules are usually installed using the following line:

.. code-block:: console

    $ python setup.py install

There are also a list of commands and phases that you can call. To see the full
list you can run:

.. code-block:: console

    $ python setup.py --help-commands
    Standard commands:
        build             build everything needed to install
        build_py          "build" pure Python modules (copy to build directory)
        build_ext         build C/C++ extensions (compile/link to build directory)
        build_clib        build C/C++ libraries used by Python extensions
        build_scripts     "build" scripts (copy and fixup #! line)
        clean             (no description available)
        install           install everything from build directory
        install_lib       install all Python modules (extensions and pure Python)
        install_headers   install C/C++ header files
        install_scripts   install scripts (Python or otherwise)
        install_data      install data files
        sdist             create a source distribution (tarball, zip file, etc.)
        register          register the distribution with the Python package index
        bdist             create a built (binary) distribution
        bdist_dumb        create a "dumb" built distribution
        bdist_rpm         create an RPM distribution
        bdist_wininst     create an executable installer for MS Windows
        upload            upload binary package to PyPI
        check             perform some checks on the package


To see the defaults that Spack has for each a methods, we will take a look
at the :code:`PythonPackage` class:

.. code-block:: console

    $ spack edit --build-system python

We see the following:


.. literalinclude:: ../../../lib/spack/spack/build_systems/python.py
   :language: python
   :lines: 35, 161-364
   :linenos:

Each of these methods have sensible defaults or they can be overridden.

We can write package files for Python packages using the :code:`Package` class,
but the class brings with it a lot of methods that are useless for Python packages.
Instead, Spack has a :code: `PythonPackage` subclass that allows packagers
of Python modules to be able to invoke :code:`setup.py` and use :code:`Distutils`,
which is much more familiar to a typical python user.


We will write a package file for Pandas_:

.. _pandas: https://pandas.pydata.org

.. code-block:: console

    $ spack create -f https://pypi.io/packages/source/p/pandas/pandas-0.19.0.tar.gz
    ==> This looks like a URL for pandas
    ==> Warning: Spack was unable to fetch url list due to a certificate verification problem. You can try running spack -k, which will not check SSL certificates. Use this at your own risk.
    ==> Found 1 version of pandas:

    0.19.0  https://pypi.io/packages/source/p/pandas/pandas-0.19.0.tar.gz

    ==> How many would you like to checksum? (default is 1, q to abort) 1
    ==> Downloading...
    ==> Fetching https://pypi.io/packages/source/p/pandas/pandas-0.19.0.tar.gz
    ######################################################################## 100.0%
    ==> Checksummed 1 version of pandas
    ==> This package looks like it uses the python build system
    ==> Changing package name from pandas to py-pandas
    ==> Created template for py-pandas package
    ==> Created package file: /Users/mamelara/spack/var/spack/repos/builtin/packages/py-pandas/package.py

And we are left with the following template:

.. literalinclude:: tutorial/examples/PyPackage/0.package.py
   :language: python
   :linenos:

As you can see this is not any different than any package template that we have
written. We have the choice of providing build options or using the sensible
defaults

Luckily for us, there is no need to provide build args.

Next we need to find the dependencies of a package. Dependencies are usually
listed in :code:`setup.py`. You can find the dependencies by searching for
:code:`install_requires` keyword in that file. Here it is for :code:`Pandas`:

.. code-block:: python

    # ... code
    if sys.version_info[0] >= 3:

    setuptools_kwargs = {
                         'zip_safe': False,
                         'install_requires': ['python-dateutil >= 2',
                                              'pytz >= 2011k',
                                              'numpy >= %s' % min_numpy_ver],
                         'setup_requires': ['numpy >= %s' % min_numpy_ver],
                         }
    if not _have_setuptools:
        sys.exit("need setuptools/distribute for Py3k"
                 "\n$ pip install distribute")

    # ... more code

You can find a more comprehensive list at the Pandas documentation_.

.. _documentation: https://pandas.pydata.org/pandas-docs/stable/install.html


By reading the documentation and :code:`setup.py` we found that :code:`Pandas`
depends on :code:`python-dateutil`, :code:`pytz`, and :code:`numpy`, :code:`numexpr`,
and finally :code:`bottleneck`.

Here is the completed :code:`Pandas` script:

.. literalinclude:: tutorial/examples/PyPackage/1.package.py
   :language: python
   :linenos:

It is quite important to declare all the dependencies of a Python package.
Spack can "activate" Python packages to prevent the user from having to
load each dependency module explictly. If a dependency is missed, Spack will
be unable to properly activate the package and it will cause an issue. To
learn more about extensions go to :ref:`cmd-spack-extensions`.

From this example, you can see that building Python modules is made easy
through the :code:`PythonPackage` class.

-------------------
Other Build Systems
-------------------

Although we won't get in depth with any of the other build systems that Spack
supports, it is worth mentioning that Spack does provide subclasses
for the following build systems:

1. :code:`IntelPackage`
2. :code:`SconsPackage`
3. :code:`WafPackage`
4. :code:`RPackage`
5. :code:`PerlPackage`
6. :code:`QMake`


Each of these classes have their own abstractions to help assist in writing
package files. For whatever doesn't fit nicely into the other build-systems,
you can use the :code:`Package` class.

Hopefully by now you can see how we aim to make packaging simple and
robust through these classes. If you want to learn more about these build
systems, check out :ref:`installation_procedure` in the Packaging Guide.
