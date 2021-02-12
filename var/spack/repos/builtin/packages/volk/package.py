# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class Volk(CMakePackage):
    """VOLK is the Vector-Optimized Library of Kernels. It is a
    library that contains kernels of hand-written SIMD code for
    different mathematical operations. Since each SIMD architecture
    can be very different and no compiler has yet come along to handle
    vectorization properly or highly efficiently, VOLK approaches the
    problem differently.

    For each architecture or platform that a developer wishes to
    vectorize for, a new proto-kernel is added to VOLK. At runtime,
    VOLK will select the correct proto-kernel. In this way, the users
    of VOLK call a kernel for performing the operation that is
    platform/architecture agnostic. This allows us to write portable
    SIMD code."""

    homepage = "https://github.com/gnuradio/volk"
    url      = "https://github.com/gnuradio/volk/archive/v2.3.0.tar.gz"

    maintainers = ['aweits']

    version('2.4.1', sha256='61d681f90e0f30894f806ab050e9ba28260799c01f1ed0f58623942d8c7f4d48')
    version('2.4.0', sha256='504a316f5bf784d68334bc9df4627b8e8deb1ac67edd70d185360507af0cb1b4')
    version('2.3.0', sha256='f42c928f561b128acfe4adb21227e4a62a3f6ab8103592fc3233765ff326d5fc')

    depends_on('python@3.4:', type=('build', 'run'))
    depends_on('py-mako@0.4.2:', type=('build', 'run'))
