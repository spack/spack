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


class Chombo(MakefilePackage):
    """The Chombo package provides a set of tools for implementing finite
       difference and finite-volume methods for the solution of partial
       differential equations on block-structured adaptively refined
       logically rectangular (i.e. Cartesian) grids."""

    homepage = "https://commons.lbl.gov/display/chombo"
    git      = "http://bitbucket.org/drhansj/chombo-xsdk.git"

    tags = ['ecp', 'ecp-apps']

    # Use whatever path Brian V. and Terry L. agreed upon, but preserve version
    version('3.2', commit='71d856c')
    version('develop', tag='master')

    variant('mpi', default=True, description='Enable MPI parallel support')
    variant('hdf5', default=True, description='Enable HDF5 support')
    variant('dims',
        default='3',
        values=('1', '2', '3', '4', '5', '6'),
        multi=False,
        description='Number of PDE dimensions [1-6]'
    )

    patch('hdf5-16api.patch', when='@3.2', level=0)
    patch('Make.defs.local.template.patch', when='@3.2', level=0)

    depends_on('blas')
    depends_on('lapack')
    depends_on('gmake', type='build')
    depends_on('mpi', when='+mpi')
    depends_on('hdf5', when='+hdf5')
    depends_on('hdf5+mpi', when='+mpi+hdf5')

    def edit(self, spec, prefix):

        # Set fortran name mangling in Make.defs
        defs_file = FileFilter('./lib/mk/Make.defs')
        defs_file.filter('^\s*#\s*cppcallsfort\s*=\s*',
                         'cppcallsfort = -DCH_FORT_UNDERSCORE')

        # Set remaining variables in Make.defs.local
        # Make.defs.local.template.patch ensures lines for USE_TIMER,
        # USE_LAPACK and lapackincflags are present
        copy('./lib/mk/Make.defs.local.template',
             './lib/mk/Make.defs.local')

        defs_file = FileFilter('./lib/mk/Make.defs.local')

        # Unconditional settings
        defs_file.filter('^\s*#\s*DEBUG\s*=\s*', 'DEBUG = FALSE')
        defs_file.filter('^\s*#\s*OPT\s*=\s*', 'OPT = TRUE')
        defs_file.filter('^\s*#\s*PIC\s*=\s*', 'PIC = TRUE')
        # timer code frequently fails compiles. So disable it.
        defs_file.filter('^\s*#\s*USE_TIMER\s*=\s*', 'USE_TIMER = FALSE')

        # LAPACK setup
        lapack_blas = spec['lapack'].libs + spec['blas'].libs
        defs_file.filter('^\s*#\s*USE_LAPACK\s*=\s*', 'USE_LAPACK = TRUE')
        defs_file.filter(
            '^\s*#\s*lapackincflags\s*=\s*',
            'lapackincflags = -I%s' % spec['lapack'].prefix.include)
        defs_file.filter(
            '^\s*#\s*syslibflags\s*=\s*',
            'syslibflags = %s' % lapack_blas.ld_flags)

        # Compilers and Compiler flags
        defs_file.filter('^\s*#\s*CXX\s*=\s*', 'CXX = %s' % spack_cxx)
        defs_file.filter('^\s*#\s*FC\s*=\s*', 'FC = %s' % spack_fc)
        if '+mpi' in spec:
            defs_file.filter(
                '^\s*#\s*MPICXX\s*=\s*',
                'MPICXX = %s' % self.spec['mpi'].mpicxx)

        # Conditionally determined settings
        defs_file.filter(
            '^\s*#\s*MPI\s*=\s*',
            'MPI = %s' % ('TRUE' if '+mpi' in spec else 'FALSE'))
        defs_file.filter(
            '^\s*#\s*DIM\s*=\s*',
            'DIM = %s' % spec.variants['dims'].value)

        # HDF5 settings
        if '+hdf5' in spec:
            defs_file.filter('^\s*#\s*USE_HDF5\s*=\s*', 'USE_HDF5 = TRUE')
            defs_file.filter(
                '^\s*#\s*HDFINCFLAGS\s*=.*',
                'HDFINCFLAGS = -I%s' % spec['hdf5'].prefix.include)
            defs_file.filter(
                '^\s*#\s*HDFLIBFLAGS\s*=.*',
                'HDFLIBFLAGS = %s' % spec['hdf5'].libs.ld_flags)
            if '+mpi' in spec:
                defs_file.filter(
                    '^\s*#\s*HDFMPIINCFLAGS\s*=.*',
                    'HDFMPIINCFLAGS = -I%s' % spec['hdf5'].prefix.include)
                defs_file.filter(
                    '^\s*#\s*HDFMPILIBFLAGS\s*=.*',
                    'HDFMPILIBFLAGS = %s' % spec['hdf5'].libs.ld_flags)

    def build(self, spec, prefix):
        with working_dir('lib'):
            gmake('all')

    def install(self, spec, prefix):
        with working_dir('lib'):
            install_tree('include', prefix.include)
            libfiles = glob.glob('lib*.a')
            libfiles += glob.glob('lib*.so')
            libfiles += glob.glob('lib*.dylib')
            mkdirp(prefix.lib)
            for lib in libfiles:
                install(lib, prefix.lib)
