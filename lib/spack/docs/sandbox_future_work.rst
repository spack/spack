..
   Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _sandbox-future-work:

Sandbox Future Work
===================

Host package ownership discovery
--------------------------------

Dependency-specific host path patterns in ``sandbox.yaml`` are a temporary way to expose files needed by external packages whose prefix is a shared system prefix such as ``/usr``.
They are read-only, apply only when the concrete build DAG contains a matching external dependency, and avoid granting the entire external prefix.

A future implementation should replace these curated patterns with package-file ownership data from the host distribution package manager.
Initial backends should query ``dpkg`` and RPM databases, with other package managers added over time.
Spack should map an external dependency to its owning host packages and grant only their required files and directories.
Package database data remains untrusted input: paths must be absolute, canonicalized, constrained to the selected package records, and admitted read-only.
Tests should cover missing databases, stale or malformed records, symlinked programs, packages split across multiple host records, and external specs that have no host-package mapping.

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
