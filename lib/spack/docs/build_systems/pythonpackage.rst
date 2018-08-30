.. _pythonpackage:

-------------
PythonPackage
-------------

Python packages and modules have their own special build system.

^^^^^^
Phases
^^^^^^

The ``PythonPackage`` base class provides the following phases that
can be overridden:

* ``build``
* ``build_py``
* ``build_ext``
* ``build_clib``
* ``build_scripts``
* ``clean``
* ``install``
* ``install_lib``
* ``install_headers``
* ``install_scripts``
* ``install_data``
* ``sdist``
* ``register``
* ``bdist``
* ``bdist_dumb``
* ``bdist_rpm``
* ``bdist_wininst``
* ``upload``
* ``check``

These are all standard ``setup.py`` commands and can be found by running:

.. code-block:: console

   $ python setup.py --help-commands


By default, only the ``build`` and ``install`` phases are run:

#. ``build`` - build everything needed to install
#. ``install`` - install everything from build directory

If for whatever reason you need to run more phases, simply modify your
``phases`` list like so:

.. code-block:: python

   phases = ['build_ext', 'install', 'bdist']


Each phase provides a function ``<phase>`` that runs:

.. code-block:: console

   $ python -s setup.py --no-user-cfg <phase>


Each phase also has a ``<phase_args>`` function that can pass arguments to
this call. All of these functions are empty except for the ``install_args``
function, which passes ``--prefix=/path/to/installation/prefix``. There is
also some additional logic specific to setuptools and eggs.

If you need to run a phase that is not a standard ``setup.py`` command,
you'll need to define a function for it like so:

.. code-block:: python

   phases = ['configure', 'build', 'install']

   def configure(self, spec, prefix):
       self.setup_py('configure')


^^^^^^^^^^^^^^^
Important files
^^^^^^^^^^^^^^^

Python packages can be identified by the presence of a ``setup.py`` file.
This file is used by package managers like ``pip`` to determine a
package's dependencies and the version of dependencies required, so if
the ``setup.py`` file is not accurate, the package will not build properly.
For this reason, the ``setup.py`` file should be fairly reliable. If the
documentation and ``setup.py`` disagree on something, the ``setup.py``
file should be considered to be the truth. As dependencies are added or
removed, the documentation is much more likely to become outdated than
the ``setup.py``.

^^^^^^^^^^^^^^^^^^^^^^^
Finding Python packages
^^^^^^^^^^^^^^^^^^^^^^^

The vast majority of Python packages are hosted on PyPI - The Python
Package Index. ``pip`` only supports packages hosted on PyPI, making
it the only option for developers who want a simple installation.
Search for "PyPI <package-name>" to find the download page. Note that
some pages are versioned, and the first result may not be the newest
version. Click on the "Latest Version" button to the top right to see
if a newer version is available. The download page is usually at:
https://pypi.org/project/<package-name>

^^^^^^^^^^^
Description
^^^^^^^^^^^

The top of the PyPI downloads page contains a description of the
package. The first line is usually a short description, while there
may be a several line "Project Description" that follows. Choose whichever
is more useful. You can also get these descriptions on the command-line
using:

.. code-block:: console

   $ python setup.py --description
   $ python setup.py --long-description


^^^^^^^^
Homepage
^^^^^^^^

Package developers use ``setup.py`` to upload new versions to PyPI.
The ``setup`` method often passes metadata like ``homepage`` to PyPI.
This metadata is displayed on the left side of the download page.
Search for the text "Homepage" under "Project links" to find it. You
should use this page instead of the PyPI page if they differ. You can
also get the homepage on the command-line by running:

.. code-block:: console

   $ python setup.py --url


^^^
URL
^^^

You may have noticed that Spack allows you to add multiple versions of
the same package without adding multiple versions of the download URL.
It does this by guessing what the version string in the URL is and
replacing this with the requested version. Obviously, if Spack cannot
guess the version correctly, or if non-version-related things change
in the URL, Spack cannot substitute the version properly.

Once upon a time, PyPI offered nice, simple download URLs like:
https://pypi.python.org/packages/source/n/numpy/numpy-1.13.1.zip

As you can see, the version is 1.13.1. It probably isn't hard to guess
what URL to use to download version 1.12.0, and Spack was perfectly
capable of performing this calculation.

However, PyPI switched to a new download URL format:
https://pypi.python.org/packages/c0/3a/40967d9f5675fbb097ffec170f59c2ba19fc96373e73ad47c2cae9a30aed/numpy-1.13.1.zip#md5=2c3c0f4edf720c3a7b525dacc825b9ae

