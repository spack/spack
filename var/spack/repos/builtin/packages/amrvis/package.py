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
# published by the Free Software Foundation) version 2.1, February 1999.  #
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


class Amrvis(MakefilePackage):
    """Amrvis is a visualization package specifically designed to
       read and display output and profiling data from codes built
       on the AMReX framework.
    """

    homepage = "https://github.com/AMReX-Codes/Amrvis"
    git      = "https://github.com/AMReX-Codes/Amrvis.git"

    version('master', tag='master')

    variant(
        'dims',
        default='3',
        values=('1', '2', '3'),
        multi=False,
        description='Number of spatial dimensions'
    )
    variant(
        'prec',
        default='DOUBLE',
        values=('FLOAT', 'DOUBLE'),
        multi=False,
        description='Floating point precision'
    )
    variant('mpi', default=True, description='Enable MPI parallel support')
    variant('debug', default=False, description='Enable debugging features')

    depends_on('gmake', type='build')
    depends_on('mpi', when='+mpi')
    depends_on('libsm')
    depends_on('libice')
    depends_on('libxpm')
    depends_on('libx11')
    depends_on('libxt')
    depends_on('libxext')
    depends_on('motif')

    # Only doing gcc and clang at the moment.
    # Intel currently fails searching for mpiicc, mpiicpc, etc.
    for comp in ['%intel', '%cce', '%nag', '%pgi', '%xl', '%xl_r']:
        conflicts(
            comp,
            msg='Amrvis currently only builds with gcc and clang'
        )

    # Need to clone AMReX into Amrvis because Amrvis uses AMReX's source
    resource(name='amrex',
             git='https://github.com/AMReX-Codes/amrex.git',
             tag='master',
             placement='amrex')

    def edit(self, spec, prefix):
        # Set all available makefile options to values we want
        makefile = FileFilter('GNUmakefile')
        makefile.filter(
            r'^AMREX_HOME\s*=.*',
            'AMREX_HOME = {0}'.format('./amrex')
        )
        makefile.filter(
            r'^PRECISION\s*=.*',
            'PRECISION = {0}'.format(spec.variants['prec'].value)
        )
        makefile.filter(
            r'^DIM\s*=.*',
            'DIM = {0}'.format(spec.variants['dims'].value)
        )
        makefile.filter(
            r'^PROFILE\s*=.*',
            'PROFILE = FALSE'
        )
        makefile.filter(
            r'^TRACE_PROFILE\s*=.*',
            'TRACE_PROFILE = FALSE'
        )
        makefile.filter(
            r'^COMM_PROFILE\s*=.*',
            'COMM_PROFILE = FALSE'
        )
        makefile.filter(
            r'^COMP\s*=.*',
            'COMP = {0}'.format(self.compiler.name)
        )
        makefile.filter(
            r'^DEBUG\s*=.*',
            'DEBUG = {0}'.format(spec.variants['debug'].value).upper()
        )
        makefile.filter(
            r'^USE_ARRAYVIEW\s*=.*',
            'USE_ARRAY_VIEW = FALSE'
        )
        makefile.filter(
            r'^USE_MPI\s*=.*',
            'USE_MPI = {0}'.format(spec.variants['mpi'].value).upper()
        )
        makefile.filter(
            r'^USE_CXX11\s*=.*',
            'USE_CXX11 = TRUE'
        )
        makefile.filter(
            r'^USE_VOLRENDER\s*=.*',
            'USE_VOLRENDER = FALSE'
        )
        makefile.filter(
            r'^USE_PARALLELVOLRENDER\s*=.*',
            'USE_PARALLELVOLRENDER = FALSE'
        )
        makefile.filter(
            r'^USE_PROFPARSER\s*=.*',
            'USE_PROFPARSER = FALSE'
        )

        # A bit risky here deleting all /usr and /opt X
        # library default search paths in makefile
        makefile.filter(
            r'^.*\b(usr|opt)\b.*$',
            '# Spack removed INCLUDE_LOCATIONS and LIBRARY_LOCATIONS'
        )

        # Read GNUmakefile into array
        with open('GNUmakefile', 'r') as file:
            contents = file.readlines()

        # Edit GNUmakefile includes and libraries to point to Spack
        # dependencies.
        # The safest bet is to put the LIBRARY_LOCATIONS and
        # INCLUDE_LOCATIONS at the beginning of the makefile.
        line_offset = 0
        count = 0
        for lib in ['libsm', 'libice', 'libxpm', 'libx11',
                    'libxt', 'libxext', 'motif']:
            contents.insert(
                line_offset + count,
                'LIBRARY_LOCATIONS += {0}\n'.format(spec[lib].prefix.lib)
            )
            contents.insert(
                line_offset + count + 1,
                'INCLUDE_LOCATIONS += {0}\n'.format(spec[lib].prefix.include)
            )
            count += 1

        # Write GNUmakefile
        with open('GNUmakefile', 'w') as file:
            file.writelines(contents)

    def setup_environment(self, spack_env, run_env):
        # Help force Amrvis to not pick up random system compilers
        if '+mpi' in self.spec:
            spack_env.set('MPI_HOME', self.spec['mpi'].prefix)
            spack_env.set('CC', self.spec['mpi'].mpicc)
            spack_env.set('CXX', self.spec['mpi'].mpicxx)
            spack_env.set('F77', self.spec['mpi'].mpif77)
            spack_env.set('FC', self.spec['mpi'].mpifc)

    def install(self, spec, prefix):
        # Install exe manually
        mkdirp(prefix.bin)
        exes = glob.iglob('*.ex')
        for exe in exes:
            install(exe, prefix.bin)
