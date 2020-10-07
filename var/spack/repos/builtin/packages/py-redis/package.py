# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyRedis(PythonPackage):
    """The Python interface to the Redis key-value store."""

    homepage = "https://pypi.org/project/redis/"
    url      = "https://pypi.io/packages/source/r/redis/redis-3.3.8.tar.gz"

    version('3.5.0', sha256='7378105cd8ea20c4edc49f028581e830c01ad5f00be851def0f4bc616a83cd89')
    version('3.3.8', sha256='98a22fb750c9b9bb46e75e945dc3f61d0ab30d06117cbb21ff9cd1d315fedd3b')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools',       type='build')
    depends_on('py-hiredis',          type=('build', 'run'))
