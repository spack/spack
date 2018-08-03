##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class SuiteSparse(Package):
    """
    SuiteSparse is a suite of sparse matrix algorithms
    """
    homepage = 'http://faculty.cse.tamu.edu/davis/suitesparse.html'
    url = 'http://faculty.cse.tamu.edu/davis/SuiteSparse/SuiteSparse-5.2.0.tar.gz'

    version('5.3.0', sha256='90e69713d8c454da5a95a839aea5d97d8d03d00cc1f667c4bdfca03f640f963d')
    version('5.2.0', '8e625539dbeed061cc62fbdfed9be7cf')
    version('5.1.0', '9c34d7c07ad5ce1624b8187faa132046')
    version('4.5.5', '0a5b38af0016f009409a9606d2f1b555')
    version('4.5.4', 'f6ab689442e64a1624a47aa220072d1b')
    version('4.5.3', '8ec57324585df3c6483ad7f556afccbd')
    version('4.5.1', 'f0ea9aad8d2d1ffec66a5b6bfeff5319')

    variant('tbb',  default=False, description='Build with Intel TBB')
    variant('pic',  default=True,  description='Build position independent code (required to link with shared libraries)')
    variant('cuda', default=False, description='Build with CUDA')
    variant('openmp', default=False, description='Build with OpenMP')

    depends_on('blas')
    depends_on('lapack')
    depends_on('cmake', when='@5.2.0:', type='build')

    depends_on('metis@5.1.0', when='@4.5.1:')
    # in @4.5.1. TBB support in SPQR seems to be broken as TBB-related linkng
    # flags does not seem to be used, which leads to linking errors on Linux.
    depends_on('tbb', when='@4.5.3:+tbb')

    depends_on('cuda', when='+cuda')

    patch('tbb_453.patch', when='@4.5.3:+tbb')

    # This patch removes unsupported flags for pgi compiler
    patch('pgi.patch', when='%pgi')

    # This patch adds '-lm' when linking libgraphblas and when using clang.
    # Fixes 'libgraphblas.so.2.0.1: undefined reference to `__fpclassify''
    patch('graphblas_libm_dep.patch', when='@5.2.0:5.2.99%clang')

    def install(self, spec, prefix):
        # The build system of SuiteSparse is quite old-fashioned.
        # It's basically a plain Makefile which include an header
        # (SuiteSparse_config/SuiteSparse_config.mk)with a lot of convoluted
        # logic in it. Any kind of customization will need to go through
        # filtering of that file

        pic_flag  = self.compiler.pic_flag if '+pic' in spec else ''

        make_args = [
            'INSTALL=%s' % prefix,
            # By default, the Makefile uses the Intel compilers if
            # they are found. The AUTOCC flag disables this behavior,
            # forcing it to use Spack's compiler wrappers.
            'AUTOCC=no',
            # CUDA=no does NOT disable cuda, it only disables internal search
            # for CUDA_PATH. If in addition the latter is empty, then CUDA is
            # completely disabled. See
            # [SuiteSparse/SuiteSparse_config/SuiteSparse_config.mk] for more.
            'CUDA=no',
            'CUDA_PATH=%s' % (spec['cuda'].prefix if '+cuda' in spec else ''),
            'CFOPENMP=%s' % (self.compiler.openmp_flag
                             if '+openmp' in spec else ''),
            'CFLAGS=-O3 %s' % pic_flag,
            # Both FFLAGS and F77FLAGS are used in SuiteSparse makefiles;
            # FFLAGS is used in CHOLMOD, F77FLAGS is used in AMD and UMFPACK.
            'FFLAGS=%s' % pic_flag,
            'F77FLAGS=%s' % pic_flag,
            # use Spack's metis in CHOLMOD/Partition module,
            # otherwise internal Metis will be compiled
            'MY_METIS_LIB=%s' % spec['metis'].libs.ld_flags,
            'MY_METIS_INC=%s' % spec['metis'].prefix.include,
            # Make sure Spack's Blas/Lapack is used. Otherwise System's
            # Blas/Lapack might be picked up. Need to add -lstdc++, following
            # with the TCOV path of SparseSuite 4.5.1's Suitesparse_config.mk,
            # even though this fix is ugly
            'BLAS=%s' % (spec['blas'].libs.ld_flags + (
                ' -lstdc++' if '@4.5.1' in spec else '')),
            'LAPACK=%s' % spec['lapack'].libs.ld_flags,
        ]

        # 64bit blas in UMFPACK:
        if (spec.satisfies('^openblas+ilp64') or
            spec.satisfies('^intel-mkl+ilp64') or
            spec.satisfies('^intel-parallel-studio+mkl+ilp64')):
            make_args.append('UMFPACK_CONFIG=-DLONGBLAS="long long"')

        # SuiteSparse defaults to using '-fno-common -fexceptions' in
        # CFLAGS, but not all compilers use the same flags for these
        # optimizations
        if any([x in spec
                for x in ('%clang', '%gcc', '%intel')]):
            make_args += ['CFLAGS+=-fno-common -fexceptions']
        elif '%pgi' in spec:
            make_args += ['CFLAGS+=--exceptions']

        if spack_f77.endswith('xlf') or spack_f77.endswith('xlf_r'):
            make_args += ['CFLAGS+=-DBLAS_NO_UNDERSCORE']

        # Intel TBB in SuiteSparseQR
        if 'tbb' in spec:
            make_args += [
                'SPQR_CONFIG=-DHAVE_TBB',
                'TBB=-L%s -ltbb' % spec['tbb'].prefix.lib,
            ]

        make('install', *make_args)

    @property
    def libs(self):
        """Export the libraries of SuiteSparse.
        Sample usage: spec['suite-sparse'].libs.ld_flags
                      spec['suite-sparse:klu,btf'].libs.ld_flags
        """
        # Component libraries, ordered by dependency. Any missing components?
        all_comps = ['klu', 'btf', 'umfpack', 'cholmod', 'colamd', 'amd',
                     'camd', 'ccolamd', 'cxsparse', 'ldl', 'rbio', 'spqr',
                     'suitesparseconfig']
        query_parameters = self.spec.last_query.extra_parameters
        comps = all_comps if not query_parameters else query_parameters
        libs = find_libraries(['lib' + c for c in comps], root=self.prefix.lib,
                              shared=True, recursive=False)
        if not libs:
            return None
        libs += find_system_libraries('librt')
        return libs
