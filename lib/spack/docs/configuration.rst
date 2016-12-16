.. _configuration:

==============================
Configuration Files in Spack
==============================

Spack has many configuration files.  Here is a quick list of them, in
case you want to skip directly to specific docs:

* :ref:`compilers.yaml <compiler-config>`
* :ref:`config.yaml <config-yaml>`
* :ref:`mirrors.yaml <mirrors>`
* :ref:`modules.yaml <modules>`
* :ref:`packages.yaml <build-settings>`
* :ref:`repos.yaml <repositories>`

-------------------------
YAML Format
-------------------------

Spack configuration files are written in YAML.  We chose YAML because
it's human readable, but also versatile in that it supports dictionaries,
lists, and nested sections. For more details on the format, see `yaml.org
<http://yaml.org>`_ and `libyaml <http://pyyaml.org/wiki/LibYAML>`_.
Here is an example ``config.yaml`` file:

.. code-block:: yaml

   config:
     install_tree: $spack/opt/spack
     module_roots:
       lmod:   $spack/share/spack/lmod
     build_stage:
       - $tempdir
       - /nfs/tmp2/$user

Each spack configuration files is nested under a top-level section
corresponding to its name. So, ``config.yaml`` starts with ``config:``,
and ``mirrors.yaml`` starts with ``mirrors:``, etc.

.. _configuration-scopes:

-------------------------
Configuration Scopes
-------------------------

Spack pulls configuration data from files in several directories. There
are three configuration scopes.  From lowest to highest:

1. **defaults**: Stored in ``$(prefix)/etc/spack/defaults/``. These are
   the "factory" settings. Users should generally not modify the settings
   here, but should override them in other configuration scopes. The
   defaults here will change from version to version of Spack.

2. **site**: Stored in ``$(prefix)/etc/spack/``.  Settings here affect
   only *this instance* of Spack, and they override defaults.  The site
   scope can can be used for per-project settings (one spack instance per
   project) or for site-wide settings on a multi-user machine (e.g., for
   a common spack instance).

3. **user**: Stored in the home directory: ``~/.spack/``. These settings
   affect all instances of Spack and take the highest precedence.

Each configuration directory may contain several configuration files,
such as ``config.yaml``, ``compilers.yaml``, or ``mirrors.yaml``.  When
configurations conflict, settings from higher-precedence scopes override
lower-precedence settings.

Commands that modify scopes (e.g., ``spack compilers``, ``spack repo``,
etc.) take a ``--scope=<name>`` parameter that you can use to control
which scope is modified.  By default they modify the highest-precedence
scope.

.. _platform-scopes:

-------------------------
Platform-specific scopes
-------------------------

For each scope above, there can *also* be platform-specific settings.
For example, on Blue Gene/Q machines, Spack needs to know the location of
cross-compilers for the compute nodes.  This configuration is in
``etc/spack/defaults/bgq/compilers.yaml``.  It will take precedence over
settings in the ``defaults`` scope, but can still be overridden by
settings in ``site``, ``site/bgq``, ``user``, or ``user/bgq``. So, the
full scope precedence is:

1. ``defaults``
2. ``defaults/<platform>``
3. ``site``
4. ``site/<platform>``
5. ``user``
6. ``user/<platform>``

You can get the name to use for ``<platform>`` by running ``spack arch
--platform``.

-------------------------
Scope precedence
-------------------------

When spack queries for configuration parameters, it searches in
higher-precedence scopes first.  So, settings in a higher-precedence file
can override those with the same key in a lower-precedence one.  For
list-valued settings, Spack *prepends* higher-precedence settings to
lower-precedence settings. Completely ignoring higher-level configuration
options is supported with the ``::`` notation for keys (see
:ref:`config-overrides` below).

^^^^^^^^^^^^^^^^^^^^^^^^
Simple keys
^^^^^^^^^^^^^^^^^^^^^^^^

Let's look at an example of overriding a single key in a Spack file.  If
your configurations look like this:

**defaults** scope:

.. code-block:: yaml

   config:
     install_tree: $spack/opt/spack
     module_roots:
       lmod:   $spack/share/spack/lmod
     build_stage:
       - $tempdir
       - /nfs/tmp2/$user

**site** scope:

.. code-block:: yaml

   config:
     install_tree: /some/other/directory

Spack will only override ``install_tree`` in the ``config`` section, and
will take the site preferences for other settings.  You can see the
final, combined configuration with the ``spack config get <configtype>``
command:

.. code-block:: console
   :emphasize-lines: 3

   $ spack config get config
   config:
     install_tree: /some/other/directory
     module_roots:
       lmod:   $spack/share/spack/lmod
     build_stage:
       - $tempdir
       - /nfs/tmp2/$user
   $ _

.. _config-overrides:

^^^^^^^^^^^^^^^^^^^^^^^^^^
Overriding entire sections
^^^^^^^^^^^^^^^^^^^^^^^^^^

Above, the site ``config.yaml`` only overrides specific settings in the
default ``config.yaml``.  Sometimes, it is useful to *completely*
override lower-precedence settings.  To do this, you can use *two* colons
at the end of a key in a configuration file.  For example, if the
**site** ``config.yaml`` above looks like this:

.. code-block:: yaml
   :emphasize-lines: 1

   config::
     install_tree: /some/other/directory

Spack will ignore all lower-precedence configuration under the
``config::`` section:

.. code-block:: console

   $ spack config get config
   config:
     install_tree: /some/other/directory

^^^^^^^^^^^^^^^^^^^^^^
List-valued settings
^^^^^^^^^^^^^^^^^^^^^^

Let's revisit the ``config.yaml`` example one more time.  The
``build_stage`` setting's value is an ordered list of directories:

**defaults**

.. code-block:: yaml

   build_stage:
     - $tempdir
     - /nfs/tmp2/$user

Suppose the user configuration adds its *own* list of ``build_stage``
paths:

**user**

.. code-block:: yaml

   build_stage:
     - /lustre-scratch/$user
     - ~/mystage

Spack will first look at the paths in the site ``config.yaml``, then the
paths in the user's ``~/.spack/config.yaml``.  The list in the
higher-precedence scope is *prepended* to the defaults.  ``spack config
get config`` shows the result:

.. code-block:: console
   :emphasize-lines: 7-10

   $ spack config get config
   config:
     install_tree: /some/other/directory
     module_roots:
       lmod:   $spack/share/spack/lmod
     build_stage:
       - /lustre-scratch/$user
       - ~/mystage
       - $tempdir
       - /nfs/tmp2/$user
   $ _

As in :ref:`config-overrides`, the higher-precedence scope can
*completely* override the lower-precedence scope using `::`.  So if the
user config looked like this:

**user**

.. code-block:: yaml
   :emphasize-lines: 1

   build_stage::
     - /lustre-scratch/$user
     - ~/mystage

The merged configuration would look like this:

.. code-block:: console
   :emphasize-lines: 7-8

   $ spack config get config
   config:
     install_tree: /some/other/directory
     module_roots:
       lmod:   $spack/share/spack/lmod
     build_stage:
       - /lustre-scratch/$user
       - ~/mystage
   $ _
