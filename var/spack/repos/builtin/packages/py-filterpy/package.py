# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFilterpy(PythonPackage):
    """This library provides Kalman filtering and various
    related optimal and non-optimal filtering software written
    in Python."""

    homepage = "https://github.com/rlabbe/filterpy/"
    url      = "https://github.com/rlabbe/filterpy/archive/1.4.5.tar.gz"

    version('1.4.5', sha256='fc371ad800ca5a5ff8b8352894a09c353b794ccc8b813c03d5187df451ccef3a')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))
