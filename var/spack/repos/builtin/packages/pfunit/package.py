##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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
#
from spack import *
import glob


class Pfunit(CMakePackage):
    """pFUnit is a unit testing framework enabling JUnit-like testing of
    serial and MPI-parallel software written in Fortran."""

    homepage = "http://pfunit.sourceforge.net/"
    url      = "https://downloads.sourceforge.net/project/pfunit/Source/pFUnit.tar.gz"
    giturl   = "https://git.code.sf.net/p/pfunit/code"

    version('3.2.9', git=giturl,
            commit='3c1d47f594a7e756f21be59074cb730d1a1e9a79')
    version('develop', git=giturl, branch='master')

    variant('mpi', default=False, description='Enable MPI')
    variant('openmp', default=False, description='Enable OpenMP')

    depends_on('python', type=('build', 'run'))
    depends_on('py-unittest2', type=('run'))
    depends_on('mpi', when='+mpi')

    def patch(self):
        # The package tries to put .mod files in directory ./mod;
        # spack needs to put them in a standard location:
        for file in glob.glob('*/CMakeLists.txt'):
            filter_file(r'.*/mod($|[^\w].*)', '', file)

    def cmake_args(self):
        spec = self.spec
        args = ['-DCMAKE_Fortran_MODULE_DIRECTORY=%s' % spec.prefix.include]
        if spec.satisfies('+mpi'):
            args.extend(['-DMPI=YES', '-DMPI_USE_MPIEXEC=YES',
                         '-DMPI_Fortran_COMPILER=%s' % spec['mpi'].mpifc])
        else:
            args.append('-DMPI=NO')
        if spec.satisfies('+openmp'):
            args.append('-DOPENMP=YES')
        else:
            args.append('-DOPENMP=NO')
        return args

    def check(self):
        """Searches the CMake-generated Makefile for the target ``test``
        and runs it if found.
        """
        args = ['tests']
        if self.spec.satisfies('+mpi'):
            args.append('MPI=YES')
        if self.spec.satisfies('+openmp'):
            args.append('OPENMP=YES')
        with working_dir(self.build_directory):
            make(*args)

    def compiler_vendor(self):
        vendors = {'%gcc': 'GNU', '%clang': 'GNU', '%intel': 'Intel',
                   '%pgi': 'PGI', '%nag': 'NAG'}
        for key, value in vendors.items():
            if self.spec.satisfies(key):
                return value
        raise InstallError('Unsupported compiler.')

    def setup_environment(self, spack_env, run_env):
        spack_env.set('PFUNIT', self.spec.prefix)
        run_env.set('PFUNIT', self.spec.prefix)
        spack_env.set('F90_VENDOR', self.compiler_vendor())
        run_env.set('F90_VENDOR', self.compiler_vendor())

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.set('PFUNIT', self.spec.prefix)
        spack_env.set('F90_VENDOR', self.compiler_vendor())
