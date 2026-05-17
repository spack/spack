# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class SyscallIntercept(CMakePackage):
    """Userspace syscall intercepting library for Linux x86_64."""

    homepage = "https://github.com/pmem/syscall_intercept"
    git = "https://github.com/pmem/syscall_intercept.git"

    license("BSD-3-Clause")

    version("master", branch="master")
    version("2026-05-17", commit="b1b9bedcc8cf7d711cd3e74f08d860722e7c301d")

    depends_on("c", type="build")
    depends_on("cmake@3.3:", type="build")
    depends_on("capstone", type=("build", "link"))

    requires("platform=linux", msg="syscall_intercept only supports Linux.")
    requires("target=x86_64:", msg="syscall_intercept only supports x86_64.")

    def cmake_args(self):
        return [
            self.define("PERFORM_STYLE_CHECKS", False),
            self.define("BUILD_TESTS", False),
            self.define("BUILD_EXAMPLES", False),
            self.define("TREAT_WARNINGS_AS_ERRORS", False),
            self.define("AUTO_RUN_CTAGS", False),
        ]
