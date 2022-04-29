# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class PyOpppy(PythonPackage):
    """The Output Parse-Plot Python (OPPPY) library is a python based data
    analysis library designed to extract, store, and plot information from
    output and dump files generated by scientific software packages."""

    homepage = "https://github.com/lanl/opppy"
    url = "https://github.com/lanl/OPPPY/archive/opppy-0_1_2.tar.gz"
    git = "https://github.com/lanl/opppy.git"
    maintainers = ['clevelam']

    version('master', branch='master')
    version('0_1_5', sha256='d9df166d347c18d4f145059b4c2fb23dbfbecf0dd5a3398f29e52d3e261844b0')
    version('0_1_4', sha256='22d81a64856f4c12f8079440c837d7d1f45153e68c405b45bed8b6d35831e948')
    version('0_1_3', sha256='c3ca97f2ff8ab319b5c7257baa8cab852387dc00d426b4534c06f0894363c541')
    version('0_1_2', sha256='ef3795d3164fa0aa7ea7da7e223d6d0a48d2960aefd03a7d90cdb8b8f480cd4c')
    version('0_1_1', sha256='505c023853e75552abc65de9777a125ecb6a99a1cb4e605a4f702af837e3168b')

    depends_on('py-setuptools', type=('build'))
    depends_on('py-sphinx',     type=('build'))
    depends_on('py-numpy@1.6:', type=('build', 'run'))
    depends_on('python@3:',     type=('build', 'run'))
    depends_on('py-scipy',      type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))
