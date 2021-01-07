# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPylops(PythonPackage):
    """"""

    pypi = "pylops/pylops-1.12.0.tar.gz"
    git      = "https://github.com/PyLops/pylops.git"

    maintainers = ['archxlith']

    version('master', branch='master')
    version('1.12.0', sha256='0e9caef46bbef9691acd133cb9b6d13e19510e8682aaa8f4eb15d9bd9ff9ebb6')
    version('1.11.1', sha256='87010358b1119ebe1f8a601b2768d16d7bd26d55bd0c91a6e83db763e5715f7c')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-numpy@1.15:', type=('build', 'run'))
    depends_on('py-scipy@1.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-llvmlite', type=('build', 'run'))
    depends_on('py-numba', type=('build', 'run'))
    depends_on('py-pyfftw', type=('build', 'run'))
    depends_on('py-pywavelets', type=('build', 'run'))
    depends_on('py-scikit-fmm', type=('build', 'run'))
    depends_on('py-spgl1', type=('build', 'run'))
