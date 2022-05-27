# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *


class FluxCore(AutotoolsPackage):
    """ A next-generation resource manager (pre-alpha) """

    homepage = "https://github.com/flux-framework/flux-core"
    url      = "https://github.com/flux-framework/flux-core/releases/download/v0.8.0/flux-core-0.8.0.tar.gz"
    git      = "https://github.com/flux-framework/flux-core.git"
    tags     = ['radiuss', 'e4s']

    maintainers = ['grondo']

    version('master', branch='master')

    version('0.38.0', sha256='69d150c3d48b5985bca606e1a4de12282eb76233b6b730de1a9fff4136faf65f')
    version('0.37.0', sha256='4779f739da573c02df32a834179cc0c157688f6e82bb4cd2049eb0aa59fffffc')
    version('0.36.0', sha256='04def00d8679a30f51c030791b69a536176725b19dc13e7bfc0df58d0041e975')
    version('0.35.0', sha256='28094c77d0a0d34f8fd71c9b397ae25dd7a4b138aad83f02e75c5a182c76b32b')
    version('0.34.0', sha256='e045b0a4f38d1a08280c2acc7f6e03a06e3715282ff84d9a0d1037b86e0aae33')
    version('0.33.0', sha256='b6f07fb6c0fc36bf300852d71df527778c46517bf61e26c7f54c6978898df2f1')
    version('0.32.0', sha256='fabe4450ce805db547de2675afebc077e4f833d86e00a8c0dd4cd0727b374e30')
    version('0.31.0', sha256='a18251de2ca3522484cacfa986df934ba8f98c54586e18940ce5d2c6147a8a7f')
    version('0.30.0', sha256='e51fde4464140367ae4bc1b44f960675ea0a6f58eede3a561cacd8a11ca3e776')
    version('0.29.0', sha256='c13b40e82d66356e75208a689a495ca01f0a013e2e45ac8ea202ed8224987323')
    version('0.28.0', sha256='9a784def7186b0036091bd8d6d8fe5bc3425ab2927e1465e1c9ad266631c285d')
    version('0.27.0', sha256='abd46d38081ba6b501adb1c111374b39d6ae72ac1aec9fbbf31943a856541d3a', deprecated=True)
    version('0.26.0', sha256='58bfd4742c59364b13cd83214e8f70735952d01793800b149cae056fddfeeff1', deprecated=True)
    version('0.25.0', sha256='3c97e21eaec51e8aa0eaee6aa8eb23246650d102a6b6a5c9943cd69e3c8e1008', deprecated=True)
    version('0.24.0', sha256='fb7e0f9a44d84144a8eaf8f42a5d7e64a4a847861d0ddc2ad8fc4908b5a9190e', deprecated=True)
    version('0.23.0', sha256='918b181be4e27c32f02d5036230212cd9235dc78dc2bde249c3651d6f75866c7', deprecated=True)
    version('0.22.0', sha256='1dd0b737199b8a40f245e6a4e1b3b28770f0ecf2f483d284232080b8b252521f', deprecated=True)
    version('0.21.0', sha256='cc1b7a46d7c1c1a3e99e8861bba0dde89a97351eabd6f1b264788bd76e64c329', deprecated=True)
    version('0.20.0', sha256='2970b9b1c389fc4a381f9e605921ce0eb6aa9339387ea741978bcffb4bd81b6f', deprecated=True)
    version('0.19.0', sha256='f45328a37d989c308c46639a9ed771f47b11184422cf5604249919fbd320d6f5', deprecated=True)
    version('0.18.0', sha256='9784bbca94177a32dbbc99728e8925bf894f3aebaa316961d6ea85df32d59545', deprecated=True)
    version('0.17.0', sha256='3f8c6cb72982028f86a96c0098cacd3a6e9de359fa1cf077380c835a20e7b7f7', deprecated=True)
    version('0.16.0', sha256='1582f7fb4d2313127418c34de7c9ce4f5fef00622d19cedca7bed929f4709f10', deprecated=True)
    version('0.15.0', sha256='51bc2eae69501f802459fc82f191eb5e8ae0b4f7e9e77ac18543a850cc8445f5', deprecated=True)

    # Avoid the infinite symlink issue
    # This workaround is documented in PR #3543
    build_directory = 'spack-build'

    variant('docs', default=False, description='Build flux manpages')
    variant('cuda', default=False, description='Build dependencies with support for CUDA')

    depends_on("libarchive", when="@0.38.0:")
    depends_on("ncurses@6.2", when="@0.32.0:")
    depends_on("libzmq@4.0.4:")
    depends_on("czmq@3.0.1:")
    depends_on("hwloc@1.11.1:1", when="@:0.17.0")
    depends_on("hwloc@1.11.1:", when="@0.17.0:")
    depends_on("hwloc +cuda", when='+cuda')
    # Provide version hints for lua so that the concretizer succeeds when no
    # explicit flux-core version is given. See issue #10000 for details
    depends_on("lua", type=('build', 'run', 'link'))
    depends_on("lua@5.1:5.2", when="@:0.17.0")
    depends_on("lua@5.1:5.3", when="@0.18.0:")
    depends_on("lua-luaposix")
    # `link` dependency on python due to Flux's `pymod` module
    depends_on("python@3.6:", when='@0.17:', type=('build', 'link', 'run'))
    depends_on("python@2.7:", type=('build', 'link', 'run'))
    depends_on("py-cffi@1.1:", type=('build', 'run'))
    depends_on("py-six@1.9:", when='@:0.24', type=('build', 'run'))
    depends_on("py-pyyaml@3.10:", type=('build', 'run'))
    depends_on("py-jsonschema@2.3:", type=('build', 'run'))
    depends_on("jansson")
    depends_on("jansson@2.10:", when="@0.21.0:")
    depends_on("pkgconfig")
    depends_on("lz4")

    depends_on("asciidoc", type='build', when="+docs")
    depends_on("py-docutils", type='build', when="@0.32.0:")

    # Need autotools when building on master:
    depends_on("autoconf", type='build', when='@master')
    depends_on("automake", type='build', when='@master')
    depends_on("libtool", type='build', when='@master')

    # Testing Dependencies
    depends_on("mpich pmi=pmi", type="test")
    depends_on("valgrind", type="test")
    depends_on("jq", type="test")

    # Patch 0.27-0.30 for build errors when czmq built with "draft APIs":
    patch('0001-build-fix-build-errors-with-side-installed-0MQ.patch',
          when='@0.27.0:0.30.0')

    def url_for_version(self, version):
        '''
        Flux uses a fork of ZeroMQ's Collective Code Construction Contract
        (https://flux-framework.readthedocs.io/projects/flux-rfc/en/latest/spec_1.html).
        This model requires a repository fork for every stable release that has
        patch releases.  For example, 0.8.0 and 0.9.0 are both tags within the
        main repository, but 0.8.1 and 0.9.5 would be releases on the v0.8 and
        v0.9 forks, respectively.

        Rather than provide an explicit URL for each patch release, make Spack
        aware of this repo structure.
        '''
        if version[-1] == 0:
            url = "https://github.com/flux-framework/flux-core/releases/download/v{0}/flux-core-{0}.tar.gz"
        else:
            url = "https://github.com/flux-framework/flux-core-v{1}/releases/download/v{0}/flux-core-{0}.tar.gz"
        return url.format(version.up_to(3), version.up_to(2))

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

    def setup_build_environment(self, env):
        #  Ensure ./fluxometer.lua can be found during flux's make check
        env.append_path('LUA_PATH', './?.lua', separator=';')

    def setup_run_environment(self, env):
        env.prepend_path(
            'LUA_PATH',
            os.path.join(self.spec.prefix, self.lua_share_dir, '?.lua'),
            separator=';')
        env.prepend_path(
            'LUA_CPATH',
            os.path.join(self.spec.prefix, self.lua_lib_dir, '?.so'),
            separator=';')
        env.prepend_path(
            'PYTHONPATH',
            os.path.join(
                self.spec.prefix.lib,
                "python{0}".format(self.spec['python'].version.up_to(2)),
                "site-packages"),
        )
        env.prepend_path('FLUX_MODULE_PATH', self.prefix.lib.flux.modules)
        env.prepend_path('FLUX_EXEC_PATH', self.prefix.libexec.flux.cmd)
        env.prepend_path(
            'FLUX_CONNECTOR_PATH',
            self.prefix.lib.flux.connectors
        )

    def configure_args(self):
        args = ['--enable-pylint=no']
        if '+docs' not in self.spec:
            args.append('--disable-docs')
        return args

    def flag_handler(self, name, flags):
        if name == 'cflags':
            # https://github.com/flux-framework/flux-core/issues/3482
            if self.spec.satisfies('%gcc@10:') and \
               self.spec.satisfies('@0.23.0:0.23'):
                if flags is None:
                    flags = []
                flags.append('-Wno-error=stringop-truncation')

            if self.spec.satisfies('%gcc@8:') and \
               self.spec.satisfies('@0.23.0'):
                if flags is None:
                    flags = []
                flags.append('-Wno-error=maybe-uninitialized')

        return (flags, None, None)
