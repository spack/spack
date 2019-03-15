# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class Embree(CMakePackage):
    """High-performance ray tracing kernel"""

    homepage = "https://embree.github.io/"
    url = "https://github.com/embree/embree/archive/v3.5.1.tar.gz"
    generator = 'Ninja'

    version('3.5.2', sha256='245af8820a820af94679fa1d43a05a9c825451be0d603b6165229556adf49517')

    depends_on('cmake@2.8.11:', type='build')
    depends_on('ispc', type='build')
    depends_on('ninja', type='build')

    def cmake_args(self):
        return ['-DEMBREE_TUTORIALS=OFF']
