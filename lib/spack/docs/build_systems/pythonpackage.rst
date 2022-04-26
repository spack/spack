.. Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _pythonpackage:

-------------
PythonPackage
-------------

Python packages and modules have their own special build system. This
documentation covers everything you'll need to know in order to write
a Spack build recipe for a Python library.

^^^^^^^^^^^
Terminology
^^^^^^^^^^^

In the Python ecosystem, there are a number of terms that are
important to understand.

**PyPI**
   The `Python Package Index <https://pypi.org/>`_, where most Python
   libraries are hosted.

**sdist**
   Source distributions, distributed as tarballs (.tar.gz) and zip
   files (.zip). Contain the source code of the package.

**bdist**
   Built distributions, distributed as wheels (.whl). Contain the
   pre-built library.

**wheel**
   A binary distribution format common in the Python ecosystem. This
   file is actually just a zip file containing specific metadata and
   code. See the
   `documentation <https://packaging.python.org/en/latest/specifications/binary-distribution-format/>`_
   for more details.

**build frontend**
   Command-line tools used to build and install wheels. Examples
   include `pip <https://pip.pypa.io/>`_,
   `build <https://pypa-build.readthedocs.io/>`_, and
   `installer <https://installer.readthedocs.io/>`_.

**build backend**
   Libraries used to define how to build a wheel. Examples
   include `setuptools <https://setuptools.pypa.io/>`__,
   `flit <https://flit.readthedocs.io/>`_, and
   `poetry <https://python-poetry.org/>`_.

^^^^^^^^^^^
Downloading
^^^^^^^^^^^

The first step in packaging a Python library is to figure out where
to download it from. The vast majority of Python packages are hosted
on `PyPI <https://pypi.org/>`_, which is
:ref:`preferred over GitHub <pypi-vs-github>` for downloading
packages. Search for the package name on PyPI to find the project
page. The project page is usually located at::

   https://pypi.org/project/<package-name>

On the project page, there is a "Download files" tab containing
download URLs. Whenever possible, we prefer to build Spack packages
from source. If PyPI only has wheels, check to see if the project is
hosted on GitHub and see if GitHub has source distributions. The
project page usually has a "Homepage" and/or "Source code" link for
this. If the project is closed-source, it may only have wheels
available. For example, ``py-azureml-sdk`` is closed-source and can
be downloaded from::

   https://pypi.io/packages/py3/a/azureml_sdk/azureml_sdk-1.11.0-py3-none-any.whl

Once you've found a URL to download the package from, run:

.. code-block:: console

   $ spack create <url>


to create a new package template.

.. _pypi-vs-github:

"""""""""""""""
PyPI vs. GitHub
"""""""""""""""

Many packages are hosted on PyPI, but are developed on GitHub or
another version control system hosting service. The source code can
be downloaded from either location, but PyPI is preferred for the
following reasons:

#. PyPI contains the bare minimum number of files needed to install
   the package.

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

The only reason to use GitHub instead of PyPI is if PyPI only has
wheels or if the PyPI sdist is missing a file needed to build the
package. If this is the case, please add a comment above the ``url``
explaining this.

^^^^
PyPI
^^^^

Since PyPI is so commonly used to host Python libraries, the
``PythonPackage`` base class has a ``pypi`` attribute that can be
set. Once set, ``pypi`` will be used to define the ``homepage``,
``url``, and ``list_url``. For example, the following:

.. code-block:: python

   homepage = 'https://pypi.org/project/setuptools/'
   url      = 'https://pypi.org/packages/source/s/setuptools/setuptools-49.2.0.zip'
   list_url = 'https://pypi.org/simple/setuptools/'


is equivalent to:

.. code-block:: python

   pypi = 'setuptools/setuptools-49.2.0.zip'


If a package has a different homepage listed on PyPI, you can
override it by setting your own ``homepage``.

^^^^^^^^^^^
Description
^^^^^^^^^^^

The top of the PyPI project page contains a short description of the
package. The "Project description" tab may also contain a longer
description of the package. Either of these can be used to populate
the package docstring.

^^^^^^^^^^^^^
Build backend
^^^^^^^^^^^^^

