# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRestfulr(RPackage):
    """R Interface to RESTful Web Services.

    Models a RESTful service as if it were a nested R list."""

    cran = "restfulr"

    version('0.0.13', sha256='7b59f5887aaf02f46a80617f4d1e0ffd4e11e4840e9e2fbd486a9a9c7f2d64b6')

    depends_on('r@3.4.0:', type=('build', 'run'))
    depends_on('r-xml', type=('build', 'run'))
    depends_on('r-rcurl', type=('build', 'run'))
    depends_on('r-rjson', type=('build', 'run'))
    depends_on('r-s4vectors@0.13.15:', type=('build', 'run'))
    depends_on('r-yaml', type=('build', 'run'))
