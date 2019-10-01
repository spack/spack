# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFlye(PythonPackage):
    """Fast and accurate de novo assembler for single molecule sequencing
       reads"""

    homepage = "https://github.com/fenderglass/Flye"
    url      = "https://github.com/fenderglass/Flye/archive/2.4.2.tar.gz"

    version('2.4.2', sha256='5b74d4463b860c9e1614ef655ab6f6f3a5e84a7a4d33faf3b29c7696b542c51a')

    depends_on('python@2.7:2.8', type=('build', 'run'))

    def setup_environment(self, spack_env, run_env):
        if self.spec.target.family == 'aarch64':
            spack_env.set('arm_neon', '1')
            spack_env.set('aarch64', '1')
