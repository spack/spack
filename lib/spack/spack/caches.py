##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
"""Caches used by Spack to store data"""
import os
import spack.paths
import spack.config
import spack.fetch_strategy
from spack.util.path import canonicalize_path
from spack.util.file_cache import FileCache


_misc_cache = None
_fetch_cache = None


def misc_cache():
    """The ``misc_cache`` is Spack's cache for small data.

    Currently the ``misc_cache`` stores indexes for virtual dependency
    providers and for which packages provide which tags.
    """
    global _misc_cache

    if _misc_cache is None:
        config = spack.config.get_config('config')
        path = config.get('misc_cache')
        if not path:
            path = os.path.join(spack.paths.user_config_path, 'cache')
        path = canonicalize_path(path)
        _misc_cache = FileCache(path)

    return _misc_cache


def fetch_cache():
    """Filesystem cache of downloaded archives.

    This prevents Spack from repeatedly fetch the same files when
    building the same package different ways or multiple times.
    """
    global _fetch_cache

    if _fetch_cache is None:
        config = spack.config.get_config('config')
        path = config.get('source_cache')
        if not path:
            path = os.path.join(spack.paths.var_path, "cache")
        path = canonicalize_path(path)
        _fetch_cache = spack.fetch_strategy.FsCache(path)

    return _fetch_cache
