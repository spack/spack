# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Pgmath(CMakePackage):
    """Flang's math library"""

    homepage = "https://github.com/flang-compiler/flang"
    url      = "https://github.com/flang-compiler/flang/archive/flang_20180612.tar.gz"
    git      = "https://github.com/flang-compiler/flang.git"

    version('develop', branch='master')
    version('20180921', sha256='f33bd1f054e474f1e8a204bb6f78d42f8f6ecf7a894fdddc3999f7c272350784')
    version('20180612', sha256='6af858bea013548e091371a97726ac784edbd4ff876222575eaae48a3c2920ed')

    depends_on("awk", type="build")
    conflicts("%gcc@:7.1.9999")

    root_cmakelists_dir = 'runtime/libpgmath'
