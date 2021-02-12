# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyOlefile(PythonPackage):
    """Python package to parse, read and write Microsoft OLE2 files"""

    homepage = "https://www.decalage.info/python/olefileio"
    pypi = "olefile/olefile-0.44.zip"

    version('0.46',   sha256='133b031eaf8fd2c9399b78b8bc5b8fcbe4c31e85295749bb17a87cba8f3c3964')
    version('0.45.1', sha256='2b6575f5290de8ab1086f8c5490591f7e0885af682c7c1793bdaf6e64078d385')
    version('0.45',   sha256='8009f50bdaafc2247546d3105be61e0bb38d21098b36dd5fc9eed05be28bba7b')
    version('0.44', sha256='61f2ca0cd0aa77279eb943c07f607438edf374096b66332fae1ee64a6f0f73ad')

    depends_on('python@2.6:', type=('build', 'run'))
