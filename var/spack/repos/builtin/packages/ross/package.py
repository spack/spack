# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ross(CMakePackage):
    """Rensselaer Optimistic Simulation System"""

    homepage = "http://ross-org.github.io"
    git      = "https://github.com/ROSS-org/ROSS.git"

    version('develop', branch='master')
    version('7.0.0', tag='v7.0.0')

    depends_on('mpi')

    def cmake_args(self):
        if 'x86_64' not in self.spec.architecture:
            raise InstallError(
                'This package currently only builds on x86_64 architectures')

        args = ["-DBUILD_SHARED_LIBS=ON",
                "-DARCH=x86_64",
                "-DCMAKE_C_COMPILER=%s" % self.spec['mpi'].mpicc,
                "-DCMAKE_CXX_COMPILER=%s" % self.spec['mpi'].mpicxx]

        return args
