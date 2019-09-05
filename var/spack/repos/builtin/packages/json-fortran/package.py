# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class JsonFortran(CMakePackage):
    """A Fortran 2008 JSON API"""

    homepage = "http://jacobwilliams.github.io/json-fortran/"
    url      = "https://github.com/jacobwilliams/json-fortran/archive/7.0.0.tar.gz"

    version('7.1.0', sha256='e7aa1f6e09b25ebacb17188147380c3f8c0a254754cd24869c001745fcecc9e6')
    version('7.0.0', sha256='9b5b6235489b27d572bbc7620ed8e039fa9d4d14d41b1581b279be9db499f32c')

    def cmake_args(self):
        return [
            '-DSKIP_DOC_GEN:BOOL=ON',
            '-DUSE_GNU_INSTALL_CONVENTION=ON',
        ]
