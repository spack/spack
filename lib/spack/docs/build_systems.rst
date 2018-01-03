
.. _build-systems:

=============
Build Systems
=============

This guide provides information specific to a particular
`build system <https://en.wikipedia.org/wiki/List_of_build_automation_software>`_.
It assumes knowledge of general Spack packaging capabilities and expands
on these ideas for each distinct build system that Spack supports:

.. toctree::
   :maxdepth: 1
   :caption: Make-based tools

   build_systems/makefilepackage

.. toctree::
   :maxdepth: 1
   :caption: Build-script generation tools

   build_systems/autotoolspackage
   build_systems/cmakepackage
   build_systems/qmakepackage

.. toctree::
   :maxdepth: 1
   :caption: Language-specific tools

   build_systems/pythonpackage
   build_systems/rpackage
   build_systems/perlpackage
   build_systems/rubypackage
   build_systems/octavepackage

.. toctree::
   :maxdepth: 1
   :caption: Non-Make-based tools

   build_systems/sconspackage
   build_systems/wafpackage

.. toctree::
   :maxdepth: 1
   :caption: Other

   build_systems/intelpackage
   build_systems/custompackage
   build_systems/cudapackage

For reference, the :py:mod:`Build System API docs <spack.build_systems>`
provide a list of build systems and methods/attributes that can be
overridden. If you are curious about the implementation of a particular
build system, you can view the source code by running:

.. code-block:: console

   $ spack edit --build-system autotools


This will open up the ``AutotoolsPackage`` definition in your favorite
editor. In addition, if you are working with a less common build system
like QMake, SCons, or Waf, it may be useful to see examples of other
packages. You can quickly find examples by running:

.. code-block:: console

   $ cd var/spack/repos/builtin/packages
   $ grep -l QMakePackage */package.py


You can then view these packages with ``spack edit``.

This guide is intended to supplement the Build System API docs with
examples of how to override commonly used methods. It also provides
rules of thumb and suggestions for package developers who are unfamiliar
with a particular build system.
