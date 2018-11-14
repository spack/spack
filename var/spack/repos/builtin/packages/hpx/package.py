# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Hpx(CMakePackage):
    """C++ runtime system for parallel and distributed applications."""

    homepage = "http://stellar.cct.lsu.edu/tag/hpx/"
    url      = "http://stellar.cct.lsu.edu/files/hpx_1.0.0.tar.gz"

    version('1.0.0', '4983e7c6402417ec794d40343e36e417')

    depends_on('boost@1.55.0:')
    depends_on('hwloc@1.6:')

    def cmake_args(self):
        args = ['-DHPX_BUILD_EXAMPLES=OFF', '-DHPX_MALLOC=system']
        return args
