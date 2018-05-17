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
