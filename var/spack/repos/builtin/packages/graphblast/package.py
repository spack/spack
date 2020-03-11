# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Graphblast(MakefilePackage, CudaPackage):
    """High-Performance Linear Algebra-based Graph Primitives on GPUs"""

    homepage    = "https://github.com/gunrock/graphblast"
    git         = "https://github.com/gunrock/graphblast.git"

    version('master', submodules=True)

    variant('cuda', default=True)

    depends_on('boost +program_options')

    # This package confirmed to compile with gcc <= 4.9.4, boost@1.58
    # TODO: the package doesn't compile as CMakePackage currently
    # once that is fixed it should be converted to a CMakePackage type.

    def install(self, spec, prefix):
        install_tree(self.build_directory, self.prefix)

    @run_before('build')
    def set_cudarch(self):
        if cuda_arch is not None:
            makefile = filterFile('common.mk')
            makefile.filter(r'CUDA_ARCH = 35', 'CUDA_ARCH = ' +
                            spec.variants['cuda_arch'].value)
