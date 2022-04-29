# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class RDebugme(RPackage):
    """Debug R Packages.

    Specify debug messages as special string constants, and control debugging
    of packages via environment variables."""

    cran = "debugme"

    version('1.1.0', sha256='4dae0e2450d6689a6eab560e36f8a7c63853abbab64994028220b8fd4b793ab1')

    depends_on('r-crayon', type=('build', 'run'))
