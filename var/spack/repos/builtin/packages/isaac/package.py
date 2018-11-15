# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Isaac(CMakePackage):
    """In Situ Animation of Accelerated Computations: Header-Only Library"""

    homepage = "http://computationalradiationphysics.github.io/isaac/"
    url      = "https://github.com/ComputationalRadiationPhysics/isaac/archive/v1.3.0.tar.gz"
    git      = "https://github.com/ComputationalRadiationPhysics/isaac.git"

    maintainers = ['ax3l']

    version('develop', branch='dev')
    version('master', branch='master')
    version('1.4.0', '3ad05c8fad4673366077204c5d39285f')
    version('1.3.3', '7aeebaf0c5a77e2cb9bea066750e369b')
    version('1.3.2', 'c557daa74de52fd79e734c9758fca38b')
    version('1.3.1', '7fe075f9af68d05355eaba0e224f20ca')
    version('1.3.0', 'c8a794da9bb998ef0e75449bfece1a12')

    variant('cuda', default=True,
            description='Generate CUDA kernels for Nvidia GPUs')
    # variant('alpaka', default=False,
    #         description='Generate kernels via Alpaka, for CPUs or GPUs')

    depends_on('cmake@3.3:', type='build')
    depends_on('jpeg', type='link')
    depends_on('jansson', type='link')
    depends_on('boost@1.56.0:', type='link')
    depends_on('boost@1.65.1:', type='link', when='^cuda@9:')
    depends_on('cuda@7.0:', type='link', when='+cuda')
    # depends_on('alpaka@0.3', when='+alpaka')
    depends_on('icet', type='link')
    depends_on('mpi', type='link')

    root_cmakelists_dir = 'lib'
