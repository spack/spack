# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPygresql(PythonPackage):
    """PyGreSQL is an open-source Python module that interfaces to a
       PostgreSQL database"""

    homepage = "http://www.pygresql.org"
    url      = "http://www.pygresql.org/files/PyGreSQL-5.0.5.tar.gz"

    version('5.0.5', 'c7d1558e85568d3369a98609174ca6a0')

    depends_on('py-setuptools', type='build')
    depends_on('postgresql', type=('build', 'run'))
