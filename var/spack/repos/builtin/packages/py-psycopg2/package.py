# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPsycopg2(PythonPackage):
    """Python interface to PostgreSQL databases"""

    homepage = "http://initd.org/psycopg/"
    url = "http://initd.org/psycopg/tarballs/PSYCOPG-2-7/psycopg2-2.7.5.tar.gz"

    version('2.7.5', '9e7d6f695fc7f8d1c42a7905449246c9')

    depends_on('py-setuptools', type='build')
    depends_on('postgresql', type=('build', 'run'))
