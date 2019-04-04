# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ross(CMakePackage):
    """Rensselaer Optimistic Simulation System"""

    homepage = "http://ross-org.github.io"
    git      = "https://github.com/ROSS-org/ROSS.git"
    url      = "https://github.com/ROSS-org/ROSS/archive/v7.0.0.tar.gz"

    version('develop', branch='master')
    version('7.0.1', sha256='40780dada4ab501d2b8ea229f70b9fea920404431d7a60081ba84dd4a50b2517')
    version('7.0.0', sha256='fd16be2c86d9d71ae64eef67c02933471ab758c8a5b01b04fe358d9228fc581e')
    version('6.0.0', sha256='07ff70518a58503e116bb7386f490e901212798afdd471da1bcd34f78a7e6030')

    depends_on('mpi')
    depends_on('cmake@3.5:', when="@7.0.1:", type='build')

    @when("@:7.0.0")
    def cmake_args(self):
        args = []

        args.append("-DBUILD_SHARED_LIBS=ON")
        args.append("-DARCH=%s" % self.spec.architecture.target)
        args.append("-DCMAKE_C_COMPILER=%s" % self.spec['mpi'].mpicc)
        args.append("-DCMAKE_CXX_COMPILER=%s" % self.spec['mpi'].mpicxx)

        return args
