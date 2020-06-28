# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAttrs(PythonPackage):
    """Classes Without Boilerplate"""

    homepage = "http://attrs.org/"
    url      = "https://pypi.io/packages/source/a/attrs/attrs-19.2.0.tar.gz"

    import_modules = ['attr']

    version('19.3.0', sha256='f7b7ce16570fe9965acd6d30101a28f62fb4a7f9e926b3bbc9b61f8b04247e72')
    version('19.2.0', sha256='f913492e1663d3c36f502e5e9ba6cd13cf19d7fab50aa13239e420fef95e1396')
    version('19.1.0', sha256='f0b870f674851ecbfbbbd364d6b5cbdff9dcedbc7f3f5e18a6891057f21fe399')
    version('18.1.0', sha256='e0d0eb91441a3b53dab4d9b743eafc1ac44476296a2053b6ca3af0b139faf87b')
    version('16.3.0', sha256='80203177723e36f3bbe15aa8553da6e80d47bfe53647220ccaa9ad7a5e473ccc')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')

    depends_on('py-coverage', type='test')
    depends_on('py-hypothesis', type='test')
    depends_on('py-pympler', type='test')
    depends_on('py-pytest', type='test')
    depends_on('py-pytest@4.3.0:', type='test', when='@19.3.0:')
    depends_on('py-six', type='test')
    depends_on('py-zope-interface', type='test')
