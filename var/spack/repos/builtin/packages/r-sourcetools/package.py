# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RSourcetools(RPackage):
    """Tools for Reading, Tokenizing and Parsing R Code."""

    homepage = "https://cloud.r-project.org/package=sourcetools"
    url      = "https://cloud.r-project.org/src/contrib/sourcetools_0.1.6.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/sourcetools"

    version('0.1.7', sha256='47984406efb3b3face133979ccbae9fefb7360b9a6ca1a1c11473681418ed2ca')
    version('0.1.6', 'c78a816384b168d04af41bd7ff4d909d')
    version('0.1.5', 'b4d7902ffafd9802e8fbff5ce824bb28')

    depends_on('r@3.0.2:', type=('build', 'run'))
