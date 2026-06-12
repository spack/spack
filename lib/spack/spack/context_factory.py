# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Construction of :py:class:`spack.context.SpackContext` instances."""

import spack.binary_distribution
import spack.caches
import spack.config
import spack.repo
import spack.store
from spack.context import SpackContext
from spack.util.lang import ensure_unwrapped


def from_config(config: spack.config.Configuration) -> SpackContext:
    """Return a context whose store, repo and buildcache index all derive from ``config``."""
    misc_cache = spack.caches.misc_cache(config=config)
    return SpackContext(
        config=config,
        store=spack.store.create(config),
        # create_and_enable() also registers the repo with the import machinery, which the
        # solver relies on to load package classes.
        repo=spack.repo.create_and_enable(config, cache=misc_cache),
        binary_index=spack.binary_distribution.BinaryIndexCache(config=config),
        misc_cache=misc_cache,
    )


def default() -> SpackContext:
    """Returns a context wrapping the current process globals (the migration shim)."""
    return SpackContext(
        config=ensure_unwrapped(spack.config.CONFIG),
        store=ensure_unwrapped(spack.store.STORE),
        repo=ensure_unwrapped(spack.repo.PATH),
        binary_index=ensure_unwrapped(spack.binary_distribution.BINARY_INDEX),
        misc_cache=ensure_unwrapped(spack.caches.MISC_CACHE),
    )
