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


def from_config(config: spack.config.Configuration) -> SpackContext:
    """Return a context whose store, repo and buildcache index all derive from ``config``.

    This takes over the import machinery for the process: ``create_and_enable`` rebinds the
    repository the ``ReposFinder`` on ``sys.meta_path`` searches, and prepends the repository's
    python paths to ``sys.path``. Package class loading is process-wide, so two contexts can
    coexist only if their repositories declare disjoint or identical namespaces.
    """
    misc_cache = spack.caches.misc_cache(config=config)
    return SpackContext(
        config=config,
        store=spack.store.create(config),
        repo=spack.repo.create_and_enable(config, cache=misc_cache),
        binary_index=spack.binary_distribution.BinaryIndexCache(config=config),
        misc_cache=misc_cache,
    )


def default() -> SpackContext:
    """Returns a context wrapping the current process globals (the migration shim).

    The globals are stored as they are, so a field that is still an unconstructed singleton is
    only built when it is read. Callers that never touch the store or the buildcache index do
    not pay for them.
    """
    return SpackContext(
        config=spack.config.CONFIG,
        store=spack.store.STORE,
        repo=spack.repo.PATH,
        binary_index=spack.binary_distribution.BINARY_INDEX,
        misc_cache=spack.caches.MISC_CACHE,
    )
