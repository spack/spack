# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBuild(PythonPackage):
    """A simple, correct PEP517 package builder."""

    homepage = "https://github.com/pypa/build"
    pypi     = "build/build-0.7.0.tar.gz"

    version('0.7.0', sha256='1aaadcd69338252ade4f7ec1265e1a19184bf916d84c9b7df095f423948cb89f')

    variant('virtualenv', default=False, description='Install optional virtualenv dependency')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-packaging@19:', type=('build', 'run'))
    depends_on('py-pep517@0.9.1:', type=('build', 'run'))
    depends_on('py-tomli@1:', type=('build', 'run'))
    depends_on('py-colorama', when='platform=windows', type=('build', 'run'))
    depends_on('py-importlib-metadata@0.22:', when='^python@:3.7', type=('build', 'run'))
    depends_on('py-virtualenv@20.0.35:', when='+virtualenv', type=('build', 'run'))

    # https://github.com/pypa/build/issues/266
    # https://github.com/pypa/build/issues/406
    patch('isolation.patch', when='@0.7.0')
