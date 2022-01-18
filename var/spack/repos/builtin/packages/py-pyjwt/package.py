# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyjwt(PythonPackage):
    """JSON Web Token implementation in Python"""

    homepage = "https://github.com/jpadilla/pyjwt"
    pypi = "PyJWT/PyJWT-1.7.1.tar.gz"

    version('2.1.0', sha256='fba44e7898bbca160a2b2b501f492824fc8382485d3a6f11ba5d0c1937ce6130')
    version('1.7.1', sha256='8d59a976fb773f3e6a39c85636357c4f0e242707394cadadd9814f5cbaa20e96')

    variant('crypto', default=False, description='Build with cryptography support')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('python@3.6:', when='@2.1.0:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-cryptography@1.4:', when='+crypto', type=('build', 'run'))
    depends_on('py-cryptography@3.3.1:3', when='@2.1.0:+crypto', type=('build', 'run'))
