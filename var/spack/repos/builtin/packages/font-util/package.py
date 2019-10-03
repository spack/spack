# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class FontUtil(AutotoolsPackage):
    """X.Org font package creation/installation utilities and fonts."""

    homepage = "http://cgit.freedesktop.org/xorg/font/util"
    url      = "https://www.x.org/archive/individual/font/font-util-1.3.1.tar.gz"
    version('1.3.2', sha256='f115a3735604de1e852a4bf669be0269d8ce8f21f8e0e74ec5934b31dadc1e76')
    version('1.3.1', 'd153a9af216e4498fa171faea2c82514')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')

    depends_on('bdftopcf', type='build')
    depends_on('mkfontscale', type='build')
    depends_on('mkfontdir', type='build')

    font_baseurl = 'https://www.x.org/archive/individual/font/'
    fonts = []
    # name, version, md5
    fonts_resource = [
        ['encodings', '1.0.4', '1a631784ce204d667abcc329b851670c'],
        ['font-alias', '1.0.3', '535138efe0a95f5fe521be6a6b9c4888'],
        ['font-adobe-100dpi', '1.0.3', 'ba61e7953f4f5cec5a8e69c262bbc7f9'],
        ['font-adobe-75dpi', '1.0.3', '7a414bb661949cec938938fd678cf649'],
        ['font-adobe-utopia-100dpi', '1.0.4',
         '128416eccd59b850f77a9b803681da3c'],
        ['font-adobe-utopia-75dpi', '1.0.4',
         '74c73a5b73c6c3224b299f1fc033e508'],
        ['font-adobe-utopia-type1', '1.0.4',
         'b0676c3495acabad519ee98a94163904'],
        ['font-arabic-misc', '1.0.3', '918457df65ef93f09969c6ab01071789'],
        ['font-bh-100dpi', '1.0.3', '09e63a5608000531179e1ab068a35878'],
        ['font-bh-75dpi', '1.0.3', '88fec4ebc4a265684bff3abdd066f14f'],
        ['font-bh-ttf', '1.0.3', '4ce741ec4edaa11cd38988d355a7578b'],
        ['font-bh-type1', '1.0.3', '62d4e8f782a6a0658784072a5df5ac98'],
        ['font-bh-lucidatypewriter-100dpi', '1.0.3',
         '5f716f54e497fb4ec1bb3a5d650ac6f7'],
        ['font-bh-lucidatypewriter-75dpi', '1.0.3',
         'cab8a44ae329aab7141c7adeef0daf5a'],
        ['font-bitstream-100dpi', '1.0.3', 'c27bf37e9b8039f93bd90b8131ed37ad'],
        ['font-bitstream-75dpi', '1.0.3', '4ff6c5d6aebe69371e27b09ad8313d25'],
        ['font-bitstream-speedo', '1.0.2', 'f0a777b351cf5adefefcf4823e0c1c01'],
        ['font-bitstream-type1', '1.0.3', 'ff91738c4d3646d7999e00aa9923f2a0'],
        ['font-cronyx-cyrillic', '1.0.3', '3119ba1bc7f775c162c96e17a912fe30'],
        ['font-cursor-misc', '1.0.3', 'a0bf70c7e498f1cd8e3fdf6154f2bb00'],
        ['font-daewoo-misc', '1.0.3', '71a7e2796f045c9d217a19c4e6c25bc1'],
        ['font-dec-misc', '1.0.3', '5a9242f6b60ecf2b8c5b158322ca2a40'],
        ['font-ibm-type1', '1.0.3', '2806116e4adcb89d3d5ff5faf65e57c1'],
        ['font-isas-misc', '1.0.3', 'ecc3b6fbe8f5721ddf5c7fc66f73e76f'],
        ['font-jis-misc', '1.0.3', 'c48ee5749ae25075d2c7a6111c195e7b'],
        ['font-micro-misc', '1.0.3', '4de3f0ce500aef85f198c52ace5e66ac'],
        ['font-misc-cyrillic', '1.0.3', 'e7b13da5325f62dd3f630beade6d2656'],
        ['font-misc-ethiopic', '1.0.3', '02ddea9338d9d36804ad38f3daadb55a'],
        ['font-misc-meltho', '1.0.3', '8380696483478449c39b04612f20eea8'],
        ['font-misc-misc', '1.1.2', '23a79b92275375315129b440206c85b9'],
        ['font-mutt-misc', '1.0.3', '6c2de53ba514f720e02af48eef28ff32'],
        ['font-schumacher-misc', '1.1.2', '1f3386a0a690ba8117fc05b501f9f91b'],
        ['font-screen-cyrillic', '1.0.4', '4cadaf2ba4c4d0f4cb9b4e7b8f0a3019'],
        ['font-sun-misc', '1.0.3', '87ce97ce0582e76bc4064a4d4d10db09'],
        ['font-winitzki-cyrillic', '1.0.3',
         '777c667b080b33793528d5abf3247a48'],
        ['font-xfree86-type1', '1.0.4', '89c33c5176cd580de6636ad50ce7777b'],
    ]
    for f_r in fonts_resource:
        f = f_r[0]
        resource(name=f, url=font_baseurl + f + '-' + f_r[1] + '.tar.gz',
                 md5=f_r[2], destination=f, when='fonts=' + f)
        fonts.append(f)

    variant('fonts',
            description='Installs fonts',
            values=fonts,
            default=','.join(fonts),
            multi=True)

    def setup_environment(self, spack_env, run_env):
        spack_env.prepend_path('PATH', self.prefix.bin)
        spack_env.prepend_path('PKG_CONFIG_PATH',
                               join_path(self.prefix.lib, 'pkgconfig'))

    @run_after('install')
    def font_install(self):
        autoconf_args = ['-ifv']
        p = join_path(self.spec['util-macros'].prefix, 'share', 'aclocal')
        autoconf_args.append('--include={0}'.format(p))
        p = join_path(self.spec.prefix, 'share', 'aclocal')
        autoconf_args.append('--include={0}'.format(p))
        fonts = self.spec.variants['fonts'].value
        autoreconf = which('autoreconf')

        for font in fonts:
            fontroot = find(font, '*', recursive=False)
            with working_dir(fontroot[0]):
                autoreconf(*autoconf_args)
                configure = Executable("./configure")
                configure('--prefix={0}'.format(self.prefix))
                make('install')
