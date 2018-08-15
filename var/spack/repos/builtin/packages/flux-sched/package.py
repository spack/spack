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
import os


class FluxSched(AutotoolsPackage):
    """ A scheduler for flux-core (pre-alpha) """

    homepage = "https://github.com/flux-framework/flux-sched"
    url      = "https://github.com/flux-framework/flux-sched/releases/download/v0.5.0/flux-sched-0.5.0.tar.gz"
    git      = "https://github.com/flux-framework/flux-sched.git"

    version('master', branch='master')
    version('0.5.0', 'a9835c9c478aa41123a4e12672500052228aaf1ea770f74cb0901dbf4a049bd7d329e99d8d3484e39cfed1f911705030b2775dcfede39bc8bea59c6afe2549b1')
    version('0.4.0', '82732641ac4594ffe9b94ca442a99e92bf5f91bc14745af92203a887a40610dd44edda3ae07f9b6c8d63799b2968d87c8da28f1488edef1310d0d12be9bd6319')

    variant('cuda', default=False, description='Build dependencies with support for CUDA')

    depends_on("boost+graph", when='@0.5.0:,master')

    depends_on("flux-core", type=('build', 'link', 'run'))
    depends_on("flux-core+cuda", when='+cuda')
    depends_on("flux-core@0.8.0", when='@0.4.0')
    depends_on("flux-core@0.9.0", when='@0.5.0')
    depends_on("flux-core@0.10.0", when='@0.6.0')
    depends_on("flux-core@master", when='@master')

    # Need autotools when building on master:
    depends_on("autoconf", type='build', when='@master')
    depends_on("automake", type='build', when='@master')
    depends_on("libtool", type='build', when='@master')

    def setup(self):
        pass

    @when('@master')
    def setup(self):
        # Check in case we are running `spack diy` from an "unshallow" clone
        if os.path.exists('.git/shallow'):
            # Allow git-describe to get last tag so flux-version works:
            git = which('git')
            git('fetch', '--unshallow')

    def autoreconf(self, spec, prefix):
        self.setup()
        if not os.path.exists('configure'):
            # Bootstrap with autotools
            bash = which('bash')
            bash('./autogen.sh')

    def configure_args(self):
        # flux-sched's ax_boost is sometimes weird about non-system locations
        # explicitly setting the path guarantees success
        return ['--with-boost={0}'.format(self.spec['boost'].prefix)]

    @property
    def lua_version(self):
        return self.spec['lua'].version.up_to(2)

    @property
    def lua_share_dir(self):
        return os.path.join('share', 'lua', str(self.lua_version))

    @property
    def lua_lib_dir(self):
        return os.path.join('lib', 'lua', str(self.lua_version))

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path(
            'LUA_PATH',
            os.path.join(self.spec.prefix, self.lua_share_dir, '?.lua'),
            separator=';')
        run_env.prepend_path(
            'LUA_CPATH',
            os.path.join(self.spec.prefix, self.lua_lib_dir, '?.so'),
            separator=';')

        run_env.prepend_path('FLUX_MODULE_PATH', self.prefix.lib.flux.modules)
        run_env.prepend_path('FLUX_MODULE_PATH',
                             self.prefix.lib.flux.modules.sched)
        run_env.prepend_path('FLUX_EXEC_PATH', self.prefix.libexec.flux.cmd)
        run_env.prepend_path('FLUX_RC_EXTRA', self.prefix.etc.flux)
