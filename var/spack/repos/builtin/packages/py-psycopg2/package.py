# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPsycopg2(PythonPackage):
    """Python interface to PostgreSQL databases"""

    homepage = "http://initd.org/psycopg/"
    url = "http://initd.org/psycopg/tarballs/PSYCOPG-2-7/psycopg2-2.7.5.tar.gz"

    version('2.7.5', sha256='eccf962d41ca46e6326b97c8fe0a6687b58dfc1a5f6540ed071ff1474cea749e')

    depends_on('py-setuptools', type='build')
    depends_on('postgresql', type=('build', 'run'))
