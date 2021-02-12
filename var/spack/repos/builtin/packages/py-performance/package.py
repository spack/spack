# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
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

    version('1.0.1', sha256='8b7dd31a2ec0a6b6c26f29d80124d4d3f137dbf60f7c4eb2137d62e3c196bae9')
    version('1.0.0', sha256='48319cca6b610d9a40c3cfe67dac10aa72f07c71b87f78e228873eb1384939f6')
    version('0.9.1', sha256='6dbd525ecfec3dac1c10799f9aff8a8ed857b93c9821e7423fc47a7f0a48457e')
    version('0.9.0', sha256='5b510da972974f609e664e27add1cbb59d5dbc5ffb19910fa746fe039ca4a435')
    version('0.8.0', sha256='3a0569ffdcb5f1245ffdd7c0bf7a8a74b854e6b1ffcf414a9a519cf0331bbb49')
    version('0.7.0', sha256='06aea9136eb2cebb80220bdc46f7572ac0065e907155abad44f34afdc43c4687')
    version('0.6.1', sha256='cc48dd7579da2f4b0e4cff0c8220811f5ba7019493bb408819c1532acf53d13a')
    version('0.6.0', sha256='4636e276445e96563f628e071cacd5df31dc587d83899e7d03fa8b31760f2cd2')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-pyperf', type=('build', 'run'))
