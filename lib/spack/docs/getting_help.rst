.. Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. meta::
   :description lang=en:
      Find out how to get help with Spack, including using the spack help command.

============
Getting Help
============

.. _cmd-spack-help:

--------------
``spack help``
--------------

If you don't find what you need here, the ``help`` subcommand will
print out a list of *all* of Spack's options and subcommands:

.. command-output:: spack help

Adding an argument, e.g., ``spack help <subcommand>``, will print out
usage information for a particular subcommand:

.. command-output:: spack help install

Alternatively, you can use ``spack --help`` in place of ``spack help``, or
``spack <subcommand> --help`` to get help on a particular subcommand.
