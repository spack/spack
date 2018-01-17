##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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
import os


class Flux(AutotoolsPackage):
    """ A next-generation resource manager (pre-alpha) """

    homepage = "https://github.com/flux-framework/flux-core"
    url      = "https://github.com/flux-framework/flux-core/releases/download/v0.8.0/flux-core-0.8.0.tar.gz"

    version('0.8.0', md5='9ee12974a8b2ab9a30533f69826f3bec')
    version('master', branch='master',
            git='https://github.com/flux-framework/flux-core')

    variant('doc', default=True, description='Build flux manpages')

    depends_on("zeromq@4.0.4:")
    depends_on("czmq@2.2:")
    depends_on("hwloc")
    depends_on("lua@5.1:5.1.99")
    depends_on("lua-luaposix")
    depends_on("munge")
    depends_on("libuuid")
    depends_on("python")
    depends_on("py-cffi", type=('build', 'run'))
    depends_on("jansson")

    depends_on("asciidoc", type='build', when="+docs")

    # Need autotools when building on master:
    depends_on("autoconf", type='build', when='@master')
    depends_on("automake", type='build', when='@master')
    depends_on("libtool", type='build', when='@master')

    def setup():
        pass

    @when('@master')
    def setup(self):
        # Allow git-describe to get last tag so flux-version works:
        git = which('git')
        git('pull', '--depth=50', '--tags')

    def autoreconf(self, spec, prefix):
        self.setup()
        if os.path.exists('autogen.sh'):
            # Bootstrap with autotools
            bash = which('bash')
            bash('./autogen.sh')

    def setup_environment(self, spack_env, run_env):
        #  Ensure ./fluxometer.lua can be found during flux's make check
        spack_env.append_path('LUA_PATH', './?.lua', separator=';')

    def configure_args(self):
        return ['--disable-docs'] if '+docs' not in self.spec else []
