# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class PyPsycopg2(PythonPackage):
    """Python interface to PostgreSQL databases"""

    homepage = "https://psycopg.org/"
    pypi = "psycopg2/psycopg2-2.8.6.tar.gz"

    version('2.9.1', sha256='de5303a6f1d0a7a34b9d40e4d3bef684ccc44a49bbe3eb85e3c0bffb4a131b7c')
    version('2.8.6', sha256='fb23f6c71107c37fd667cb4ea363ddeb936b348bbd6449278eb92c189699f543')
    version('2.7.5', sha256='eccf962d41ca46e6326b97c8fe0a6687b58dfc1a5f6540ed071ff1474cea749e')

    # https://www.psycopg.org/docs/install.html#prerequisites
    depends_on('python@3.6:3.9', type=('build', 'link', 'run'), when='@2.9:')
    depends_on('python@2.7:2.8,3.4:3.8', type=('build', 'link', 'run'), when='@2.8')
    depends_on('python@2.6:2.8,3.2:3.7', type=('build', 'link', 'run'), when='@:2.7')
    depends_on('py-setuptools', type='build')
    depends_on('postgresql@9.1:13', type=('build', 'link', 'run'), when='@2.9:')
    depends_on('postgresql@9.1:12', type=('build', 'link', 'run'), when='@:2.8')
