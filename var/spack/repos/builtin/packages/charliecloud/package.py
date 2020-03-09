# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Charliecloud(AutotoolsPackage):
    """Lightweight user-defined software stacks for HPC."""

    homepage = "https://hpc.github.io/charliecloud"
    url      = "https://github.com/hpc/charliecloud/releases/download/v0.9.10/charliecloud-0.9.10.tar.gz"
    git      = "https://github.com/hpc/charliecloud.git"

    version('master', branch='master')
    version('0.13',   sha256='5740bff6e410ca99484c1bdf3dbe834c0f753c846d55c19d6162967a3e2718e0')

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

    def configure_args(self):

        args = []

        if '+docs' not in self.spec:
            args.append('--disable-html')

        if '+builder' not in self.spec:
            args.append('--disable-ch-grow')

        return args
