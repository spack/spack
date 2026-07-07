..
   Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. meta::
   :description lang=en:
      Learn how to use include directives to modularize your Spack YAML configuration files for better organization and reusability.

.. _include-yaml:

Include Settings (include.yaml)
===============================

Spack allows you to include configuration files through ``include.yaml``, or in the ``include:`` section in an environment.
You can specify includes using local paths, remote paths, and ``git`` URLs.
Included paths become configuration scopes in Spack and can even be used to override built-in scopes.

Local files
~~~~~~~~~~~

You can include a single configuration file or an entire configuration *scope* like this:

.. code-block:: yaml

   include:
   - /path/to/a/required/config.yaml
   - $MY_SPECIAL_CONFIG_FILE
   - path: $HOME/path/to/my/project/packages.yaml
   - path: /path/to/$os/$target/config
     optional: true
   - path: /path/to/os-specific/config-dir
     when: os == "ventura"

Included paths may be absolute, relative (to the configuration file), specified as URLs, or provided in environment variables (e.g., ``$MY_SPECIAL_CONFIG_FILE``).

* ``optional``: Spack will raise an error when an included configuration file does not exist, *unless* it is explicitly made ``optional: true``, like the second path above.
* ``when``: Configuration scopes can also be included *conditionally* with ``when``.
  ``when:`` conditions are evaluated as described for :ref:`Spec List References <spec-list-references>`.


The same conditions and variables in :ref:`Spec List References <spec-list-references>` can be used for conditional activation in the ``when`` clauses.

Remote file URLs
~~~~~~~~~~~~~~~~

Only the ``ftp``, ``http``, and ``https`` protocols (or schemes) are supported for remote file URLs.
Spack-specific, environment, and user path variables can be used.
(See :ref:`config-file-variables` for more information.)

A ``sha256`` is required.
For example, suppose you have a ``/etc/spack/include.yaml`` file that specifies a remote ``config.yaml`` file as follows::

   include:
   - path: https://github.com/path/to/raw/config/config.yaml
     sha256: 26e871804a92cd07bb3d611b31b4156ae93d35b6a6d6e0ef3a67871fcb1d258b

The ``config.yaml`` file is downloaded to a subdirectory of ``/etc/spack``.
The contents of the downloaded file are read and included in Spack's configuration when Spack configuration files are processed.

.. note::

   You can check the destination of the downloaded file by running: ``spack config scopes -p``.

.. warning::

   Remote file URLs must link to the **raw** form of the file's contents (e.g., `GitHub <https://docs.github.com/en/repositories/working-with-files/using-files/viewing-and-understanding-files#viewing-or-copying-the-raw-file-content>`_ or `GitLab <https://docs.gitlab.com/ee/api/repository_files.html#get-raw-file-from-repository>`_).

   If the directory containing the ``include.yaml`` file is not writable when the remote file is downloaded, then the destination will be a temporary directory.


``git`` repository files
~~~~~~~~~~~~~~~~~~~~~~~~

You can also include configuration files from a ``git`` repository.
The ``branch``, ``commit``, or ``tag`` to be checked out is required.
A list of relative paths in which to find the configuration files is also required.
Inclusion of the repository (and its paths) can be optional or conditional.
If you want to control the :ref:`name of the configuration scope <named-config-scopes>`, you can provide a ``name``.

For example, suppose we only want to include the ``config.yaml`` and ``packages.yaml`` files from the `spack/spack-configs <https://github.com/spack/spack-configs>`_ repository's ``USC/config`` directory when using the ``centos7`` operating system.
And we want the configuration scope name to start ``common``.
We could then configure the include in, for example, the user scope include file (i.e., ``$HOME/.spack/include.yaml`` by default), as follows::

   include:
   - name: common
     git: https://github.com/spack/spack-configs.git
     branch: main
     when: os == "centos7"
     paths:
     - USC/config/config.yaml
     - USC/config/packages.yaml

.. note::

   The git URL could be specified through an environment variable (e.g., ``$MY_USC_CONFIG_URL``).

