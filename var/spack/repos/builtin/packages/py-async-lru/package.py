# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAsyncLru(PythonPackage):
    """Simple lru_cache for asyncio"""

    homepage = "https://github.com/wikibusiness/async_lru"
    pypi     = "async_lru/async_lru-1.0.2.tar.gz"

    maintainers = ['iarspider']

    version('1.0.2', sha256='baa898027619f5cc31b7966f96f00e4fc0df43ba206a8940a5d1af5336a477cb')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
