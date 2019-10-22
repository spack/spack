# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMongo(PythonPackage):
    """Python driver for MongoDB <http://www.mongodb.org>"""

    homepage = "http://github.com/mongodb/mongo-python-driver"
    url      = "https://pypi.io/packages/source/p/pymongo/pymongo-3.6.0.tar.gz"

    version('3.6.0', sha256='c6de26d1e171cdc449745b82f1addbc873d105b8e7335097da991c0fc664a4a8')
    version('3.3.0', sha256='3d45302fc2622fabf34356ba274c69df41285bac71bbd229f1587283b851b91e')

    depends_on('python@2.6:2.8,3.3:')

    depends_on('py-setuptools', type='build')
