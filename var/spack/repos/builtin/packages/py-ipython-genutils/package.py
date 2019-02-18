# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyIpythonGenutils(PythonPackage):
    """Vestigial utilities from IPython"""

    homepage = "https://pypi.python.org/pypi/ipython_genutils"
    url      = "https://pypi.io/packages/source/i/ipython_genutils/ipython_genutils-0.1.0.tar.gz"

    version('0.1.0', '9a8afbe0978adbcbfcb3b35b2d015a56')

    depends_on('python@2.7:2.8,3.3:')
