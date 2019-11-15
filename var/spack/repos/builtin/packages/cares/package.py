# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cares(CMakePackage):
    """c-ares: A C library for asynchronous DNS requests"""

    homepage = "https://c-ares.haxx.se"
    url      = "https://github.com/c-ares/c-ares/archive/cares-1_13_0.tar.gz"
    git      = "https://github.com/c-ares/c-ares.git"

    version('develop', branch='master')
    version('1.13.0', sha256='7c48c57706a38691041920e705d2a04426ad9c68d40edd600685323f214b2d57')

    def url_for_version(self, version):
        url = "https://github.com/c-ares/c-ares/archive/cares-{0}.tar.gz"
        return url.format(version.underscored)
