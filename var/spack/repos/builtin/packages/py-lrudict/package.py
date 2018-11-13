# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyLrudict(PythonPackage):
    """ A fast LRU cache"""

    homepage = "https://github.com/amitdev/lru-dict"
    url      = "https://pypi.io/packages/source/l/lru-dict/lru-dict-1.1.6.tar.gz"

    version('1.1.6', 'b33f54f1257ab541f4df4bacc7509f5a')

    depends_on('python@2.7:')
    depends_on('py-setuptools', type=('build'))