Once you've determined the basic metadata for a package, the next
step is to determine the build backend. ``PythonPackage`` uses
`pip <https://pip.pypa.io/>`_ to install the package, but pip
requires a backend to actually build the package.

To determine the build backend, look for a ``pyproject.toml`` file.
If there is no ``pyproject.toml`` file and only a ``setup.py`` or
``setup.cfg`` file, you can assume that the project uses
:ref:`setuptools`. If there is a ``pyproject.toml`` file, see if it
contains a ``[build-system]`` section. For example:

.. code-block:: toml

   [build-system]
   requires = [
       "setuptools>=42",
       "wheel",
   ]
   build-backend = "setuptools.build_meta"


This section does two things: the ``requires`` key lists build
dependencies of the project, and the ``build-backend`` key defines
the build backend. All of these build dependencies should be added as
dependencies to your package:

.. code-block:: python

   depends_on('py-setuptools@42:', type='build')


Note that ``py-wheel`` is already listed as a build dependency in the
``PythonPackage`` base class, so you don't need to add it unless you
need to specify a specific version requirement or change the
dependency type.

See `PEP 517 <https://www.python.org/dev/peps/pep-0517/>`_ and
`PEP 518 <https://www.python.org/dev/peps/pep-0518/>`_ for more
information on the design of ``pyproject.toml``.

Depending on which build backend a project uses, there are various
places that run-time dependencies can be listed.

"""""""""
distutils
"""""""""

Before the introduction of setuptools and other build backends,
Python packages had to rely on the built-in distutils library.
Distutils is missing many of the features that setuptools and other
build backends offer, and users are encouraged to use setuptools
instead. In fact, distutils was deprecated in Python 3.10 and will be
removed in Python 3.12. Because of this, pip actually replaces all
imports of distutils with setuptools. If a package uses distutils,
you should instead add a build dependency on setuptools. Check for a
``requirements.txt`` file that may list dependencies of the project.

.. _setuptools:

""""""""""
setuptools
""""""""""

If the ``pyproject.toml`` lists ``setuptools.build_meta`` as a
``build-backend``, or if the package has a ``setup.py`` that imports
``setuptools``, or if the package has a ``setup.cfg`` file, then it
uses setuptools to build. Setuptools is a replacement for the
distutils library, and has almost the exact same API. Dependencies
can be listed in the ``setup.py`` or ``setup.cfg`` file. Look for the
following arguments:

* ``python_requires``

  This specifies the version of Python that is required.

* ``setup_requires``

  These packages are usually only needed at build-time, so you can
  add them with ``type='build'``.

* ``install_requires``

  These packages are required for building and installation. You can
  add them with ``type=('build', 'run')``.

* ``extras_require``

  These packages are optional dependencies that enable additional
  functionality. You should add a variant that optionally adds these
  dependencies. This variant should be False by default.

* ``tests_require``

  These are packages that are required to run the unit tests for the
  package. These dependencies can be specified using the
  ``type='test'`` dependency type. However, the PyPI tarballs rarely
  contain unit tests, so there is usually no reason to add these.

See https://setuptools.pypa.io/en/latest/userguide/dependency_management.html
for more information on how setuptools handles dependency management.
See `PEP 440 <https://www.python.org/dev/peps/pep-0440/#version-specifiers>`_
for documentation on version specifiers in setuptools.

""""
flit
""""

There are actually two possible ``build-backend`` for flit, ``flit``
and ``flit_core``. If you see these in the ``pyproject.toml``, add a
build dependency to your package. With flit, all dependencies are
listed directly in the ``pyproject.toml`` file. Older versions of
flit used to store this info in a ``flit.ini`` file, so check for
this too.

Either of these files may contain keys like:

* ``requires-python``

  This specifies the version of Python that is required

* ``dependencies`` or ``requires``

  These packages are required for building and installation. You can
  add them with ``type=('build', 'run')``.

* ``project.optional-dependencies`` or ``requires-extra``

  This section includes keys with lists of optional dependencies
  needed to enable those features. You should add a variant that
  optionally adds these dependencies. This variant should be False
  by default.

