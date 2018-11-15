# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
