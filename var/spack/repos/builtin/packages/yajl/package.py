# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Yajl(CMakePackage):
    """Yet Another JSON Library (YAJL)"""

    homepage = "http://lloyd.github.io/yajl/"
    url      = "https://github.com/lloyd/yajl/archive/2.1.0.zip"
    git      = "https://github.com/lloyd/yajl.git"

    version('develop', branch='master')
    version('2.1.0', '5eb9c16539bf354b937fcb20e263d1eb')
