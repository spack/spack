# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Wcs(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://github.com/LLNL/wcs.git"
    git      = "https://github.com/LLNL/wcs.git"
    maintainers = ['rblake-llnl']

    version('master', branch='master')
    version('devel', branch='devel')

    depends_on('boost+graph+filesystem+regex+system')
    depends_on('cmake@3.12:', type='build')
    depends_on('cereal', type='build')

    def cmake_args(self):
        spec = self.spec
        args = [
            "-DBOOST_ROOT=" + spec['boost'].prefix,
            "-DCEREAL_ROOT=" + spec['cereal'].prefix,
        ]
        return args
