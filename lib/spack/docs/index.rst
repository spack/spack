.. Spack documentation master file, created by
   sphinx-quickstart on Mon Dec  9 15:32:41 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

===================
Spack Documentation
===================

Spack is a package management tool designed to support multiple
versions and configurations of software on a wide variety of platforms
and environments.  It was designed for large supercomputing centers,
where many users and application teams share common installations of
software on clusters with exotic architectures, using libraries that
do not have a standard ABI.  Spack is non-destructive: installing a
new version does not break existing installations, so many
configurations can coexist on the same system.

Most importantly, Spack is *simple*.  It offers a simple *spec* syntax
so that users can specify versions and configuration options
concisely.  Spack is also simple for package authors: package files
are written in pure Python, and specs allow package authors to
maintain a single file for many different builds of the same package.

See the :doc:`features` for examples and highlights.

Get spack from the `github repository
<https://github.com/llnl/spack>`_ and install your first
package:

.. code-block:: console

   $ git clone https://github.com/llnl/spack.git
   $ cd spack/bin
   $ ./spack install libelf

If you're new to spack and want to start using it, see :doc:`getting_started`,
or refer to the full manual below.


.. toctree::
   :maxdepth: 2
   :caption: Tutorials

   features
   getting_started
   basic_usage
   workflows
   module_file_tutorial

.. toctree::
   :maxdepth: 2
   :caption: Reference Manual

   configuration
   config_yaml
   build_settings
   mirrors
   module_file_support
   package_list
   command_index

.. toctree::
   :maxdepth: 2
   :caption: Contributing to Spack

   contribution_guide
   packaging_guide
   developer_guide
   API Docs <spack>


==================
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
