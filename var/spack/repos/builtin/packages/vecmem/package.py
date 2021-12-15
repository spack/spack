# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Vecmem(CMakePackage):
    """VecMem is a vectorised data model base and helper classes."""

    homepage = "https://github.com/acts-project/vecmem"
    url      = "https://github.com/acts-project/vecmem/archive/refs/tags/v0.5.0.tar.gz"
    list_url = "https://github.com/acts-project/vecmem/releases"

    maintainers = ['wdconinc', 'HadrienG2']

    version('0.5.0', sha256='b9739e8fcdf27fa9ef509743cd8f8f62f871b53b0a63b93f24ea9865c2b00a3a')
    version('0.4.0', sha256='51dfadc2b97f34530c642abdf86dcb6392e753dd68ef011bac89382dcf8aaad4')
    version('0.3.0', sha256='4e7851ab46fee925800405c5ae18e99b62644d624d3544277a522a06fb812dbf')
    version('0.2.0', sha256='33aea135989684e325cb097e455ff0f9d1a9e85ff32f671e3b3ed6cc036176ac')
    version('0.1.0', sha256='19e24e3262aa113cd4242e7b94e2de34a4b362e78553730a358f64351c6a0a01')

    variant('cuda', default=False, description='Build the vecmem::cuda library')
    variant('hip', default=False, description='Build the vecmem::hip library')
    variant('sycl', default=False, description='Build the vecmem::sycl library')

    depends_on('cmake@3.8:', type='build')
    depends_on('cuda', when='+cuda')
    depends_on('hip', when='+hip')
    depends_on('sycl', when='+sycl')

    def cmake_args(self):
        args = [
            self.define_from_variant('VECMEM_BUILD_CUDA_LIBRARY', 'cuda'),
            self.define_from_variant('VECMEM_BUILD_HIP_LIBRARY', 'hip'),
            self.define_from_variant('VECMEM_BUILD_SYCL_LIBRARY', 'sycl'),
            self.define('VECMEM_BUILD_TESTING', self.run_tests)
        ]
        return args
