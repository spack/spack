# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySncosmo(PythonPackage):
    """SNCosmo is a Python library for high-level supernova cosmology
    analysis."""

    homepage = "http://sncosmo.readthedocs.io/"
    pypi = "sncosmo/sncosmo-1.2.0.tar.gz"

    version('2.3.0', sha256='cb4492745dffe7d0f5f8e70f88e36eaf453a047d0e2dc593e3117c1fd0093d11')
    version('2.2.0', sha256='a119eaf13a195cceabb151ef6c26dabeaab9c16e2eb41b4619ecbb6a071e8a5f')
    version('2.1.0', sha256='5f9db64a551c3e70bcbf1a0164ff39018848ea0c338c9ffc33a3a52315b3a92f')
    version('2.0.0', sha256='19ff49f2a65123190fb02eaa1eb8c39ed189446ed6ad5ec67d54023e533c3992')
    version('1.8.2', sha256='552e3d9ee67dae8cf00ef198de5940ee93b231bf50946b2d6589c4963aaf1766')
    version('1.8.1', sha256='997123a2640b8b135e622441201fa03e2e8d79a335beada74585db7809780e35')
    version('1.8.0', sha256='93590c47ac5d5a4849b622d2fba8a867d31b8697363c19abe85d040b9e970ba0')
    version('1.7.1', sha256='0a0b46197fcd4bac779d39b62a418fe2443cae13c2cb82df4f06cc615764df32')
    version('1.7.0', sha256='b9440ae69d2810afe0c500922398dd46513af8e0cb1c33d08b3e933ee688ed12')
    version('1.6.0', sha256='d4eedd4b82328c06d2ae2f17c44245985ceeed9f3009092be76ed2d42e1c5466')
    version('1.5.3', sha256='3d4c85ce8799dc8777f5667b85a9781cd891d846e5aeac7494be0237e3391f27')
    version('1.5.2', sha256='0a3ee8790cde3b82f09c76e6f2f49768c362c5450608b645ba22effca30e9431')
    version('1.5.1', sha256='208fb25a8bdae62a31253d13e7f802bf0c72043c06e4af84f1fd765991d84a63')
    version('1.5.0', sha256='44cf3b58565d35ab38f68556aa1fa1c56864c98215bf895e134c2845b2899774')
    version('1.4.0', sha256='a26bcb0504213fb095217343a111dd077516d01226e7e1c66e67a8f6ebc352f7')
    version('1.3.2', sha256='48e0dd539893fc23439404fd32ae74886560fce8bffb4b4137da7683cf6e24ad')
    version('1.3.1', sha256='6b2b541b0d88c4bbc7d494bad41ab134093907dc760bef9ee29123fa0114da5a')
    version('1.3.0', sha256='4923b0c6947c11f9bd9874b53424adc5c44a37ce4f7e5e65fc53d76bf20ce19a')
    version('1.2.0', sha256='f3969eec5b25f60c70418dbd64765a2b4735bb53c210c61d0aab68916daea588')

    # Required dependencies
    # py-sncosmo binaries are duplicates of those from py-astropy
    extends('python', ignore=r'bin/.*')
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-astropy', type=('build', 'run'))

    # Recommended dependencies
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('py-iminuit', type=('build', 'run'))
    depends_on('py-emcee', type=('build', 'run'))
    depends_on('py-nestle', type=('build', 'run'))
