# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Brynet(CMakePackage):
    """Header Only Cross platform high performance TCP network library
    using C++ 11."""

    homepage = "https://github.com/IronsDu/brynet"
    url      = "https://github.com/IronsDu/brynet/archive/v1.0.8.tar.gz"

    version('1.0.8', sha256='e37dee5fa14acec99bdd7ce8530a00ff5116f608f0a5401cd2e32e10f23975fc')
    version('1.0.7', sha256='60116fccff108d03f3ff0a3d5c1fb5ad442bad7ef155bf1a3c7819ffc9d57524')
    version('1.0.6', sha256='5e94b5b64fbdfbcb4e33b11fb7832cf0ca3898ab6b6461867182598bab7ca65f')

    def cmake_args(self):
        args = []
        args.append('-Dbrynet_BUILD_EXAMPLES=ON')
        args.append('-Dbrynet_BUILD_TESTS=ON')
        return args
