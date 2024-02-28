# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Re2(MakefilePackage, CMakePackage):
    """RE2 is a fast, safe, thread-friendly alternative to backtracking
    regular expression engines like those used in PCRE, Perl, and Python."""

    # The makefile build is preferred, but cmake and bazel are also supported:
    # https://github.com/google/re2/wiki/Install
    build_system(conditional("cmake", when="@:2021-06-01"), "makefile", default="makefile")

    homepage = "https://github.com/google/re2"
    url = "https://github.com/google/re2/releases/download/2023-11-01/re2-2023-11-01.tar.gz"
    git = "https://github.com/google/re2.git"
    list_url = "https://github.com/google/re2/releases"

    maintainers("cosmicexplorer")

    license("BSD-3-Clause")

    version("main", branch="main")

    version(
        "2024-02-01", sha256="cd191a311b84fcf37310e5cd876845b4bf5aee76fdd755008eef3b6478ce07bb"
    )
    version(
        "2023-11-01", sha256="4e6593ac3c71de1c0f322735bc8b0492a72f66ffccfad76e259fa21c41d27d8a"
    )
    version(
        "2023-09-01", sha256="5bb6875ae1cd1e9fedde98018c346db7260655f86fdb8837e3075103acd3649b"
    )
    version(
        "2023-06-01", sha256="8b4a8175da7205df2ad02e405a950a02eaa3e3e0840947cd598e92dca453199b"
    )
    version(
        "2021-06-01", sha256="26155e050b10b5969e986dab35654247a3b1b295e0532880b5a9c13c0a700ceb"
    )
    version(
        "2020-08-01", sha256="6f4c8514249cd65b9e85d3e6f4c35595809a63ad71c5d93083e4d1dcdf9e0cd6"
    )
    version(
        "2020-04-01", sha256="98794bc5416326817498384a9c43cbb5a406bab8da9f84f83c39ecad43ed5cea"
    )

    variant("shared", default=False, description="Build shared instead of static libraries")
    variant("pic", default=True, description="Enable position independent code")

    depends_on("abseil-cpp", when="@2023-09-01:")

    conflicts("+shared ~pic", msg="shared libs must have PIC code!")
    conflicts(
        "+pic ~shared build_system=makefile",
        msg="the makefile build does not support static libs with PIC code!",
    )

    def cmake_args(self):
        args = [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("CMAKE_POSITION_INDEPENDENT_CODE", "pic"),
        ]
        return args

    @when("build_system=makefile")
    def patch(self):
        filter_file("prefix=/usr/local", "prefix={}".format(self.prefix), "Makefile", string=True)

    @property
    def build_targets(self):
        if "+shared" in self.spec:
            return ["shared"]
        return ["static"]

    @property
    def install_targets(self):
        if "+shared" in self.spec:
            return ["shared-install"]
        return ["static-install"]
