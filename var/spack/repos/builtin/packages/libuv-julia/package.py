# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class LibuvJulia(AutotoolsPackage):
    """Multi-platform library with a focus on asynchronous IO"""
    homepage = "https://libuv.org"
    url      = "https://github.com/JuliaLang/libuv/archive/refs/heads/julia-uv2-1.44.1.tar.gz"

    version('1.44.1', sha256='f931e7825702cbb6d07486d92e5436990cf20f91e2b56d6f759822c0f832b13e')

    @property
    def libs(self):
        return find_libraries(['libuv'], root=self.prefix, recursive=True)
