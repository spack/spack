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

import inspect
import os.path
import shutil

from spack import *


class Pexsi(Package):
    """The PEXSI library is written in C++, and uses message passing interface
    (MPI) to parallelize the computation on distributed memory computing
    systems and achieve scalability on more than 10,000 processors.

    The Pole EXpansion and Selected Inversion (PEXSI) method is a fast
    method for electronic structure calculation based on Kohn-Sham density
    functional theory. It efficiently evaluates certain selected elements
    of matrix functions, e.g., the Fermi-Dirac function of the KS Hamiltonian,
    which yields a density matrix. It can be used as an alternative to
    diagonalization methods for obtaining the density, energy and forces
    in electronic structure calculations.
    """
    homepage = 'https://math.berkeley.edu/~linlin/pexsi/index.html'
    url = 'https://math.berkeley.edu/~linlin/pexsi/download/pexsi_v0.9.0.tar.gz'

    version('0.9.0', '0c1a2de891ba1445dfc184b2fa270ed8')

    depends_on('parmetis')
    depends_on('superlu-dist@3.3', when='@0.9.0')

    parallel = False

    def install(self, spec, prefix):

        substitutions = {
            '@MPICC': self.spec['mpi'].mpicc,
            '@MPICXX': self.spec['mpi'].mpicxx,
            '@MPIFC': self.spec['mpi'].mpifc,
            '@MPICXX_LIB': self.spec['mpi:cxx'].libs.joined(),
            '@RANLIB': 'ranlib',
            '@PEXSI_STAGE': self.stage.source_path,
            '@SUPERLU_PREFIX': self.spec['superlu-dist'].prefix,
            '@METIS_PREFIX': self.spec['metis'].prefix,
            '@PARMETIS_PREFIX': self.spec['parmetis'].prefix,
            '@LAPACK_PREFIX': self.spec['lapack'].prefix,
            '@BLAS_PREFIX': self.spec['blas'].prefix,
            '@LAPACK_LIBS': self.spec['lapack'].libs.joined(),
            '@BLAS_LIBS': self.spec['blas'].libs.joined(),
            # FIXME : what to do with compiler provided libraries ?
            '@STDCXX_LIB': ' '.join(self.compiler.stdcxx_libs)
        }

        template = join_path(
            os.path.dirname(inspect.getmodule(self).__file__),
            'make.inc'
        )
        makefile = join_path(
            self.stage.source_path,
            'make.inc'
        )
        shutil.copy(template, makefile)
        for key, value in substitutions.items():
            filter_file(key, value, makefile)

        make()
        # 'make install' does not exist, despite what documentation says
        mkdirp(self.prefix.lib)
        install(
            join_path(self.stage.source_path, 'src', 'libpexsi_linux.a'),
            join_path(self.prefix.lib, 'libpexsi.a')
        )
        install_tree(
            join_path(self.stage.source_path, 'include'),
            self.prefix.include
        )
        # fortran "interface"
        make('-C', 'fortran')
        install_tree(
            join_path(self.stage.source_path, 'fortran'),
            join_path(self.prefix, 'fortran')
        )
