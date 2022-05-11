# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class RBase64enc(RPackage):
    """Tools for base64 encoding.

    This package provides tools for handling base64 encoding. It is more
    flexible than the orphaned base64 package."""

    cran = "base64enc"

    version('0.1-3', sha256='6d856d8a364bcdc499a0bf38bfd283b7c743d08f0b288174fba7dbf0a04b688d')

    depends_on('r@2.9.0:', type=('build', 'run'))
