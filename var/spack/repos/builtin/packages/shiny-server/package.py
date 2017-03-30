##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
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


class ShinyServer(Package):
    """Shiny server lets you put shiny web applications and interactive
       documents online. Take your shiny apps and share them with your
       organization or the world."""

    homepage = "https://www.rstudio.com/products/shiny/shiny-server/"
    url = "https://github.com/rstudio/shiny-server/archive/v1.5.3.838.tar.gz"

    version('1.5.3.838', '96f20fdcdd94c9e9bb851baccb82b97f')

    depends_on('python@2.7.13') # docs say: "Really.  3.x will not work"
    depends_on('cmake@2.8.10:')
    # depends_on('gcc@5.4.0')
    depends_on('git')
    depends_on('r')
    depends_on('openssl')

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            bash = which('bash')
            cmake('..',
                  "-DPYTHON=%s" % join_path(spec['python'].prefix.bin, 
                                            'python'),
                  *std_cmake_args)
            make()
            mkdirp('../build')
            bash('-c', 'cd .. && ./bin/npm --python="$PYTHON" install')
            bash('-c', 'cd .. && ./bin/node ./ext/node/lib/node_modules/npm/node_modules/node-gyp/bin/node-gyp.js --python="$PYTHON" rebuild')  # noqa: E501
            make("install")

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PATH',
                             join_path(self.prefix, 'shiny-server', 'bin'))
        # shiny comes with its own pandoc; hook it up...
        run_env.prepend_path('PATH',
                             join_path(self.prefix, 'shiny-server', 
                                       'ext', 'pandoc', 'static'))
