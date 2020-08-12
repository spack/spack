# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class Metall(CMakePackage):
    """An allocator for persistent memory"""

    homepage = "https://github.com/LLNL/metall"
    git      = "https://github.com/LLNL/metall.git"
    url      = "https://github.com/LLNL/metall/archive/v0.2.tar.gz"

    maintainers = ['KIwabuchi', 'rogerpearce', 'mayagokhale']

    version('develop', branch='develop')
    version('0.2', sha256='35cdf3505d2f8d0282a0d5c60b69a0ec5ec6d77ac3facce7549eb874df27be1d')

    depends_on('boost@1.64:', type=('build', 'link'))

    def cmake_args(self):
        args = []
        args.append('-DINSTALL_HEADER_ONLY=ON')
        return args
