# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class Vacuumms(CMakePackage):
    """VACUUMMS: (Void Analysis Codes and Unix Utilities for Molecular Modeling and
    Simulation) is a collection of research codes for the compuational analysis of
    free volume in molecular structures, including the generation of code for the
    production of high quality ray-traced images and videos. Note that production of the
    images from the generated code is considered post-processing and requires POVRay
    and feh (on X11 systems) as post-processing dependencies. VACUUMMS has been tested
    under Linux on x86_64 and ARM64. Please submit questions, pull requests, and bug
    reports via github. https://dl.acm.org/doi/abs/10.1145/2335755.2335826"""

    homepage = "https://github.com/frankwillmore/VACUUMMS"
    url      = "https://github.com/frankwillmore/VACUUMMS/archive/refs/tags/v1.0.0.tar.gz"
    git      = "https://github.com/frankwillmore/VACUUMMS.git"

    maintainers = ['frankwillmore']

    version('master', branch='master')
    version('1.1.1', tag='v1.1.1')
    version('1.0.0', 'c18fe52f5041880da7f50d3808d37afb3e9c936a56f80f67838d045bf7af372f', deprecated=True)

    variant('tiff', default=False, description='Build TIFF utilities')
    variant('cuda', default=False, description='Build CUDA applications and utilities')

    depends_on('libtiff', type=('link', 'run'), when='+tiff')
    depends_on('cuda', type=('link', 'run'), when='+cuda')
    depends_on('libx11', type=('link', 'run'))
    depends_on('libxext', type=('link', 'run'))
    depends_on('libsm', type=('link', 'run'))
    depends_on('libice', type=('link', 'run'))

    def cmake_args(self):
        return [self.define_from_variant('BUILD_CUDA_COMPONENTS', 'cuda'),
                self.define_from_variant('BUILD_TIFF_UTILS', 'tiff')]
