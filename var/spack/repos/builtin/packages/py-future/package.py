# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFuture(PythonPackage):
    """Clean single-source support for Python 3 and 2"""

    homepage = "https://python-future.org/"
    url = "https://pypi.io/packages/source/f/future/future-0.16.0.tar.gz"

    version('0.17.1', sha256='67045236dcfd6816dc439556d009594abf643e5eb48992e36beac09c2ca659b8')
    version('0.17.0', sha256='eb6d4df04f1fb538c99f69c9a28b255d1ee4e825d479b9c62fc38c0cf38065a4')
    version('0.16.0', '3e8e88a2bda48d54b1da7634d04760d7')
    version('0.15.2', 'a68eb3c90b3b76714c5ceb8c09ea3a06')

    depends_on('py-setuptools', type='build')
    depends_on('py-importlib', type=('build', 'run'), when='^python@:2.6')
    depends_on('py-argparse', type=('build', 'run'), when='^python@:2.6')
