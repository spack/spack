# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Rapidjson(CMakePackage):
    """A fast JSON parser/generator for C++ with both SAX/DOM style API"""

    homepage = "http://rapidjson.org"
    url      = "https://github.com/Tencent/rapidjson/archive/v1.1.0.tar.gz"

    version('1.1.0', 'badd12c511e081fec6c89c43a7027bce')
    version('1.0.2', '97cc60d01282a968474c97f60714828c')
    version('1.0.1', '48cc188df49617b859d13d31344a50b8')
    version('1.0.0', '08247fbfa464d7f15304285f04b4b228')

    # released versions compile with -Werror and fail with gcc-7
    # branch-fall-through warnings
    patch('0001-turn-off-Werror.patch')

    patch('arm.patch', when='@1.1.0 target=aarch64: %gcc@:5.9')
