# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDbf(PythonPackage):
    """Pure python package for reading/writing dBase, FoxPro, and Visual FoxPro
    .dbf files (including memos)"""

    homepage = 'https://pypi.python.org/pypi/dbf'
    url      = "https://pypi.io/packages/source/d/dbf/dbf-0.96.005.tar.gz"

    version('0.96.005', 'bce1a1ed8b454a30606e7e18dd2f8277')
    version('0.94.003', '33a659ec90d7e8d8ffcd69d2189c0c6c')
