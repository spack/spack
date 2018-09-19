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
import sys


class AutodockVina(MakefilePackage):
    """AutoDock Vina is an open-source program for doing molecular docking"""

    homepage = "http://vina.scripps.edu/"
    url = "http://vina.scripps.edu/download/autodock_vina_1_1_2.tgz"

    version('1_1_2', 'b467b71ee77dd155b65b1c5364e4220f')

    depends_on('boost@1.65.0')

    # Replacing depecrated function call of boost with current function call
    patch('main.patch')
    patch('split.patch')

    @property
    def build_directory(self):
        if sys.platform == "darwin":
            return join_path('build', 'mac', 'release')
        else:
            return join_path('build', 'linux', 'release')

    def edit(self, spec, prefix):
        with working_dir(self.build_directory):
            makefile = FileFilter('Makefile')
            makefile.filter('BOOST_INCLUDE = .*', 'BOOST_INCLUDE = %s' %
                            self.spec['boost'].prefix.include)
            makefile.filter('C_PLATFORM=.*', 'C_PLATFORM=-pthread')
            makefile.filter('GPP=.*', 'GPP=%s' % spack_cc)
            mcp = FileFilter('../../makefile_common')
            mcp.filter('LIBS = ', 'LIBS = -l stdc++ -lm ')

    def build(self, spec, prefix):
        with working_dir(self.build_directory):
            make()

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            mkdirp(prefix.bin)
            install('vina', prefix.bin)
            install('vina_split', prefix.bin)
