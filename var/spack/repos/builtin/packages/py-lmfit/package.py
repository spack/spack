# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyLmfit(PythonPackage):
    """Least-Squares Minimization with Bounds and Constraints"""

    homepage = "http://lmfit.github.io/lmfit-py/"
    url      = "https://pypi.io/packages/source/l/lmfit/lmfit-0.9.5.tar.gz"

    version('0.9.5', '3a38aa3e4510a564d9e2f606d2537522')

    depends_on('py-numpy@1.5:',  type=('build', 'run'))
    depends_on('py-scipy@0.14:', type=('build', 'run'))
    depends_on('py-setuptools',  type='build')
