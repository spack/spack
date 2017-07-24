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
import inspect


class Hpgmg(AutotoolsPackage):
    """HPGMG implements full multigrid (FMG) algorithms using
    finite-volume and finite-element methods.
    Different algorithmic variants adjust the arithmetic intensity
    and architectural properties that are tested. These FMG methods
    converge up to discretization error in one F-cycle,
    thus may be considered direct solvers. An F-cycle visits
    the finest level a total of two times,
    the first coarsening (8x smaller) 4 times,
    the second coarsening 6 times, etc."""

    homepage = "https://bitbucket.org/hpgmg/hpgmg"
    url      = "https://bitbucket.org/hpgmg/hpgmg/get/master.tar.gz"
    tags     = ['proxy-app']

    version('master', '4a2b139e1764c84ed7fe06334d3f8d8a')

    variant(
        'fe_fv', default='both',
        values=('both', 'fe', 'fv'),
        description='Build finite element, finite volume, or both solvers')
    variant('mpi', default=True, description='Build with MPI support')
    variant('cuda', default=False, description='Build with CUDA')

    depends_on('petsc', when='fe_fv=fe')
    depends_on('petsc', when='fe_fv=both')
    depends_on('mpi', when='+mpi')
    depends_on('cuda', when='+cuda')
    depends_on('python', type='build')

    def configure_args(self):
        args = []
        if 'fe_fv=fv' in self.spec:
            args.extend(['--no-fe'])
        else:
            args.extend(['--fe'])

        if 'fe_fv=fe' in self.spec:
            if '+mpi' in self.spec:
                args.extend(['--no-fv-mpi'])
            else:
                args.extend(['--no-fv'])

        if 'fe_fv=fv' or 'fe_fv=both' in self.spec:
            args.extend(['--CFLAGS=' + self.compiler.openmp_flag])

        if '+mpi' in self.spec:
            args.extend(['--CC={0}'.format(self.spec['mpi'].mpicc)])

        return args

    def configure(self, spec, prefix):
        options = self.configure_args()

        with working_dir(self.build_directory, create=True):
            inspect.getmodule(self).configure(*options)

    def build(self, spec, prefix):
        with working_dir(self.build_directory):
            make()

    def install(self, spec, prefix):
        install_tree('build/bin', prefix.bin)
