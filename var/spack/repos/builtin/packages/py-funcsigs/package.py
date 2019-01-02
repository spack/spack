# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFuncsigs(PythonPackage):
    """Python function signatures from PEP362 for Python 2.6, 2.7 and 3.2."""

    homepage = "https://pypi.python.org/pypi/funcsigs"
    url      = "https://pypi.io/packages/source/f/funcsigs/funcsigs-1.0.2.tar.gz"

    import_modules = ['funcsigs']

    version('1.0.2', '7e583285b1fb8a76305d6d68f4ccc14e')
    version('0.4',   'fb1d031f284233e09701f6db1281c2a5')

    depends_on('py-setuptools@17.1:', type='build')
    depends_on('py-unittest2', type='test')
