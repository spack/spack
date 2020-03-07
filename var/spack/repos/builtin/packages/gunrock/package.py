# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gunrock(CMakePackage, CudaPackage):
    """High-Performance Graph Primitives on GPUs"""

    homepage = "https://gunrock.github.io/docs/"
    git      = "https://github.com/gunrock/gunrock.git"

    version('master',   submodules=True)
    version('1.1',      submodules=True, tag='v1.1')
    version('1.0',      submodules=True, tag='v1.0')
    version('0.5.1',    submodules=True, tag='v0.5.1')
    version('0.5',      submodules=True, tag='v0.5')
    version('0.4',      submodules=True, tag='v0.4')
    version('0.3.1',    submodules=True, tag='v0.3.1')
    version('0.3',      submodules=True, tag='v0.3')
    version('0.2',      submodules=True, tag='v0.2')
    version('0.1',      submodules=True, tag='v0.1')

    depends_on('cuda')

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            install_tree('bin', prefix.bin)
            install_tree('lib', prefix.lib)
