# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Arpack(AutotoolsPackage):
    """ARPACK is a collection of Fortran 77 subroutines designed to solve
    large scale eigenvalue problems."""

    homepage = "https://github.com/inducer/arpack"
    url      = "https://github.com/inducer/arpack/archive/v0.92.1.tar.gz"

    version('0.92.1', sha256='c42c02da2c9113b5d27a82b4e9e82a77e25fe70ab1b393e2a78872a3f4a7c4e0')
    version('0.92',   sha256='dbd11c68483858775529d7eb108ef193204787e86cfd9f56611ced5cf33c6816')
    version('0.91',   sha256='f98062f308e0e26726ef1cbb1490a3ceea33f293592875c58b432fe1022579d7')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
