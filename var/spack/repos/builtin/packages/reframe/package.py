# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Reframe(Package):
    """ReFrame is a framework for writing regression tests for HPC systems.
    The goal of this framework is to abstract away the complexity of the
    interactions with the system, separating the logic of a regression test
    from the low-level details, which pertain to the system configuration and
    setup. This allows users to write easily portable regression tests,
    focusing only on the functionality."""

    homepage = 'https://reframe-hpc.readthedocs.io'
    url      = 'https://github.com/eth-cscs/reframe/archive/v2.21.tar.gz'
    git      = 'https://github.com/eth-cscs/reframe.git'

    # notify when the package is updated.
    maintainers = ['victorusu', 'vkarak']

    version('master',   branch='master')
    version('2.21',      sha256='f35d4fda2f9672c87d3ef664d9a2d6eb0c01c88218a31772a6645c32c8934c4d')
    version('2.20',      sha256='310c18d705858bbe6bd9a2dc4d382b254c1f093b0671d72363f2111e8c162ba4')
    version('2.17.3',    sha256='dc8dfb2ccb9a966303879b7cdcd188c47063e9b7999cbd5d6255223b066bf357')
    version('2.17.2',    sha256='092241cdc15918040aacb922c806aecb59c5bdc3ff7db034a4f355d39aecc101')
    version('2.17.1',    sha256='0b0d32a892607840a7d668f5dcea6f03f7022a26b23e5042a0faf5b8c41cb146')

    depends_on('python@3.5:', type=('run'))

    def install(self, spec, prefix):
        install_tree(self.stage.source_path, self.prefix)
