# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPomegranate(PythonPackage):
    """Fast, flexible and easy to use probabilistic modelling in Python."""

    homepage = "https://github.com/jmschrei/pomegranate"
    pypi = "pomegranate/pomegranate-0.12.0.tar.gz"

    version('0.14.2', sha256='a00f541cd3d08f1e086cda4915d6e73c9dc0bbbfc657bcca77dab7f0b17c9b8b')
    version('0.14.0', sha256='41b08b321b6248361fbd3cd950f12a01e6d48317dbafb32b5dd3223b66532618')
    version('0.13.5', sha256='b1b803fa18c8a8ca4a8fd2824573914bbff7574e3dc6be770ab68efd00503341')
    version('0.13.4', sha256='aa726b6b40337b0fd316aa8f6976fba3d58d421ce1d7d42fa48f54a8a409e42a')
    version('0.13.3', sha256='10eb625f405c3be7d4d906c81369edbd4b3632f7a4a45859fb0ccda632784cb7')
    version('0.13.2', sha256='a50e4248bc851dce580b478a642a1689d6f6122941aa92cf3ba28281514383cd')
    version('0.13.0', sha256='65cb3fccf099ff9c2eafdb53648f4e048df182899b442fe622af32d207618a09')
    version('0.12.2', sha256='942a7bd3b3d5a540a00edc7a12166b37384a068cc4b2f1fdb10f3afeeb6e9eeb')
    version('0.12.0', sha256='8b00c88f7cf9cad8d38ea00ea5274821376fefb217a1128afe6b1fcac54c975a')

    depends_on('py-setuptools', type='build')
    depends_on('py-cython@0.22.1:', type='build')
    depends_on('py-numpy@1.8.0:', type=('build', 'run'))
    depends_on('py-joblib@0.9.0b4:', type=('build', 'run'))
    depends_on('py-networkx@2.0:', type=('build', 'run'))
    depends_on('py-scipy@0.17.0:', type=('build', 'run'))
    depends_on('py-pyyaml', type=('build', 'run'))
