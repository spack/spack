# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Scons(PythonPackage):
    """SCons is a software construction tool"""

    homepage = "http://scons.org"
    url      = "https://pypi.io/packages/source/s/scons/scons-3.0.1.tar.gz"

    version('3.0.1', 'b6a292e251b34b82c203b56cfa3968b3',
            url="https://pypi.python.org/packages/c1/0a/520a3c86ce5cff36e81af5e91d4dcd741ebc189c2f0f42d54cc12a8a7519/scons-3.0.1.tar.gz")
    version('2.5.1', '3eac81e5e8206304a9b4683c57665aa4',
            url="https://pypi.python.org/packages/2c/ee/a9601b958c94e93410e635a5d67ed95300998ffdc36127b16d322b054ff0/scons-2.5.1.tar.gz")
    version('2.5.0', 'bda5530a70a41a7831d83c8b191c021e',
            url="https://pypi.python.org/packages/17/f0/60464796a3fd16899a2cf54e22615c38bbe8124386cf3763c17ff367c2af/scons-2.5.0.tar.gz")

    # Python 3 support was added in SCons 3.0.0
    depends_on('python@:2', when='@:2', type=('build', 'run'))
