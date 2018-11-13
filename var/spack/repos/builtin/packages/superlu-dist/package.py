# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class SuperluDist(CMakePackage):
    """A general purpose library for the direct solution of large, sparse,
    nonsymmetric systems of linear equations on high performance machines."""

    homepage = "http://crd-legacy.lbl.gov/~xiaoye/SuperLU/"
    url      = "https://github.com/xiaoyeli/superlu_dist/archive/v6.0.0.tar.gz"
    git      = "https://github.com/xiaoyeli/superlu_dist.git"

    version('develop', branch='master')
    version('xsdk-0.2.0', tag='xsdk-0.2.0')
    version('6.0.0', 'ff6cdfa0263d595708bbb6d11fb780915d8cfddab438db651e246ea292f37ee4')
    version('5.4.0', '3ac238fe082106a2c4dbaf0c22af1ff1247308ffa8f053de9d78c3ec7dd0d801')
    version('5.3.0', '49ed110bdef1e284a0181d6c7dd1fae3aa110cb45f67c6aa5cb791070304d670')
    version('5.2.2', '65cfb9ace9a81f7affac4ad92b9571badf0f10155b3468531b0fffde3bd8e727')
    version('5.2.1', '67cf3c46cbded4cee68e2a9d601c30ab13b08091c8cdad95b0a8e018b6d5d1f1')
    version('5.1.3', '58e3dfdb4ae6f8e3f6f3d5ee5e851af59b967c4483cdb3b15ccd1dbdf38f44f9')
    version('5.1.2', 'e34865ad6696ee6a6d178b4a01c8e19103a7d241ba9de043603970d63b0ee1e2')
    version('5.1.0', '73f292ab748b590b6dd7469e6986aeb95d279b8b8b3da511c695a396bdbc996c')
    version('5.0.0', '78d1d6460ff16b3f71e4bcd7306397574d54d421249553ccc26567f00a10bfc6')

    variant('int64', default=False, description='Build with 64 bit integers')
    variant('shared', default=True, description='Build shared libraries')

    depends_on('mpi')
    depends_on('blas')
    depends_on('lapack')
    depends_on('parmetis')
    depends_on('metis@5:')

    def cmake_args(self):
        spec = self.spec
        lapack_blas = spec['lapack'].libs + spec['blas'].libs
        args = [
            '-DCMAKE_C_COMPILER=%s' % spec['mpi'].mpicc,
            '-DCMAKE_CXX_COMPILER=%s' % spec['mpi'].mpicxx,
            '-DCMAKE_INSTALL_LIBDIR:STRING=%s' % self.prefix.lib,
            '-DTPL_BLAS_LIBRARIES=%s' % lapack_blas.ld_flags,
            '-DUSE_XSDK_DEFAULTS=YES',
            '-DTPL_PARMETIS_LIBRARIES=%s' % spec['parmetis'].libs.ld_flags +
            ';' + spec['metis'].libs.ld_flags,
            '-DTPL_PARMETIS_INCLUDE_DIRS=%s' % spec['parmetis'].prefix.include
        ]

        if '+int64' in spec:
            args.append('-DXSDK_INDEX_SIZE=64')
        else:
            args.append('-DXSDK_INDEX_SIZE=32')

        if '+shared' in spec:
            args.append('-DBUILD_SHARED_LIBS:BOOL=ON')
        else:
            args.append('-DBUILD_SHARED_LIBS:BOOL=OFF')
        return args

    def flag_handler(self, name, flags):
        flags = list(flags)
        if name == 'cxxflags':
            flags.append(self.compiler.cxx11_flag)
        if name == 'cflags' and '%pgi' not in self.spec:
            flags.append('-std=c99')
        return (None, None, flags)
