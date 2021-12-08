# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCachecontrol(PythonPackage):
    """httplib2 caching for requests"""

    homepage = "https://github.com/ionrock/cachecontrol"
    pypi     = "CacheControl/CacheControl-0.12.10.tar.gz"

    version('0.12.10', sha256='d8aca75b82eec92d84b5d6eb8c8f66ea16f09d2adb09dbca27fe2d5fc8d3732d')

    depends_on('python@3.6:',       type=('build', 'run'))
    depends_on('py-setuptools',     type='build')
    depends_on('py-requests',       type=('build', 'run'))
    depends_on('py-msgpack@0.5.2:', type=('build', 'run'))
    depends_on('py-lockfile@0.9:',  type=('build', 'run'), when='+filecache')
    depends_on('py-redis@2.10.5:',  type=('build', 'run'), when='+redis')

    variant('filecache', default=False, description='Add file-based cache support')
    variant('redis', default=False, description='Add redis-based cache support')
