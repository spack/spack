# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyKombu(PythonPackage):
    """Messaging library for Python."""

    homepage = "https://pypi.org/project/kombu/"
    url      = "https://pypi.io/packages/source/k/kombu/kombu-4.3.0.tar.gz"

    version('4.6.6', sha256='1760b54b1d15a547c9a26d3598a1c8cdaf2436386ac1f5561934bc8a3cbbbd86')
    version('4.5.0', sha256='389ba09e03b15b55b1a7371a441c894fd8121d174f5583bbbca032b9ea8c9edd')
    version('4.3.0', sha256='529df9e0ecc0bad9fc2b376c3ce4796c41b482cf697b78b71aea6ebe7ca353c8')

    depends_on('python@2.7:2.8,3.5:', type=('build', 'run'))

    depends_on('py-setuptools', type='build')
    depends_on('py-amqp@2.5.2:2.5.999', type=('build', 'run'))
    depends_on('py-importlib-metadata@0.18:', type=('build', 'run'))
