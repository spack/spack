# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class Sol2(CMakePackage):
    """a C++ <-> Lua API wrapper with advanced features and top notch performance"""

    homepage = "https://github.com/ThePhD/sol2"
    url      = "https://github.com/ThePhD/sol2/archive/v3.0.3.tar.gz"

    version('3.2.3',       sha256='f74158f92996f476786be9c9e83f8275129bb1da2a8d517d050421ac160a4b9e')
    version('3.2.2',       sha256='141790dae0c1821dd2dbac3595433de49ba72545845efc3ec7d88de8b0a3b2da')
    version('3.2.1',       sha256='b10f88dc1246f74a10348faef7d2c06e2784693307df74dcd87c4641cf6a6828')
    version('3.2.0', sha256='733f03d82df6e0e8a15967831840d240dcb2c606982bec753bd173a9cc1b3435')
    version('3.0.3', sha256='bf089e50387edfc70063e24fd7fbb693cceba4a50147d864fabedd1b33483582')

    depends_on('lua@5.1:')
