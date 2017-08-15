.. _contexts:

Contexts
============

A context is used to group together a set of specs. This description
can be used to replicate a set of installed packages on other systems.
It can also be used to collect the environment modifications necessary
to expose that subset of packages to a user.

You start by creating the context:

.. code-block:: console

   $ spack context create c1

Then you add some specs to it and concretize/install them:

.. code-block:: console

   $ spack context add c1 mpileaks
   $ spack context add c1 python
   $ spack context concretize c1
   $ spack context install c1

The context is stored in a file that can be relocated to another
system. You can install all the packages in the context with the
same specifications.

Once the packages are installed, you can list all the module files
which are needed to expose the packages in the context to the user:

.. code-block:: console

   $ spack context list-modules c1

Usage 
-----
spack context create <context name>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a new context to group a set of specs.

spack context add <context name> <spec>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Add ``spec`` to ``context name``. This does not concretize the spec
and so does not detect whether it is possible to concretize. It does
check whether the spec is properly-formatted.

spack context concretize <context name>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Concretize each spec added to the context with ``spack context add``.
This does not install any concretized specs, but it does update the
saved context object.

spack context list-modules <context name>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

List the locations of all module files associated with all link and
run dependencies of packages that have been added to the specified
context.
