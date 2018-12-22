# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Brigand(Package):
    """Brigand Meta-programming library"""

    homepage = "https://github.com/edouarda/brigand"
    url      = "https://github.com/edouarda/brigand/archive/1.0.0.tar.gz"
    git      = "https://github.com/edouarda/brigand.git"

    version('master', branch='master')
    version('1.3.0', '0bea9713b3b712229aed289e218d577b')
    version('1.2.0', '32c0f73e7e666d33ff123334f5c9c92f')
    version('1.1.0', '073b7c8e2cbda3a81bbeb1ea5b9ca0eb')
    version('1.0.0', 'eeab3d437090f0bb7bc4eb69a5cd9c49')

    def install(self, spec, prefix):
        install_tree('include', prefix.include)
