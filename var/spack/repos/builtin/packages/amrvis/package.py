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


class Amrvis(MakefilePackage):
    """Amrvis is a visualization package specifically designed to
       read and display output and profiling data from codes built
       on the AMReX framework.
    """

    homepage = "https://github.com/AMReX-Codes/Amrvis"
    url      = "https://github.com/AMReX-Codes/Amrvis.git"

    version('master',
            git='https://github.com/AMReX-Codes/Amrvis.git', tag='master')

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
    variant('mpi', default=False, description='Enable MPI parallel support')
    variant('debug', default=False, description='Enable debugging features')

    depends_on('mpi', when='+mpi')
    depends_on('libsm')
    depends_on('libice')
    depends_on('libxpm')
    depends_on('libx11')
    depends_on('libxt')
    depends_on('libxext')
    depends_on('motif')

    conflicts('%cce',
              msg='Amrvis currently only builds with gcc, clang, and intel')
    conflicts('%nag',
              msg='Amrvis currently only builds with gcc, clang, and intel')
    conflicts('%pgi',
              msg='Amrvis currently only builds with gcc, clang, and intel')
    conflicts('%xl',
              msg='Amrvis currently only builds with gcc, clang, and intel')
    conflicts('%xl_r',
              msg='Amrvis currently only builds with gcc, clang, and intel')

    resource(name='amrex',
             git='https://github.com/AMReX-Codes/amrex.git',
             tag='master',
             placement='amrex')

    def edit(self, spec, prefix):
        filter_file(r'^AMREX_HOME\s*=.*',
                    'AMREX_HOME = {0}'.format('./amrex'),
                    'GNUmakefile')
        filter_file(r'^PRECISION\s*=.*',
                    'PRECISION = {0}'.format(spec.variants['prec'].value),
                    'GNUmakefile')
        filter_file(r'^DIM\s*=.*',
                    'DIM = {0}'.format(spec.variants['dims'].value),
                    'GNUmakefile')
        filter_file(r'^PROFILE\s*=.*',
                    'PROFILE = FALSE',
                    'GNUmakefile')
        filter_file(r'^TRACE_PROFILE\s*=.*',
                    'TRACE_PROFILE = FALSE',
                    'GNUmakefile')
        filter_file(r'^COMM_PROFILE\s*=.*',
                    'COMM_PROFILE = FALSE',
                    'GNUmakefile')
        # Only doing gcc, clang, and intel at the moment
        filter_file(r'^COMP\s*=.*',
                    'COMP = {0}'.format(self.compiler.name),
                    'GNUmakefile')
        filter_file(r'^DEBUG\s*=.*',
                    'DEBUG = {0}'.format(spec.variants['debug'].value).upper(),
                    'GNUmakefile')
        filter_file(r'^USE_ARRAYVIEW\s*=.*',
                    'USE_ARRAY_VIEW = FALSE',
                    'GNUmakefile')
        filter_file(r'^USE_MPI\s*=.*',
                    'USE_MPI = {0}'.format(spec.variants['mpi'].value).upper(),
                    'GNUmakefile')
        filter_file(r'^USE_CXX11\s*=.*',
                    'USE_CXX11 = TRUE',
                    'GNUmakefile')
        filter_file(r'^USE_VOLRENDER\s*=.*',
                    'USE_VOLRENDER = FALSE',
                    'GNUmakefile')
        filter_file(r'^USE_PARALLELVOLRENDER\s*=.*',
                    'USE_PARALLELVOLRENDER = FALSE',
                    'GNUmakefile')
        filter_file(r'^USE_PROFPARSER\s*=.*',
                    'USE_PROFPARSER = FALSE',
                    'GNUmakefile')

        # Delete all /usr and /opt X library default search paths in makefile
        filter_file(r'^.*\b(usr|opt)\b.*$',
                    '# Spack removed INCLUDE_LOCATIONS and LIBRARY_LOCATIONS',
                    'GNUmakefile')

        # Read GNUmakefile into array
        with open('GNUmakefile', 'r') as file:
            contents = file.readlines()

        # Edit GNUmakefile INCLUDES and LIBRARIES to use Spack dependencies.
        # Assuming the default GNUmakefile doesn't change, this is the best
        # place for LIBRARY_LOCATIONS and INCLUDE_LOCATIONS.
        line_offset = 63
        contents.insert(
            line_offset + 1,
            'LIBRARY_LOCATIONS += {0}\n'.format(spec['libsm'].prefix.lib)
        )
        contents.insert(
            line_offset + 2,
            'INCLUDE_LOCATIONS += {0}\n'.format(spec['libsm'].prefix.include)
        )
        contents.insert(
            line_offset + 3,
            'LIBRARY_LOCATIONS += {0}\n'.format(spec['libice'].prefix.lib)
        )
        contents.insert(
            line_offset + 4,
            'INCLUDE_LOCATIONS += {0}\n'.format(spec['libice'].prefix.include)
        )
        contents.insert(
            line_offset + 5,
            'LIBRARY_LOCATIONS += {0}\n'.format(spec['libxpm'].prefix.lib)
        )
        contents.insert(
            line_offset + 6,
            'INCLUDE_LOCATIONS += {0}\n'.format(spec['libxpm'].prefix.include)
        )
        contents.insert(
            line_offset + 7,
            'LIBRARY_LOCATIONS += {0}\n'.format(spec['libx11'].prefix.lib)
        )
        contents.insert(
            line_offset + 8,
            'INCLUDE_LOCATIONS += {0}\n'.format(spec['libx11'].prefix.include)
        )
        contents.insert(
            line_offset + 9,
            'LIBRARY_LOCATIONS += {0}\n'.format(spec['libxt'].prefix.lib)
        )
        contents.insert(
            line_offset + 10,
            'INCLUDE_LOCATIONS += {0}\n'.format(spec['libxt'].prefix.include)
        )
        contents.insert(
            line_offset + 11,
            'LIBRARY_LOCATIONS += {0}\n'.format(spec['libxext'].prefix.lib)
        )
        contents.insert(
            line_offset + 12,
            'INCLUDE_LOCATIONS += {0}\n'.format(spec['libxext'].prefix.include)
        )
        contents.insert(
            line_offset + 13,
            'LIBRARY_LOCATIONS += {0}\n'.format(spec['motif'].prefix.lib)
        )
        contents.insert(
            line_offset + 14,
            'INCLUDE_LOCATIONS += {0}\n'.format(spec['motif'].prefix.include)
        )

        # Write GNUmakefile
        with open('GNUmakefile', 'w') as file:
            file.writelines(contents)

    def setup_environment(self, build_env, run_env):
        if '+mpi' in self.spec:
            # Set MPI location
            build_env.set('MPI_HOME', self.spec['mpi'].prefix)
            build_env.set('MPIHOME', self.spec['mpi'].prefix)

    def install(self, spec, prefix):
        # Set exe name options
        dim = spec.variants['dims'].value
        comp = self.compiler.name
        if spec.satisfies('%gcc'):
            comp = 'gnu'
        if '+mpi' in self.spec:
            mpi = '.MPI'
        else:
            mpi = ''
        if '+debug' in self.spec:
            debug = '.DEBUG'
        else:
            debug = ''

        # Construct exe name
        exe = 'amrvis%sd.%s%s%s.ex' % (dim, comp, debug, mpi)

        # Install exe manually
        mkdirp(prefix.bin)
        install(exe, prefix.bin)
