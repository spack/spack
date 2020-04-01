.. Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _sippackage:

----------
SIPPackage
----------

SIP is a tool that makes it very easy to create Python bindings for C and C++
libraries. It was originally developed to create PyQt, the Python bindings for
the Qt toolkit, but can be used to create bindings for any C or C++ library.

SIP comprises a code generator and a Python module. The code generator
processes a set of specification files and generates C or C++ code which is
then compiled to create the bindings extension module. The SIP Python module
provides support functions to the automatically generated code.

^^^^^^
Phases
^^^^^^

The ``SIPPackage`` base class comes with the following phases:

#. ``configure`` - configure the package
#. ``build`` - build the package
#. ``install`` - install the package

By default, these phases run:

.. code-block:: console

   $ python configure.py --bindir ... --destdir ...
   $ make
   $ make install


^^^^^^^^^^^^^^^
Important files
^^^^^^^^^^^^^^^

Each SIP package comes with a custom ``configure.py`` build script,
written in Python. This script contains instructions to build the project.

^^^^^^^^^^^^^^^^^^^^^^^^^
Build system dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^

``SIPPackage`` requires several dependencies. Python is needed to run
the ``configure.py`` build script, and to run the resulting Python
libraries. Qt is needed to provide the ``qmake`` command. SIP is also
needed to build the package. All of these dependencies are automatically
added via the base class

.. code-block:: python

   extends('python')

   depends_on('qt', type='build')

   depends_on('py-sip', type='build')

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Passing arguments to ``configure.py``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Each phase comes with a ``<phase_args>`` function that can be used to pass
arguments to that particular phase. For example, if you need to pass
arguments to the configure phase, you can use:

.. code-block:: python

   def configure_args(self, spec, prefix):
       return ['--no-python-dbus']


A list of valid options can be found by running ``python configure.py --help``.

^^^^^^^
Testing
^^^^^^^

Just because a package successfully built does not mean that it built
correctly. The most reliable test of whether or not the package was
correctly installed is to attempt to import all of the modules that
get installed. To get a list of modules, run the following command
in the site-packages directory:

.. code-block:: console

   $ python
   >>> import setuptools
   >>> setuptools.find_packages()
   ['QtPy5']


Large, complex packages like ``QtPy5`` will return a long list of
packages, while other packages may return an empty list. These packages
only install a single ``foo.py`` file. In Python packaging lingo,
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

   import_modules = ['PyQt5']


When you run ``spack install --test=root py-pyqt5``, Spack will attempt
to import the ``PyQt5`` module after installation.

These tests most often catch missing dependencies and non-RPATHed
libraries.

^^^^^^^^^^^^^^^^^^^^^^
External documentation
^^^^^^^^^^^^^^^^^^^^^^

For more information on the SIP build system, see:

* https://www.riverbankcomputing.com/software/sip/intro
* https://www.riverbankcomputing.com/static/Docs/sip/
* https://wiki.python.org/moin/SIP
