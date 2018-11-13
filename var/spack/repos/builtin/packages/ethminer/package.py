# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ethminer(CMakePackage):
    """The ethminer is an Ethereum GPU mining worker."""

    homepage = "https://github.com/ethereum-mining/ethminer"
    url = "https://github.com/ethereum-mining/ethminer/archive/v0.12.0.tar.gz"

    version('0.12.0', '1c7e3df8476a146702a4050ad984ae5a')

    variant('opencl', default=True, description='Enable OpenCL mining.')
    variant('cuda', default=False, description='Enable CUDA mining.')
    variant('stratum', default=True,
            description='Build with Stratum protocol support.')

    depends_on('python')
    depends_on('boost')
    depends_on('json-c')
    depends_on('curl')
    depends_on('zlib')
    depends_on('cuda', when='+cuda')
    depends_on('mesa', when='+opencl')

    def cmake_args(self):
        spec = self.spec
        return [
            '-DETHASHCL=%s' % ('YES' if '+opencl' in spec else 'NO'),
            '-DETHASHCUDA=%s' % ('YES' if '+cuda' in spec else 'NO'),
            '-DETHSTRATUM=%s' % ('YES' if '+stratum' in spec else 'NO')]
