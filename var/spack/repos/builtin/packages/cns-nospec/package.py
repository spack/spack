##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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


class CnsNospec(MakefilePackage):
    """A simple, explicit, stencil-based test code for integrating
    the compressible Navier-Stokes equations. The code uses
    8th order finite differences in space and a 3rd order,
    low-storage TVD RK algorithm in time."""

    homepage = "https://ccse.lbl.gov/ExaCT/index.html"
    url      = "https://ccse.lbl.gov/ExaCT/CNS_Nospec.tgz"
    tags     = ['proxy-app']

    version('master', '14ff5be62539d829b30b17281688ee3f')

    variant('mpi', default=True, description='Build with MPI support')
    variant('debug', default=False, description='Build with debugging')
    variant('omp', default=False, description='Build with OpenMP support')
    variant('prof', default=False, description='Build with profiling')

    depends_on('mpi', when='+mpi')
    depends_on('gmake', type='build')

    build_directory = 'MiniApps/CNS_NoSpec'

    def edit(self, spec, prefix):
        def_file = FileFilter('Tools/F_mk/GMakedefs.mak')
        def_file.filter('tdir = t/.*', 'tdir := t/$(suf)')
        def_file.filter('hdir = t/.*', 'hdir := t/html')
        def_file.filter('include $(BOXLIB_HOME)/Tools/F_mk/GMakeMPI.mak', '#')

        if '+mpi' in spec:
            def_file.filter('FC.*:=.*', 'FC = {0}'.format(spec['mpi'].mpifc))
            def_file.filter('F90.*:=.*', 'F90 = {0}'.format(spec['mpi'].mpifc))
            def_file.filter(
                'mpi_include_dir =.*',
                'mpi_include_dir = {0}'.format(spec['mpi'].prefix.include))
            def_file.filter(
                'mpi_lib_dir =.*',
                'mpi_lib_dir = {0}'.format(spec['mpi'].prefix.lib))

        with working_dir(self.build_directory):
            makefile = FileFilter('GNUmakefile')
            if '+mpi' in spec:
                makefile.filter('MPI .*', 'MPI := t')
            if '+debug' in spec:
                makefile.filter('NDEBUG.*', '#')
            if '+omp' in spec:
                makefile.filter('OMP.*', 'OMP := t')
            if '+prof' in spec:
                makefile.filter('PROF.*', 'PROF := t')

            if self.compiler.name == 'gcc':
                makefile.filter('COMP .*', 'COMP = gfortran')
            if self.compiler.name == 'intel':
                makefile.filter('COMP .*', 'COMP = Intel')
            if self.compiler.name == 'pgi':
                makefile.filter('COMP .*', 'COMP = PGI')
            if self.compiler.name == 'xl':
                makefile.filter('COMP .*', 'COMP = IBM')
            if self.compiler.name == 'cce':
                makefile.filter('COMP .*', 'COMP = Cray')

    @property
    def build_targets(self):
        spec = self.spec
        if '+mpi' in spec:
            return ['CC = {0}'.format(spec['mpi'].mpicc),
                    'CXX = {0}'.format(spec['mpi'].mpicxx)]
        else:
            return []

    def build(self, spec, prefix):
        with working_dir(self.build_directory):
            gmake()

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        files = glob.glob(join_path(self.build_directory, '*.exe'))
        for f in files:
            install(f, prefix.bin)
        install('README.txt', prefix)
        install('license.txt', prefix)
        install(join_path(self.build_directory, 'README'), prefix)
