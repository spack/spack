# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class IncludeWhatYouUse(CMakePackage):
    """A tool for use with clang to analyze #includes in C and C++ source files"""

    homepage = "https://github.com/include-what-you-use/include-what-you-use"
    url = "https://github.com/include-what-you-use/include-what-you-use/archive/refs/tags/0.22.tar.gz"
    git = "https://github.com/include-what-you-use/include-what-you-use.git"

    maintainers = ["jmcarcell"]

    version("0.22", sha256="34c7636da2abe7b86580b53b762f5269e71efff460f24f17d5913c56eb99cb7c")
    version("0.21", sha256="a472fe8587376d041585c72e5643200f8929899f787725f0ba9e5b3d3820d401")

    depends_on("llvm@18", when="@0.22")
    depends_on("llvm@17", when="@0.21")

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.bin)

    def install(self, spec, prefix):
        super().install(spec, prefix)
        # Make a symbolic link to the clang include folder
        # See https://github.com/include-what-you-use/include-what-you-use/blob/master/README.md#how-to-install
        with working_dir(self.prefix):
            llvm_version = self.spec["llvm"].version.up_to(1)
            mkdirp(join_path(self.prefix.lib.clang, llvm_version))
            symlink(
                join_path(self.spec["llvm"].prefix.lib.clang, llvm_version, "include"),
                join_path(self.prefix.lib.clang, llvm_version, "include"),
            )
