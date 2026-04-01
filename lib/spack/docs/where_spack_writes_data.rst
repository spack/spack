..
   Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. meta::
   :description lang=en:
      Learn how to control where Spack generates files.

.. _where_spack_writes_data:

Controlling where spack writes data
===================================

A fresh checkout of spack will not write anything into the `$spack`` prefix; instead, all data is placed under the user's home directory.
You can control this in the following ways:

* Redirect everything with environment variables: set ``SPACK_HOME`` and one of ``SPACK_USER_CONFIG_PATH`` or ``SPACK_DISABLE_LOCAL_CONFIG=1``
* Or redirect everything with config:

  * set ``config:locations:home``
  * Update the ``user`` config scope with ``spack config --scope=spack edit include``
* Or redirect installs, environments, and cached downloads (everything that takes up significant space) by setting ``SPACK_DATA_HOME``
* Or use finer-grained configuration settings, for example:

  * ``config:install_tree:root`` to control where installs go
  * ``config:build_stage`` to control where builds are staged

For more on this, see:

* :ref:`Variables controlling data location <config-file-data-variables>`
* :ref:`include.yaml <include-yaml>`
* :ref:`config.yaml <config-yaml>`