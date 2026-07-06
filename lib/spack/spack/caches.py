# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Caches used by Spack to store data"""

from typing import cast

import spack.config
import spack.fetch_strategy
import spack.paths
import spack.util.file_cache
import spack.util.lang


def misc_cache_location():
    """The ``MISC_CACHE`` is Spack's cache for small data.

    Currently the ``MISC_CACHE`` stores indexes for virtual dependency
    providers and for which packages provide which tags.
    """
    path = spack.config.get("config:misc_cache", spack.paths.default_misc_cache_path)
    return spack.config.canonicalize_path(path)


def _misc_cache():
    path = misc_cache_location()
    return spack.util.file_cache.FileCache(path)


#: Spack's cache for small data
MISC_CACHE = cast(spack.util.file_cache.FileCache, spack.util.lang.Singleton(_misc_cache))


def fetch_cache_location():
    """Filesystem cache of downloaded archives.

    This prevents Spack from repeatedly fetch the same files when
    building the same package different ways or multiple times.
    """
    path = spack.config.get("config:source_cache")
    if not path:
        path = spack.paths.default_fetch_cache_path
    path = spack.config.canonicalize_path(path)
    return path


def _fetch_cache():
    path = fetch_cache_location()
    return spack.fetch_strategy.FsCache(path)


class MirrorCache(spack.fetch_strategy.FsCacheBase):
    def __init__(self, root, skip_unstable_versions):
        super().__init__(root)
        self.skip_unstable_versions = skip_unstable_versions

    def store(self, fetcher, relative_dest):
        """Fetch and relocate the fetcher's target into our mirror cache.

        Note: archives package sources even if not normally cached (e.g. tip of hg/git branch).
        """
        super().store(fetcher, relative_dest)


#: Spack's local cache for downloaded source archives
FETCH_CACHE = cast(spack.fetch_strategy.FsCache, spack.util.lang.Singleton(_fetch_cache))
