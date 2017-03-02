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
import glob
import os


class Superlu(Package):
    """SuperLU is a general purpose library for the direct solution of large,
    sparse, nonsymmetric systems of linear equations on high performance
    machines. SuperLU is designed for sequential machines."""

    homepage = "http://crd-legacy.lbl.gov/~xiaoye/SuperLU/#superlu"
    url      = "http://crd-legacy.lbl.gov/~xiaoye/SuperLU/superlu_5.2.1.tar.gz"

    version('5.2.1', '3a1a9bff20cb06b7d97c46d337504447')
    version('4.3', 'b72c6309f25e9660133007b82621ba7c')

    variant('fpic',    default=False,
            description='Build with position independent code') 

    depends_on('cmake', when='@5.2.1:', type='build')
    depends_on('blas')

    # CMake installation method
    def install(self, spec, prefix):
        cmake_args = [
            '-Denable_blaslib=OFF',
            '-DBLAS_blas_LIBRARY={0}'.format(spec['blas'].libs.joined())
        ]

        if '+fpic' in spec:
            cmake_args.extend([
                '-DCMAKE_POSITION_INDEPENDENT_CODE=ON'
            ])

        cmake_args.extend(std_cmake_args)

        with working_dir('spack-build', create=True):
            cmake('..', *cmake_args)
            make()
            make('install')

    # Pre-cmake installation method
    @when('@4.3')
    def install(self, spec, prefix):
        config = []

        # Define make.inc file
        config.extend([
            'PLAT       = _x86_64',
            'SuperLUroot = %s' % self.stage.source_path,
            # 'SUPERLULIB = $(SuperLUroot)/lib/libsuperlu$(PLAT).a',
            'SUPERLULIB = $(SuperLUroot)/lib/libsuperlu_{0}.a' \
            .format(self.spec.version),
            'BLASDEF    = -DUSE_VENDOR_BLAS',
            'BLASLIB    = {0}'.format(spec['blas'].libs.ld_flags),
            # or BLASLIB      = -L/usr/lib64 -lblas
            'TMGLIB     = libtmglib.a',
            'LIBS       = $(SUPERLULIB) $(BLASLIB)',
            'ARCH       = ar',
            'ARCHFLAGS  = cr',
            'RANLIB     = {0}'.format('ranlib' if which('ranlib') else 'echo'),
            'CC         = {0}'.format(os.environ['CC']),
            'FORTRAN    = {0}'.format(os.environ['FC']),
            'LOADER     = {0}'.format(os.environ['CC']),
            'CDEFS      = -DAdd_'
        ])

        if '+fpic' in spec:
            config.extend([
                # Use these lines instead when pic_flag capability arrives
                'CFLAGS     = -O3 {0}'.format(self.compiler.pic_flag),
                'NOOPTS     = {0}'.format(self.compiler.pic_flag),
                'FFLAGS     = -O2 {0}'.format(self.compiler.pic_flag),
                'LOADOPTS   = {0}'.format(self.compiler.pic_flag)
            ])
        else:
            config.extend([
                'CFLAGS     = -O3',
                'NOOPTS     = ',
                'FFLAGS     = -O2',
                'LOADOPTS   = '
            ])

        # Write configuration options to make.inc file
        with open('make.inc', 'w') as inc:
            for option in config:
                inc.write('{0}\n'.format(option))

        make(parallel=False)

        # Install manually
        install_tree('lib', prefix.lib)
        headers = glob.glob(join_path('SRC', '*.h'))
        mkdir(prefix.include)
        for h in headers:
            install(h, prefix.include) 
