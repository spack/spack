# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyJaracoFunctools(PythonPackage):
    """Functools like those found in stdlib"""

    homepage = "https://github.com/jaraco/jaraco.functools"
    pypi = "jaraco.functools/jaraco.functools-2.0.tar.gz"

    version('3.2.0', sha256='e11a692db72f9e03bbfc5eae30e8670d1fc7f8c9610cd1c20ebff03beb0376e1')
    version('3.1.0', sha256='7de095757115ebd370ddb14659b48ca83fcd075e78e0b3c575041c0edbf718e0')
    version('3.0.1', sha256='9fedc4be3117512ca3e03e1b2ffa7a6a6ffa589bfb7d02bfb324e55d493b94f4')
    version('3.0.0', sha256='5cb0eea0f254584241c519641328a4d4ec2001a86c3cd6d17a8fd228493f6d97')
    version(
        '2.0', sha256='35ba944f52b1a7beee8843a5aa6752d1d5b79893eeb7770ea98be6b637bf9345')

    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm@1.15.0:', type='build')
    depends_on('py-backports-functools-lru-cache@1.0.3:',
               when='^python@:2', type=('build', 'run'))
    depends_on('py-more-itertools', type=('build', 'run'))
    depends_on('python@2.7:', type=('build', 'run'))
