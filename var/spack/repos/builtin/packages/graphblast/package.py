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

    # This package is confirmed to compile with gcc <= 5.4.0,boost@1.58,cuda@9.2
    # TODO: the package doesn't compile as CMakePackage currently
    # once that is fixed it should be converted to a CMakePackage type.

    conflicts('%gcc@5.5.0:')

    conflicts('cuda_arch=none', when='+cuda', msg='Must specify CUDA compute capabilities of your GPU. See "spack info graphblast"')

    def install(self, spec, prefix):
        install_tree(self.build_directory, self.prefix)

    @run_before('build')
    def set_cudarch(self):
        cuda_arch_list = self.spec.variants['cuda_arch'].value
        arches='ARCH = '
        for i in cuda_arch_list:
            arches = arches + ' -gencode arch=compute_{0},code=compute_{0}'.format(i)
        makefile = FileFilter('common.mk')
        makefile.filter(r'^ARCH =.*', arches)
