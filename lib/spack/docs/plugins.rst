..
   Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _spack_plugin_system:

Plugins
=======

Plugins are Python packages available in the Python environment running Spack.
They register entry points under ``spack.plugins.<subsystem>`` and are selected under ``config:plugins``.
Installing a plugin does not activate it.

Installer UI Plugins
--------------------

The initial use of plugins is to customize the installer's terminal UI.
The ``spack.plugins.ui`` entry-point group provides installer frontends implementing ``spack.installer.ui.InstallerUI``.
``TerminalUI`` is the built-in default and can be subclassed to customize its behavior.
Other plugin uses may be added in the future.

The streaming UI is a complete example in ``lib/spack/spack/installer/streaming``.
From the Spack checkout, install and enable it in the Python environment running Spack:

.. code-block:: console

   $ python -m pip install ./lib/spack/spack/installer/streaming
   $ spack config add config:plugins:ui:streaming

For plugin development, install it in editable mode instead so changes to the source are available without reinstalling:

.. code-block:: console

   $ python -m pip install -e ./lib/spack/spack/installer/streaming
   $ spack config add config:plugins:ui:streaming

The streaming UI displays the selected build's log while keeping the overview of all builds visible.
When available, it shows build progress percentages after elapsed times and excerpts from build output to the right of the progress information.
With ``spack install -v``, streaming starts automatically.

Installing and Enabling
-----------------------

Install the plugin into the Python environment that runs Spack:

.. code-block:: console

   $ python -m pip install /path/to/my-suite

For plugin development, an editable installation makes source changes available without reinstalling the package:

.. code-block:: console

   $ python -m pip install -e /path/to/my-suite

pip installs dependencies declared by the package.
Select the plugin by its entry-point name, not its Python distribution name:

.. code-block:: yaml

   config:
     plugins:
       ui: suite-ui

Set ``ui`` to ``null`` or ``default``, or leave it unset, to use the built-in UI.

Declaring a Plugin
------------------

The following complete ``pyproject.toml`` registers a UI plugin alongside an ordinary Python dependency:

.. code-block:: toml

   [build-system]
   requires = ["setuptools>=64"]
   build-backend = "setuptools.build_meta"

   [project]
   name = "my-spack-plugin-suite"
   version = "0.1.0"
   dependencies = ["packaging>=20"]

   [project.entry-points."spack.plugins.ui"]
   suite-ui = "suite_ui:setup"

   [tool.setuptools]
   py-modules = ["suite_ui"]

Put the following in ``suite_ui.py``:

.. code-block:: python

   from packaging.version import Version

   from spack.installer.ui import TerminalUI


   class SuiteUI(TerminalUI):
       suite_version = Version("0.1.0")


   def setup():
       if not callable(getattr(TerminalUI, "on_jobs_changed", None)):
           raise RuntimeError("This UI requires TerminalUI.on_jobs_changed")
       return SuiteUI

The distribution owns its entry-point declarations and compatibility checks; Spack has no special cases for plugin names.

Contract and Setup Hooks
------------------------

An entry point may provide a concrete subclass, a compatible preconstructed instance, or a zero-argument setup hook returning either.
The result must implement ``InstallerUI``.
Abstract classes, unrelated objects, missing names, and ambiguous duplicate names are rejected with a warning and the built-in default is used.
Only the selected entry point is loaded.

UI classes receive ``total``, ``verbose``, ``filter_padding``, and ``show_log_on_error`` as constructor keywords.
An explicitly supplied UI object still takes precedence over the configured UI plugin.
When a setup hook returns an instance, the hook owns initialization and the consumer does not pass constructor arguments to it; such instances must already be configured appropriately.

Setup hooks should check the runtime APIs their implementations require and raise an exception when incompatible.
Spack warns and uses the default on discovery, import, setup, interface validation, or plugin-constructor errors.
An error constructing the built-in itself propagates, as do errors in later UI callbacks; fallback is not a rollback mechanism.
``KeyboardInterrupt`` and ``SystemExit`` are not swallowed.
Only install and enable trusted plugins, since entry points execute Python code with Spack's privileges.
These interfaces are experimental, and plugin authors must track their compatibility.
