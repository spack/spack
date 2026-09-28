..
   Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _sandbox-future-work:

Sandbox Future Work
===================

Filesystem-type path selection
------------------------------

The namespace sandbox currently classifies paths from static policy and trusted Spack state.
A future change should also consider the filesystem type of host mounts before preserving their paths.
The default should be an allowlist of filesystem types needed by builds, rather than enumerating individual filesystems that should be excluded.
Mountpoints on unlisted filesystems should remain hidden unless another explicit policy rule requires them.

This filtering must happen before namespace mount plans are compiled.
It should parse the kernel mount table as structured mount data, account for nested mounts, and preserve the existing rule that explicitly writable paths take precedence.
The filesystem type alone must not grant access or make a path writable.

Real-world smoke coverage
-------------------------

Add an installer-level smoke package whose ``install()`` method verifies that ordinary host paths are visible only when selected and cannot be modified.
The test should cover the user's home directory, the Spack source tree and its parent, ``/proc``, ``/sys``, and representative host mountpoints.
It should also verify that the stage, install prefix, worker temporary state, required devices, and explicit ``allow_write`` paths remain writable.

Filesystem-specific cases should exercise whichever non-allowlisted mounts are available on the test host, without requiring a particular one.
Useful Linux examples include ``efivarfs``, ``debugfs`` at ``/sys/kernel/debug``, ``tracefs`` at ``/sys/kernel/tracing``, and ``fusectl`` at ``/sys/fs/fuse/connections``.
Tests must skip unavailable examples and still prove the generic filesystem-type rule with a controlled fixture or mount-namespace setup.

The smoke test should run through ``spack install`` so it covers policy selection, worker setup, namespace activation, and package execution together.
Unit tests should separately cover mount-table parsing, allowlist decisions, nested mounts, and conflicts with explicit read and write policy.
