# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Librsync(CMakePackage):
    """Remote delta-compression library"""

    homepage = "https://github.com/librsync/librsync]"
    url = "https://github.com/librsync/librsync/archive/refs/tags/v2.3.2.tar.gz"

    maintainers = ["JBlaschke"]

    version("2.3.2", sha256="ef8ce23df38d5076d25510baa2cabedffbe0af460d887d86c2413a1c2b0c676f")

    def cmake_args(self):
        args = []
        return args
