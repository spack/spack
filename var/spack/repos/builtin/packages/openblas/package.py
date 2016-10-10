##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
from spack.package_test import *
import os


class Openblas(Package):
    """OpenBLAS: An optimized BLAS library"""
    homepage = "http://www.openblas.net"
    url = "http://github.com/xianyi/OpenBLAS/archive/v0.2.15.tar.gz"

    version('0.2.19', '28c998054fd377279741c6f0b9ea7941')
    version('0.2.18', '805e7f660877d588ea7e3792cda2ee65')
    version('0.2.17', '664a12807f2a2a7cda4781e3ab2ae0e1')
    version('0.2.16', 'fef46ab92463bdbb1479dcec594ef6dc')
    version('0.2.15', 'b1190f3d3471685f17cfd1ec1d252ac9')

    variant('shared', default=True,
            description="Build shared libraries as well as static libs.")
    variant('openmp', default=False,
            description="Enable OpenMP support.")
    variant('fpic',   default=True,
            description="Build position independent code")

    # virtual dependency
    provides('blas')
    provides('lapack')

    patch('make.patch')

    @property
    def blas_libs(self):
        shared = True if '+shared' in self.spec else False
        return find_libraries(
            ['libopenblas'], root=self.prefix, shared=shared, recurse=True
        )

    @property
    def lapack_libs(self):
        return self.blas_libs

    def install(self, spec, prefix):
        # As of 06/2016 there is no mechanism to specify that packages which
        # depends on Blas/Lapack need C or/and Fortran symbols. For now
        # require both.
        if self.compiler.f77 is None:
            raise InstallError('OpenBLAS requires both C and Fortran ',
                               'compilers!')

        # Configure fails to pick up fortran from FC=/abs/path/to/f77, but
        # works fine with FC=/abs/path/to/gfortran.
        # When mixing compilers make sure that
        # $SPACK_ROOT/lib/spack/env/<compiler> have symlinks with reasonable
        # names and hack them inside lib/spack/spack/compilers/<compiler>.py
        make_defs = ['CC=%s' % spack_cc,
                     'FC=%s' % spack_f77,
                     'MAKE_NO_J=1']

        make_targets = ['libs', 'netlib']

        # Build shared if variant is set.
        if '+shared' in spec:
            make_targets += ['shared']
        else:
            if '+fpic' in spec:
                make_defs.extend(['CFLAGS=-fPIC', 'FFLAGS=-fPIC'])
            make_defs += ['NO_SHARED=1']

        # fix missing _dggsvd_ and _sggsvd_
        if spec.satisfies('@0.2.16'):
            make_defs += ['BUILD_LAPACK_DEPRECATED=1']

        # Add support for OpenMP
        if '+openmp' in spec:
            # Openblas (as of 0.2.18) hardcoded that OpenMP cannot
            # be used with any (!) compiler named clang, bummer.
            if spec.satisfies('%clang'):
                raise InstallError('OpenBLAS does not support ',
                                   'OpenMP with clang!')

            make_defs += ['USE_OPENMP=1']

        make_args = make_defs + make_targets
        make(*make_args)

        make("tests", *make_defs)

        # no quotes around prefix (spack doesn't use a shell)
        make('install', "PREFIX=%s" % prefix, *make_defs)

        # Openblas may pass its own test but still fail to compile Lapack
        # symbols. To make sure we get working Blas and Lapack, do a small
        # test.
        self.check_install(spec)

    def check_install(self, spec):
        source_file = join_path(os.path.dirname(self.module.__file__),
                                'test_cblas_dgemm.c')
        blessed_file = join_path(os.path.dirname(self.module.__file__),
                                 'test_cblas_dgemm.output')

        include_flags = ["-I%s" % join_path(spec.prefix, "include")]
        link_flags = self.lapack_libs.ld_flags.split()
        link_flags.extend(["-lpthread"])
        if '+openmp' in spec:
            link_flags.extend([self.compiler.openmp_flag])

        output = compile_c_and_execute(source_file, include_flags, link_flags)
        compare_output_file(output, blessed_file)
