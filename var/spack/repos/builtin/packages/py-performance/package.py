# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPerformance(PythonPackage):
    """The performance project is intended to be an authoritative source
    of benchmarks for all Python implementations.

    The focus is on real-world benchmarks, rather than synthetic benchmarks,
    using whole applications when possible.
    """

    homepage = 'http://pyperformance.readthedocs.io/'
    url = 'https://github.com/python/performance/archive/0.6.1.tar.gz'

    version('0.6.1', '95477b584a284582b66c922a5335b427')
    version('0.6.0', 'b93661e07668fa0b461236dca164eedf')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-perf', type=('build', 'run'))
