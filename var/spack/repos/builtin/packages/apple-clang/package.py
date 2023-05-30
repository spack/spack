# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from spack.package import *
import spack.compilers.apple_clang


class AppleClang(Package):
    def install(self, spec, prefix):
        raise NotImplementedError

    executables = [r"^clang\+\+", r"^clang"]

    @classmethod
    def determine_version(cls, exe):
        try:
            output = spack.compiler.get_compiler_version_output(exe, "--version")
        except Exception:
            output = ""

        version = spack.compilers.apple_clang.AppleClang.extract_version_from_output(output)
        if version == "unknown":
            return None
        return version

    @classmethod
    def determine_variants(cls, exes, version_str):
        compilers = {}
        for exe in exes:
            basename = os.path.basename(exe)
            if basename == "clang":
                compilers["c"] = exe
            elif basename == "clang++":
                compilers["cxx"] = exe
        return "", {"compilers": compilers}
