# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *


class PyPycrypto(PythonPackage):
    """The Python Cryptography Toolkit"""

    homepage = "https://www.dlitz.net/software/pycrypto/"
    url      = "https://pypi.io/packages/source/p/pycrypto/pycrypto-2.6.1.tar.gz"

    version('2.6.1', '55a61a054aa66812daf5161a0d5d7eda')

    # depends_on('py-setuptools', type='build')
    depends_on('gmp')
