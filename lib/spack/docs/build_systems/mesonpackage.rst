.. _mesonpackage:

------------
MesonPackage
------------

Much like Autotools and CMake, Meson is a build-script generator.
In its simplest form, Spack's
``MesonPackage`` runs the following steps:

.. code-block:: console

   $ meson
   $ ninja
   $ ninja check  # optional
   $ ninja install

^^^^^^
Phases
^^^^^^

The ``MesonPackage`` base class comes with the following phases:

#. ``meson`` - generate ninja files
#. ``build`` - build the project
#. ``install`` - install the project

By default, these phases run:

.. code-block:: console

   $ meson
   $ ninja
   $ ninja install


Any of these phases can be overridden in your package as necessary.
There is also a ``check`` method that looks for a ``check`` target
in the build file. If a ``check`` target exists and the user runs:

.. code-block:: console

   $ spack install --test=root <meson-package>


Spack will run ``ninja check`` after the build phase.

^^^^^^^^^^^^^^^
Important files
^^^^^^^^^^^^^^^

Packages that use the Meson build system can be identified by the
presence of a ``meson.build`` file. This file declares things
like build instructions and dependencies.

^^^^^^^^^^^^^^^^^^^^^^^^^
Build system dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^

At the bare minimum, packages that use the Meson build system needs
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
       return ['-recursive']


This method can be used to pass flags as well as variables.

^^^^^^^^^^^^^^^^^^^^^^
External documentation
^^^^^^^^^^^^^^^^^^^^^^

For more information on the Meson build system, see:
http://mesonbuild.com/index.html
