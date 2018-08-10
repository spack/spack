.. _mesonpackage:

------------
MesonPackage
------------

Much like Autotools and CMake, Meson is a build system.  But it is
meant to be both fast and as user friendly as possible.  GNOME's goal
is to port modules to use the Meson build system.

^^^^^^
Phases
^^^^^^

The ``MesonPackage`` base class comes with the following phases:

#. ``meson`` - generate ninja files
#. ``build`` - build the project
#. ``install`` - install the project

By default, these phases run:

.. code-block:: console

   $ mkdir spack-build
   $ cd spack-build
   $ meson .. --prefix=/path/to/installation/prefix
   $ ninja
   $ ninja test  # optional
   $ ninja install


Any of these phases can be overridden in your package as necessary.
There is also a ``check`` method that looks for a ``test`` target
in the build file. If a ``test`` target exists and the user runs:

.. code-block:: console

   $ spack install --test=root <meson-package>


Spack will run ``ninja test`` after the build phase.

^^^^^^^^^^^^^^^
Important files
^^^^^^^^^^^^^^^

Packages that use the Meson build system can be identified by the
presence of a ``meson.build`` file. This file declares things
like build instructions and dependencies.

^^^^^^^^^^^^^^^^^^^^^^^^^
Build system dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^

At the bare minimum, packages that use the Meson build system need
``meson`` and ```ninja``` dependencies. Since this is always the case,
the ``MesonPackage`` base class already contains:

.. code-block:: python

   depends_on('meson', type='build')
   depends_on('ninja', type='build')

^^^^^^^^^^^^^^^^^^^^^^^^^^
Passing arguments to meson
^^^^^^^^^^^^^^^^^^^^^^^^^^

If you need to pass any arguments to the ``meson`` call, you can
override the ``meson_args`` method like so:

.. code-block:: python

   def meson_args(self):
       return ['--default-library=both']


This method can be used to pass flags as well as variables.

^^^^^^^^^^^^^^^^^^^^^^
External documentation
^^^^^^^^^^^^^^^^^^^^^^

For more information on the Meson build system, see:
https://mesonbuild.com/index.html
