.. _environments:

Environments
============

An environment is used to group together a set of specs. This description
can be used to replicate a set of installed packages on other systems.
It can also be used to collect the environment modifications necessary
to expose that subset of packages to a user.

You start by creating the environment:

.. code-block:: console

   $ spack env c1 create

Then you add some specs to it and concretize/install them:

.. code-block:: console

   $ spack env c1 add mpileaks
   $ spack env c1 add python
   $ spack env c1 concretize
   $ spack env c1 install

The environment is stored in a file that can be relocated to another
system. You can install all the packages in the environment with the
same specifications. To use the environment as-is, the destination
system must have the same OS and compiler used on the source system.
The ``spack env relocate`` command can reconcretize the specs in a
copied environment with the OS and architecture of the target system
if it differs.

Once the packages are installed, you can generate a script which
includes all the module files that are needed to expose the packages
in the environment to the user:

.. code-block:: console

   $ spack env c1 loads

Usage 
-----
spack env <environment name> create
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a new environment to group a set of specs.

spack env <environment name> add <spec>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Add ``spec`` to ``environment name``. This does not concretize the spec
and so does not detect whether it is possible to concretize. It does
check whether the spec is properly-formatted.

spack env <environment name> concretize
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Concretize each spec added to the environment with ``spack env add``.
This does not install any concretized specs, but it does update the
saved environment object.

spack env <environment name> loads
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Generate a script which loads modules associated with all link and
run dependencies of packages that have been added to the specified
environment.
