..
   Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. meta::
   :description lang=en:
      Learn how Spack installs packages: the interactive terminal UI, parallelism
      via a POSIX jobserver, multi-process installs, background execution, and
      handling build failures.

.. _installing:

Installing Packages
===================

This page covers the ``spack install`` experience in detail, including the interactive terminal UI (TUI), parallelism, background execution, and handling build failures.

Before diving in, ensure you are familiar with :doc:`package_fundamentals` for basic usage and spec syntax.

.. versionadded:: 1.2
   The TUI and POSIX jobserver are new in Spack 1.2 and require a Unix-like platform.


Interactive terminal UI
-----------------------

By default, ``spack install`` shows live progress inline in the terminal.
Completed packages scroll into terminal history, while active builds update dynamically below the progress header.

Every package in the install plan is shown with its current status:

.. code-block:: text

   $ spack install -j16 python
   [+] abc1234 zlib@1.3.1 /home/user/spack/opt/spack/... (4s)
   [+] def5678 pkgconf@2.2.0 /home/user/spack/opt/spack/... (6s)
   [+] 9ab0123 ncurses@6.5 /home/user/spack/opt/spack/... (23s)
   Progress: 3/7  +/-: 4 jobs  /: filter  v: logs  n/p: next/prev
   [/] cde4567 readline@8.2 configure (11s)
   [/] fgh8901 openssl@3.4.1 build (18s)

Status indicators:

* ``[+]`` finished successfully
* ``[x]`` failed
* ``[/]``, ``[-]``, ``[\]``, ``[|]`` building (rotating spinner)
* ``[e]`` external

**Log-following mode**: press ``v`` to switch from the overview to a live view of build output.
Press ``v``, ``q``, or ``Esc`` to return to the overview.

While in log-following mode, press ``n`` / ``p`` to cycle to the next or previous build.
Press ``/``, type a pattern, and press ``Enter`` to jump to a matching build (``Esc`` cancels the filter).

When a build fails, press ``v`` to see a parsed error summary and the path to the full log.


Parallelism
-----------

Spack controls parallelism at two levels: the number of build jobs shared across all packages (``-j``), and the number of packages building concurrently (``-p``).

Build-level parallelism (``-j``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``-j`` flag controls the **total** number of concurrent build jobs via a POSIX jobserver.
All build processes (``make``, ``cmake``, ``ninja``, etc.) share the same jobserver, so ``-j16`` means at most 16 build jobs across *all* packages combined.
This is the primary concurrency knob.

.. code-block:: console

   $ spack install -j16 python

Spack creates a POSIX jobserver compatible with GNU Make's jobserver protocol.
Child build systems automatically respect it through ``MAKEFLAGS``, so total CPU usage stays bounded regardless of how many packages are building concurrently.

.. note::

   If an external jobserver is already present in ``MAKEFLAGS``, for example when Spack itself is invoked from inside a larger ``make`` build, Spack attaches to the existing jobserver instead of creating its own.

Package-level parallelism (``-p``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``-p`` / ``--concurrent-packages`` flag limits how many packages can be in the build queue simultaneously.
By default there is no limit, and packages are started as jobserver tokens become available.

.. code-block:: console

   $ spack install -j16 -p4 python

This builds with 16 total make-jobs but never more than 4 packages at once.

Dynamic adjustment
^^^^^^^^^^^^^^^^^^

You can adjust parallelism while a build is running:

* Press ``+`` to add a job (increases ``-j`` by 1)
* Press ``-`` to remove a job (decreases ``-j`` by 1)

When reducing parallelism, Spack waits for currently running jobs to finish before the new limit takes effect; it does not kill active processes.
The progress header shows the adjustment in progress, e.g. ``+/-: 4=>2 jobs``, until the actual count reaches the target.


Multi-process and multi-node installs
--------------------------------------

Multiple ``spack install`` processes can safely run concurrently, whether on the same machine or across multiple nodes in a cluster with a shared filesystem.
Spack coordinates through :ref:`per-prefix filesystem locks <filesystem-requirements>`: before building a package, the process acquires an exclusive lock on its install prefix.
If another process already holds the lock, Spack waits rather than building a second copy.
When a process encounters a prefix that was already installed, it simply skips it and moves on to the next install.

For best results on a cluster, it's recommended to limit per-process package-level parallelism (e.g., ``spack install -p2``) for better load balancing.


Non-interactive mode
--------------------

When the controlling process is not a tty, such as in CI pipelines, when redirecting output to a file, or when running in the background, Spack skips the TUI and prints simple line-based status updates instead.
Use ``spack install -v`` to also print build output.

You can also background builds:

* **Suspend and resume**: press ``Ctrl-Z`` to suspend the install, then ``bg`` to let it continue in the background or ``fg`` to bring it back.
  Child builds are paused while suspended, and resumed when continued in the background or foreground.
  The TUI is suppressed while backgrounded and restored on ``fg``.
* **Start in the background**: run ``spack install ... &`` to skip the TUI entirely and build in the background from the start.

.. tip::

   You don't need a new terminal or SSH session to keep a build running — just suspend it with ``Ctrl-Z`` and ``bg``, then continue working.


Handling failures
-----------------

By default, Spack continues building other packages when one fails (best-effort).
Use ``--fail-fast`` to stop immediately on the first failure.

.. code-block:: console

   $ spack install --fail-fast python

Failed builds show ``[x]`` in the overview.
Navigate to a failed build and press ``v`` to see a parsed error summary and the path to the full log.

See :ref:`spack install <spack-install>` for the full set of flags related to debugging and controlling build behavior.


Build isolation and sandboxing (Linux)
--------------------------------------

Spack can run builds in an unprivileged sandbox to restrict filesystem and network access.
This opt-in feature requires Linux 5.13+ with Landlock support (network restrictions require Linux 6.7+).
Sandboxing is meant for build reproducibility and bug containment rather than acting as a strict security boundary, as package recipes still execute outside the sandbox ahead of the build.

When enabled, the stage directory, install prefix, system temp directory and ``/dev/null`` are implicitly writable.
Spack-installed dependencies (excluding externals) are implicitly readable.
All other paths must be explicitly allowed in configuration:

.. code-block:: yaml

   config:
     sandbox:
       enable: true          # Enable for all builds
       allow_network: false  # Disable TCP network access during the build phase
       allow_read:           # Additional paths with read and execute permissions
       - /usr
       allow_write:          # Additional paths with write and execute permissions
       - /scratch

The sandbox activates immediately after source extraction and prefix creation.
Note that network restrictions only apply during the build phases, leaving Spack's own fetch operations unaffected.

File system restrictions are complementary to existing file permissions and ACLs; they cannot grant access to files the user does not already have permission to read or write.

Spack's sandboxing complements external containerization tools like Podman or Bubblewrap: while a container must grant the main Spack process write access to the entire software store, Landlock dynamically confines each build subprocess strictly to its exact, package-specific install prefix.
