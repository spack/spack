# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Sas(CMakePackage):
    """SAS (Static Analysis Suite) is a powerful tool for running static
    analysis on C++ code."""

    homepage = "https://github.com/dpiparo/SAS"
    url      = "https://github.com/dpiparo/SAS/archive/0.1.3.tar.gz"

    version('0.2.0', 'e6fecfb71d9cdce342c8593f4728c9f0')
    version('0.1.4', '20d7311258f2a59c9367ae1576c392b6')
    version('0.1.3', '1e6572afcc03318d16d7321d40eec0fd')

    depends_on('python@2.7:')
    depends_on('llvm@3.5:')
    depends_on('cmake@2.8:', type='build')

    def cmake_args(self):
        args = [
            '-DLLVM_DEV_DIR=%s' % self.spec['llvm'].prefix
        ]
        return args
