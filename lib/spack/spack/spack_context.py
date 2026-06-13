# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""A coherent bundle of the external resources an operation reads.

Every member except ``config`` is derived from ``config``, so the members cannot drift apart.
Build a context with :meth:`SpackContext.from_config` for an explicit configuration, or with
:meth:`SpackContext.default` to wrap the current process globals.

``default()`` is the migration shim used while Spack is being incrementally de-globalized:
because it reads the same singletons that the not-yet-migrated code reads, migrated and
unmigrated units observe identical data within a single operation (configuration does not mutate
mid-operation).
"""

from typing import NamedTuple

import spack.binary_distribution
import spack.config
import spack.repo
import spack.store
from spack.llnl.util.lang import ensure_unwrapped


class SpackContext(NamedTuple):
    """External resources a single operation reads from."""

    #: Layered configuration driving the operation.
    config: spack.config.Configuration
    #: Installed-spec store, derived from ``config``.
    store: spack.store.Store
    #: Package repositories, derived from ``config``.
    repo: spack.repo.RepoPath
    #: Buildcache index handle. Mutable: lazily fetches remote indices.
    binary_index: spack.binary_distribution.BinaryIndexCache

    @classmethod
    def from_config(cls, config: spack.config.Configuration) -> "SpackContext":
        """Return a context whose store, repo and buildcache index all derive from ``config``."""
        return cls(
            config=config,
            store=spack.store.create(config),
            # create_and_enable() also registers the repo with the import machinery, which the
            # solver relies on to load package classes.
            repo=spack.repo.create_and_enable(config),
            binary_index=spack.binary_distribution.BinaryIndexCache(),
        )

    @classmethod
    def default(cls) -> "SpackContext":
        """Returns a context wrapping the current process globals (the migration shim)."""
        return cls(
            config=ensure_unwrapped(spack.config.CONFIG),
            store=ensure_unwrapped(spack.store.STORE),
            repo=ensure_unwrapped(spack.repo.PATH),
            binary_index=ensure_unwrapped(spack.binary_distribution.BINARY_INDEX),
        )
