# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMongo(PythonPackage):
    """Python driver for MongoDB <http://www.mongodb.org>"""

    homepage = "http://github.com/mongodb/mongo-python-driver"
    url      = "https://pypi.io/packages/source/p/pymongo/pymongo-3.6.0.tar.gz"

    version('3.6.0', '2f64fa7691c77535b72050704cc12afb')
    version('3.3.0', '42cd12a5014fb7d3e1987ca04f5c651f')

    depends_on('python@2.6:2.8,3.3:')

    depends_on('py-setuptools', type='build')
