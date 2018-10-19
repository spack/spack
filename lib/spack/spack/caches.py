# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Caches used by Spack to store data"""
import os

import llnl.util.lang

import spack.paths
import spack.config
import spack.fetch_strategy
import spack.util.file_cache
from spack.util.path import canonicalize_path


def _misc_cache():
    """The ``misc_cache`` is Spack's cache for small data.

    Currently the ``misc_cache`` stores indexes for virtual dependency
    providers and for which packages provide which tags.
    """
    path = spack.config.get('config:misc_cache')
    if not path:
        path = os.path.join(spack.paths.user_config_path, 'cache')
    path = canonicalize_path(path)

    return spack.util.file_cache.FileCache(path)


#: Spack's cache for small data
misc_cache = llnl.util.lang.Singleton(_misc_cache)


def _fetch_cache():
    """Filesystem cache of downloaded archives.

    This prevents Spack from repeatedly fetch the same files when
    building the same package different ways or multiple times.
    """
    path = spack.config.get('config:source_cache')
    if not path:
        path = os.path.join(spack.paths.var_path, "cache")
    path = canonicalize_path(path)

    return spack.fetch_strategy.FsCache(path)


#: Spack's local cache for downloaded source archives
fetch_cache = llnl.util.lang.Singleton(_fetch_cache)
