# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPykwalify(PythonPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url      = "https://pypi.io/packages/source/p/pykwalify/pykwalify-1.7.0.tar.gz"

    version('1.7.0', sha256='7e8b39c5a3a10bc176682b3bd9a7422c39ca247482df198b402e8015defcceb2')
    version('1.6.1', sha256='')

    depends_on('py-setuptools', type='build')
    depends_on('py-docopt@0.6.2:', type=('build', 'run'))
    depends_on('py-ruamel-yaml@0.11.0:', type=('build', 'run'))
    depends_on('py-python-dateutil@2.4.2:', type=('build', 'run'))
    depends_on('py-pyyaml@3.11:', type=('build', 'run'), when='@1.6.1')

    conflicts('py-ruamel@0.16.0:', when='@1.6.1')
    conflicts('python@2.8.0:3.2.99', when='@1.6.1')
    conflicts('python@2.8.0:3.4.99', when='@1.7.0:')
