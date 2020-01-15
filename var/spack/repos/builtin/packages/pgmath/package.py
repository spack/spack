# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Pgmath(CMakePackage):
    """Flang's math library"""

    homepage = "https://github.com/flang-compiler/flang"
    url      = "https://github.com/flang-compiler/flang/archive/flang_20190329.tar.gz"
    git      = "https://github.com/flang-compiler/flang.git"

    maintainers = ['naromero77']

    version('master', branch='master')
    version('20190329', sha256='b8c621da53829f8c53bad73125556fb1839c9056d713433b05741f7e445199f2')
    version('20181226', sha256='00e716bea258c3bb60d6a5bb0c82bc79f67000062dc89939693e75f501883c36')
    version('20180921', sha256='f33bd1f054e474f1e8a204bb6f78d42f8f6ecf7a894fdddc3999f7c272350784')
    version('20180612', sha256='6af858bea013548e091371a97726ac784edbd4ff876222575eaae48a3c2920ed')

    # work around for this issue
    # https://github.com/flang-compiler/flang/issues/602
    patch('https://github.com/flang-compiler/flang/commit/7fcd6346a9427977afe4534c0f19bbbba04c99a3.diff',
          sha256='4014df1e5855dd21242b0fc938a4e7835941c20f9a89c3a7a5314e74b6232bcb',
          when='@20190329')

    # workaround for this issue
    # https://github.com/flang-compiler/flang/issues/838
    patch('libpgmath_symbols.patch', when='@20190329,master')

    depends_on("awk", type="build")
    conflicts("%gcc@:7.1.9999")

    root_cmakelists_dir = 'runtime/libpgmath'
