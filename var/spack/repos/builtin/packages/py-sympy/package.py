# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySympy(PythonPackage):
    """SymPy is a Python library for symbolic mathematics."""
    homepage = "https://pypi.python.org/pypi/sympy"
    url      = "https://pypi.io/packages/source/s/sympy/sympy-0.7.6.tar.gz"

    version('1.3', sha256='e1319b556207a3758a0efebae14e5e52c648fc1db8975953b05fff12b6871b54')
    version('1.1.1', 'c410a9c2346878716d16ec873d72e72a')
    version('1.0', '43e797de799f00f9e8fd2307dba9fab1')
    version('0.7.6', '3d04753974306d8a13830008e17babca')

    depends_on('py-mpmath', when='@1.0:', type=('build', 'run'))
