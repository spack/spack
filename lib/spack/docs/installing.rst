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
   The TUI and GNU Make jobserver support are new in Spack 1.2.
   Spack supports the POSIX jobserver, Windows jobserver support will be added in a future release.

.. index:: TUI

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

.. index::
   single: jobserver; in spack install
   single: build job; in spack install

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

.. index::
   single: concurrent packages; in spack install

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


.. admonition:: Windows Support

   On Windows, due to a lack of file lock support, concurrent Spack processes are not guaranteed to function.
   On Windows, due to a lack of jobserver support, jobserver orchestration and dynamic adjustment of build parallelism is not supported.

.. index:: non-interactive

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

   You don't need a new terminal or SSH session to keep a build running --- just suspend it with ``Ctrl-Z`` and ``bg``, then continue working.


Handling failures
-----------------

By default, Spack continues building other packages when one fails (best-effort).
Use ``--fail-fast`` to stop immediately on the first failure.

.. code-block:: console

   $ spack install --fail-fast python

Failed builds show ``[x]`` in the overview.
Navigate to a failed build and press ``v`` to see a parsed error summary and the path to the full log.

See :ref:`spack install <spack-install>` for the full set of flags related to debugging and controlling build behavior.


.. index::
   single: sandbox; configuring

Build isolation and sandboxing
--------------------------------------

Spack can run builds in an unprivileged sandbox to restrict filesystem and network access.
Sandboxing is meant for build reproducibility and bug containment rather than acting as a strict security boundary, as package recipes still execute outside the sandbox ahead of the build.

When enabled, the stage directory, install prefix, system temp directory and ``/dev/null`` are implicitly writable.
Spack-installed dependencies (excluding externals) are implicitly readable.
All other paths must be explicitly allowed in configuration:

.. code-block:: yaml

   config:
     sandbox:
       enable: true          # Enable for all builds
       allow_network: false  # Disable network access during the build phase
       allow_read:           # Additional paths with read and execute permissions
       - /usr
       allow_write:          # Additional paths with write and execute permissions
       - /scratch

The sandbox activates immediately after source extraction and prefix creation.
Note that network restrictions only apply during the build phases, leaving Spack's own fetch operations unaffected.

File system restrictions are complementary to existing file permissions and ACLs; they cannot grant access to files the user does not already have permission to read or write.

The underlying isolation mechanism is platform-specific; see below for details.

Linux (Landlock)
^^^^^^^^^^^^^^^^

On Linux, sandboxing uses the Landlock LSM and requires Linux 5.13+ (network restrictions require Linux 6.7+).

Because Landlock lets a running process restrict itself in place, Spack applies the sandbox to
the build process itself just before running the package's build phases: everything from that
point on, including direct Python file I/O performed by the package recipe, is confined by the
kernel.

Spack's sandboxing complements external containerization tools like Podman or Bubblewrap: while a container must grant the main Spack process write access to the entire software store, Landlock dynamically confines each build subprocess strictly to its exact, package-specific install prefix.

Windows (AppContainer)
^^^^^^^^^^^^^^^^^^^^^^^

On Windows, sandboxing uses `AppContainer isolation
<https://learn.microsoft.com/en-us/windows/win32/secauthz/appcontainer-isolation>`_ and requires
Windows 8 / Server 2012 or later.

Unlike Landlock, a Windows AppContainer can only be established when a process is *created*;
there is no supported way to confine an already-running process. Because of this, the Windows
sandbox only confines the external build-tool subprocesses spawned during the build (compilers,
``cmake``, ``make``, MSBuild, etc.); direct Python-level file I/O performed in-process by a
package recipe (e.g. ``shutil.copy``, ``filter_file``, an in-process ``setup.py``) is **not**
confined. This is an intentional, narrower guarantee than on Linux.

Enforcement also works in the opposite direction from Landlock. Landlock removes access from a
process that already has it, whereas an AppContainer starts with essentially nothing and is
granted access one object at a time: a file is reachable only if its ACL names the container's
own SID, one of its capabilities, or the built-in ``ALL APPLICATION PACKAGES`` group. Spack
implements ``allow_read``/``allow_write`` by adding inheritable ACL entries for the container's
SID to each allowed path, and removes them again when the build finishes.

Two consequences follow from that model, and both usually need action:

* **Build tools must be explicitly allowed.** ``C:\Windows`` and ``C:\Windows\System32`` grant
  ``ALL APPLICATION PACKAGES`` read and execute by default, so they keep working, but most
  installed software does not. In particular the MSVC toolchain and Windows SDK under
  ``C:\Program Files (x86)\Microsoft Visual Studio`` and ``C:\Program Files (x86)\Windows Kits``
  are **not** reachable from inside the sandbox unless you add them to ``allow_read``:

  .. code-block:: yaml

     config:
       sandbox:
         enable: true
         allow_read:
         - 'C:\Program Files\Microsoft Visual Studio'
         - 'C:\Program Files (x86)\Windows Kits'

* **Networking is opt-in, not opt-out.** An AppContainer has no network access at all by
  default. ``allow_network: true`` therefore actively grants the ``internetClient``,
  ``internetClientServer`` and ``privateNetworkClientServer`` capabilities (the last is what
  makes a mirror on the local network reachable); ``allow_network: false`` simply grants none of
  them. There is no kernel-version-style gating the way Landlock requires ABI v4+.

Known limitations:

* AppContainer processes cannot reach ``127.0.0.1``/localhost without a separate loopback
  exemption, which Spack does not configure automatically. Builds or tests that rely on
  contacting a local server will fail inside the sandbox, even with ``allow_network: true``.
* Because access is granted by editing real ACLs, allowing a path with a large directory tree
  costs an inheritance propagation pass over that tree, both when the sandbox is applied and
  when it is torn down.
* If a build is hard-killed mid-phase, the AppContainer profile and its granted ACL entries can
  be left behind. This residue is inert (nothing can authenticate as the orphaned SID again) but
  is not automatically reaped. After a clean build the granted entries are removed again; the
  only lasting mark is the ``SE_DACL_AUTO_INHERITED`` control flag, which Windows sets on any
  DACL it rewrites and which conveys no access.
