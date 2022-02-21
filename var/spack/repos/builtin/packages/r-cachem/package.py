# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RCachem(RPackage):
    """Cache R Objects with Automatic Pruning.

    Key-value stores with automatic pruning. Caches can limit either their
    total size or the age of the oldest object (or both), automatically pruning
    objects to maintain the constraints."""

    cran = "cachem"

    version('1.0.6', sha256='9a9452f7bcf3f79436c418b3c3290449fb8fd338714d9b992153754d112f1864')

    depends_on('r-rlang', type=('build', 'run'))
    depends_on('r-fastmap', type=('build', 'run'))
