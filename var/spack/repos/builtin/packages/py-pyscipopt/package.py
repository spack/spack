# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyscipopt(PythonPackage):
    """Python interface for the SCIP Optimization Suite"""

    homepage = "https://github.com/scipopt/PySCIPOpt"
    url      = "https://github.com/scipopt/PySCIPOpt/archive/refs/tags/v3.3.0.zip"
    pyip     = "pyscipopt/pysciopt-3.3.0.tar.gz"

    version('3.3.0', sha256='bae5e19014583f0049018bf6079905a86076da2b06093e989e16838cac88c071')

    depends_on('python',        type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-cython',     type=('build', 'run'))
    depends_on('py-wheel',      type=('build', 'run'))
    depends_on('scipoptsuite',  type=('link', 'build', 'run'))
