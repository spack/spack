# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBcolz(PythonPackage):
    """bcolz provides columnar and compressed data containers. Column
    storage allows for efficiently querying tables with a large number
    of columns. It also allows for cheap addition and removal of column.
    In addition, bcolz objects are compressed by default for reducing
    memory/disk I/O needs. The compression process is carried out internally
    by Blosc, a high-performance compressor that is optimized for binary data.
    """

    homepage = "https://github.com/Blosc/bcolz"
    url      = "https://files.pythonhosted.org/packages/5c/4e/23942de9d5c0fb16f10335fa83e52b431bcb8c0d4a8419c9ac206268c279/bcolz-1.2.1.tar.gz"

    version('1.2.1', sha256='c017d09bb0cb5bbb07f2ae223a3f3638285be3b574cb328e91525b2880300bd1')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-numpy@1.8:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