See https://flit.readthedocs.io/en/latest/pyproject_toml.html for
more information.

""""""
poetry
""""""

Like flit, poetry also has two possible ``build-backend``, ``poetry``
and ``poetry_core``. If you see these in the ``pyproject.toml``, add
a build dependency to your package. With poetry, all dependencies are
listed directly in the ``pyproject.toml`` file. Dependencies are
listed in a ``[tool.poetry.dependencies]`` section, and use a
`custom syntax <https://python-poetry.org/docs/dependency-specification/#version-constraints>`_
for specifying the version requirements. Note that ``~=`` works
differently in poetry than in setuptools and flit for versions that
start with a zero.

""""""
wheels
""""""

Some Python packages are closed-source and are distributed as Python
wheels. For example, ``py-azureml-sdk`` downloads a ``.whl`` file. This
file is simply a zip file, and can be extracted using:

.. code-block:: console

   $ unzip *.whl


The zip file will not contain a ``setup.py``, but it will contain a
``METADATA`` file which contains all the information you need to
write a ``package.py`` build recipe. Check for lines like::

   Requires-Python: >=3.5,<4
   Requires-Dist: azureml-core (~=1.11.0)
   Requires-Dist: azureml-dataset-runtime[fuse] (~=1.11.0)
   Requires-Dist: azureml-train (~=1.11.0)
   Requires-Dist: azureml-train-automl-client (~=1.11.0)
   Requires-Dist: azureml-pipeline (~=1.11.0)
   Provides-Extra: accel-models
   Requires-Dist: azureml-accel-models (~=1.11.0); extra == 'accel-models'
   Provides-Extra: automl
   Requires-Dist: azureml-train-automl (~=1.11.0); extra == 'automl'


``Requires-Python`` is equivalent to ``python_requires`` and
``Requires-Dist`` is equivalent to ``install_requires``.
``Provides-Extra`` is used to name optional features (variants) and
a ``Requires-Dist`` with ``extra == 'foo'`` will list any
dependencies needed for that feature.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Passing arguments to setup.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The default install phase should be sufficient to install most
packages. However, the installation instructions for a package may
suggest passing certain flags to the ``setup.py`` call. The
``PythonPackage`` class has two techniques for doing this.

""""""""""""""
Global options
""""""""""""""

These flags are added directly after ``setup.py`` when pip runs
``python setup.py install``. For example, the ``py-pyyaml`` package
has an optional dependency on ``libyaml`` that can be enabled like so:

.. code-block:: python

   def global_options(self, spec, prefix):
       options = []
       if '+libyaml' in spec:
           options.append('--with-libyaml')
       else:
           options.append('--without-libyaml')
       return options


"""""""""""""""
Install options
"""""""""""""""

These flags are added directly after ``install`` when pip runs
``python setup.py install``. For example, the ``py-pyyaml`` package
allows you to specify the directories to search for ``libyaml``:

.. code-block:: python

   def install_options(self, spec, prefix):
       options = []
       if '+libyaml' in spec:
           options.extend([
               spec['libyaml'].libs.search_flags,
               spec['libyaml'].headers.include_flags,
           ])
       return options


^^^^^^^
Testing
^^^^^^^

``PythonPackage`` provides a couple of options for testing packages
both during and after the installation process.

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


whereas a "module" is a single Python file.

The ``PythonPackage`` base class automatically detects these package
and module names for you. If, for whatever reason, the module names
detected are wrong, you can provide the names yourself by overriding
``import_modules`` like so:

.. code-block:: python

   import_modules = ['six']


Sometimes the list of module names to import depends on how the
package was built. For example, the ``py-pyyaml`` package has a
``+libyaml`` variant that enables the build of a faster optimized
version of the library. If the user chooses ``~libyaml``, only the
``yaml`` library will be importable. If the user chooses ``+libyaml``,
both the ``yaml`` and ``yaml.cyaml`` libraries will be available.
This can be expressed like so:

.. code-block:: python

   @property
   def import_modules(self):
       modules = ['yaml']
       if '+libyaml' in self.spec:
           modules.append('yaml.cyaml')
       return modules