If the condition is satisfied, then the ``main`` branch of the repository will be cloned -- under ``$HOME/.spack/includes`` -- when configuration scopes are initially created.
Once cloned, the settings for the two files under the ``USC/config`` directory will be integrated into Spack's configuration.
In this example, the new scopes and their paths can be seen by running::

   $ spack config scopes -p
   Scope               Path
   command_line
   spack                           /Users/username/spack/etc/spack/
   user                            /Users/username/.spack/
   common:USC/config/config.yaml   /Users/username/.spack/includes/common/USC/config/config.yaml
   common:USC/config/packages.yaml /Users/username/.spack/includes/common/USC/config/packages.yaml
   site                            /Users/username/spack/etc/spack/site/
   system                          /etc/spack/
   defaults                        /Users/username/spack/etc/spack/defaults/
   defaults:darwin                 /Users/username/spack/etc/spack/defaults/darwin/
   defaults:base                   /Users/username/spack/etc/spack/defaults/base/
   _builtin

Since there are two unique paths, each results in a separate configuration scope.
If only the ``USC/config`` directory was listed under ``paths``, then there would be only one configuration scope, named ``USC``, and the configuration settings from all of the configuration files within that directory would be integrated.

.. versionadded:: 1.1
   ``git:``, ``branch:``, ``commit:``, and ``tag:`` attributes.

.. versionadded:: 1.2
   ``name:`` attribute and git environment variable support.

Precedence
~~~~~~~~~~

Using ``include:`` adds the included files as a configuration scope *below* the including file.
This is so that you can override settings from files you include.
If you want one file to take precedence over another, you can put the include with higher precedence earlier in the list:

.. code-block:: yaml

   include:
   - /path/to/higher/precedence/scope/
   - /path/to/middle/precedence/scope/
   - git: https://github.com/org/git-repo-scope
     commit: 95c59784bd02ea248bf905d79d063df38e087b19

``prefer_modify``
^^^^^^^^^^^^^^^^^

When you use commands like ``spack compiler find``, ``spack external find``, ``spack config edit`` or ``spack config add``, they modify the topmost writable scope in the current configuration.
Scopes can tell Spack to prefer to edit their included scopes instead, using ``prefer_modify``:

.. code-block:: yaml

   include:
   - name: "preferred"
     path: /path/to/scope/we/want-to-write
     prefer_modify: true

Now, if the including scope is the highest precedence scope and would otherwise be selected automatically by one of these commands, they will instead prefer to edit ``preferred``.
The including scope can still be modified by using the ``--scope`` argument (e.g., ``spack compiler find --scope NAME``).

.. warning::

   Recursive includes are not currently processed in a breadth-first manner, so the value of a configuration option that is altered by multiple included files may not be what you expect.
   This will be addressed in a future update.

.. versionadded:: 1.1 The ``prefer_modify:`` attribute.

Overriding local paths
~~~~~~~~~~~~~~~~~~~~~~

Optionally, you can enable a local path to be overridden by an environment variable using ``path_override_env_var:``:

.. code-block:: yaml

   include:
   - path_override_env_var: SPECIAL_CONFIG_PATH
     path: /path/to/special/config.yaml

Here, If ``SPECIAL_CONFIG_PATH`` is set, its value will be used as the path.
If not, Spack will instead use the ``path:`` specified in configuration.

.. note::

   ``path_override_env_var:`` is currently only supported for ``path:`` includes, not ``git:`` includes.

.. versionadded:: 1.1
   The ``path_override_env_var:`` attribute.

.. _named-config-scopes:

Named configuration scopes
~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, the included scope names are constructed by appending ``:`` and the included scope's basename to the parent scope name.
For example, Spack's own ``defaults`` scope includes a ``base`` scope and a platform-specific scope::

    $ spack config scopes -p
    Scope            Path
    command_line
    spack            /home/username/spack/etc/spack/
    user             /home/username/.spack/
    site             /home/username/spack/etc/spack/site/
    defaults         /home/username/spack/etc/spack/defaults/
    defaults:darwin  /home/username/spack/etc/spack/defaults/darwin/
    defaults:base    /home/username/spack/etc/spack/defaults/base/
    _builtin

