# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJsonschema(PythonPackage):
    """Jsonschema: An(other) implementation of JSON Schema for Python."""

    homepage = "https://github.com/Julian/jsonschema"
    pypi = "jsonschema/jsonschema-3.2.0.tar.gz"

    version('4.4.0', sha256='636694eb41b3535ed608fe04129f26542b59ed99808b4f688aa32dcf55317a83')
    version('3.2.0', sha256='c8a85b28d377cc7737e46e2d9f2b4f44ee3c0e1deac6bf46ddefc7187d30797a')
    version('3.1.1', sha256='2fa0684276b6333ff3c0b1b27081f4b2305f0a36cf702a23db50edb141893c3f')
    version('3.0.2', sha256='8d4a2b7b6c2237e0199c8ea1a6d3e05bf118e289ae2b9d7ba444182a2959560d')
    version('3.0.1', sha256='0c0a81564f181de3212efa2d17de1910f8732fa1b71c42266d983cd74304e20d')
    version('2.6.0', sha256='6ff5f3180870836cae40f06fa10419f557208175f13ad7bc26caa77beb1f6e02')
    version('2.5.1', sha256='36673ac378feed3daa5956276a829699056523d7961027911f064b52255ead41')

    depends_on('python@3.7:', when='@4:', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.5:', when='@3:', type=('build', 'run'))
    depends_on('python@2.6:2.8,3.4:', type=('build', 'run'))

    depends_on('py-setuptools@40.6.0:', when='@4:', type='build')
    depends_on('py-setuptools', when='@3', type=('build', 'run'))
    depends_on('py-setuptools', when='@:2', type='build')
    depends_on('py-vcversioner', when='@:2', type='build')
    depends_on('py-setuptools-scm+toml@3.4:', when='@4:', type='build')
    depends_on('py-setuptools-scm', when='@3', type='build')

    depends_on('py-attrs@17.4:', when='@3:', type=('build', 'run'))
    depends_on('py-importlib-metadata', when='@3.1.1: ^python@:3.7', type=('build', 'run'))
    depends_on('py-importlib-resources@1.4:', when='@4.2.1: ^python@:3.8', type=('build', 'run'))
    depends_on('py-importlib-resources', when='@4.2.0 ^python@:3.8', type=('build', 'run'))
    depends_on('py-pyrsistent@0.14:0.16,0.17.3:', when='@4:', type=('build', 'run'))
    depends_on('py-pyrsistent@0.14:', when='@3', type=('build', 'run'))
    depends_on('py-typing-extensions', when='@4.3: ^python@:3.7', type=('build', 'run'))

    depends_on('py-six@1.11:', when='@3', type=('build', 'run'))
    depends_on('py-functools32', when="^python@:2", type=('build', 'run'))
