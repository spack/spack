# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Fpchecker(CMakePackage):
    """FPChecker (Floating-Point Checker) is a dynamic analysis tool
       to detect floating-point errors in HPC applications.
    """

    homepage = "https://fpchecker.org/"
    url      = "https://github.com/LLNL/FPChecker/archive/refs/tags/v0.3.2.tar.gz"

    maintainers = ['ilagunap']

    version('0.3.2', sha256='aa591962734a3027c97ec050e126166912aaecfc2743b2d739eff844ea7418db')

    depends_on('llvm@12.0.1')
    depends_on('cmake@3.4:', type='build')
    depends_on('python@3:', type='run')

    conflicts('%intel', 
          msg='FPChecker cannot be built with Intel ICC. Please use LLVM.')
    conflicts('%gcc', 
          msg='FPChecker cannot be built with GCC. Please use LLVM.')
    conflicts('%pgi', 
          msg='FPChecker cannot be built with PGI. Please use LLVM.')

    def cmake_args(self):
        args = ['-DCMAKE_C_COMPILER=clang', '-DCMAKE_CXX_COMPILER=clang++']
        return args
