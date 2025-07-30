# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack_repo.builtin_mock.build_systems.cmake import CMakePackage

from spack.package import *


class LlvmClient(CMakePackage):
    """A client package that depends on llvm and needs C and C++ compilers."""

    git = "https://github.com/mycpptutorial/helloworld-cmake"

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    version("develop", branch="master")

    depends_on("llvm")
