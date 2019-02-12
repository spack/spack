# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class FluxSched(AutotoolsPackage):
    """ A scheduler for flux-core (pre-alpha) """

    homepage = "https://github.com/flux-framework/flux-sched"
    url      = "https://github.com/flux-framework/flux-sched/releases/download/v0.5.0/flux-sched-0.5.0.tar.gz"
    git      = "https://github.com/flux-framework/flux-sched.git"

    version('master', branch='master')
    version('0.7.0', sha256='69267a3aaacaedd9896fd90cfe17aef266cba4fb28c77f8123d95a31ce739a7b')
    version('0.6.0', '8aad185949038c7fb6b277e6a8282947917084ebbec5c5bf0ee3a81a0dcdbe41ba18b1df837c669ae7b48ca5f1e492a5172bffa6b9feb4dda1c6a7a85abed4e8')
    version('0.5.0', 'a9835c9c478aa41123a4e12672500052228aaf1ea770f74cb0901dbf4a049bd7d329e99d8d3484e39cfed1f911705030b2775dcfede39bc8bea59c6afe2549b1')
    version('0.4.0', '82732641ac4594ffe9b94ca442a99e92bf5f91bc14745af92203a887a40610dd44edda3ae07f9b6c8d63799b2968d87c8da28f1488edef1310d0d12be9bd6319')

    # Avoid the infinite symlink issue
    # This workaround is documented in PR #3543
    build_directory = 'spack-build'

    variant('cuda', default=False, description='Build dependencies with support for CUDA')

    depends_on("boost+graph@1.53.0,1.59.0:", when='@0.5.0:,master')
    depends_on("py-pyyaml", when="@0.7.0:,master")
    depends_on("libxml2@2.9.1:", when="@0.6.0,master")
    depends_on("yaml-cpp", when="@0.7.0:")
    depends_on("libuuid")

    depends_on("flux-core", type=('build', 'link', 'run'))
    depends_on("flux-core+cuda", when='+cuda')
    depends_on("flux-core@0.8.0", when='@0.4.0')
    depends_on("flux-core@0.9.0", when='@0.5.0')
    depends_on("flux-core@0.10.0", when='@0.6.0')
    depends_on("flux-core@0.11.0", when='@0.7.0')
    depends_on("flux-core@master", when='@master')

    # Need autotools when building on master:
    depends_on("autoconf", type='build', when='@master')
    depends_on("automake", type='build', when='@master')
    depends_on("libtool", type='build', when='@master')

    def setup(self):
        pass

    @when('@master')
    def setup(self):
        with working_dir(self.stage.source_path):
            # Allow git-describe to get last tag so flux-version works:
            git = which('git')
            git('fetch', '--unshallow')
            git("config", "remote.origin.fetch",
                "+refs/heads/*:refs/remotes/origin/*")
            git('fetch', 'origin')

    def autoreconf(self, spec, prefix):
        self.setup()
        if os.path.exists(self.configure_abs_path):
            return
        # make sure configure doesn't get confused by the staging symlink
        with working_dir(self.configure_directory):
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
