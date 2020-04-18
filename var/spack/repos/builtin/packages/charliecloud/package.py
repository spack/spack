# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Charliecloud(AutotoolsPackage):
    """Lightweight user-defined software stacks for HPC."""

    maintainers = ['j-ogas']
    homepage = "https://hpc.github.io/charliecloud"
    url      = "https://github.com/hpc/charliecloud/releases/download/v0.14/charliecloud-0.14.tar.gz"
    git      = "https://github.com/hpc/charliecloud.git"

    version('master', branch='master')
    version('0.15',   sha256='2163420d43c934151c4f44a188313bdb7f79e576d5a86ba64b9ea45f784b9921')
    version('0.14',   sha256='4ae23c2d6442949e16902f9d5604dbd1d6059aeb5dd461b11fc5c74d49dcb194')
    version('0.13',   sha256='5740bff6e410ca99484c1bdf3dbe834c0f753c846d55c19d6162967a3e2718e0')
    version('0.12',   sha256='8a90f33406905cee935b5673a1159232b0b71845f4b6a26d28ca88f5d3f55891')
    version('0.11',   sha256='942d3c7a74c978fd7420cb2b255e618f4f0acaafb6025160bc3a4deeb687ef3c')
    version('0.10',   sha256='5cf00b170e7568750ca0b828c43c0857c39674860b480d757057450d69f1a21e')
    version('0.9.10', sha256='44e821b62f9c447749d3ed0d2b2e44d374153058814704a5543e83f42db2a45a')
    version('0.9.9',  sha256='7f83d25dd77b90232f8529c83c689e565117414b7be996dbd2dd4bf3220b2166')
    version('0.9.8',  sha256='330071ef9e597df75278b8c870af3cd1acfdf6d702ceae25071c7cb8cd5d84b5')

    depends_on('m4',       type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')

    depends_on('python@3.5:',    type='run')
    depends_on('py-lark-parser', type='run')
    depends_on('py-requests',    type='run')

    # man pages and html docs variant
    variant('docs', default=False, description='Build man pages and html docs')
    depends_on('rsync',               type='build', when='+docs')
    depends_on('py-sphinx',           type='build', when='+docs')
    depends_on('py-sphinx-rtd-theme', type='build', when='+docs')

    conflicts('platform=darwin', msg='This package does not build on macOS')

    # bash automated testing harness (bats)
    depends_on('bats@0.4.0', type='test')

    def configure_args(self):

        args = []

        if '+docs' in self.spec:
            args.append('--enable-html')
        else:
            args.append('--disable-html')

        return args