and more recently:
https://files.pythonhosted.org/packages/b0/2b/497c2bb7c660b2606d4a96e2035e92554429e139c6c71cdff67af66b58d2/numpy-1.14.3.zip

As you can imagine, it is impossible for Spack to guess what URL to
use to download version 1.12.0 given this URL. There is a solution,
however. PyPI offers a new hidden interface for downloading
Python packages that does not include a hash in the URL:
https://pypi.io/packages/source/n/numpy/numpy-1.13.1.zip

This URL redirects to the files.pythonhosted.org URL. The general syntax for
this pypi.io URL is:
https://pypi.io/packages/source/<first-letter-of-name>/<name>/<name>-<version>.<extension>

Please use the pypi.io URL instead of the pypi.python.org URL. If both
``.tar.gz`` and ``.zip`` versions are available, ``.tar.gz`` is preferred.
If some releases offer both ``.tar.gz`` and ``.zip`` versions, but some
only offer ``.zip`` versions, use ``.zip``.

"""""""""""""""
PyPI vs. GitHub
"""""""""""""""

Many packages are hosted on PyPI, but are developed on GitHub and other
version control systems. The tarball can be downloaded from either
location, but PyPI is preferred for the following reasons:

#. PyPI contains the bare minimum of files to install the package.

   You may notice that the tarball you download from PyPI does not
   have the same checksum as the tarball you download from GitHub.
   When a developer uploads a new release to PyPI, it doesn't contain
   every file in the repository, only the files necessary to install
   the package. PyPI tarballs are therefore smaller.

#. PyPI is the official source for package managers like ``pip``.

   Let's be honest, ``pip`` is much more popular than Spack. If the
   GitHub tarball contains a file not present in the PyPI tarball that
   causes a bug, the developers may not realize this for quite some
   time. If the bug was in a file contained in the PyPI tarball, users
   would notice the bug much more quickly.

#. GitHub release may be a beta version.

   When a developer releases a new version of a package on GitHub,
   it may not be intended for most users. Until that release also
   makes its way to PyPI, it should be assumed that the release is
   not yet ready for general use.

#. The checksum for a GitHub release may change.

   Unfortunately, some developers have a habit of patching releases
   without incrementing the version number. This results in a change
   in tarball checksum. Package managers like Spack that use checksums
   to verify the integrity of a download tarball grind to a halt when
   the checksum for a known version changes. Most of the time, the
   change is intentional, and contains a needed bug fix. However,
   sometimes the change indicates a download source that has been
   compromised, and a tarball that contains a virus. If this happens,
   you must contact the developers to determine which is the case.
   PyPI is nice because it makes it physically impossible to
   re-release the same version of a package with a different checksum.

There are some reasons to prefer downloading from GitHub:

#. The GitHub tarball may contain unit tests

   As previously mentioned, the PyPI tarball contains the bare minimum
   of files to install the package. Unless explicitly specified by the
   developers, it will not contain development files like unit tests.
   If you desire to run the unit tests during installation, you should
   use the GitHub tarball instead.

#. Spack does not yet support ``spack versions`` and ``spack checksum``
   with PyPI URLs

   These commands work just fine with GitHub URLs. This is a minor
   annoyance, not a reason to prefer GitHub over PyPI.

If you really want to run these unit tests, no one will stop you from
submitting a PR for a new package that downloads from GitHub.

^^^^^^^^^^^^^^^^^^^^^^^^^
Build system dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^

There are a few dependencies common to the ``PythonPackage`` build system.

""""""
Python
""""""

Obviously, every ``PythonPackage`` needs Python at build-time to run
``python setup.py build && python setup.py install``. Python is also
needed at run-time if you want to import the module. Due to backwards
incompatible changes between Python 2 and 3, it is very important to
specify which versions of Python are supported. If the documentation
mentions that Python 3 is required, this can be specified as:

