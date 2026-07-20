# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""A coherent bundle of the external resources an operation reads."""

from typing import NamedTuple

import spack.binary_distribution
import spack.caches
import spack.config
import spack.repo
import spack.store
import spack.util.file_cache
from spack.util.lang import ensure_unwrapped


class SpackContext(NamedTuple):
    """External resources a single operation reads from."""

    #: Layered configuration driving the operation.
    config: spack.config.Configuration
    #: Installed-spec store, derived from ``config``.
    store: spack.store.Store
    #: Package repositories, derived from ``config``.
    repo: spack.repo.RepoPath
    #: Buildcache index handle.
    binary_index: spack.binary_distribution.BinaryIndexCache
    #: Cache for small data (package indexes, ...), derived from ``config``.
    misc_cache: spack.util.file_cache.FileCache

    @classmethod
    def from_config(cls, config: spack.config.Configuration) -> "SpackContext":
        """Return a context whose store, repo and buildcache index all derive from ``config``."""
        misc_cache = spack.caches.misc_cache(config=config)
        return cls(
            config=config,
            store=spack.store.create(config),
            # create_and_enable() also registers the repo with the import machinery, which the
            # solver relies on to load package classes.
            repo=spack.repo.create_and_enable(config, cache=misc_cache),
            binary_index=spack.binary_distribution.BinaryIndexCache(
                cache_root=spack.binary_distribution.binary_index_location(config=config),
                config=config,
            ),
            misc_cache=misc_cache,
        )

    @classmethod
    def default(cls) -> "SpackContext":
        """Returns a context wrapping the current process globals (the migration shim)."""
        return cls(
            config=ensure_unwrapped(spack.config.CONFIG),
            store=ensure_unwrapped(spack.store.STORE),
            repo=ensure_unwrapped(spack.repo.PATH),
            binary_index=ensure_unwrapped(spack.binary_distribution.BINARY_INDEX),
            misc_cache=ensure_unwrapped(spack.caches.MISC_CACHE),
        )
