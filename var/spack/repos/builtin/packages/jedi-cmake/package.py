# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: Apache-2.0

import os
from spack import *

class JediCmake(CMakePackage):
    """CMake/ecbuild toolchains to facilitate portability on different systems."""

    homepage = "https://github.com/JCSDA/jedi-cmake"
    git = "https://github.com/JCSDA/jedi-cmake.git"
    url = "https://github.com/JCSDA/jedi-cmake/archive/refs/tags/1.3.0.tar.gz"

    maintainers = ['climbfuji', 'rhoneyager']

    version('master', branch='master', no_cache=True)
    version('develop', branch='develop', no_cache=True)
    version('1.3.0', sha256='b217e2250398f6c34f0da0a50a8efe500684af4d484adebaa87a9de630eee1b7', preferred=True)
    version('1.2.0', sha256='eb9f1c403d1b43a90a5e774097382b183d56d5b40a1204b51af2da8db1559b21')
    version('1.1.0', sha256='f1fe41eb5edd343bdf57eb76bea6d1b9f015878f0a9d0eb1e9dba18b903d3b35')
    version('1.0.0', sha256='d773a800350e69372355b45e89160b593818cd438a86925b8a689c47996a0b9a')

    depends_on('cmake @3.10:', type=('build'))

