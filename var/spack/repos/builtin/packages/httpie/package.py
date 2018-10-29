# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Httpie(PythonPackage):
    """Modern command line HTTP client."""

    homepage = "https://httpie.org/"
    url      = "https://pypi.io/packages/source/h/httpie/httpie-0.9.8.tar.gz"

    version('0.9.9', '13ed0b79b65e793eb288e563db38b2a2')
    version('0.9.8', 'e0d1af07d0959a2e081e7954797ce260')

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
    depends_on('py-argparse@1.2.1:', type=('build', 'run'))
