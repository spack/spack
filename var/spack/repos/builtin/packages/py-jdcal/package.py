# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyJdcal(PythonPackage):
    """Julian dates from proleptic Gregorian and Julian calendars"""

    homepage = "http://github.com/phn/jdcal"
    pypi = "jdcal/jdcal-1.3.tar.gz"

    version('1.4.1', sha256='472872e096eb8df219c23f2689fc336668bdb43d194094b5cc1707e1640acfc8')
    version('1.4',   sha256='ea0a5067c5f0f50ad4c7bdc80abad3d976604f6fb026b0b3a17a9d84bb9046c9')
    version('1.3', sha256='b760160f8dc8cc51d17875c6b663fafe64be699e10ce34b6a95184b5aa0fdc9e')
    version('1.2', sha256='5ebedb58b95ebabd30f56abef65139c6f69ec1687cf1d2f3a7c503f9a2cdfa4d')

    depends_on('py-setuptools', type='build')
