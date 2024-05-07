.. Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)


.. _concretizer-options:

==========================================
Concretization Settings (concretizer.yaml)
==========================================

The ``concretizer.yaml`` configuration file allows to customize aspects of the
algorithm used to select the dependencies you install. The default configuration
is the following:

.. literalinclude:: _spack_root/etc/spack/defaults/concretizer.yaml
   :language: yaml

--------------------------------
Reuse already installed packages
--------------------------------

The ``reuse`` attribute controls how aggressively Spack reuses binary packages during concretization. The
attribute can either be a single value, or an object for more complex configurations.

In the former case ("single value") it allows Spack to:

1. Reuse installed packages and buildcaches for all the specs to be concretized, when ``true``
2. Reuse installed packages and buildcaches only for the dependencies of the root specs, when ``dependencies``
3. Disregard reusing installed packages and buildcaches, when ``false``

In case a finer control over which specs are reused is needed, then the value of this attribute can be
an object, with the following keys:

1. ``roots``: if ``true`` root specs are reused, if ``false`` only dependencies of root specs are reused
2. ``from``: list of sources from which reused specs are taken

Each source in ``from`` is itself an object:

.. list-table:: Attributes for a source or reusable specs
   :header-rows: 1

   * - Attribute name
     - Description
   * - type (mandatory, string)
     - Can be ``local``, ``buildcache``, or ``external``
   * - include (optional, list of specs)
     - If present, reusable specs must match at least one of the constraint in the list
   * - exclude (optional, list of specs)
     - If present, reusable specs must not match any of the constraint in the list.

For instance, the following configuration:

.. code-block:: yaml

   concretizer:
     reuse:
       roots: true
       from:
       - type: local
         include:
         - "%gcc"
         - "%clang"

tells the concretizer to reuse all specs compiled with either ``gcc`` or ``clang``, that are installed
in the local store. Any spec from remote buildcaches is disregarded.

To reduce the boilerplate in configuration files, default values for the ``include`` and
``exclude`` options can be pushed up one level:

.. code-block:: yaml

   concretizer:
     reuse:
       roots: true
       include:
       - "%gcc"
       from:
       - type: local
       - type: buildcache
       - type: local
         include:
         - "foo %oneapi"

In the example above we reuse all specs compiled with ``gcc`` from the local store
and remote buildcaches, and we also reuse ``foo %oneapi``. Note that the last source of
specs override the default ``include`` attribute.

For one-off concretizations, the are command line arguments for each of the simple "single value"
configurations. This means a user can:

.. code-block:: console

   % spack install --reuse <spec>

to enable reuse for a single installation, or:

.. code-block:: console

   spack install --fresh <spec>

to do a fresh install if ``reuse`` is enabled by default.

.. seealso::

   FAQ: :ref:`Why does Spack pick particular versions and variants? <faq-concretizer-precedence>`

------------------------------------------
Selection of the target microarchitectures
------------------------------------------

The options under the ``targets`` attribute control which targets are considered during a solve.
Currently the options in this section are only configurable from the ``concretizer.yaml`` file
and there are no corresponding command line arguments to enable them for a single solve.

The ``granularity`` option can take two possible values: ``microarchitectures`` and ``generic``.
If set to:

.. code-block:: yaml

   concretizer:
     targets:
       granularity: microarchitectures

Spack will consider all the microarchitectures known to ``archspec`` to label nodes for
compatibility. If instead the option is set to:

.. code-block:: yaml

   concretizer:
     targets:
       granularity: generic

Spack will consider only generic microarchitectures. For instance, when running on an
Haswell node, Spack will consider ``haswell`` as the best target in the former case and
``x86_64_v3`` as the best target in the latter case.

The ``host_compatible`` option is a Boolean option that determines whether or not the
microarchitectures considered during the solve are constrained to be compatible with the
host Spack is currently running on. For instance, if this option is set to ``true``, a
user cannot concretize for ``target=icelake`` while running on an Haswell node.

---------------
Duplicate nodes
---------------

The ``duplicates`` attribute controls whether the DAG can contain multiple configurations of
the same package. This is mainly relevant for build dependencies, which may have their version
pinned by some nodes, and thus be required at different versions by different nodes in the same
DAG.

The ``strategy`` option controls how the solver deals with duplicates. If the value is ``none``,
then a single configuration per package is allowed in the DAG. This means, for instance, that only
a single ``cmake`` or a single ``py-setuptools`` version is allowed. The result would be a slightly
faster concretization, at the expense of making a few specs unsolvable.

If the value is ``minimal`` Spack will allow packages tagged as ``build-tools`` to have duplicates.
This allows, for instance, to concretize specs whose nodes require different, and incompatible, ranges
of some build tool. For instance, in the figure below the latest `py-shapely` requires a newer `py-setuptools`,
while `py-numpy` still needs an older version:

.. figure::  images/shapely_duplicates.svg
   :scale: 70 %
   :align: center

Up to Spack v0.20 ``duplicates:strategy:none`` was the default (and only) behavior. From Spack v0.21 the
default behavior is ``duplicates:strategy:minimal``.