These tests often catch missing dependencies and non-RPATHed
libraries. Make sure not to add modules/packages containing the word
"test", as these likely won't end up in the installation directory,
or may require test dependencies like pytest to be installed.

Import tests can be run during the installation using ``spack install
--test=root`` or at any time after the installation using
``spack test run``.

""""""""""
Unit tests
""""""""""

The package may have its own unit or regression tests. Spack can
run these tests during the installation by adding test methods after
installation.

For example, ``py-numpy`` adds the following as a check to run
after the ``install`` phase:

.. code-block:: python

   @run_after('install')
   @on_package_attributes(run_tests=True)
   def install_test(self):
       with working_dir('spack-test', create=True):
           python('-c', 'import numpy; numpy.test("full", verbose=2)')


when testing is enabled during the installation (i.e., ``spack install
--test=root``).

.. note::

   Additional information is available on :ref:`install phase tests
   <install_phase-tests>`.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Setup file in a sub-directory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Many C/C++ libraries provide optional Python bindings in a
subdirectory. To tell pip which directory to build from, you can
override the ``build_directory`` attribute. For example, if a package
provides Python bindings in a ``python`` directory, you can use:

.. code-block:: python

   build_directory = 'python'


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
PythonPackage vs. packages that use Python
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are many packages that make use of Python, but packages that depend
on Python are not necessarily ``PythonPackage``'s.

"""""""""""""""""""""""
Choosing a build system
"""""""""""""""""""""""

First of all, you need to select a build system. ``spack create``
usually does this for you, but if for whatever reason you need to do
this manually, choose ``PythonPackage`` if and only if the package
contains one of the following files:

* ``pyproject.toml``
* ``setup.py``
* ``setup.cfg``

"""""""""""""""""""""""
Choosing a package name
"""""""""""""""""""""""

Selecting the appropriate package name is a little more complicated
than choosing the build system. By default, ``spack create`` will
prepend ``py-`` to the beginning of the package name if it detects
that the package uses the ``PythonPackage`` build system. However, there
are occasionally packages that use ``PythonPackage`` that shouldn't
start with ``py-``. For example:

* awscli
* aws-parallelcluster
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
installed to ``<prefix>/lib/pythonX.Y/site-packages``, then you
should use ``extends``. If Python libraries are installed elsewhere
or the only files that get installed reside in ``<prefix>/bin``, then
don't use ``extends``, as symlinking the package wouldn't be useful.

^^^^^^^^^^^^^^^^^^^^^
Alternatives to Spack
^^^^^^^^^^^^^^^^^^^^^

PyPI has hundreds of thousands of packages that are not yet in Spack,
and ``pip`` may be a perfectly valid alternative to using Spack. The
main advantage of Spack over ``pip`` is its ability to compile
non-Python dependencies. It can also build cythonized versions of a
package or link to an optimized BLAS/LAPACK library like MKL,
resulting in calculations that run orders of magnitudes faster.
Spack does not offer a significant advantage over other python-management
systems for installing and using tools like flake8 and sphinx.
But if you need packages with non-Python dependencies like
numpy and scipy, Spack will be very valuable to you.

Anaconda is another great alternative to Spack, and comes with its own
``conda`` package manager. Like Spack, Anaconda is capable of compiling
non-Python dependencies. Anaconda contains many Python packages that
are not yet in Spack, and Spack contains many Python packages that are
not yet in Anaconda. The main advantage of Spack over Anaconda is its
ability to choose a specific compiler and BLAS/LAPACK or MPI library.
Spack also has better platform support for supercomputers, and can build
optimized binaries for your specific microarchitecture.

^^^^^^^^^^^^^^^^^^^^^^
External documentation
^^^^^^^^^^^^^^^^^^^^^^

For more information on Python packaging, see:

* https://packaging.python.org/

For more information on build and installation frontend tools, see:

* pip: https://pip.pypa.io/
* build: https://pypa-build.readthedocs.io/
* installer: https://installer.readthedocs.io/

For more information on build backend tools, see:

* setuptools: https://setuptools.pypa.io/
* flit: https://flit.readthedocs.io/
* poetry: https://python-poetry.org/
