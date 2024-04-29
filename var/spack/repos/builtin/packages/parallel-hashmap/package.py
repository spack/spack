# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ParallelHashmap(CMakePackage):
    """A family of header-only, very fast and memory-friendly hashmap and btree
    containers."""

    homepage = "https://github.com/greg7mdp/parallel-hashmap"
    url = "https://github.com/greg7mdp/parallel-hashmap/archive/refs/tags/v1.3.11.tar.gz"

    license("Apache-2.0")

    version("1.3.11", sha256="0515a681bfb24207013786a7737e9d8561302e656689d8a65ea480bbabab460f")

    depends_on("cmake@3.8:", type="build")

    patch("pthread.patch")
