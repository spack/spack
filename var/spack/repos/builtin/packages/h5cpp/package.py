# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class H5cpp(CMakePackage):
    """Easy to use HDF5 C++ templates for Serial and Parallel HDF5"""

    homepage = "http://h5cpp.org"
    url      = "https://github.com/steven-varga/h5cpp/archive/v1.10.4-5.tar.gz"
    git      = "https://github.com/steven-varga/h5cpp.git"

    maintainers = ['eschnett']

    version('master', branch='master')
    version('1.10.4-5', sha256='42d0ca1aaff1ead8998a26d892a51c12b1b89023382f191dc438bd0fa4513455')

    variant('mpi', default=True, description='Include MPI support')

    depends_on('cmake @3.10:', type='build')
    depends_on('hdf5 @1.10.4:')
    depends_on('hdf5 +mpi', when='+mpi')
    depends_on('mpi', when='+mpi')

    def cmake_args(self):
        return ['-DH5CPP_BUILD_TESTS=OFF']
