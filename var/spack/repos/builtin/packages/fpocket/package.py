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


class Fpocket(Package):
    """fpocket is a very fast open source protein pocket detection algorithm
       based on Voronoi tessellation."""

    homepage = "https://github.com/Discngine/fpocket"
    version('develop', branch='master',
            git='https://github.com/Discngine/fpocket.git')

    depends_on("netcdf")

    def setup_environment(self, spack_env, run_env):
        if self.compiler.name == 'gcc':
            spack_env.set('CXX', 'g++')

    def patch(self):
        makefile = FileFilter(join_path(self.stage.source_path, 'makefile'))
        makefile.filter('BINDIR .*', 'BINDIR = %s/bin' % self.prefix)
        makefile.filter('MANDIR .*', 'MANDIR = %s/man/man8' % self.prefix)

    def install(self, spec, prefix):
        make()
        make('install')
