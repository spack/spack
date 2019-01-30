# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyNumexpr(PythonPackage):
    """Fast numerical expression evaluator for NumPy"""
    homepage = "https://pypi.python.org/pypi/numexpr"
    url      = "https://pypi.io/packages/source/n/numexpr/numexpr-2.6.9.tar.gz"

    version('2.6.9', sha256='fc218b777cdbb14fa8cff8f28175ee631bacabbdd41ca34e061325b6c44a6fa6')
    version('2.6.5', 'c9b5859c11bd6da092f6c8a84a472e77')
    version('2.6.1', '6365245705b446426df9543ad218dd8e')
    version('2.5',   '84f66cced45ba3e30dcf77a937763aaa')
    version('2.4.6', '17ac6fafc9ea1ce3eb970b9abccb4fbd')

    depends_on('python@2.6:')
    depends_on('py-numpy@1.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
