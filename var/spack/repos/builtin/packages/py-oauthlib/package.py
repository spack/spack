# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyOauthlib(PythonPackage):
    """
    A generic, spec-compliant, thorough implementation of the OAuth
    request-signing logic
    """

    homepage = "https://github.com/oauthlib/oauthlib"
    pypi = "oauthlib/oauthlib-3.1.0.tar.gz"

    version('3.1.1', sha256='8f0215fcc533dd8dd1bee6f4c412d4f0cd7297307d43ac61666389e3bc3198a3')
    version('3.1.0', sha256='bee41cc35fcca6e988463cacc3bcb8a96224f470ca547e697b604cc697b2f889')
    version('3.0.1', sha256='0ce32c5d989a1827e3f1148f98b9085ed2370fc939bf524c9c851d8714797298')
    version('2.0.2', sha256='b3b9b47f2a263fe249b5b48c4e25a5bce882ff20a0ac34d553ce43cff55b53ac')

    variant('extras', default=True, description='Build with pyjwt, blinker, cryptography')

    depends_on('py-setuptools',           type='build')
    depends_on('py-pyjwt@1.0.0:',         type=('build', 'run'), when='+extras')
    depends_on('py-pyjwt@2.0.0:2',        type=('build', 'run'), when='+extras @3.1.1:')
    depends_on('py-blinker',              type=('build', 'run'), when='+extras')
    depends_on('py-blinker@1.4:',          type=('build', 'run'), when='+extras @3.1.1:')
    depends_on('py-cryptography',         type=('build', 'run'), when='+extras')
    depends_on('py-cryptography@3.0.0:3', type=('build', 'run'), when='+extras @3.1.1:')
    depends_on('python@2.7:2.8,3.4:',     type=('build', 'run'))
    depends_on('python@3.6:',             type=('build', 'run'), when='@3.1.1:')
