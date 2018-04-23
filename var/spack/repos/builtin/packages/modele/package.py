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


class Modele(CMakePackage):

    """General Circulation (Climate) Model from the Columbia/NASA Goddard
    Institute of Space Studes"""

    homepage = "http://www.giss.nasa.gov/tools/modelE"

    maintainers = ['citibeth']

    # ModelE has no valid versions.
    # This must be built with "spack spconfig" in a local repo
    version('landice',
            git='simplex.giss.nasa.gov:/giss/gitrepo/modelE.git',
            branch='landice')

    version('master',
            git='simplex.giss.nasa.gov:/giss/gitrepo/modelE.git',
            branch='master',
            preferred=True)

    # --- Variants controlling dependencies
    variant('everytrace', default=True,
            description='Link to enhanced staktrace capabilities')
    variant('pnetcdf', default=True, description=''
            'Link with the PNetCDF library; required for some rundecks.')
    variant('icebin', default=False,
            description='Link with the Icebin Ice Model Coupler')
    variant('mpi', default=True,
            description='Build parallel version with MPI')
    variant('fexception', default=False, description=''
            'Use the FException library, for getting good stack traces.')

    # --- Variants controlling what we build
    variant('model', default=True,
            description='Build main model')
    variant('tests', default=False,
        description='Build unit tests')
    variant('aux', default=False,
            description='Build aux directory')
    variant('diags', default=False,
            description='Build mk_diags directory.')
    variant('ic', default=False,
            description='Build init_cond directory')

    # --- Variants controlling how we build
    variant('mods', default=False,
            description='Install .mod files')

    # ----------------------------------------
    # Build dependencies
    depends_on('m4', type='build')
    depends_on('cmake@3.2:', type='build')

    # Link dependencies
    depends_on('everytrace+fortran+mpi', when='+everytrace')
    depends_on('parallel-netcdf+fortran', when='+pnetcdf')
    depends_on('icebin+coupler', when='+icebin')
    depends_on('mpi', when='+mpi')
    depends_on('fexception', when='+fexception')
    depends_on('pfunit+mpi', when='+tests')
    depends_on('netcdf-fortran')

    def cmake_args(self):
        spec = self.spec
        return [
            '-DUSE_EVERYTRACE=%s' % ('YES' if '+everytrace' in spec else 'NO'),
            '-DUSE_PNETCDF=%s' % ('YES' if '+pnetcdf' in spec else 'NO'),
            '-DUSE_ICEBIN=%s' % ('YES' if '+icebin' in spec else 'NO'),
            '-DUSE_MPI=%s' % ('YES' if '+mpi' in spec else 'NO'),
            '-DUSE_FEXCEPTION=%s' % ('YES' if '+fexception' in spec else 'NO'),

            '-DBUILD_MODEL=%s' % ('YES' if '+model' in spec else 'NO'),
            '-DBUILD_TESTS=%s' % ('YES' if '+tests' in spec else 'NO'),
            '-DBUILD_AUX=%s' % ('YES' if '+aux' in spec else 'NO'),
            '-DBUILD_DIAGS=%s' % ('YES' if '+diags' in spec else 'NO'),
            '-DBUILD_IC=%s' % ('YES' if '+ic' in spec else 'NO'),


            '-DCMAKE_BUILD_TYPE=%s' %
            '-DINSTALL_MODS=%s' % ('YES' if '+mods' in spec else 'NO')]
