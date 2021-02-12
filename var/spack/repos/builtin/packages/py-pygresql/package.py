# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPygresql(PythonPackage):
    """PyGreSQL is an open-source Python module that interfaces to a
       PostgreSQL database"""

    homepage = "http://www.pygresql.org"
    url      = "http://www.pygresql.org/files/PyGreSQL-5.0.5.tar.gz"

    version('5.1.2', sha256='82b6e944211cc06d45a6e1219d5444530b385811128aeb9f633ab7e35e6a65a5')
    version('5.1',   sha256='ac4aacd22df95b2a76de2c2b9fca0265f67135c6e2f6d9a7adfea2ab7c842a0d')
    version('5.0.7', sha256='f3ad8056cfbe4d3afb93989579c973041113dc3c1640512e9c8c96f938f1931f')
    version('5.0.6', sha256='274e799698b87e71ef8f7fc72464779dd1335de183983b567baa559691f1b524')
    version('5.0.5', sha256='ff5e76b840600d4912b79daf347b44274a1c0368663e7b57529c406f8426479c')

    depends_on('py-setuptools', type='build')
    depends_on('postgresql', type=('build', 'run'))
