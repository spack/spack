# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class OmptOpenmp(CMakePackage):
    """LLVM/Clang OpenMP runtime with OMPT support. This is a fork of the
       OpenMPToolsInterface/LLVM-openmp fork of the official LLVM OpenMP
       mirror.  This library provides a drop-in replacement of the OpenMP
       runtimes for GCC, Intel and LLVM/Clang.

    """
    homepage = "https://github.com/OpenMPToolsInterface/LLVM-openmp"
    url      = "http://github.com/khuck/LLVM-openmp/archive/v0.1.tar.gz"

    version('0.1', '59d6933a2e9b7d1423fb9c7c77d5663f')

    depends_on('cmake@2.8:', type='build')

    conflicts('%gcc@:4.7')

    root_cmakelists_dir = 'runtime'

    @property
    def libs(self):
        return find_libraries('libomp', root=self.prefix, recursive=True)
