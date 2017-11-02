.. _build-systems:

==============================
Spack Package Build Systems
==============================

You may begin to notice after writing a couple of package template files a 
pattern emerge for some packages. For example, you may find yourself writing
an `install` method that invokes: `configure`, `make`, `make install` or `cmake`.
You may also find yourself writing `prefix= + prefix` as an argument to configure
or cmake. Rather than having you repeat these lines, Spack has package subclasses
that can take care of these patterns to avoid having to repeat yourself. In 
addition, these package files allow for finer grained control of these build 
systems. In this section we will describe each build system and give examples
on how these can be manipulated to install a package.

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
package relates. Each subclass inherits from the `PackageBaseClass` super class.
The bulk of the work is done in this super class which includes fetching,
extracting to a staging directory and installing. Each subclass thus adds 
additional functionality that includes adding the correct parameters for the
build system. In the following sections, we will go over examples of how to
utilize each subclass and to see how powerful these abstractions are when
packaging.

-----------------
Package
-----------------

We've already seen examples of Package classes in our walkthrough for writing
package files, so we won't be spending much time with examples. Briefly, Package
classes are vanilla classes than can be used for any of the common build systems
such as GNU Autotools and CMake. Spack will revert to using a Package class
if it cannot determine the build system. If Spack is unable to correctly
identify the build system for your package and you happen to know what it is
we recommend that you switch to the proper subclass.

-----------------
Makefile
-----------------

Packages that utilize GNU Make require a custom written Makefile
to build from source. Let's try to recreate the bowtie_ package:

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

Spack was successfully able to detect that bowtie uses GNU Make. Let's add
in the rest of our details for our package:

.. literalinclude:: tutorial/examples/Makefile/1.package.py
   :language: python

If the application is simple to build then the contents present in our package.py
is enough and we don't have to override any methods in our Makefile package. In
fact, for most of the build systems, overriding methods is optional and packages
can be kept as simple as what we have already. 

Unfortunately, the defaults that bowtie sets up are not what we 
need. If we look inside the Makefile, we see that CC and CXX point to our GNU
compiler:

.. code-block:: make
    
    CPP = g++ -w
    CXX = $(CPP)
    CC = gcc
    LIBS = $(LDFLAGS) -lz
    HEADERS = $(wildcard *.h)

To fix this we need to use the edit method which is used to write to our custom
Makefile:

.. literalinclude:: tutorial/examples/Makefile/2.package.py
   :language: python

Here we used regex to make CC and CXX point at whatever Spack sets
CC and CXX to. This allows us to build bowtie with whatever compiler we specify
through Spack's specs. We can also specify our build targets and install targets
usng the build() and install() methods.

.. literalinclude:: tutorial/examples/Makefile/3.package.py
   :language: python

In our build stage we are able to provide an argument to make whether we
decide to build with tbb support or not. For the install, phase we provide
the prefix and then invoke make install. 

Through this example, we are able to see that we can change the Makefile through
our edit method, as well as invoke build, and install to specify our build
and install targets, respectively.

-------------------
Autotools
-------------------

As mentioned earlier, Autotools consist of three parts:  autoconf, automake,
and libtool. Your typical build incantation will consist of the following:

.. code-block:: console

    ./configure --prefix=/path/to/install_dir
    make
    make install

Although it is possible to write these packages using the vanilla Package 
class, Spack has an Autotools class that automatically sets up common 
arguments to configure. In the Autotools class we can override four phases: 
autoreconf, configure, build, and install. Autoreconf is only necessary if 
there is no configure script present and one has to be generated using. 
Most packagers will only need to override the helper method 
configure_args since Spack provides sensible defaults for each phase. 

Let's look at the mpileaks package.py file that we worked on earlier:


.. code-block:: console
    
    $ spack edit mpileaks

Notice that mpileaks is a Package class but uses the Autotools build system 
(the configure, make, make install incantation gives us a hint). Although
this package is acceptable lets make this into an AutotoolsPackage class and
simplify it further.

