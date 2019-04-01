# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class EcpIoSdk(CMakePackage):
    """ECP I/O Services SDK"""

    homepage = "https://github.com/chuckatkins/ecp-data-viz-sdk"
    git      = "https://github.com/chuckatkins/ecp-data-viz-sdk.git"

    version('1.0', branch='master')

    # FIXME: Add dependencies if required.
    # depends_on('foo')

    def cmake_args(self):
        return [ '-DIO=ON' ]
