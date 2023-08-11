# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Googletest(CMakePackage):
    """Google test framework for C++.  Also called gtest."""

    homepage = "https://github.com/google/googletest"
    url = "https://github.com/google/googletest/archive/release-1.10.0.tar.gz"
    git = "https://github.com/google/googletest"

    maintainers("sethrj")

    version("main", branch="main")
    version("1.12.1", sha256="81964fe578e9bd7c94dfdb09c8e4d6e6759e19967e397dbea48d1c10e45d0df2")
    version("1.12.0", sha256="2a4f11dce6188b256f3650061525d0fe352069e5c162452818efbbf8d0b5fe1c")
    version("1.11.0", sha256="07b0896360f8e14414a8419e35515da0be085c5b4547c914ab8f4684ef0a3a8e")
    version("1.10.0", sha256="e4a7cd97c903818abe7ddb129db9c41cc9fd9e2ded654be57ced26d45c72e4c9")
    version("1.8.1", sha256="8e40a005e098b1ba917d64104549e3da274e31261dedc57d6250fe91391b2e84")
    version("1.8.0", sha256="d8c33605d23d303b08a912eaee7f84c4e091d6e3d90e9a8ec8aaf7450dfe2568")
    version("1.7.0", sha256="9639cf8b7f37a4d0c6575f52c01ef167c5f11faee65252296b3ffc2d9acd421b")
    version("1.6.0", sha256="a61e20c65819eb39a2da85c88622bac703b865ca7fe2bfdcd3da734d87d5521a")

    variant("gmock", default=True, when="@1.8:", description="Build with gmock")
    variant("pthreads", default=True, description="Build multithreaded version with pthreads")
    variant("shared", default=True, description="Build shared libraries (DLLs)")

    variant(
        "cxxstd",
        default="11",
        values=("98", "11", "14", "17"),
        multi=False,
        description="Use the specified C++ standard when building",
    )
    conflicts("cxxstd=98", when="@1.9:")
    conflicts("cxxstd=11", when="@1.13:")

    def cmake_args(self):
        spec = self.spec
        args = [
            self.define_from_variant("gtest_disable_pthreads", "pthreads"),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
        ]
        if spec.satisfies("@1.8:"):
            # New style (contains both Google Mock and Google Test)
            args.append(self.define("BUILD_GTEST", True))
            args.append(self.define_from_variant("BUILD_GMOCK", "gmock"))

        return args

    @when("@:1.7.0")
    def install(self, spec, prefix):
        """Make the install targets"""
        with working_dir(self.build_directory):
            # Google Test doesn't have a make install
            # We have to do our own install here.
            install_tree(join_path(self.stage.source_path, "include"), prefix.include)

            mkdirp(prefix.lib)
            if "+shared" in spec:
                install("libgtest.{0}".format(dso_suffix), prefix.lib)
                install("libgtest_main.{0}".format(dso_suffix), prefix.lib)
            else:
                install("libgtest.a", prefix.lib)
                install("libgtest_main.a", prefix.lib)

    @run_after("install")
    def darwin_fix(self):
        # The shared library is not installed correctly on Darwin; fix this
        if self.spec.satisfies("platform=darwin"):
            fix_darwin_install_name(self.prefix.lib)
