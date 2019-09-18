# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Charliecloud(MakefilePackage):
    """Lightweight user-defined software stacks for HPC."""

    homepage = "https://hpc.github.io/charliecloud"
    url      = "https://github.com/hpc/charliecloud/releases/download/v0.9.10/charliecloud-0.9.10.tar.gz"
    git      = "https://github.com/hpc/charliecloud.git"

    version('master', branch='master')
    version('0.11',   sha256='942d3c7a74c978fd7420cb2b255e618f4f0acaafb6025160bc3a4deeb687ef3c')
    version('0.10',   sha256='5cf00b170e7568750ca0b828c43c0857c39674860b480d757057450d69f1a21e')
    version('0.9.10', sha256='44e821b62f9c447749d3ed0d2b2e44d374153058814704a5543e83f42db2a45a')
    version('0.9.9',  sha256='2624c5a0b19a01c9bca0acf873ceeaec401b9185a23e9108fadbcee0b9d74736')
    version('0.9.8',  sha256='903bcce05b19501b5524ef57a929d2f4c6ddeacb0e8443fcb2fe6963e2f29229')
    version('0.9.7',  sha256='ec80a4b9bef3a2161a783e11d99cc58e09a32dfbc8a6234c8f7ce7fa76e2f62d')
    version('0.9.6',  sha256='50e20d5e2a3710cd06e7c999db22495b07ef0fb15ffbc0af3bccac5387f0fddb')
    version('0.9.3',  sha256='f1bf032377b8845bc9a93b8a4fad6386161e35900223c0acc61d1f3aa3a87bc7')
    version('0.9.2',  sha256='8d0e4804d412beef720a66f886a0a78bce42f3269e880ebf11f602581f8047d4')
    version('0.9.1',  sha256='8e69150a271285da71ece7a09b48251ef6593f72207c5126741d9976aa737d95')
    version('0.9.0',  sha256='7e74cb16e31fd9d502198f7509bab14d1049ec68ba90b15e277e76f805db9458')
    version('0.2.4',  'b112de661c2c360174b42c99022c1967')

    depends_on('python@3.4:', type=('build', 'run'))

    # experimental builder (ch-grow)
    variant('builder', default=False, description='Bundle dependencies for unprivileged builder (ch-grow)')
    depends_on('py-lark-parser', type='run', when='+builder')
    depends_on('skopeo', type='run', when='+builder')
    depends_on('umoci', type='run', when='+builder')

    # man pages and html docs
    variant('docs', default=False, description='Build man pages and html docs')
    depends_on('rsync',               type='build', when='+docs')
    depends_on('py-sphinx',           type='build', when='+docs')
    depends_on('py-sphinx-rtd-theme', type='build', when='+docs')

    # bash automated testing harness (bats)
    depends_on('bats@0.4.0', type='test')

    def url_for_version(self, version):
        if version >= Version('0.9.8'):
            url = "https://github.com/hpc/charliecloud/releases/download/v{0}/charliecloud-{0}.tar.gz"
        else:
            url = "https://github.com/hpc/charliecloud/archive/v{0}.tar.gz"
        return url.format(version)

    @property
    def install_targets(self):
        return ['install', 'PREFIX=%s' % self.prefix]
