.. _build-systems:

==============================
Spack Package Build Systems
==============================

You may begin to notice after writing a couple of package template files a 
pattern emerge for some packages. For example, you may find yourself writing
an :code:`install` method that invokes: :code:`configure`, :code:`cmake`, 
:code:`make`, :code:`make install`. You may also find yourself writing 
:code:`prefix= + prefix` as an argument to configure or cmake. Rather than 
having you repeat these lines for all packages, Spack has classes that can 
take care of these patterns to avoid having to repeat yourself. In addition, 
these package files allow for finer grained control of these build  systems. 
In this section we will describe each build system and give examples on how 
these can be manipulated to install a package.

-----------------------
Package class Hierarchy
-----------------------
.. graphviz::

    digraph {
        Package -> PackageBaseClass;
        MakefilePackage -> PackageBaseClass;
        AutotoolsPackage -> PackageBaseClass;
        CMakePackage -> PackageBaseClass;
        PythonPackage -> PackageBaseClass;
        RPackage -> PackageBaseClass;
    }

The above diagram gives a high level view of the class hierarchy and how each
package relates. Each subclass inherits from the :code:`PackageBaseClass` 
super class. The bulk of the work is done in this super class which includes 
fetching, extracting to a staging directory and installing. Each subclass 
thus adds additional functionality that includes adding the correct parameters 
for the build system. In the following sections, we will go over examples of 
how to utilize each subclass and to see how powerful these abstractions are 
when packaging.

-----------------
Package
-----------------

We've already seen examples of a Package class in our walkthrough for writing
package files, so we won't be spending much time with them here. Briefly,
the Package class allows for abitrary control over the build process, whereas
subclasses rely on certain patterns (e.g. :code:`configure` :code:`make` 
:code:`make install`) to be useful. Package classes are particularly useful 
for packages that have a non-conventional way of being built since the packager 
can utilize some of Spack's helper functions to customize the building and 
installing of a package.

-------------------
Autotools
-------------------

As we have seen earlier, packages using Autotools use :code:`configure`, 
:code:`make` and :code:`make install` commands to execute the build and 
install process. In our Package class, your typical build incantation will 
consist of the following:

.. code-block:: python

    def install(self, spec, prefix):
        configure("--prefix=" + prefix)
        make()
        make("install")

You'll see that this looks similar to what we wrote in our packaging tutorial.

The Autotools subclass aims to simplify writing package files and provides
convenience methods to manipulate each of the different phases for a Autotools
build system.

Autotools packages consist of four phases:

1. :code:`autoreconf()`
2. :code:`configure()`
3. :code:`build()`
4. :code:`install()`


Each of these phases have sensible defaults. Let's take a quick look at some 
the internals of the Autotools class:

.. note:: 
    The examples showing code for these classes is abridged to avoid having
    long examples. We only show what is relevant to the packager.


.. literalinclude:: tutorial/examples/Autotools/autotools_class.py
    :language: python
    :emphasize-lines: 42,45,62
    :lines: 40-95,259-267
    :linenos:


Important to note are lines 42 and 45 (highlighted here). 
These properties allow the packager to set what build targets and install 
targets they want for their package. If, for example, we wanted to add as our
build target :code:`foo` then we can append to our :code:`build_targets` 
property:

.. code-block:: python

    build_targets = ["foo"]

Which is similiar to invoking make in our Package 

.. code-block:: python
    
     make("foo")

Another thing we have highlighted is in the :code:`configure()` method. 
Here we see that the prefix option is already included which reduces 
repeated code.

Let's look at the mpileaks package.py file that we worked on earlier:


.. code-block:: console
    
    $ spack edit mpileaks

Notice that mpileaks is a Package class but uses the Autotools build system 
(the configure, make, make install incantation gives us a hint). Although
this package is acceptable lets make this into an AutotoolsPackage class and
simplify it further.

.. literalinclude:: tutorial/examples/Autotools/0.package.py
   :language: python
   :emphasize-lines: 28
   :linenos:

We first inherit from the AutotoolsPackage class. 

We can keep the install method but we can simplify this further by adding 
configure_args:

.. literalinclude:: tutorial/examples/Autotools/1.package.py
   :language: python
   :emphasize-lines: 42,43
   :linenos:

Since Spack takes care of setting the prefix for us we can exclude that as
an argument to :code:`configure`. Our packages look simpler, and the packager
does not need to worry about whether they have properly included :code:`configure`
and :code:`make`.

-----------------
Makefile
-----------------

Packages that utilize GNU Make require a custom written Makefile
to build from source. These packages are handled by the Makefile subclass which
provides convenience methods to help write these types of packages. 

A Makefile class has three phases that can be overridden. These include:

    1. :code:`edit()`
    2. :code:`build()`
    3. :code:`install()`

Packagers then have the ability to control how a makefile is edited, and
what targets to include for the build phase or install phase.

Let's also take a look inside the MakefilePackage class:

.. literalinclude:: tutorial/examples/Makefile/makefile_class.py
   :language: python
   :lines: 33-79,89-107
   :emphasize-lines: 48,54,61
   :linenos:

Similar to Autotools, MakefilePackage class has properties that can be set
by the packager. We can also override the different methods highlighted.


Let's try to recreate the bowtie_ package:

.. _bowtie: http://bowtie-bio.sourceforge.net/index.shtml


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
usual fashion and create a template of a MakefilePackage package.py.

.. literalinclude:: tutorial/examples/Makefile/0.package.py
   :language: python
   :linenos:

Spack was successfully able to detect that bowtie uses GNU Make. Let's add
in the rest of our details for our package:

