# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class Flcl(CMakePackage):
    """API for Fortran to C++ and C++ to Fortran multi-dimensional array
    interoperability using Kokkos."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://github.com/kokkos/kokkos-fortran-interop"
    git      = "https://github.com/kokkos/kokkos-fortran-interop.git"
    url      = "https://github.com/kokkos/kokkos-fortran-interop/releases/download/0.2/0.2.tar.gz"

    maintainers = ['womeld']

    version('develop', branch='develop')
    version('spackaging', branch='spackaging')
    version('0.2', sha256='514d97fe91a168245897b2c914ad66454199647cc806bd9fec940206a0f434f7')

    depends_on('kokkos')
    depends_on('cmake@3.17:', type='build')

    def cmake_args(self):
        # FIXME: Add arguments other than
        # FIXME: CMAKE_INSTALL_PREFIX and CMAKE_BUILD_TYPE
        # FIXME: If not needed delete this function
        args = []
        return args
