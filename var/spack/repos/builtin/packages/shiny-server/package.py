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


class ShinyServer(CMakePackage):
    """Shiny server lets you put shiny web applications and interactive
       documents online. Take your shiny apps and share them with your
       organization or the world."""

    #
    # HEADS UP:
    # 1. The shiny server installation step will download various node
    #    and npm bits from the net.  They seem to have them well
    #    constrained ("npm shrinkwrap"?), but this package is not
    #    "air gappable".
    # 2. Docs say that it requires 'gcc'.  depends_on() won't do the
    #    right thing, it's Up To You.
    #
    homepage = "https://www.rstudio.com/products/shiny/shiny-server/"
    url = "https://github.com/rstudio/shiny-server/archive/v1.5.3.838.tar.gz"

    version('1.5.3.838', '96f20fdcdd94c9e9bb851baccb82b97f')

    depends_on('python@:2.8')  # docs say: "Really.  3.x will not work"
    depends_on('cmake@2.8.10:')
    depends_on('git')
    depends_on('r+X')
    depends_on('openssl')

    def cmake_args(self):
        spec = self.spec
        options = []

        options.append("-DPYTHON=%s" % spec['python'].command.path)

        return options

    # Recompile the npm modules included in the project
    @run_after('build')
    def build_node(self):
        bash = which('bash')
        mkdirp('build')
        bash('-c', 'bin/npm --python="$PYTHON" install')
        bash('-c', 'bin/node ./ext/node/lib/node_modules/npm/node_modules/node-gyp/bin/node-gyp.js --python="$PYTHON" rebuild')  # noqa: E501

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PATH',
                             join_path(self.prefix, 'shiny-server', 'bin'))
        # shiny comes with its own pandoc; hook it up...
        run_env.prepend_path('PATH',
                             join_path(self.prefix, 'shiny-server',
                                       'ext', 'pandoc', 'static'))
