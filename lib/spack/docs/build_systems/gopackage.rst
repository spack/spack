.. Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _gopackage:

-----------
GoPackage
-----------

There are a couple of things to be aware of about applications built
with Go:

* Go-based projects use a variety of build tools: simple invocations
  of ``go build``, custom go "scripts" that leverage ``go run``, Make,
  and *etc...*.

* Go's dependency management story has evolved from an initial
  do-it-yourself attitude through a small number of commonly used
  tools to an officially supported approach (Go "modules").  The Go
  team provides an `introduction to Go modules
  <https://blog.golang.org/using-go-modules>`_ and maintains a site
  that tracks `the gory details
  <https://github.com/golang/go/wiki/Modules>`_.

  Go modules are the future, ``GOPATH`` will likely be deprecated in
  Go 1.14.

Not surprisingly, the best approach to packaging a Go-based project
for Spack depends on the details of the project.

The ``GoPackage`` base class is intended to make it easy to package
simple projects.  Tools & techniques that it uses may also be useful
when using other build system base classes (e.g. ``MakefilePackage``),
in particular:

- Use the package's ``setup_build_environment`` to set
  ``GO111MODULE=on`` to enable module mode and set
  ``GOFLAGS="-mod-vendor"`` to enable vendoring, which prevents ``go``
  from downloading libraries at build time.
- If the application hasn't vendored its dependencies, use
  ``modules2tuple`` to generate "bulk" resource statements and include
  them in the package definition via ``import_resources``.

^^^^^^^^^^^^^^^^^^^^^^^^^^
Simple package definitions
^^^^^^^^^^^^^^^^^^^^^^^^^^

The simplest case is a project that uses a simple invocation of ``go
build`` to compile an executable, *and* uses modules, *and* has
vendored its dependencies.  Here's an example of a package definition
which is only slightly complicated by the fact that it requires a
newer version of Go than ``GoPackage`` provides by default:

.. code-block:: python

    from spack import *


    class Lazygit(GoPackage):
        """Simple terminal UI for git commands."""

        homepage = "https://github.com/jesseduffield/lazygit"
        url      = "https://github.com/jesseduffield/lazygit/archive/v0.11.3.tar.gz"

        version('0.11.3', sha256='b3c503de6b34fd4284fd70655e7f42feafc07f090e7f7cc00db261f56c583c46')

        depends_on('go@1.13:', type='build')  # go.mod value overrides default

        executables = ['lazygit']

While it generally follows the common patterns of a Spack package,
it's worth calling attention to its:

* adding a *build* dependency on the version of the Go package that it
  requires (from the existing `go.mod`);
* using the default ``build`` and ``install`` steps that ``GoPackage``
  provides; and
* providing the name of the executable to be installed by the default
  ``install`` step.

The ``GoPackage`` provides a `setup_build_environment` that sets
`GO111MODULES=on` and `GOFLAGS=-mod=vendor` and its default build step
invokes ``go build``.  Additional arguments to ``go build`` can be
provided by setting ``build_args``, e.g. one could

.. code-block:: python

        build_args = ['-p', '12']  # adjust parallelism of build cmd

to invoke ``go build -p 12``.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Slightly more complicated packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Packages that can be built with a simple invocation of ``go build``,
that use modules, *but have not vendored their dependencies* require a
bit of extra work.  In particular, in order to satisfy Spack's
requirement that nothing is downloaded during the build step, the
package needs to define "resources" that describe from whence to fetch
each dependency, where to emplace it, and the version of the package
to which it applies.  It is possible (likely) that each release of the
project will new set of resources definitions covering the correct
versions.

In the general case, compiling these resource is complicated.

Fortunately, packagers of projects that use modules can use an
automated tool (``modules2tuple``) to provide the resource definitions
and ``import_resources`` to include them without overly-complicating
the package definition.  ``modules2tuple``
(https://github.com/dmgk/modules2tuple) was originally developed by
the FreeBSD Ports team to generate the Makefile fragment their build
system uses to represent a Go application's dependencies.  For the
curious, their Porters Handbook includes more details about `packaging
Go Applications
<https://www.freebsd.org/doc/en_US.ISO8859-1/books/porters-handbook/building.html#using-go>`_
for FreeBSD.

There are three steps to describing the dependencies in the package
definition:

* First, stage the application and use the Go tool chain to
  solve the set of required dependencies and build a vendor directory.

* Second, run the newly created ``vendor/modules.txt`` file through
  ``module2tuples`` to generate a JSON file containing resource
  definitions.

.. code-block:: console

    # in the root directory of the project (where the go.mod file lives)
    $ go mod vendor
    $ modules2tuple -spack -app_version=1.2.3 vendor/modules.txt > resources-1.2.3.json

* Finally, copy that file into the Spack package directory and add an
  `import_resources` statement that refers to it in the package
  definition.

.. code-block:: python

        import_resources("resources-1.2.3.py", when="@1.2.3")

^^^^^^^^^^^^^^^
Advanced topics
^^^^^^^^^^^^^^^

Packaging projects that don't fit into either of the previous two
categories is "left as an exercise for the reader".

More seriously, there are two things to keep in mind:

* the package should use a "run" dependency on go (unless something
  wacky is happening at run time); and

* you'll need to provide ``resource`` definitions for dependencies
  (``modules2tuples`` might be helpful) and ensure that ``go`` does
  not access the network while building (perhaps by invoking it with
  the ``-mod=vendor`` flag).

* ensure that the use of the ``GOFLAGS`` environment variable does not
  conflict with attempts to set arguments on the command line.