.. literalinclude:: tutorial/examples/Makefile/1.package.py
   :language: python
   :emphasize-lines: 29,30,32,33,37,39
   :linenos:

Most packages using GNU Make require a makefile to be edited. The Makefile
subclass makes it easy to edit these makefiles by having an edit phase during
the install process. Some packages may have a default makefile distributed with
their system but these defaults may not satisfy a particular packager's needs.



Let's take a look at the default makefile that :code:`bowtie` provides. 
If we look inside, we see that CC and CXX point to our GNU
compiler:

.. code-block:: make
    
    CPP = g++ -w
    CXX = $(CPP)
    CC = gcc
    LIBS = $(LDFLAGS) -lz
    HEADERS = $(wildcard *.h)

To fix this, we need to use the edit method to write our custom makefile.


.. literalinclude:: tutorial/examples/Makefile/2.package.py
   :language: python
   :emphasize-lines: 42,43,44
   :linenos:

Here we used regex to make CC and CXX point at whatever Spack sets
CC and CXX to. This allows us to build bowtie with whatever compiler we specify
through Spack's specs. We can also specify our build targets and install targets
usng the build() and install() methods.

.. literalinclude:: tutorial/examples/Makefile/3.package.py
   :language: python
   :emphasize-lines: 46, 52
   :linenos:

In our build stage, we are able to provide an argument to :code:`make` whether 
we decide to build with tbb support or not. For the install phase, we provide
the prefix and then invoke make install. 

---------------
CMake
---------------

CMake_ is another common build system that has been gaining popularity. It works
in a similar manner to `Autotools` but with differences in variable names,
the number of configuration options available, and the handling of shared libraries.
Typical build incantations look like this:

.. _CMake: https://cmake.org

.. code-block:: python

    cmake("-DCMAKE_INSTALL_PREFIX:PATH=/path/to/install_dir ..")
    make()
    make("install")

As you can see from the example above, it's very similar to invoking 
:code:`configure` and :code:`make` in an Autotools build system. However, 
the variable names and options differ. Most options in CMake are prefixed 
with a '-D' flag to indicate a configuration setting.

In the CMakePackage class we can override the following phases:

1. :code:`cmake()`
2. :code:`build()`
3. :code:`install()`

The CMakePackage class also provides sensible defaults so we only need to
override :code:`cmake_args()`.

Let's look at these defaults in the CMakePackage class:

.. literalinclude:: tutorial/examples/Cmake/cmake_class.py
   :language: python
   :lines: 37-92, 94-155, 174-211
   :emphasize-lines: 57,68,99,100,101,102,135,136
   :linenos:

Spack sets up the location of CMakelists.txt as well as the following default
args emphasized in line 135-140. We can also see that the cmake method
takes whatever arguments are returned from :code:`cmake_args()` and appends 
them to the default list of args and invokes :code:`cmake()`. 
Packagers wishing to change these defaults and behavior can override these 
methods.

Let's try to recreate callpath:

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
and to make writing Cmake package files simpler.

In callpath, we want to add options to :code:`CALLPATH_WALKER` as well as add 
compiler flags. We add the following options like so:

.. literalinclude:: tutorial/examples/Cmake/2.package.py
   :language: python
   :linenos:
   :emphasize-lines: 45,49,50

Now we can control our build options using cmake_args. Again if defaults are
sufficient enough for the package, we can leave out :code:`cmake_args()` 
in our package.py

CMake classes allow for control of other features in the build system. For example,
you can specify the path to the "out of source" build directory and also point
to the root of the CMakeLists.txt file if it is placed in a non-standard 
location.

--------------
PythonPackage
--------------

Python extensions and modules are built differently from source than most
applications. Python uses a setup.py script to install Python modules. 
The script consists of a call to setup() which provides the information 
required to build a module to Distutils. If you're familiar with pip or 
easy_install, setup.py does the same thing.

These modules are usually installed using the following line:

.. code-block:: console
    
    $ python setup.py install <module>

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


For each of these commands, Spack has a method that can be overridden. 

To see the defaults that Spack has for each a methods, we will take a look
at the PythonPackage class:

.. literalinclude:: tutorial/examples/PyPackage/python_package_class.py
   :language: python
   :lines: 35, 161-364
   :linenos:

As noted earlier, each of those methods have sensible defaults or they can
be overridden.

Using the Package class is possible but it brings with it a lot of unnecessary
methods that are useless for a Python package. Instead, Spack has a PythonPackage
subclass that allows packagers of Python modules to be able to invoke setup.py
and use Distutils, which is much more familiar to a typical python user. 



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

Luckily for us, there is no need to provide build args. The default args
that Spack provides is 'build' which builds everything needed to install. Once
the build phase is completed the install phase will commence and soon we will
have our python module. 

Here is the completed Pandas script:

.. literalinclude:: tutorial/examples/PyPackage/1.package.py
   :language: python
   :linenos:

As you can see, Pandas is easy to install since we do not have to do anything
rather convoluted and complex. Instead, Spack has provided us the right abstractions
to make installing Python packages easy.

-------------------
Other Build Systems
-------------------

Although we won't get in depth with any of the other build systems that Spack
has support for me it is worth mentioning that Spack does provide subclasses
for the following build systems:

1. :code:`IntelPackage`
2. :code:`SconsPackage`
3. :code:`WafPackage`
4. :code:`RPackage`
5. :code:`PerlPackage`
6. :code:`QMake`


Each of these classes have their own abstractions to help assist the packager
write for these types of packages. For whatever doesn't fit nicely into the
other packages, the Package class can be used.

At this point, we hope you have seen the capabilities that Spack has offered
to deal with various build systems and their, at times, complex behavior. Our
aim is to make packaging as simple but robust as possible. 
