# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Justbuild(Package):
    "just, a generic build tool"

    git = "https://github.com/just-buildsystem/justbuild.git"

    homepage = "https://github.com/just-buildsystem/justbuild"

    tags = ["build-tools"]

    executables = ["^just$"]

    maintainers("asartori86")

    version("master", branch="master")
    version("1.0.0", tag="v1.0.0")

    depends_on("python@3:", type=("build", "run"))
    depends_on("wget", type=("build", "run"))

    sanity_check_is_file = [join_path("bin", "just"), join_path("bin", "just-mr")]

    def setup_build_environment(self, env):
        ar = which("ar")
        if self.spec.satisfies("%gcc@10:"):
            gcc = which("gcc")
            gpp = which("g++")
            env.set(
                "JUST_BUILD_CONF",
                "  {"
                + '  "CC":"{0}"'.format(gcc.path)
                + ', "CXX":"{0}"'.format(gpp.path)
                + ', "AR":"{0}"'.format(ar.path)
                + ', "COMPILER_FAMILY":"unknown"'
                + ', "ENV":{'
                + '    "PATH":"{0}"'.format(os.environ["PATH"])
                + "   }"
                + "}",
            )
        elif self.spec.satisfies("%clang@11:") or spec.satisfies("%apple-clang@11:"):
            clang = which("clang")
            clangpp = which("clang++")
            env.set(
                "JUST_BUILD_CONF",
                "  {"
                + '  "CC":"{0}"'.format(clang.path)
                + ', "CXX":"{0}"'.format(clangpp.path)
                + ', "AR":"{0}"'.format(ar.path)
                + ', "COMPILER_FAMILY":"unknown"'
                + ', "ENV":{'
                + '    "PATH":"{0}"'.format(os.environ["PATH"])
                + "   }"
                + "}",
            )
        else:
            raise InstallError("please use gcc >= 10 or clang >= 11")

    def install(self, spec, prefix):
        python = which("python3")
        python(os.path.join("bin", "bootstrap.py"), ".", prefix)
        mkdirp(prefix.bin)
        install(os.path.join(prefix, "out", "bin", "just"), prefix.bin)
        install(os.path.join("bin", "just-mr.py"), os.path.join(prefix.bin, "just-mr"))

    @classmethod
    def determine_version(cls, exe):
        import json

        try:
            s = os.popen(exe + " version").read()
            d = json.loads(s)
            return ".".join(map(str, d["version"])) + d["suffix"].replace("~", "-")
        except Exception:
            return None