.. literalinclude:: tutorial/examples/Autotools/0.package.py

We first inherit from the AutotoolsPackage class. 

We can keep the install method but we can simplify this further by adding configure_args:

.. literalinclude:: tutorial/examples/Autotools/1.package.py

A couple of things to note here: We got rid of "prefix=" + prefix, and also
the calls to make() and make("install"). So not only does our package.py
file look simpler, but we can also get rid of repeated code and not have to
worry about having to invoke configure and make, make install. Even better
is that we have allowed further control over what targets we choose to 
build during our make phase as well as additional functionality. For example,
if we wish to add a check or test phase in our install we can add:

.. code-block:: python
    
    def check()

to our package.py file. 

---------------
CMake
---------------

CMake_ is another common build system that has been gaining popularity. It works
in a similar manner to autotools but with differences in variable names,
the number of configuration options available, and the handling of shared libraries.
Most CMake projects are built out of source which means that there is a dedicated
build directory that is separate from the source directory.
Typical build incantations look like this:

.. _CMake: https://cmake.org

.. code-block:: console

    mkdir BUILD && cd BUILD
    cmake -DCMAKE_INSTALL_PREFIX=/path/to/install_dir ..
    make
    make install

As you can see from the example above, it's very similar to invoking configure
and make in an Autotools build system. However, the variable names and options
differ. Most options in CMake are prefixed with a -D flag to indicate a 
configuration setting.

For this example we will try to recreate callpath:

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

Again we fill in the details:

.. literalinclude:: tutorial/examples/Cmake/1.package.py
   :language: python

Spack will automatically add -DCMAKE_INSTALL_PREFIX, -DCMAKE_BUILD_TYPE, 
-DCMAKE_VERBOSE_MAKEFILE as well as a number of other options to cmake without
the user having to explictly add those arguments. 

In callpath, we want to add options to CALLPATH_WALKER as well as add compiler flags.
We add the following options like so:

.. literalinclude:: tutorial/examples/Cmake/2.package.py
   :language: python

Now we can control our build options using cmake_args. Again if defaults are
sufficient enough for the package, we can leave out cmake_args in our package.py

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
required to building a module to Distutils. If you're familiar with pip or 
easy_install, setup.py does the same thing.

These modules are usually installed using the following line:

.. code-block:: console
    
    $ python setup.py install <module>

There are also a list of commands and phases that you can call. To see the full
list you can run:
    
.. code-block:: console
    
    $ python setup.py --help-commands

For each of these commands, Spack has a method that can be overridden. 

Using the Package class is possible but it brings with it a lot of unnecessary
methods that are useless for a Python package. Instead, Spack has a PythonPackage
subclass that allows packagers of Python modules to be able to invoke setup.py
and use Distutils.  

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

As you can see this is not any different than any package template that we have
written. Spack will provide sensible defaults and we have the option of providing
it.

Luckily for us, there is no need to provide build args. The default args
that Spack provides is 'build' which builds everything needed to install. Once
the build phase is completed the install phase will commence and soon we will
have our python module. 

Here is the completed Pandas script:

.. literalinclude:: tutorial/examples/PyPackage/1.package.py

As you can see, Pandas is easy to install since we do not have to do anything
rather convoluted and complex. Instead, Spack has provided us the right abstractions
to make installing Python packages easy.

-------------------
Other Build Systems
-------------------

Although we won't get in depth with any of the other build systems that Spack
has support for me it is worth mentioning that Spack does provide subclasses
for the following build systems:

IntelPackage, SconsPackage, WafPackage, RPackage, PerlPackage, and QMake.


Each of these classes have their own abstractions to help assist the packager
write for these types of packages. 

At this point, we hope you have seen the capabilities that Spack has offered
to deal with various build systems and their, at times, complex behavior. Our
aim is to make packaging as simple but robust as possible. 
