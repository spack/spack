# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Mptensor(CMakePackage):
    """mptensor is parallel C++ libarary for tensor calculations.
       It provides similar interfaces as Numpy and Scipy in Python."""

    homepage = "https://github.com/smorita/mptensor"
    url      = "https://github.com/smorita/mptensor/archive/v0.3.0.tar.gz"

    version('0.3.0', sha256='819395a91551bddb77958615042fcb935a4b67ee37f912b9a2ca5b49c71befae')

    variant('mpi', default=False, description='Build with MPI library')
    variant("doc", default=False, description="build documentation with Doxygen")

    depends_on('cmake@3.6:', type='build')
    depends_on('mpi', when="+mpi")
    depends_on('blas')
    depends_on('lapack')
    depends_on('scalapack', when="+mpi")
    depends_on('doxygen@:1.8.11', type="build", when="+doc")

    def cmake_args(self):
        spec = self.spec
        options = []

        if "+mpi" in spec:
            options.extend([
                '-DCMAKE_C_COMPILER=%s'       % spec['mpi'].mpicc,
                '-DCMAKE_CXX_COMPILER=%s'     % spec['mpi'].mpicxx,
                '-DCMAKE_Fortran_COMPILER=%s' % spec['mpi'].mpifc,
                '-DSCALAPACK_LIBRARIES=%s'    % spec['scalapack'].libs,
            ])
        else:
            options.extend([
                '-DCMAKE_C_COMPILER=%s'       % spack_cc,
                '-DCMAKE_CXX_COMPILER=%s'     % spack_cxx,
                '-DCMAKE_Fortran_COMPILER=%s' % spack_fc,
            ])

        blas = spec['blas'].libs
        lapack = spec['lapack'].libs
        options.extend([
            '-DLAPACK_LIBRARIES=%s' % ';'.join(lapack),
            '-DBLAS_LIBRARIES=%s'   % ';'.join(blas),
            self.define_from_variant('ENABLE_MPI', 'mpi'),
            self.define_from_variant('BUILD_DOC', 'doc')
        ])

        return options
