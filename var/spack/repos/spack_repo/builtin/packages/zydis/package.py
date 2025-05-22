# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Zydis(CMakePackage):
    """The ultimate, open-source x86 and x86-64 decoder/disassembler library."""

    homepage = "https://zydis.re"
    url = "https://github.com/zyantific/zydis/archive/refs/tags/v0.0.0.tar.gz"

    maintainers("RMeli")

    license("MIT", checked_by="RMeli")

    version("4.1.1", sha256="45c6d4d499a1cc80780f7834747c637509777c01dca1e98c5e7c0bfaccdb1514")

    depends_on("c", type="build")

    depends_on("zycore-c")

    def cmake_args(self):
        args = []
        return args
