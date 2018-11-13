# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Mallocmc(CMakePackage):
    """mallocMC: Memory Allocator for Many Core Architectures.

    This project provides a framework for fast memory managers on
    many core accelerators. Currently, it supports NVIDIA GPUs of
    compute capability sm_20 or higher through the ScatterAlloc
    algorithm.

    mallocMC is header-only, but requires a few other C++ libraries
    to be available.
    """

    homepage = "https://github.com/ComputationalRadiationPhysics/mallocMC"
    url      = "https://github.com/ComputationalRadiationPhysics/mallocMC/archive/2.2.0crp.tar.gz"
    git      = "https://github.com/ComputationalRadiationPhysics/mallocMC.git"

    maintainers = ['ax3l']

    version('develop', branch='dev')
    version('master', branch='master')
    version('2.2.0crp', '3e5c5fc963d1a9abc829ff701504e54c')
    version('2.1.0crp', 'd2bd2644012b64a246048575e9a9051c')
    version('2.0.1crp', '1f674d5d1ae05446d9a4e4b65465dca0')
    version('2.0.0crp', '2c63c3ea2a882f29962c67b095d8f7a8')
    version('1.0.2crp', '8f5edf07daa527261e52bc61be340ae6')

    depends_on('cmake@2.8.12.2:', type='build')
    depends_on('boost@1.48.0:', type='link')
    depends_on('cuda@5.0:', type='link')
