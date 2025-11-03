..
   Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. meta::
   :description lang=en:
      Learn how to use include directives to modularize your Spack YAML configuration files for better organization and reusability.

.. _include-yaml:

Include Settings (include.yaml)
===============================

Spack allows you to include configuration files through ``include.yaml``.
Using the ``include:`` heading results in pulling in external configuration information to be used by any Spack command.
Paths to configuration files may reside on the local file system, be a URL to a remote file, or be paths associated with a ``git`` repository.

Included configuration files are required *unless* they are explicitly optional or the entry's condition evaluates to ``False``.
Optional includes are specified with the ``optional`` clause and conditional ones with the ``when`` clause.

.. hint::

   The same conditions and variables in :ref:`Spec List References <spec-list-references>` can be used for conditional activation in the ``when`` clauses.

.. warning::

   Recursive includes are not currently processed in a breadth-first manner, so the value of a configuration option that is altered by multiple included files may not be what you expect.
   This will be addressed in a future update.

Local paths
~~~~~~~~~~~

Local configuration files can be specified by path or by their parent directory.
Paths may be absolute, relative (to the configuration file including the path), or specified as URLs.
For example,

.. code-block:: yaml

   include:
   - /path/to/a/required/config.yaml
   - path: /path/to/$os/$target/config
     optional: true
   - path: /path/to/os-specific/config-dir
     when: os == "ventura"

illustrates required, optional, and conditional includes, respectively.
The first entry only provides a local path, ``/path/to/a/required/config.yaml``, meaning that the file is required (so must exist).
Use of ``optional: true`` for ``/path/to/$os/$target/config`` means the path is only included if it exists.
The condition ``os == "ventura"`` in the ``when`` clause for ``/path/to/os-specific/config-dir`` means the path is only included when the operating system (``os``) is ``ventura``.

Remote file URLs
~~~~~~~~~~~~~~~~

Only the ``file``, ``ftp``, ``http``, and ``https`` protocols (or schemes) are supported for remote file URLs.
Spack-specific, environment, and user path variables can be used.
(See :ref:`config-file-variables` for more information.)

A ``sha256`` is required and must be specified as follows:

.. code-block:: yaml

   include:
   - path: https://github.com/path/to/raw/config/config.yaml
     sha256: 26e871804a92cd07bb3d611b31b4156ae93d35b6a6d6e0ef3a67871fcb1d258b

The ``config.yaml`` file would be cached locally to a special include location and its contents included in Spack's configuration.

.. warning::

   Remote file URLs must link to the **raw** form of the file's contents (e.g., `GitHub <https://docs.github.com/en/repositories/working-with-files/using-files/viewing-and-understanding-files#viewing-or-copying-the-raw-file-content>`_ or `GitLab <https://docs.gitlab.com/ee/api/repository_files.html#get-raw-file-from-repository>`_).

``git`` repository files
~~~~~~~~~~~~~~~~~~~~~~~~

You can also include configuration files from a ``git`` repository.
The `branch`, `commit`, or `tag` to be checked out is required.
A list of relative paths in which to find the configuration files is also required.
Inclusion of the repository (and its paths) can be optional or conditional.

For example, suppose we only want to include the ``config.yaml`` and ``packages.yaml`` files from the `spack/spack-configs <https://github.com/spack/spack-configs>`_ repository's ``USC/config`` directory when using the ``centos7`` operating system.
We would then configure the ``include.yaml`` file as follows:

.. code-block:: yaml

   include:
   - git: https://github.com/spack/spack-configs
     branch: main
     when: os == "centos7"
     paths:
     - USC/config/config.yaml
     - USC/config/packages.yaml

If the condition is satisfied, then the ``main`` branch of the repository will be cloned and the settings for the two files integrated into Spack's configuration.
