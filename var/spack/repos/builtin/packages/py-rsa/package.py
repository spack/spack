# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyRsa(PythonPackage):
    """Pure-Python RSA implementation"""

    homepage = "https://stuvel.eu/rsa"
    pypi = "rsa/rsa-3.4.2.tar.gz"

    version('4.7',   sha256='69805d6b69f56eb05b62daea3a7dbd7aa44324ad1306445e05da8060232d00f4')
    version('4.6',   sha256='109ea5a66744dd859bf16fe904b8d8b627adafb9408753161e766a92e7d681fa')
    version('4.5',   sha256='4d409f5a7d78530a4a2062574c7bd80311bc3af29b364e293aa9b03eea77714f')
    version('4.4.1', sha256='efaf0c32afee1c136e5cd2e7ceecf2dfc65dac00fb812a1b3b8b72f6fea38dbb')
    version('4.4',   sha256='5d95293bbd0fbee1dd9cb4b72d27b723942eb50584abc8c4f5f00e4bcfa55307')
    version('4.3',   sha256='7b863ff461f751373b4203dc09cfd07d92564575e8fafa45cc24fcde039153a0')
    version('4.2',   sha256='aaefa4b84752e3e99bd8333a2e1e3e7a7da64614042bd66f775573424370108a')
    version('4.1.1', sha256='1a7245638fa914ed6196b5e88fa5064cd95c7e65df800ec5d4f288e2b19fb4af')
    version('4.1',   sha256='6fa6a54eb72bfc0abca7f27880b978b14a643ba2a6ad9f4a56a95be82129ca1b')
    version('4.0',   sha256='1a836406405730121ae9823e19c6e806c62bbad73f890574fff50efa4122c487')
    version('3.4.2', sha256='25df4e10c263fb88b5ace923dd84bf9aa7f5019687b5e55382ffcdb8bede9db5')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-pyasn1@0.1.3:', type=('build', 'run'))
