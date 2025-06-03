# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class ZycoreC(CMakePackage):
    """Platform independent types, macros and a fallback for environments without LibC"""

    homepage = "https://github.com/zyantific/zycore-c"
    url = "https://github.com/zyantific/zycore-c/archive/refs/tags/v0.0.0.tar.gz"

    maintainers("RMeli")

    license("MIT", checked_by="RMeli")

    version("1.5.1", sha256="292ec0b30a68a6be416119756238efb5ab34122de80cca884e269e28f6fc126b")

    depends_on("c", type="build")

    def cmake_args(self):
        args = []
        return args
