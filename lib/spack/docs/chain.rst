.. Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. chain:

============================
Chaining Spack Installations
============================

You can point your Spack installation to another installation to use any
packages that are installed there. To register the other Spack instance,
you can add it as an entry to ``config.yaml``:

.. code-block:: yaml

  config:
    upstreams:
      spack-instance-1:
        install_tree: /path/to/other/spack/opt/spack
      spack-instance-2:
        install_tree: /path/to/another/spack/opt/spack

``install_tree`` must point to the ``opt/spack`` directory inside of the
Spack base directory.

This other instance of Spack has no knowledge of the local Spack instance
and may not have the same permissions or ownership as the local Spack instance.
This has the following consequences:

#. Upstream Spack instances are not locked. Therefore it is up to users to
   make sure that the local instance is not using an upstream instance when it
   is being modified.

#. Users should not uninstall packages from the upstream instance. Since the
   upstream instance doesn't know about the local instance, it cannot prevent
   the installation of packages which the local instance depends on.

---------------------------------------
Using Multiple Upstream Spack Instances
---------------------------------------

You can list multiple other Spack instances. Spack will search upstream
instances in the order you list them in your configuration If your installation
refers to instances X and Y, in that order, then instance X must list Y as an
upstream in its own ``config.yaml``

-------------------------------------------
Using Modules from Upstream Spack Instances
-------------------------------------------

There are two requirements to use the modules created by an upstream Spack
instance: firstly the upstream instance must do a ``spack module tcl refresh``,
which generates an index file that maps installed packages to their modules;
secondly, the local Spack instance must add a ``modules`` entry to the
configuration:

.. code-block:: yaml

  config:
    upstreams:
      spack-instance-1:
        install_tree: /path/to/other/spack/opt/spack
        modules:
          tcl: /path/to/other/spack/share/spack/modules

Each time new packages are installed in the upstream Spack instance, the
upstream Spack maintainer should run ``spack module tcl refresh`` (or the
corresponding command for the type of module they intend to use)

.. note::

   Spack can generate modules that :ref:`automatically load
   <autoloading-dependencies>` the modules of dependency packages. Spack cannot
   currently do this for modules in upstream packages.
