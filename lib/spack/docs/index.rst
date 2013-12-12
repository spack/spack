.. Spack documentation master file, created by
   sphinx-quickstart on Mon Dec  9 15:32:41 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Spack Documentation
=================================

Spack builds and installs software the way you want it.  Other tools
let you install the latest version once.  Spack lets you install the
versions you want, built with the compilers, libraries, and options
you want.  Spack is non-destructive; installing a new version does not
break your old installs.  See the :doc:`features` for more highlights.

Get spack and install your first package:

.. code-block:: sh

   $ git clone ssh://git@cz-stash.llnl.gov:7999/scale/spack.git
   $ cd spack/bin
   $ ./spack install mpich

If you're new to spack and want to start using it, see :doc:`getting_started`,
or refer to the full manual below.

Table of Contents
---------------------

.. toctree::
   :maxdepth: 2

   features
   getting_started
   basic_usage
   packaging_guide
   site_configuration
   developer_guide
   API Docs <spack>

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
