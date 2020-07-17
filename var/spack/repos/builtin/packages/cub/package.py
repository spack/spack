# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cub(Package):
    """CUB is a C++ header library of cooperative threadblock primitives
    and other utilities for CUDA kernel programming."""

    homepage = "https://nvlabs.github.com/cub"
    url      = "https://github.com/NVlabs/cub/archive/v1.7.1.zip"
    git      = "https://github.com/NVlabs/cub.git"

    version('1.8.0', sha256='6bfa06ab52a650ae7ee6963143a0bbc667d6504822cbd9670369b598f18c58c3')
    version('1.7.5', sha256='8f8e0b101324a9839003ff1154c8439137cd38b2039f403a92e76d5c52cee23f')
    version('1.7.4', sha256='20a1a39fd97e5da7f40f5f2e7fd73fd2ea59f9dc4bb8a6c5f228aa543e727e31')
    version('1.7.3', sha256='b7ead9e291d34ffa8074243541c1380d63be63f88de23de8ee548db573b72ebe')
    version('1.7.2', sha256='09b478d4df8e6c62f8425d23ade9e2a52bc279a20057c7d22ce2160f3923764a')
    version('1.7.1', sha256='50b8777b83093fdfdab429a61fccdbfbbb991b3bbc08385118e5ad58e8f62e1d')

    def install(self, spec, prefix):
        mkdirp(prefix.include)
        install_tree('cub', join_path(prefix.include, 'cub'))