You can see ``defaults`` and the included ``defaults:base`` and ``defaults:darwin`` scopes here.

If you want to define your own name for an included scope, you can supply an optional ``name:`` argument when you include it:

.. code-block:: yaml

   spack:
     include:
     - path: foo
       name: myscope

You can see the ``myscope`` name when we activate this environment::

    > spack -e ./env config scopes -p
    Scope                    Path
    command_line
    env:/home/username/env   /home/username/env/spack.yaml/
    myscope                  /home/username/env/foo/
    spack                    /home/username/spack/etc/spack/
    user                     /home/username/.spack/
    site                     /home/username/spack/etc/spack/site/
    defaults                 /home/username/spack/etc/spack/defaults/
    defaults:darwin          /home/username/spack/etc/spack/defaults/darwin/
    defaults:base            /home/username/spack/etc/spack/defaults/base/
    _builtin

You can now use the argument ``myscope`` to refer to this, for example with ``spack config --scope myscope add ...``.

Built-in configuration scopes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The default ``user``, ``system``, and ``site`` scopes are defined using ``include:`` in ``$spack/etc/spack/include.yaml``:

.. literalinclude:: _spack_root/etc/spack/include.yaml
   :language: yaml

You can see that all three of these scopes are given meaningful names, and all three are ``optional``, i.e., they'll be ignored if their directories do not exist.
The ``user`` and ``system`` scopes can also be disabled by setting ``SPACK_DISABLE_LOCAL_CONFIG``.
Finally, the ``user`` scope can be overridden with a path in ``SPACK_USER_CONFIG_PATH`` if it is set.

Overriding scopes by name
^^^^^^^^^^^^^^^^^^^^^^^^^

Configuration scopes have unique names.
This means that you can use the ``name:`` attribute to *replace* a builtin scope.
If you supply an environment like this:

.. code-block:: yaml

   spack:
     include:
     - path: foo
       name: user

The newly included ``user`` scope will *completely* override the builtin ``user`` scope::

  > spack -e ~/env config scopes -p
  Scope                    Path
  command_line
  env:/home/username/env   /home/username/env/spack.yaml/
  user                     /home/username/env/foo/
  spack                    /home/username/spack/etc/spack/
  site                     /home/username/spack/etc/spack/site/
  defaults                 /home/username/spack/etc/spack/defaults/
  defaults:darwin          /home/username/spack/etc/spack/defaults/darwin/
  defaults:base            /home/username/spack/etc/spack/defaults/base/
  _builtin

.. warning::

   Overriding the ``defaults`` scope can have **very** unexpected consequences and is not advised.

.. versionadded:: 1.1
   The ``name:`` attribute.

Overriding built-in scopes with ``include::``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In some cases, you may want to override *all* of the built-in configuration scopes.
The ``user`` and ``system`` scopes depend on the user and the machine on which Spack is running, and they can end up bringing in unexpected configuration settings in surprising ways.

If you want to eliminate them completely from an environment, you can write:

.. code-block:: yaml

   spack:
     include:: []

This overrides all scopes except the ``defaults`` that Spack needs in order to function.
You can see that ``spack``, ``user``, and ``site`` are overridden::

  > spack -e ~/env config scopes -vp
  Scope                    Type          Status    Path
  command_line             internal      active
  env:/home/username/env   env,path      active    /home/username/env/spack.yaml/
  spack                    path          override  /home/username/spack/etc/spack/
  user                     include,path  override  /home/username/.spack/
  site                     include,path  override  /home/username/spack/etc/spack/site/
  defaults                 path          active    /home/username/spack/etc/spack/defaults/
  defaults:darwin          include,path  active    /home/username/spack/etc/spack/defaults/darwin/
  defaults:base            include,path  active    /home/username/spack/etc/spack/defaults/base/
  _builtin                 internal      active

And if you run ``spack config blame``, the settings from these scopes will no longer show up.
``defaults`` are not overridden as they are needed by Spack to function.
This allows you to create completely isolated environments that do not bring in external settings.

.. versionadded:: 1.1
   ``include::`` with two colons for overriding.
