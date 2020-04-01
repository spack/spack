# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Erfa(AutotoolsPackage):
    """ERFA(Essential Routines for Fundamental Astronomy)
    is a C library containing key algorithms for astronomy."""

    homepage = "https://github.com/liberfa/erfa"
    url      = "https://github.com/liberfa/erfa/archive/v1.4.0.tar.gz"

    version('1.4.0', sha256='90113f18a1a05a3d26970a95b70a71ec52d71156b967ffd6c26dd1626d92e946')

    depends_on('m4', type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
