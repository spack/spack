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


class ModeleUtils(CMakePackage):
    """Utities for GISS GCM"""

    homepage = "http://www.giss.nasa.gov/tools/modelE"

    # This must be built by a user with access to simplex.
    version('develop',
            git='simplex.giss.nasa.gov:/giss/gitrepo/modelE.git',
            branch='landice')

    maintainers = ['citibeth']

    variant('ic', default=False,
            description='Build init_cond directory')
    variant('diags', default=True,
            description='Build mk_diags directory.')
    variant('aux', default=False,
            description='Build aux directory')

    # Build dependencies
    depends_on('m4', type='build')
    depends_on('cmake@3.2:', type='build')

    # Link dependencies
    depends_on('netcdf-fortran')

    # depends_on('netcdf-cxx', when='+pnetcdf')

    # Run dependencies

    def cmake_args(self):
        spec = self.spec
        return [
            '-DCMAKE_BUILD_TYPE=%s' %
            ('Debug' if '+debug' in spec else 'Release'),
            '-DBUILD_MODEL=NO',
            '-DBUILD_IC=%s' % ('YES' if '+ic' in spec else 'NO'),
            '-DBUILD_DIAGS=%s' % ('YES' if '+diags' in spec else 'NO'),
            '-DBUILD_AUX=%s' % ('YES' if '+aux' in spec else 'NO'),
            '-DMPI=NO',
            '-DUSE_PNETCDF=NO',
            '-DUSE_FEXCEPTION=NO',
            '-DUSE_EVERYTRACE=NO',
            '-DUSE_ICEBIN=NO']
