# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import re
import shutil


class Fzf(MakefilePackage):
    """fzf is a general-purpose command-line fuzzy finder."""

    homepage = "https://github.com/junegunn/fzf"
    url      = "https://github.com/junegunn/fzf/archive/0.17.5.tar.gz"

    executables = ['^fzf$']

    version('0.25.1',   sha256='22ffce1a9fd4b7a1d53ec5fc9c36b0abc5a61eccfa89898149b6d4e3871e637d')
    version('0.25.0',   sha256='70996bb38b3f74c29d5f663e4f19d7cd5e2c231835090bdd51044a3400dafa69')
    version('0.24.4',   sha256='bbb200f99e183b2aa587b4b968abbbcbc7c45d01726a5bf059dceb3f260798bd')
    version('0.24.3',   sha256='68d3fdf1aaed9813986c6e501602297f8fdf1c428eee06dc65ebda6e8285c308')
    version('0.24.2',   sha256='6a053adc620d1adc5aead7c80596db748f2f9f251b75e3c97783f96cc96c5b68')
    version('0.24.1',   sha256='211c438fffcd4751c24a7f36101030a671d350f8926bffe1f663f3efacc45f6a')
    version('0.24.0-1', sha256='d61fb19048467c2bb4901d6d032e98b4879d85e9b322e0056260a598815f9c00')
    version('0.24.0',   sha256='8cf8435e64b418646c309c9ddc3c8fe34b2a0fff73d1b7b9a69f3c587bf012fb')
    version('0.23.1',   sha256='07576e47d2d446366eb7806fd9f825a2340cc3dc7f799f1f53fe038ca9bf30f6')
    version('0.22.0',   sha256='3090748bb656333ed98490fe62133760e5da40ba4cd429a8142b4a0b69d05586')
    version('0.17.5',   sha256='de3b39758e01b19bbc04ee0d5107e14052d3a32ce8f40d4a63d0ed311394f7ee')
    version('0.17.4',   sha256='a4b009638266b116f422d159cd1e09df64112e6ae3490964db2cd46636981ff0')
    version('0.17.3',   sha256='e843904417adf926613431e4403fded24fade56269446e92aac6ff1db86af81e')
    version('0.17.1',   sha256='9c881e55780c0f56b5a30b87df756634d853bfd3938e7e53cb2df6ed63aa84a7')
    version('0.17.0-2', sha256='a084415231b452b92a6b8aa87a69c0c02ee59bfe95774bf0d4fcc9a6251ece20')
    version('0.17.0',   sha256='23569faf64cd6831c09aad7030c8b4bace0eb7a979c580b33cc4e4f9ff303e29')
    version('0.16.11',  sha256='e3067d4ad58d7be51eba9a35c06518cd7145c0cc297882796c7e40285f268a99')
    version('0.16.10',  sha256='a6b9d8abcba4239d30201cc7911e9c305a5cd750081ce5cd389f8e7425f4dc93')
    version('0.16.9',   sha256='dd9434576c68313481613a5bd52dbf623eee37a5c87f7bb66ca71ac8add5ff94')
    version('0.16.8',   sha256='daef99f67cff3dad261dbcf2aef995bb78b360bcc7098d7230cb11674e1ee1d4')

    depends_on('go@1.11:', type='build')

    variant('vim', default=False, description='Install vim plugins for fzf')

    patch("github_mirrors.patch", when='@:0.17.5')

    @classmethod
    def determine_version(cls, exe):
        candidate = Executable(exe)('--version', output=str, error=str)
        match = re.match(r'(^[\d.]+)', candidate)
        return match.group(1) if match else None

    @when('@:0.17.5')
    def patch(self):
        glide_home = os.path.join(self.build_directory, 'glide_home')
        os.environ['GLIDE_HOME'] = glide_home
        shutil.rmtree(glide_home, ignore_errors=True)
        os.mkdir(glide_home)

    def install(self, spec, prefix):
        make('install')

        mkdir(prefix.bin)
        install('bin/fzf', prefix.bin)

    @run_after('install')
    def post_install(self):
        if '+vim' in self.spec:
            mkdir(self.prefix.plugin)
            install('plugin/fzf.vim', self.prefix.plugin)
