.. Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _dags:

====
Dags
====

You can use spack to generate DAGs, or directed acyclic graphs, for usage
with other build systems and workflow managers. Currently, we just have
support for Snakemake, which will produce a ``Snakefile``.

---------
Snakemake
---------

If you aren't familiar with Snakemake, you can learn more about it
`here <https://about.gitlab.com/product/continuous-integration/>`_) 

^^^^^^^^^^^^^^^^^^^^^
Create an environment
^^^^^^^^^^^^^^^^^^^^^

Let's start with a really simple environment - one that has a few biology
relevant stacks.

.. code-block:: yaml

    spack:
        specs:
          - bcftools
          - samtools


We would put this in some directory, let's say "bio" named ``spack.yaml``

.. code-block:: console

    $ ls
    bio/
       spack.yaml


To activate the environment, we might then do:

.. code-block:: console

     $ spack env activate bio
     $ cd bio/


In a normal "let's get this environment working" scenario, we might then do:

.. code-block:: console

     $ spack install
     
But wait - maybe we can do it faster? Let's try using the workflow manager Snakemake
to install the environment. Instead of doing the above command, let's ask spack
to generate us a ``Snakefile``, which is the workflow instructions for Snakemake.
They will be specific to the spack install here, as they have hard coded paths for
the expected final install location.


.. code-block:: console

     $ spack dag generate-snakemake


You'll notice a Snakefile appear in the present working directory, the "bio" folder.

.. code-block:: console

    $ ls
    Snakefile  spack.lock  spack.yaml

Next, we are assuming that you have `snakemake installed <https://snakemake.readthedocs.io/en/stable/getting_started/installation.html>`_
You can run snakemake in the present working directory with some number of cores (N) as.

.. code-block:: console
    
    $ snakemake --cores 4


and this will install the packages in your environment. Snakemake will generate an internal
DAG based on dependencies so nothing should attempt to be installed because it's requirement exists.
This approach assumes a shared filesystem - if we want to be able to have isolated installs, we will
need to add some shared build cache.
