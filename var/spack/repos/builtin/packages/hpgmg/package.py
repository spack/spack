##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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


class Hpgmg(Package):
    """HPGMG implements full multigrid (FMG) algorithms using finite-volume and
       finite-element methods.  Different algorithmic variants adjust the
       arithmetic intensity and architectural properties that are tested. These
       FMG methods converge up to discretization error in one F-cycle, thus may
       be considered direct solvers. An F-cycle visits the finest level a total
       of two times, the first coarsening (8x smaller) 4 times, the second
       coarsening 6 times, etc.
    """

    homepage = "https://bitbucket.org/hpgmg/hpgmg"
    url      = "https://hpgmg.org/static/hpgmg-0.tar.gz"
    git      = "https://bitbucket.org/hpgmg/hpgmg.git"

    tags = ['proxy-app']

    version('develop', branch='master')
    version('a0a5510df23b', 'b9c50f25e541428d4735fb07344d1d0ed9fc821bdde918d8e0defa78c0d9b4f9')
    version('0.3',          '12a65da216fec91daea78594ae4b5a069c8f1a700f1ba21eed9f45a79a68c793')

    variant(
        'fe', default=False, description='Build finite element solver')
    variant(
        'fv', default='mpi', values=('serial', 'mpi', 'none'),
        description='Build finite volume solver with or without MPI support')
    variant('cuda', default=False, description='Build with CUDA')
    variant('debug', default=False, description='Build in debug mode')

    depends_on('petsc', when='+fe')
    depends_on('mpi', when='+fe')
    depends_on('mpi', when='fv=mpi')
    depends_on('cuda', when='+cuda')
    depends_on('python', type='build')

    phases = ['configure', 'build', 'install']

    def configure_args(self):
        args = []
        if '+fe' in self.spec and not ('@0.3' in self.spec):
            args.append('--fe')

        if 'fv=serial' in self.spec:
            args.append('--no-fv-mpi')

        if 'mpi' in self.spec:
            args.append('--CC={0}'.format(self.spec['mpi'].mpicc))

        cflags = []
        if 'fv=none' in self.spec:
            args.append('--no-fv')
        else:
            # Apple's Clang doesn't support OpenMP
            if not (self.spec.satisfies('%clang') and self.compiler.is_apple):
                cflags.append(self.compiler.openmp_flag)

        if '+debug' in self.spec:
            cflags.append('-g')
        elif any(map(self.spec.satisfies, ['%gcc', '%clang', '%intel'])):
            cflags += ['-O3', '-march=native']

        args.append('--CFLAGS=' + ' '.join(cflags))

        # Explicitly specify the build directory to ensure that
        # PETSC_ARCH is not used from the environment.
        args.append('--arch=build')

        return args

    def configure(self, spec, prefix):
        configure(*self.configure_args())

    def build(self, spec, prefix):
        make('-C', 'build')

    def install(self, spec, prefix):
        install_tree('build/bin', prefix.bin)
        install('README.md', prefix)
        install('LICENSE', prefix)
