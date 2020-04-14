# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libtree(CMakePackage):
    """ldd as a tree with an option to bundle dependencies into a
       single folder"""

    homepage = "https://github.com/haampie/libtree"
    url      = "https://github.com/haampie/libtree/releases/download/v1.0.3/sources.tar.gz"

    maintainers = ['haampie']

    version('1.0.3', sha256='67ce886c191d50959a5727246cdb04af38872cd811c9ed4e3822f77a8f40b20b')