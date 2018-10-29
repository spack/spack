# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMonotonic(PythonPackage):
    """An implementation of time.monotonic() for Python 2 & < 3.3"""

    homepage = "https://pypi.python.org/pypi/monotonic"
    url      = "https://pypi.io/packages/source/m/monotonic/monotonic-1.2.tar.gz"

    version('1.2', 'd14c93aabc3d6af25ef086b032b123cf')

    depends_on('py-setuptools', type='build')
