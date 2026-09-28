# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack_repo.builtin_mock.build_systems.generic import Package
from spack_repo.builtin_mock.packages.garply.package import c_compiler

from spack.package import *


class RpathRoot(Package):
    """Package with an executable that has an RPATH entry for each of its link dependencies"""

    homepage = "http://www.example.com"
    has_code = False

    version("1.0")

    depends_on("rpath-mid")
    depends_on("rpath-other")

    def install(self, spec, prefix):
        with open("main.c", "w", encoding="utf-8") as f:
            f.write("int main(void) { return 0; }\n")
        rpaths = [prefix.lib] + [
            d.prefix.lib for d in spec.traverse(root=False, order="topo", deptype="link")
        ]
        if sys.platform == "darwin":
            # Leave room in the header for relocation, like the compiler wrapper does
            flags = ["-Wl,-headerpad_max_install_names"]
        else:
            flags = ["-Wl,--disable-new-dtags"]
        mkdirp(prefix.bin)
        c_compiler()(
            *flags, *(f"-Wl,-rpath,{rpath}" for rpath in rpaths), "-o", prefix.bin.app, "main.c"
        )
