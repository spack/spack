# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class RPkgdepends(RPackage):
    """Package Dependency Resolution and Downloads.

    Find recursive dependencies of 'R' packages from various sources. Solve the
    dependencies to obtain a consistent set of packages to install. Download
    packages, and install them. It supports packages on 'CRAN', 'Bioconductor'
    and other 'CRAN-like' repositories, 'GitHub', package 'URLs', and local
    package trees and files. It caches metadata and package files via the
    'pkgcache' package, and performs all 'HTTP' requests, downloads, builds and
    installations in parallel. 'pkgdepends' is the workhorse of the 'pak'
    package."""

    cran = "pkgdepends"

    version('0.2.0', sha256='59afdbe0e59663088ba4facac5cd011a0a05b0b9c540103fb8b9f0a673bf4d94')

    depends_on('r-callr@3.3.1:', type=('build', 'run'))
    depends_on('r-cli@2.1.0:', type=('build', 'run'))
    depends_on('r-crayon', type=('build', 'run'))
    depends_on('r-curl', type=('build', 'run'))
    depends_on('r-desc@1.2.0:', type=('build', 'run'))
    depends_on('r-filelock@1.0.2:', type=('build', 'run'))
    depends_on('r-glue', type=('build', 'run'))
    depends_on('r-jsonlite', type=('build', 'run'))
    depends_on('r-lpsolve', type=('build', 'run'))
    depends_on('r-pkgbuild@1.0.2:', type=('build', 'run'))
    depends_on('r-pkgcache@1.3.0:', type=('build', 'run'))
    depends_on('r-prettyunits@1.1.1:', type=('build', 'run'))
    depends_on('r-processx@3.4.2:', type=('build', 'run'))
    depends_on('r-ps', type=('build', 'run'))
    depends_on('r-rematch2', type=('build', 'run'))
    depends_on('r-rprojroot', type=('build', 'run'))
    depends_on('r-r6', type=('build', 'run'))
    depends_on('r-tibble', type=('build', 'run'))
    depends_on('r-withr@2.1.1:', type=('build', 'run'))
    depends_on('r-zip@2.1.0:', type=('build', 'run'))
