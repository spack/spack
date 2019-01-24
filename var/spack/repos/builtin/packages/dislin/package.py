# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
