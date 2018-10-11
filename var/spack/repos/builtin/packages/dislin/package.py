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


class Dislin(Package):
    """DISLIN is a high level and easy to use graphics library for displaying
       data as curves,  bar graphs,  pie charts,  3D-colour plots,  surfaces,
       contours and maps."""

    homepage = "http://www.mps.mpg.de/dislin"
    url      = "ftp://ftp.gwdg.de/pub/grafik/dislin/linux/i586_64/dislin-11.0.linux.i586_64.tar.gz"

    version('11.1.linux.i586_64', '34218c257efedaf706f058bdf111ce9d')
    version('11.0.linux.i586_64', '6fb099b54f41db009cafc702eebb5bc6')

    depends_on('motif')
    depends_on('mesa')

    @property
    def libs(self):
        query_parameters = self.spec.last_query.extra_parameters
        query2libraries = {
            tuple(): ['libdislin'],
            ('d',): ['libdislin_d'],
            ('c', ): ['libdislnc'],
            ('cd',): ['libdislnc_d'],
            ('cxx',): ['libdiscpp'],
            ('java',): ['libdisjava']
        }

        key = tuple(query_parameters)
        libraries = query2libraries[key]

        return find_libraries(
            libraries, root=self.prefix, shared=True, recursive=True
        )

    def setup_environment(self, spack_env, run_env):
        spack_env.set('DISLIN', self.prefix)
        run_env.set('DISLIN', self.prefix)
        run_env.prepend_path('PATH', self.prefix)
        run_env.prepend_path('LD_LIBRARY_PATH', self.prefix)
        run_env.prepend_path('LD_LIBRARY_PATH', self.spec['motif'].prefix.lib)
        run_env.prepend_path('LD_LIBRARY_PATH', self.spec['mesa'].prefix.lib)

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        run_env.prepend_path('LD_LIBRARY_PATH', self.prefix)

    def install(self, spec, prefix):
        install = Executable('./INSTALL')
        install()
        with working_dir('examples'):
            install('dislin_d.h', prefix)
