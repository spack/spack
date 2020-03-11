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

    depends_on('boost +program_options')
    depends_on('gcc@:4')

    def install(self, spec, prefix):
        install_tree(self.build_directory, self.prefix)
