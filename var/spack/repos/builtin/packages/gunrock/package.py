# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gunrock(CMakePackage, CudaPackage):
    """High-Performance Graph Primitives on GPUs"""

    homepage = "https://gunrock.github.io/docs/"
    url      = "https://github.com/gunrock/gunrock/archive/v1.1.tar.gz"
    git      = "https://github.com/gunrock/gunrock.git"

    version('develop', git=git, submodules=True)
    version('1.1', git=git, submodules=True, tag='v1.1', preferred=True)
    version('1.0', git=git, submodules=True, tag='v1.0')
    version('0.5.1', git=git, submodules=True, tag='v0.5.1')
    version('0.5', git=git, submodules=True, tag='v0.5')
    version('0.4', git=git, submodules=True, tag='v0.4')
    version('0.3.1', git=git, submodules=True, tag='v0.3.1')
    version('0.3', git=git, submodules=True, tag='v0.3')
    version('0.2', git=git, submodules=True, tag='v0.2')
    version('0.1', git=git, submodules=True, tag='v0.1')

    depends_on('cuda')

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            install_tree('bin', prefix.bin)
            install_tree('lib', prefix.lib)
