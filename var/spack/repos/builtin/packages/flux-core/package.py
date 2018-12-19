# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class FluxCore(AutotoolsPackage):
    """ A next-generation resource manager (pre-alpha) """

    homepage = "https://github.com/flux-framework/flux-core"
    url      = "https://github.com/flux-framework/flux-core/releases/download/v0.8.0/flux-core-0.8.0.tar.gz"
    git      = "https://github.com/flux-framework/flux-core.git"

    version('master',  branch='master')
    version('0.10.0', 'a84a1ed53a69c805c253bc940540cbf667a059b2008fd2a6a9bb890a985ead08e88dcbba68c01567f887357306fbfded41b93cc33edfa7809955ba5ba5870284')
    version('0.9.0',  '70eaec1005aa49e8d8cf397570789cebedfb5d917efe963390d456ee4c473eefb15b0c81ea83f60a1fd057fe7be356bbafdebcae64b499844d194c48f6aefa05')
    version('0.8.0',  'b0fec05acedc530bcdf75b2477ac22f39d2adddc7af8ff76496208a5e1e8185b1b4a18677871d95c3cfbf34b05f391953651200917fe029931f4e2beb79d70df')

    # Avoid the infinite symlink issue
    # This workaround is documented in PR #3543
    build_directory = 'spack-build'

    variant('docs', default=False, description='Build flux manpages')
    variant('cuda', default=False, description='Build dependencies with support for CUDA')

    depends_on("zeromq@4.0.4:")
    depends_on("czmq")
    depends_on("czmq@2.2:3.99", when="@0.1:0.6.99")
    depends_on("czmq@3.0.1:", when="@0.7:,master")
    depends_on("hwloc@1.11.1:1.99")
    depends_on("hwloc +cuda", when='+cuda')
    # Provide version hints for lua so that the concretizer succeeds when no
    # explicit flux-core version is given. See issue #10000 for details
    depends_on("lua@5.1:5.2.99", type=('build', 'run', 'link'))
    depends_on("lua@5.1:5.1.99", when="@0.1.0:0.9.0")
    depends_on("lua@5.1:5.2.99", when="@0.10.0:,master")
    depends_on("lua-luaposix")
    depends_on("munge", when="@0.1.0:0.10.0")
    depends_on("libuuid")
    depends_on("python", type=('build', 'run'))
    depends_on("python@2.7:2.99", when="@0.1.0:0.10.0")
    depends_on("python@2.7:", when="@0.11.0:,master")
    depends_on("py-cffi", type=('build', 'run'))
    depends_on("py-six", type=('build', 'run'), when="@0.11.0:,master")
    depends_on("jansson")
    depends_on("yaml-cpp")
    depends_on("lz4", when="@0.11.0:,master")

    # versions up to 0.8.0 uses pylint to check Flux's python binding
    # later versions provide a configure flag and disable the check by default
    depends_on("py-pylint", when='@:0.8.0', type='build')

    depends_on("asciidoc", type='build', when="+docs")

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
        if not os.path.exists('configure'):
            # Bootstrap with autotools
            bash = which('bash')
            bash('./autogen.sh')

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
        #  Ensure ./fluxometer.lua can be found during flux's make check
        spack_env.append_path('LUA_PATH', './?.lua', separator=';')

        run_env.prepend_path(
            'LUA_PATH',
            os.path.join(self.spec.prefix, self.lua_share_dir, '?.lua'),
            separator=';')
        run_env.prepend_path(
            'LUA_CPATH',
            os.path.join(self.spec.prefix, self.lua_lib_dir, '?.so'),
            separator=';')
        run_env.prepend_path(
            'PYTHONPATH',
            os.path.join(
                self.spec.prefix.lib,
                "python{0}".format(self.spec['python'].version.up_to(2)),
                "site-packages"),
        )
        run_env.prepend_path('FLUX_MODULE_PATH', self.prefix.lib.flux.modules)
        run_env.prepend_path('FLUX_EXEC_PATH', self.prefix.libexec.flux.cmd)
        run_env.prepend_path('FLUX_RC_PATH', self.prefix.etc.flux)

    def configure_args(self):
        args = ['--enable-pylint=no']
        if '+docs' not in self.spec:
            args.append('--disable-docs')
        return args
