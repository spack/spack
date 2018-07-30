##############################################################################
# Copyright (c) 2017, Los Alamos National Security, LLC
# Produced at the Los Alamos National Laboratory.
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
import glob


class Sw4lite(MakefilePackage):
    """Sw4lite is a bare bone version of SW4 intended for testing
    performance optimizations in a few important numerical kernels of SW4."""

    tags = ['proxy-app', 'ecp-proxy-app']

    homepage = "https://geodynamics.org/cig/software/sw4"
    url      = "https://github.com/geodynamics/sw4lite/archive/v1.0.zip"
    git      = "https://github.com/geodynamics/sw4lite.git"

    version('develop', branch='master')
    version('1.0', '3d911165f4f2ff6d5f9c1bd56ab6723f')

    variant('openmp', default=True, description='Build with OpenMP support')
    variant('precision', default='double', values=('float', 'double'),
            multi=False, description='Floating point precision')
    variant('ckernel', default=False, description='C or Fortran kernel')

    depends_on('blas')
    depends_on('lapack')
    depends_on('mpi')

    parallel = False

    @property
    def build_targets(self):
        targets = []
        spec = self.spec

        if spec.variants['precision'].value == 'double':
            cxxflags = ['-I../src', '-I../src/double']
        else:
            cxxflags = ['-I../src', '-I../src/float']
        cflags = []
        fflags = []

        if '+openmp' in self.spec:
            cflags.append('-DSW4_OPENMP')
            cflags.append(self.compiler.openmp_flag)
            cxxflags.append('-DSW4_OPENMP')
            cxxflags.append(self.compiler.openmp_flag)
            fflags.append(self.compiler.openmp_flag)

        if spec.variants['ckernel'].value is True:
            cxxflags.append('-DSW4_CROUTINES')
            targets.append('ckernel=yes')

        targets.append('FC=' + spec['mpi'].mpifc)
        targets.append('CXX=' + spec['mpi'].mpicxx)

        targets.append('CFLAGS={0}'.format(' '.join(cflags)))
        targets.append('CXXFLAGS={0}'.format(' '.join(cxxflags)))
        targets.append('FFLAGS={0}'.format(' '.join(fflags)))

        targets.append('EXTRA_CXX_FLAGS=')
        targets.append('EXTRA_FORT_FLAGS=')
        lapack_blas = spec['lapack'].libs + spec['blas'].libs
        if spec.satisfies('%gcc'):
            targets.append('EXTRA_LINK_FLAGS={0} -lgfortran'
                           .format(lapack_blas.ld_flags))
        else:
            targets.append('EXTRA_LINK_FLAGS={0}'.format(lapack_blas.ld_flags))

        return targets

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        exe_name = glob.glob('*/sw4lite')[0]
        install(exe_name, prefix.bin)
        install_tree('tests', prefix.tests)