.. code-block:: python

   depends_on('python@3:', type=('build', 'run')


If Python 2 is required, this would look like:

.. code-block:: python

   depends_on('python@:2', type=('build', 'run')


If Python 2.7 is the only version that works, you can use:

.. code-block:: python

   depends_on('python@2.7:2.8', type=('build', 'run')


The documentation may not always specify supported Python versions.
Another place to check is in the ``setup.py`` file. Look for a line
containing ``python_requires``. An example from
`py-numpy <https://github.com/spack/spack/blob/develop/var/spack/repos/builtin/packages/py-numpy/package.py>`_
looks like:

.. code-block:: python

   python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*'


More commonly, you will find a version check at the top of the file:

.. code-block:: python

   if sys.version_info[:2] < (2, 7) or (3, 0) <= sys.version_info[:2] < (3, 4):
       raise RuntimeError("Python version 2.7 or >= 3.4 required.")


This can be converted to Spack's spec notation like so:

.. code-block:: python

   depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))


""""""""""
setuptools
""""""""""

Originally, the Python language had a single build system called
distutils, which is built into Python. Distutils provided a common
framework for package authors to describe their project and how it
should be built. However, distutils was not without limitations.
Most notably, there was no way to list a project's dependencies
with distutils. Along came setuptools, a non-builtin build system
designed to overcome the limitations of distutils. Both projects
use a similar API, making the transition easy while adding much
needed functionality. Today, setuptools is used in around 75% of
the Python packages in Spack.

Since setuptools isn't built-in to Python, you need to add it as a
dependency. To determine whether or not a package uses setuptools,
search the file for an import statement like:

.. code-block:: python

   import setuptools


or:

.. code-block:: python

   from setuptools import setup


Some packages are designed to work with both setuptools and distutils,
so you may find something like:

.. code-block:: python

   try:
       from setuptools import setup
   except ImportError:
       from distutils.core import setup


This uses setuptools if available, and falls back to distutils if not.
In this case, you would still want to add a setuptools dependency, as
it offers us more control over the installation.

Unless specified otherwise, setuptools is usually a build-only dependency.
That is, it is needed to install the software, but is not needed at
run-time. This can be specified as:

.. code-block:: python

   depends_on('py-setuptools', type='build')


""""""
cython
""""""

Compared to compiled languages, interpreted languages like Python can
be quite a bit slower. To work around this, some Python developers
rewrite computationally demanding sections of code in C, a process
referred to as "cythonizing". In order to build these package, you
need to add a build dependency on cython:

.. code-block:: python

   depends_on('py-cython', type='build')


Look for references to "cython" in the ``setup.py`` to determine
whether or not this is necessary. Cython may be optional, but
even then you should list it as a required dependency. Spack is
designed to compile software, and is meant for HPC facilities
where speed is crucial. There is no reason why someone would not
want an optimized version of a library instead of the pure-Python
version.

^^^^^^^^^^^^^^^^^^^
Python dependencies
^^^^^^^^^^^^^^^^^^^

When you install a package with ``pip``, it reads the ``setup.py``
file in order to determine the dependencies of the package.
If the dependencies are not yet installed, ``pip`` downloads them
and installs them for you. This may sound convenient, but Spack
cannot rely on this behavior for two reasons:

#. Spack needs to be able to install packages on air-gapped networks.

   If there is no internet connection, ``pip`` can't download the
   package dependencies. By explicitly listing every dependency in
   the ``package.py``, Spack knows what to download ahead of time.

#. Duplicate installations of the same dependency may occur.

   Spack supports *activation* of Python extensions, which involves
   symlinking the package installation prefix to the Python installation
   prefix. If your package is missing a dependency, that dependency
   will be installed to the installation directory of the same package.
   If you try to activate the package + dependency, it may cause a
   problem if that package has already been activated.

For these reasons, you must always explicitly list all dependencies.
Although the documentation may list the package's dependencies,
often the developers assume people will use ``pip`` and won't have to
worry about it. Always check the ``setup.py`` to find the true
dependencies.

If the package relies on ``distutils``, it may not explicitly list its
dependencies. Check for statements like:

.. code-block:: python

   try:
       import numpy
   except ImportError:
       raise ImportError("numpy must be installed prior to installation")


Obviously, this means that ``py-numpy`` is a dependency.

If the package uses ``setuptools``, check for the following clues:

* ``install_requires``

  These packages are required for installation.

* ``extra_requires``

  These packages are optional dependencies that enable additional
  functionality. You should add a variant that optionally adds these
  dependencies.

* ``test_requires``

  These are packages that are required to run the unit tests for the
  package. These dependencies can be specified using the
  ``type='test'`` dependency type.

In the root directory of the package, you may notice a
``requirements.txt`` file. It may look like this file contains a list
of all of the package's dependencies. Don't be fooled. This file is
used by tools like Travis to install the pre-requisites for the
package... and a whole bunch of other things. It often contains
dependencies only needed for unit tests, like:

* mock
* nose
* pytest

It can also contain dependencies for building the documentation, like
sphinx. If you can't find any information about the package's
dependencies, you can take a look in ``requirements.txt``, but be sure
not to add test or documentation dependencies.

""""""""""
setuptools
""""""""""

Setuptools is a bit of a special case. If a package requires setuptools
at run-time, how do they express this? They could add it to
``install_requires``, but setuptools is imported long before this and
needed to read this line. And since you can't install the package
without setuptools, the developers assume that setuptools will already
be there, so they never mention when it is required. We don't want to
add run-time dependencies if they aren't needed, so you need to
determine whether or not setuptools is needed. Grep the installation
directory for any files containing a reference to ``setuptools`` or
``pkg_resources``. Both modules come from ``py-setuptools``.
``pkg_resources`` is particularly common in scripts in ``prefix/bin``.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Passing arguments to setup.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The default build and install phases should be sufficient to install
most packages. However, you may want to pass additional flags to
either phase.

You can view the available options for a particular phase with:

.. code-block:: console

   $ python setup.py <phase> --help


Each phase provides a ``<phase_args>`` function that can be used to
pass arguments to that phase. For example,
`py-numpy <https://github.com/spack/spack/blob/develop/var/spack/repos/builtin/packages/py-numpy/package.py>`_
adds:

.. code-block:: python

   def build_args(self, spec, prefix):
       args = []

       # From NumPy 1.10.0 on it's possible to do a parallel build.
       if self.version >= Version('1.10.0'):
           # But Parallel build in Python 3.5+ is broken.  See:
           # https://github.com/spack/spack/issues/7927
           # https://github.com/scipy/scipy/issues/7112
           if spec['python'].version < Version('3.5'):
               args = ['-j', str(make_jobs)]

       return args


^^^^^^^
Testing
^^^^^^^

``PythonPackage`` provides a couple of options for testing packages.

""""""""""""
Import tests
""""""""""""

Just because a package successfully built does not mean that it built
correctly. The most reliable test of whether or not the package was
correctly installed is to attempt to import all of the modules that
get installed. To get a list of modules, run the following command
in the source directory:

.. code-block:: console

   $ python
   >>> import setuptools
   >>> setuptools.find_packages()
   ['numpy', 'numpy._build_utils', 'numpy.compat', 'numpy.core', 'numpy.distutils', 'numpy.doc', 'numpy.f2py', 'numpy.fft', 'numpy.lib', 'numpy.linalg', 'numpy.ma', 'numpy.matrixlib', 'numpy.polynomial', 'numpy.random', 'numpy.testing', 'numpy.core.code_generators', 'numpy.distutils.command', 'numpy.distutils.fcompiler']


Large, complex packages like ``numpy`` will return a long list of
packages, while other packages like ``six`` will return an empty list.
``py-six`` installs a single ``six.py`` file. In Python packaging lingo,
a "package" is a directory containing files like:

.. code-block:: none

   foo/__init__.py
   foo/bar.py
   foo/baz.py


whereas a "module" is a single Python file. Since ``find_packages``
only returns packages, you'll have to determine the correct module
names yourself. You can now add these packages and modules to the
package like so:

.. code-block:: python

   import_modules = ['six']


When you run ``spack install --test=root py-six``, Spack will attempt
to import the ``six`` module after installation.

These tests most often catch missing dependencies and non-RPATHed
libraries. Make sure not to add modules/packages containing the word
"test", as these likely won't end up in installation directory.

""""""""""
Unit tests
""""""""""

The package you want to install may come with additional unit tests.
By default, Spack runs:

.. code-block:: console

   $ python setup.py test


if it detects that the ``setup.py`` file supports a ``test`` phase.
You can add additional build-time or install-time tests by overriding
``test`` and ``installtest``, respectively. For example, ``py-numpy``
adds:

.. code-block:: python

   def install_test(self):
        with working_dir('..'):
            python('-c', 'import numpy; numpy.test("full", verbose=2)')


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Setup file in a sub-directory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In order to be compatible with package managers like ``pip``, the package
is required to place its ``setup.py`` in the root of the tarball. However,
not every Python package cares about ``pip`` or PyPI. If you are installing
a package that is not hosted on PyPI, you may find that it places its
``setup.py`` in a sub-directory. To handle this, add the directory containing
``setup.py`` to the package like so:

.. code-block:: python

   build_directory = 'source'


^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Alternate names for setup.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As previously mentioned, packages need to call their setup script ``setup.py``
in order to be compatible with package managers like ``pip``. However, some
packages like
`py-meep <https://github.com/spack/spack/blob/develop/var/spack/repos/builtin/packages/py-meep/package.py>`_  and
`py-adios <https://github.com/spack/spack/blob/develop/var/spack/repos/builtin/packages/py-adios/package.py>`_
come with multiple setup scripts, one for a serial build and another for a
parallel build. You can override the default name to use like so:

.. code-block:: python

   def setup_file(self):
       return 'setup-mpi.py' if '+mpi' in self.spec else 'setup.py'


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
PythonPackage vs. packages that use Python
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are many packages that make use of Python, but packages that depend
on Python are not necessarily ``PythonPackages``.

"""""""""""""""""""""""
Choosing a build system
"""""""""""""""""""""""

First of all, you need to select a build system. ``spack create`` usually
does this for you, but if for whatever reason you need to do this manually,
choose ``PythonPackage`` if and only if the package contains a ``setup.py``
file.

"""""""""""""""""""""""
Choosing a package name
"""""""""""""""""""""""

Selecting the appropriate package name is a little more complicated
than choosing the build system. By default, ``spack create`` will
prepend ``py-`` to the beginning of the package name if it detects
that the package uses the ``PythonPackage`` build system. However, there
are occasionally packages that use ``PythonPackage`` that shouldn't
start with ``py-``. For example:

* busco
* easybuild
* httpie
* mercurial
* scons
* snakemake

The thing these packages have in common is that they are command-line
tools that just so happen to be written in Python. Someone who wants
to install ``mercurial`` with Spack isn't going to realize that it is
written in Python, and they certainly aren't going to assume the package
is called ``py-mercurial``. For this reason, we manually renamed the
package to ``mercurial``.

Likewise, there are occasionally packages that don't use the
``PythonPackage`` build system but should still be prepended with ``py-``.
For example:

* py-genders
* py-py2cairo
* py-pygobject
* py-pygtk
* py-pyqt
* py-pyserial
* py-sip
* py-xpyb

These packages are primarily used as Python libraries, not as
command-line tools. You may see C/C++ packages that have optional
Python language-bindings, such as:

* antlr
* cantera
* conduit
* pagmo
* vtk

Don't prepend these kind of packages with ``py-``. When in doubt,
think about how this package will be used. Is it primarily a Python
library that will be imported in other Python scripts? Or is it a
command-line tool, or C/C++/Fortran program with optional Python
modules? The former should be prepended with ``py-``, while the
latter should not.

""""""""""""""""""""""
extends vs. depends_on
""""""""""""""""""""""

This is very similar to the naming dilemma above, with a slight twist.
As mentioned in the :ref:`Packaging Guide <packaging_extensions>`,
``extends`` and ``depends_on`` are very similar, but ``extends`` adds
the ability to *activate* the package. Activation involves symlinking
everything in the installation prefix of the package to the installation
prefix of Python. This allows the user to import a Python module without
having to add that module to ``PYTHONPATH``.

When deciding between ``extends`` and ``depends_on``, the best rule of
thumb is to check the installation prefix. If Python libraries are
installed to ``prefix/lib/python2.7/site-packages`` (where 2.7 is the
MAJOR.MINOR version of Python you used to install the package), then
you should use ``extends``. If Python libraries are installed elsewhere
or the only files that get installed reside in ``prefix/bin``, then
don't use ``extends``, as symlinking the package wouldn't be useful.

^^^^^^^^^^^^^^^^^^^^^
Alternatives to Spack
^^^^^^^^^^^^^^^^^^^^^

PyPI has hundreds of thousands of packages that are not yet in Spack,
and ``pip`` may be a perfectly valid alternative to using Spack. The
main advantage of Spack over ``pip`` is its ability to compile
non-Python dependencies. It can also build cythonized versions of a
package or link to an optimized BLAS/LAPACK library like MKL,
resulting in calculations that run orders of magnitude faster.
Spack does not offer a significant advantage to other python-management
systems for installing and using tools like flake8 and sphinx.
But if you need packages with non-Python dependencies like
numpy and scipy, Spack will be very valuable to you.

Anaconda is another great alternative to Spack, and comes with its own
``conda`` package manager. Like Spack, Anaconda is capable of compiling
non-Python dependencies. Anaconda contains many Python packages that
are not yet in Spack, and Spack contains many Python packages that are
not yet in Anaconda. The main advantage of Spack over Anaconda is its
ability to choose a specific compiler and BLAS/LAPACK or MPI library.
Spack also has better platform support for supercomputers. On the
other hand, Anaconda offers Windows support.

^^^^^^^^^^^^^^^^^^^^^^
External documentation
^^^^^^^^^^^^^^^^^^^^^^

For more information on Python packaging, see:
https://packaging.python.org/
