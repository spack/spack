# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""A coherent bundle of the external resources an operation reads."""

from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    import spack.binary_distribution
    import spack.config
    import spack.repo
    import spack.store
    import spack.util.file_cache


class SpackContext(NamedTuple):
    """External resources a single operation reads from.

    Annotations are strings and the imports above are guarded, so this module imports no other
    Spack module at runtime. Instances are built by ``spack.context_factory``.
    """

    #: Layered configuration driving the operation.
    config: "spack.config.Configuration"
    #: Installed-spec store, derived from ``config``.
    store: "spack.store.Store"
    #: Package repositories, derived from ``config``.
    repo: "spack.repo.RepoPath"
    #: Buildcache index handle.
    binary_index: "spack.binary_distribution.BinaryIndexCache"
    #: Cache for small data (package indexes, ...), derived from ``config``.
    misc_cache: "spack.util.file_cache.FileCache"
