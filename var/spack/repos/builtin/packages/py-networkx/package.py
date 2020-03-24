# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyNetworkx(PythonPackage):
    """NetworkX is a Python package for the creation, manipulation, and study
    of the structure, dynamics, and functions of complex networks."""
    homepage = "http://networkx.github.io/"
    url      = "https://pypi.io/packages/source/n/networkx/networkx-1.11.tar.gz"

    version('2.2', sha256='45e56f7ab6fe81652fb4bc9f44faddb0e9025f469f602df14e3b2551c2ea5c8b',
            url='https://pypi.io/packages/source/n/networkx/networkx-2.2.zip')
    version('2.1', sha256='64272ca418972b70a196cb15d9c85a5a6041f09a2f32e0d30c0255f25d458bb1',
            url='https://pypi.io/packages/source/n/networkx/networkx-2.1.zip')
    version('1.11', sha256='0d0e70e10dfb47601cbb3425a00e03e2a2e97477be6f80638fef91d54dd1e4b8')
    version('1.10', sha256='ced4095ab83b7451cec1172183eff419ed32e21397ea4e1971d92a5808ed6fb8')

    depends_on('py-decorator', type=('build', 'run'))
    depends_on('py-decorator@4.1.0:', type=('build', 'run'), when='@2.1:')
    depends_on('py-setuptools', type='build')
