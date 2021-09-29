# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Dataspaces(CMakePackage):
    """DataSpaces v2 based on margo, also called dspaces"""

    homepage = "wwww.dataspaces.org"
    url = ""
    git = "https://github.com/rdi2dspaces/dspaces.git"

    maintainers = ['pradsubedi', 'pdavis']

    version('master', branch='master', submodules=True)

    variant('pybind', default=True, description='build Python bindings')

    depends_on('mpi')
    depends_on('py-numpy', when='+pybind')
    depends_on('swig', when='+pybind')
    depends_on('cmake', type="build")
    depends_on('mochi-margo')
    depends_on('pkgconfig', type="build")
    depends_on('libtool', type="build")

    def cmake_args(self):
        """Populate cmake arguments for Dspaces."""
        extra_args = ['-DCMAKE_C_COMPILER=%s' % self.spec['mpi'].mpicc]
        extra_args.extend(['-DCMAKE_CXX_COMPILER=%s' % self.spec['mpi'].mpicxx])
        extra_args.extend(['-DENABLE_TESTS=ON'])
        return extra_args
