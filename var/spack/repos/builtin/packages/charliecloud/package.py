# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Charliecloud(AutotoolsPackage):
    """Lightweight user-defined software stacks for HPC."""

    maintainers = ['j-ogas']
    homepage = "https://hpc.github.io/charliecloud"
    url      = "https://github.com/hpc/charliecloud/releases/download/v0.14/charliecloud-0.9.10.tar.gz"
    git      = "https://github.com/hpc/charliecloud.git"

    version('master', branch='master')
    version('0.14',   sha256='4ae23c2d6442949e16902f9d5604dbd1d6059aeb5dd461b11fc5c74d49dcb194')

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

    # bash automated testing harness (bats)
    depends_on('bats@0.4.0', type='test')

    def configure_args(self):

        args = []

        if '+docs' in self.spec:
            args.append('--enable-html')
        else:
            args.append('--disable-html')

        return args
