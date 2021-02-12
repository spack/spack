# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Httpie(PythonPackage):
    """Modern command line HTTP client."""

    homepage = "https://httpie.org/"
    pypi = "httpie/httpie-0.9.8.tar.gz"

    version('2.4.0', sha256='4d1bf5779cf6c9007351cfcaa20bd19947267dc026af09246db6006a8927d8c6')
    version('2.3.0', sha256='d540571991d07329d217c31bf1ff95fd217957da2aa2def09bcfa0c0fca0cf96')
    version('2.2.0', sha256='31ac28088ee6a0b6f3ba7a53379000c4d1910c1708c9ff768f84b111c14405a0')
    version('2.1.0', sha256='a76f1c72e83bd03cde3478c5f345d5570fdb2967ed19d68d09518088640b9e8e')
    version('2.0.0', sha256='8c04f9756f1a7eac71a6dfa0834d0f6813dc8a982d8564f3a7418dcd19107c09')
    version('1.0.3', sha256='6d1b6e21da7d3ec030ae95536d4032c1129bdaf9de4adc72c596b87e5f646e80')
    version('1.0.2', sha256='fc676c85febdf3d80abc1ef6fa71ec3764d8b838806a7ae4e55e5e5aa014a2ab')
    version('1.0.0', sha256='1650342d2eca2622092196bf106ab8f68ea2dbb2ed265d37191185618e159a25')
    version('0.9.9', sha256='f1202e6fa60367e2265284a53f35bfa5917119592c2ab08277efc7fffd744fcb')
    version('0.9.8', sha256='515870b15231530f56fe2164190581748e8799b66ef0fe36ec9da3396f0df6e1')

    variant('socks', default=True,
            description='Enable SOCKS proxy support')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-pygments@2.1.3:', type=('build', 'run'))
    depends_on('py-requests@2.11.0:', type=('build', 'run'))
    depends_on('py-pysocks', type=('build', 'run'), when="+socks")
    # Concretization problem breaks this.  Unconditional for now...
    # https://github.com/spack/spack/issues/3628
    # depends_on('py-argparse@1.2.1:', type=('build', 'run'),
    #            when='^python@:2.6,3.0:3.1')
    depends_on('py-argparse@1.2.1:', type=('build', 'run'), when='^python@:2.6')
