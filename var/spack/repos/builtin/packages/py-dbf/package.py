# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class PyDbf(PythonPackage):
    """Pure python package for reading/writing dBase, FoxPro, and Visual FoxPro
    .dbf files (including memos)"""

    pypi = "dbf/dbf-0.96.005.tar.gz"

    version('0.96.005', sha256='d6e03f1dca40488c37cf38be9cb28b694c46cec747a064dcb0591987de58ed02')
    version('0.94.003', sha256='c95b688d2f28944004368799cc6e2999d78af930a69bb2643ae098c721294444')

    # pip silently replaces distutils with setuptools
    depends_on('py-setuptools', type='build')
