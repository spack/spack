# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class PyFlitCore(PythonPackage):
    """Distribution-building parts of Flit."""

    homepage = "https://github.com/takluyver/flit"
    pypi = "flit-core/flit_core-3.3.0.tar.gz"
    maintainers = ['takluyver']

    version('3.6.0', sha256='5892962ab8b8ea945835b3a288fe9dd69316f1903d5288c3f5cafdcdd04756ad')
    version('3.5.1', sha256='3083720351a6cb00e0634a1ec0e26eae7b273174c3c6c03d5b597a14203b282e')
    version('3.5.0', sha256='2db800d33ff41e4c6e7c1b594666cb2a11553024106655272c7245933b1d75bd')
    version('3.4.0', sha256='29468fa2330969167d1f5c23eb9c0661cb6dacfcd46f361a274609a7f4197530')
    version('3.3.0', sha256='b1404accffd6504b5f24eeca9ec5d3c877f828d16825348ba81515fa084bd5f0')
    version('3.2.0', sha256='ff87f25c5dbc24ef30ea334074e35030e4885e4c5de3bf4e21f15746f6d99431')
    version('3.1.0', sha256='22ff73be39a2b3c9e0692dfbbea3ad4a9d127e5733736a87dbb8ddcbf7309b1e')
    version('3.0.0', sha256='a465052057e2d6d957e6850e9915245adedfc4fd0dd5737d0791bf3132417c2d')
    version('2.3.0', sha256='a50bcd8bf5785e3a7d95434244f30ba693e794c5204ac1ee908fc07c4acdbf80')

    # Dependencies listed in flit_core/build_thyself.py
    depends_on('python@3.6:', when='@3.4:', type=('build', 'run'))
    depends_on('python@3.4:', when='@3:', type=('build', 'run'))
    depends_on('python@2.7,3.4:', type=('build', 'run'))
    depends_on('py-tomli', when='@3.4:3.5', type='run')
    depends_on('py-toml', when='@3.1:3.3', type='run')
    depends_on('py-pytoml', when='@:3.0', type='run')
