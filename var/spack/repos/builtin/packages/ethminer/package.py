# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ethminer(CMakePackage):
    """The ethminer is an Ethereum GPU mining worker."""

    homepage = "https://github.com/ethereum-mining/ethminer"
    url = "https://github.com/ethereum-mining/ethminer/archive/v0.12.0.tar.gz"

    version('0.19.0', sha256='8cedd087542dee74568c062960aec10f0c95ab3355c553f68e9b7023e01a4582')
    version('0.18.0', sha256='f666cb171cd05ab397b138b99cd205fdfe449b629f892f0dd7eac5bb50f4bed4')
    version('0.17.1', sha256='823908ab8a22b6c319eda4922a4708ae2600061f09683325f72b330119769a1d')
    version('0.17.0', sha256='2cb8d1c3f37757e1cc440656962780585699ce8d7db7b3d47dafa503d7c672c7')
    version('0.16.2', sha256='c66ed82c830fec094d5e53e565bc7d91a42b4961f48b91b89202f79a8958dfe8')
    version('0.12.0', sha256='71122c8aa1be2c29e46d7f07961fa760b1eb390e4d9a2a21cf900f6482a8755a')

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
