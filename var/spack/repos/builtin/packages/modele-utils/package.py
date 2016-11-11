##############################################################################
# Copyright (c) 2016, Lawrence Livermore National Security, LLC.
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


class ModeleUtils(CMakePackage):
    """Utities for GISS GCM"""

    homepage = "http://www.giss.nasa.gov/tools/modelE"

    # This must be built a user with access to simplex.
    version('cmake',
            git='simplex.giss.nasa.gov:/giss/gitrepo/modelE.git',
            branch='cmake',
            preferred=True)

    variant('ic', default=True,
            description='Build init_cond directory')
    variant('diags', default=True,
            description='Build mk_diags directory.')
    variant('aux', default=True,
            description='Build aux directory')

    # Build dependencies
    depends_on('m4')
    depends_on('cmake')

    # Link dependencies
    depends_on('netcdf-fortran')

    # depends_on('netcdf-cxx', when='+pnetcdf')

    # Run dependencies

    def configure_args(self):
        spec = self.spec
        return [
            '-DCMAKE_BUILD_TYPE=%s' %
            ('Debug' if '+debug' in spec else 'Release'),
            '-DCOMPILE_WITH_TRAPS=NO',
            '-DCOMPILE_MODEL=NO',
            '-DCOMPILE_IC=%s' % ('YES' if '+ic' in spec else 'NO'),
            '-DCOMPILE_DIAGS=%s' % ('YES' if '+diags' in spec else 'NO'),
            '-DCOMPILE_AUX=%s' % ('YES' if '+aux' in spec else 'NO'),
            '-DMPI=NO',
            '-DUSE_PNETCDF=NO',
            '-DUSE_FEXCEPTION=NO',
            '-DUSE_EVERYTRACE=NO',
            '-DUSE_GLINT2=NO']

    def setup_environment(self, spack_env, env):
        """Add <prefix>/bin to the module"""
        env.prepend_path('PATH', join_path(self.prefix, 'bin'))
