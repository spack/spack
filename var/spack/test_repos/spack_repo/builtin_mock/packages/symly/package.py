# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os
import sys

from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class Symly(Package):
    """A toy package full of symlinks."""

    homepage = "https://www.example.com"
    has_code = False
    version("3.0.0")

    def install(self, spec, prefix):
        symly_c = """
#include <stdio.h>

int main() {
    printf("I'm just here to give the build system something to do...");
    return 0;
}
"""
        mkdirp(f"{self.stage.source_path}/symly")
        with open(f"{self.stage.source_path}/symly/symly.c", "w", encoding="utf-8") as f:
            f.write(symly_c)
        gcc = which("/usr/bin/gcc")
        if sys.platform == "darwin":
            gcc = which("/usr/bin/clang")
        mkdirp(prefix.bin)
        mkdirp(prefix.lib64)
        gcc("-o", "symly.bin", "symly/symly.c")
        print("prefix.bin", prefix.bin)
        copy("symly.bin", f"{prefix.bin}/symly")
        # create a symlinked file.
        os.symlink(f"{prefix.bin}/symly", f"{prefix.lib64}/symly")
        # Create a symlinked directory.
        os.symlink(prefix.bin, prefix.include)
