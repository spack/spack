# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyNeo(PythonPackage):
    """Neo is a package for representing electrophysiology data in Python,
    together with support for reading a wide range of neurophysiology
    file formats"""

    homepage = "http://neuralensemble.org/neo"
    pypi = "neo/neo-0.4.1.tar.gz"

    version('0.9.0', sha256='6e31c88d7c52174fa2512df589b2b5003e9471fde27fca9f315f4770ba3bd3cb')
    version('0.8.0', sha256='3382a37b24a384006238b72981f1e9259de9bfa71886f8ed564d35d254ace458')
    version('0.7.2', sha256='5c81abfed4c773779279f8b9a353992fbb56e709cab39a5024386b90b3a67381')
    version('0.7.1', sha256='bae3a2ddbe54362a1fe54613a0f5c24deb2c6372a72a619942035c9227714dc0')
    version('0.7.0', sha256='452d440738683943497959e5b6fb898a519665513b6360a4fb0df2247eac8657')
    version('0.6.1', sha256='b711d871d25cc97651d445d5bf6d06a1a74b121bc28ea623e2538b6fbd2a7d1f')
    version('0.6.0', sha256='0d8f4d119663670913fb12d393b043e0f34fae47c9aeb9f7f7006717166d6cf3')
    version('0.5.2', sha256='1de436b7d5e72a5b4f1baa68bae5b790624a9ac44b2673811cb0b6ef554d3f8b')
    version('0.4.1', sha256='a5a4f3aa31654d52789f679717c9fb622ad4f59b56d227dca490357b9de0a1ce')

    depends_on('py-setuptools',        type='build')
    depends_on('py-numpy@1.7.1:',      type=('build', 'run'))
    depends_on('py-quantities@0.9.0:', type=('build', 'run'))
