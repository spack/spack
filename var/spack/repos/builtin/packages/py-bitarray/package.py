# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBitarray(PythonPackage):
    """Efficient array of booleans - C extension"""

    homepage = "https://pypi.python.org/pypi/bitarray"
    url      = "https://pypi.io/packages/source/b/bitarray/bitarray-0.8.1.tar.gz"

    version('0.8.1', '3825184f54f4d93508a28031b4c65d3b')

    depends_on('python')
    depends_on('py-setuptools', type='build')
