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


class Exasp2(MakefilePackage):
    """ExaSP2 is a reference implementation of typical linear algebra algorithms
    and workloads for a quantum molecular dynamics (QMD) electronic structure
    code. The algorithm is based on a recursive second-order Fermi-Operator
    expansion method (SP2) and is tailored for density functional based
    tight-binding calculations of material systems. The SP2 algorithm variants
    are part of the Los Alamos Transferable Tight-binding for Energetics
    (LATTE) code, based on a matrix expansion of the Fermi operator in a
    recursive series of generalized matrix-matrix multiplications. It is
    created and maintained by Co-Design Center for Particle Applications
    (CoPA). The code is intended to serve as a vehicle for co-design by
    allowing others to extend and/or reimplement as needed to test performance
    of new architectures, programming models, etc."""

    tags = ['proxy-app']

    homepage = "https://github.com/ECP-copa/ExaSP2"
    url      = "https://github.com/ECP-copa/ExaSP2/tarball/v1.0"
    git      = "https://github.com/ECP-copa/ExaSP2.git"

    version('develop', branch='master')
    version('1.0', 'dba545995acc73f2bd1101bcb377bff5')

    variant('mpi', default=True, description='Build With MPI Support')

    depends_on('bml')
    depends_on('blas')
    depends_on('lapack')
    depends_on('mpi', when='+mpi')
    depends_on('bml@1.2.3:+mpi', when='+mpi')

    build_directory = 'src'

    @property
    def build_targets(self):
        targets = []
        spec = self.spec
        if '+mpi' in spec:
            targets.append('PARALLEL=MPI')
            targets.append('MPICC={0}'.format(spec['mpi'].mpicc))
            targets.append('MPI_LIB=-L' + spec['mpi'].prefix.lib + ' -lmpi')
            targets.append('MPI_INCLUDE=-I' + spec['mpi'].prefix.include)
        else:
            targets.append('PARALLEL=NONE')
        # NOTE: no blas except for mkl has been properly tested. OpenBlas was
        #   briefly but not rigoruously tested. Using generic blas approach to
        #   meet Spack requirements
        targets.append('BLAS=GENERIC_SPACKBLAS')
        math_libs = str(spec['lapack'].libs)
        math_libs += ' ' + str(spec['lapack'].libs)
        targets.append('SPACKBLASLIBFLAGS=' + math_libs)
        math_includes = spec['lapack'].prefix.include
        math_includes += " -I" + spec['blas'].prefix.include
        targets.append('SPACKBLASINCLUDES=' + math_includes)
        # And BML
        bml_lib_dirs = spec['bml'].libs.directories[0]
        targets.append('BML_PATH=' + bml_lib_dirs)
        targets.append('--file=Makefile.vanilla')
        return targets

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        mkdir(prefix.doc)
        for files in glob.glob('bin/ExaSP2-*'):
            install(files, prefix.bin)
        install('LICENSE.md', prefix.doc)
        install('README.md', prefix.doc)
