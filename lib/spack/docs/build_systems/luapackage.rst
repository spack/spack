.. Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _luapackage:

------------
LuaPackage
------------

LuaPackage is a helper for the common case of Lua packages that provide
a rockspec file.  This is not meant to take a rock archive, but to build
a source archive or repository that provides a rockspec, which should cover
most lua packages. In the case a Lua package builds by Make rather than
luarocks, prefer MakefilePackage.

^^^^^^
Phases
^^^^^^

The ``LuaPackage`` base class comes with the following phases:

#. ``preprocess`` - generate ninja files
#. ``install`` - install the project

By default, these phases run:

.. code-block:: console

   $ # preprocess is a noop by default
   $ luarocks make .


Any of these phases can be overridden in your package as necessary.

^^^^^^^^^^^^^^^
Important files
^^^^^^^^^^^^^^^

Packages that use the Lua/LuaRocks build system can be identified by the
presence of a ``*.rockspec`` file. This file declares things
like build instructions and dependencies.

It is common for the rockspec file to list the lua version required in
a dependency, the LuaPackage class adds appropriate dependencies on a Lua
implementation, but it is a good idea to specify the version required with
a ``depends_on`` statement.  The block normally will be a table definition like
this:

.. code-block:: lua
   dependencies = {
      "lua >= 5.1",
   }

^^^^^^^^^^^^^^^^^^^^^^^^^
Build system dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^

All base dependencies are added by the package, but LuaRocks is run to avoid
downloading extra Lua dependencies during build.  If the package needs Lua
libraries outside the standard set, they should be added as dependencies.

If the package requires LuaJit rather than Lua, a ``depends_on("luajit")``
should be used to ensure a LuaJit distribution is used instead of the Lua
interpreter.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Passing arguments to luarocks make
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you need to pass any arguments to the ``luarocks make`` call, you can
override the ``luarocks_args`` method like so:

.. code-block:: python

    def luarocks_args(self):
        return ['flag1', 'flag2']

One common use of this is to override warnings or flags for newer compilers, as in:

.. code-block:: python

    def luarocks_args(self):
        return ["CFLAGS='-Wno-error=implicit-function-declaration'"]

^^^^^^^^^^^^^^^^^^^^^^
External documentation
^^^^^^^^^^^^^^^^^^^^^^

For more information on the LuaRocks build system, see:
https://luarocks.org/
