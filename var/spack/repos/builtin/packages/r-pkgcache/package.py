# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class RPkgcache(RPackage):
    """Cache 'CRAN'-Like Metadata and R Packages.

    Metadata and package cache for CRAN-like repositories. This is a utility
    package to be used by package management tools that want to take advantage
    of caching."""

    cran = "pkgcache"

    version('1.3.0', sha256='bd5f460a3bee9fc1298cf9f747bc59a6b9fbed90e92454bc6ea6bf82c15b9471')

    depends_on('r@3.1:', type=('build', 'run'))
    depends_on('r-assertthat', type=('build', 'run'))
    depends_on('r-callr@2.0.4.9000:', type=('build', 'run'))
    depends_on('r-cli@2.0.0:', type=('build', 'run'))
    depends_on('r-curl@3.2:', type=('build', 'run'))
    depends_on('r-digest', type=('build', 'run'))
    depends_on('r-filelock', type=('build', 'run'))
    depends_on('r-glue', type=('build', 'run'))
    depends_on('r-jsonlite', type=('build', 'run'))
    depends_on('r-prettyunits', type=('build', 'run'))
    depends_on('r-r6', type=('build', 'run'))
    depends_on('r-processx@3.3.0.9001:', type=('build', 'run'))
    depends_on('r-rappdirs', type=('build', 'run'))
    depends_on('r-rlang', type=('build', 'run'))
    depends_on('r-tibble', type=('build', 'run'))
    depends_on('r-uuid', type=('build', 'run'))
