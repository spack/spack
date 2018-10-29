# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBackportsFunctoolsLruCache(PythonPackage):
    """Backport of functools.lru_cache from Python 3.3"""

    homepage = "https://github.com/jaraco/backports.functools_lru_cache"
    url = "https://pypi.io/packages/source/b/backports.functools_lru_cache/backports.functools_lru_cache-1.4.tar.gz"

    version('1.5', '20f53f54cd3f04b3346ce75a54959754')
    version('1.4', 'b954e7d5e2ca0f0f66ad2ed12ba800e5')
    version('1.0.1', 'c789ef439d189330b99872746a6d9e85',
            url="https://pypi.io/packages/source/b/backports.functools_lru_cache/backports.functools_lru_cache-1.0.1.zip")

    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm@1.15.0:', type='build')
    depends_on('python@2.6.0:3.3.99',        type=('build', 'run'))
