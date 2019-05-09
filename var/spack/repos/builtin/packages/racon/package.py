# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Racon(CMakePackage):
    """Ultrafast consensus module for raw de novo genome assembly of long
     uncorrected reads."""

    homepage = "https://github.com/isovic/racon"
    url      = "https://github.com/isovic/racon/releases/download/1.2.1/racon-v1.2.1.tar.gz"

    version('1.3.2', sha256='7c99380a0f1091f5ee138b559e318d7e9463d3145eac026bf236751c2c4b92c7')
    version('1.3.1', sha256='7ce3b1ce6abdb6c6a63d50755b1fc55d5a4d2ab8f86a1df81890d4a7842d9b75')
    version('1.3.0', 'e00d61f391bce2af20ebd2a3aee1e05a')
    version('1.2.1', '7bf273b965a5bd0f41342a9ffe5c7639')

    depends_on('cmake@3.2:', type='build')
    depends_on('python', type='build')

    conflicts('%gcc@:4.7')
    conflicts('%clang@:3.1')

    def cmake_args(self):
        args = ['-Dracon_build_wrapper=ON']
        return args

    def install(self, spec, prefix):
        install_tree('spack-build/bin', prefix.bin)
        install_tree('spack-build/lib', prefix.lib)
