# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

class Metall(CMakePackage):
    """An allocator for persistent memory"""

    homepage = "https://github.com/LLNL/metall"
    git      = "git@github.com:LLNL/metall.git"

    maintainers = ['KIwabuchi', 'rogerpearce', 'mayagokhale']

    version('develop', branch='develop')

    variant('boost', default=False, description='Install a proper version of Boost')
    depends_on('boost@1.64:', type=('link'), when='+boost')

    def cmake_args(self):
      args = []
      args.append('-DINSTALL_HEADER_ONLY=ON')
      return args
