# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""New installer that will ultimately replace installer.py. It features an event loop, non-blocking
I/O, and a POSIX jobserver to limit concurrency. It also has a more advanced terminal UI. It's
mostly self-contained to avoid interfering with the rest of Spack too much while it's being
developed and tested.

The installer consists of a UI process that manages multiple build processes and handles updates
to the database. It detects or creates a jobserver, and then kicks off an event loop in which it
runs through a build queue, always running at least one build. Concurrent builds run as jobserver
tokens are obtained. This means only one -j flag is needed to control concurrency.

The UI process has two modes: an overview mode where it shows the status of all builds, and a
mode where it follows the logs of a specific build. It listens to keyboard input to switch between
modes.

The build process does an ordinary install, but also spawns a "tee" thread that forwards its build
output to both a log file and the UI process (if the UI process has requested it). This thread also
runs an event loop to listen for control messages from the UI process (to enable/disable echoing
of logs), and for output from the build process.

The parent-side orchestrator :class:`PackageInstaller` lives in :mod:`spack.installer.core`,
the build subprocess in :mod:`spack.installer.build`, the terminal UI in
:mod:`spack.installer.ui`, and the build graph/scheduling in
:mod:`spack.installer.schedule`. Shared low-level primitives are in
:mod:`spack.installer.base`, with platform-specific implementations in
``spack.installer.posix`` and ``spack.installer.windows``."""

from spack.installer.core import PackageInstaller

__all__ = ["PackageInstaller"]
