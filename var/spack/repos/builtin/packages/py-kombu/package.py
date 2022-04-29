# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class PyKombu(PythonPackage):
    """Messaging library for Python."""

    pypi = "kombu/kombu-4.3.0.tar.gz"

    version('5.2.3', sha256='81a90c1de97e08d3db37dbf163eaaf667445e1068c98bfd89f051a40e9f6dbbd')
    version('5.0.2', sha256='f4965fba0a4718d47d470beeb5d6446e3357a62402b16c510b6a2f251e05ac3c')
    version('4.6.11', sha256='ca1b45faac8c0b18493d02a8571792f3c40291cf2bcf1f55afed3d8f3aa7ba74')
    version('4.6.6', sha256='1760b54b1d15a547c9a26d3598a1c8cdaf2436386ac1f5561934bc8a3cbbbd86')
    version('4.5.0', sha256='389ba09e03b15b55b1a7371a441c894fd8121d174f5583bbbca032b9ea8c9edd')
    version('4.3.0', sha256='529df9e0ecc0bad9fc2b376c3ce4796c41b482cf697b78b71aea6ebe7ca353c8')

    depends_on('python@3.7:', type=('build', 'run'), when="@5.2.3:")
    depends_on('python@2.7:2.8,3.5:', type=('build', 'run'))

    variant('redis', default=False, description="Use redis transport")

    depends_on('py-setuptools', type='build')
    depends_on('py-amqp@2.5.2:2.5', when="@:4.6.6", type=('build', 'run'))
    depends_on('py-amqp@2.6.0:2.6', when="@4.6.7:4", type=('build', 'run'))
    depends_on('py-amqp@5.0.0:5', when="@5.0.0:5.0.2", type=('build', 'run'))
    depends_on('py-amqp@5.0.9:5.0', when="@5.2.3", type=('build', 'run'))
    depends_on('py-vine', when="@5.1.0:", type=('build', 'run'))
    depends_on('py-importlib-metadata@0.18:', type=('build', 'run'), when='python@:3.7')
    depends_on('py-cached-property', type=('build', 'run'), when='python@:3.7')

    depends_on('py-redis@3.4.1:3,4.0.2:', when='+redis', type=('build', 'run'))
