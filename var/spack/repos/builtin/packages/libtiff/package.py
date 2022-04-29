# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class Libtiff(AutotoolsPackage):
    """LibTIFF - Tag Image File Format (TIFF) Library and Utilities."""

    homepage = "http://www.simplesystems.org/libtiff/"
    url      = "https://download.osgeo.org/libtiff/tiff-4.1.0.tar.gz"

    maintainers = ['adamjstewart']

    version('4.3.0',  sha256='0e46e5acb087ce7d1ac53cf4f56a09b221537fc86dfc5daaad1c2e89e1b37ac8')
    version('4.2.0',  sha256='eb0484e568ead8fa23b513e9b0041df7e327f4ee2d22db5a533929dfc19633cb')
    version('4.1.0',  sha256='5d29f32517dadb6dbcd1255ea5bbc93a2b54b94fbf83653b4d65c7d6775b8634')
    version('4.0.10', sha256='2c52d11ccaf767457db0c46795d9c7d1a8d8f76f68b0b800a3dfe45786b996e4')
    version('4.0.9',  sha256='6e7bdeec2c310734e734d19aae3a71ebe37a4d842e0e23dbb1b8921c0026cfcd')
    version('4.0.8',  sha256='59d7a5a8ccd92059913f246877db95a2918e6c04fb9d43fd74e5c3390dac2910')
    version('4.0.7',  sha256='9f43a2cfb9589e5cecaa66e16bf87f814c945f22df7ba600d63aac4632c4f019')
    version('4.0.6',  sha256='4d57a50907b510e3049a4bba0d7888930fdfc16ce49f1bf693e5b6247370d68c')
    version('3.9.7',  sha256='f5d64dd4ce61c55f5e9f6dc3920fbe5a41e02c2e607da7117a35eb5c320cef6a')

    variant('zlib', default=False, description='Enable Zlib usage')
    variant('libdeflate', default=False, description='Enable libdeflate usage')
    variant('pixarlog', default=False, description='Enable support for Pixar log-format algorithm')
    variant('jpeg', default=False, description='Enable IJG JPEG library usage')
    variant('old-jpeg', default=False, description='Enable support for Old JPEG compression')
    variant('jpeg12', default=False, description='Enable libjpeg 8/12bit dual mode')
    variant('jbig', default=False, description='Enable JBIG-KIT usage')
    variant('lerc', default=False, description='Enable liblerc usage')
    variant('lzma', default=False, description='Enable liblzma usage')
    variant('zstd', default=False, description='Enable libzstd usage')
    variant('webp', default=False, description='Enable libwebp usage')

    depends_on('zlib', when='+zlib')
    depends_on('zlib', when='+pixarlog')
    depends_on('jpeg@5:', when='+jpeg')
    depends_on('jbigkit', when='+jbig')
    depends_on('lerc', when='+lerc')
    depends_on('xz', when='+lzma')
    depends_on('zstd@1:', when='+zstd')
    depends_on('libwebp', when='+webp')

    conflicts('+libdeflate', when='~zlib')
    conflicts('+libdeflate', when='@:4.1')
    conflicts('+jpeg12', when='~jpeg')
    conflicts('+jpeg12', when='@:3')
    conflicts('+lerc', when='~zlib')
    conflicts('+lerc', when='@:4.2')
    conflicts('+lzma', when='@:3')
    conflicts('+zstd', when='@:4.0.9')
    conflicts('+webp', when='@:4.0.9')

    # https://gitlab.com/libtiff/libtiff/-/merge_requests/243
    patch('no-include-root.patch', when='@4.3.0 platform=darwin')

    depends_on('gl', when='@4.3.0 platform=darwin')
    depends_on('glu', when='@4.3.0 platform=darwin')
    depends_on('freeglut', when='@4.3.0 platform=darwin')
    depends_on('libsm', when='@4.3.0 platform=darwin')
    depends_on('libice', when='@4.3.0 platform=darwin')
    depends_on('libxi', when='@4.3.0 platform=darwin')
    depends_on('libx11', when='@4.3.0 platform=darwin')

    depends_on('automake', when='@4.3.0 platform=darwin', type='build')
    depends_on('autoconf', when='@4.3.0 platform=darwin', type='build')
    depends_on('libtool', when='@4.3.0 platform=darwin', type='build')
    depends_on('m4', when='@4.3.0 platform=darwin', type='build')

    @property
    def force_autoreconf(self):
        return self.spec.satisfies('@4.3.0 platform=darwin')

    def patch(self):
        # Remove flags not recognized by the NVIDIA compiler
        if self.spec.satisfies('%nvhpc@:20.11'):
            filter_file('vl_cv_prog_cc_warnings="-Wall -W"',
                        'vl_cv_prog_cc_warnings="-Wall"', 'configure')

    def configure_args(self):
        args = []
        args += self.enable_or_disable('zlib')
        if self.spec.satisfies('@4.2:'):
            args += self.enable_or_disable('libdeflate')
        args += self.enable_or_disable('pixarlog')
        args += self.enable_or_disable('jpeg')
        args += self.enable_or_disable('old-jpeg')
        if self.spec.satisfies('@4:'):
            args += self.enable_or_disable('jpeg12')
        args += self.enable_or_disable('jbig')
        if self.spec.satisfies('@4.3:'):
            args += self.enable_or_disable('lerc')
        if self.spec.satisfies('@4:'):
            args += self.enable_or_disable('lzma')
        if self.spec.satisfies('@4.0.10:'):
            args += self.enable_or_disable('zstd')
            args += self.enable_or_disable('webp')
        return args
