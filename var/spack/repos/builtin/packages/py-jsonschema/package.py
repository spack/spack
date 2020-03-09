# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyJsonschema(PythonPackage):
    """Jsonschema: An(other) implementation of JSON Schema for Python."""

    homepage = "http://github.com/Julian/jsonschema"
    url      = "https://pypi.io/packages/source/j/jsonschema/jsonschema-2.6.0.tar.gz"

    version('3.0.1', sha256='0c0a81564f181de3212efa2d17de1910f8732fa1b71c42266d983cd74304e20d')
    version('2.6.0', sha256='6ff5f3180870836cae40f06fa10419f557208175f13ad7bc26caa77beb1f6e02')
    version('2.5.1', sha256='36673ac378feed3daa5956276a829699056523d7961027911f064b52255ead41')

    depends_on('python@2.6:2.8,3.4:', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.5:', when='@3:', type=('build', 'run'))

    depends_on('py-setuptools', type='build', when='@:2')
    depends_on('py-setuptools', type=('build', 'run'), when='@3:')
    depends_on('py-vcversioner', type='build', when='@:2')
    depends_on('py-setuptools-scm', type='build', when='@3:')

    depends_on('py-functools32', when="^python@:2", type=('build', 'run'))
    depends_on('py-attrs@17.4.0:', when='@3:', type=('build', 'run'))
    depends_on('py-pyrsistent@0.14.0:', when='@3:', type=('build', 'run'))
    depends_on('py-six@1.11.0:', when='@3:', type=('build', 'run'))
