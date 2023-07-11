# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class Re2c(Package):
    """re2c: a free and open-source lexer generator for C and C++"""

    homepage = "https://re2c.org/index.html"
    url = "https://github.com/skvadrik/re2c/releases/download/1.2.1/re2c-1.2.1.tar.xz"
    tags = ["windows"]

    version("2.2", sha256="0fc45e4130a8a555d68e230d1795de0216dfe99096b61b28e67c86dfd7d86bda")
    version("2.1.1", sha256="036ee264fafd5423141ebd628890775aa9447a4c4068a6307385d7366fe711f8")
    version("2.1", sha256="8cba0d95c246c670de8f97f57def83a9c0f2113eaa6f7e4867a941f48f633540")
    version("2.0.3", sha256="b2bc1eb8aaaa21ff2fcd26507b7e6e72c5e3d887e58aa515c2155fb17d744278")
    version("2.0.2", sha256="6cddbb558dbfd697a729cb4fd3f095524480283b89911ca5221835d8a67ae5e0")
    version("2.0.1", sha256="aef8b50bb75905b2d55a7236380c0efdc756fa077fe16d808aaacbb10fb53531")
    version("2.0", sha256="89a9d7ee14be10e3779ea7b2c8ea4a964afce6e76b8dbcd5479940681db46d20")
    version("1.3", sha256="f37f25ff760e90088e7d03d1232002c2c2672646d5844fdf8e0d51a5cd75a503")
    version("1.2.1", sha256="1a4cd706b5b966aeffd78e3cf8b24239470ded30551e813610f9cd1a4e01b817")

    phases = ["configure", "build", "install"]

    depends_on("cmake", when="platform=windows")

    @property
    def make_tool(self):
        if sys.platform == "win32":
            return ninja
        else:
            return make

    def configure_args(self):
        return [
            "--disable-benchmarks",
            "--disable-debug",
            "--disable-dependency-tracking",
            "--disable-docs",
            "--disable-lexers",  # requires existing system re2c
            "--disable-libs",  # experimental
            "--enable-golang",
        ]

    def configure(self, spec, prefix):
        with working_dir(self.stage.source_path, create=True):
            configure("--prefix=" + prefix, *self.configure_args())

    @when("platform=windows")
    def configure(self, spec, prefix):
        with working_dir(self.stage.source_path, create=True):
            args = ["-G", "Ninja", "-DCMAKE_INSTALL_PREFIX=%s" % prefix]
            cmake(*args)

    def build(self, spec, prefix):
        with working_dir(self.stage.source_path):
            self.make_tool()

    def install(self, spec, prefix):
        with working_dir(self.stage.source_path):
            self.make_tool("install")
