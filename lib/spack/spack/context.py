# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""A coherent bundle of the external resources an operation reads.

This module imports the configuration, the store, the repositories and the buildcache index at
runtime. Modules that need :py:class:`SpackContext` only in annotations import this one under
``if TYPE_CHECKING:``; a runtime import from any module those four import is an import cycle.
"""

from typing import NamedTuple

import spack.binary_distribution
import spack.caches
import spack.config
import spack.repo
import spack.store
import spack.util.file_cache


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
