# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
