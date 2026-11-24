# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os
import sys

from spack_repo.builtin_mock.build_systems.generic import Package
from spack_repo.builtin_mock.packages.garply.package import c_compiler

from spack.package import *


class Quux(Package):
    """Toy package for testing dependencies"""

    homepage = "https://www.example.com"
    has_code = False
    version("3.0.0")

    depends_on("garply")

    def install(self, spec, prefix):
        # Trivial C sources. The library embeds its install path both as an
        # rpath (relocated by relocate_elf_binaries) and as a hard-coded
        # .rodata string (relocated by relocate_text_bin), so both relocation
        # code paths are exercised.
        garply = spec["garply"].prefix
        with open("quux.h", "w", encoding="utf-8") as f:
            f.write("int quuxify(void);\n")
        with open("quux.c", "w", encoding="utf-8") as f:
            f.write(
                '#include "quux.h"\n#include "garply/garply.h"\n'
                'const char *quux_config = "%s";\n'
                "int quuxify(void) { return garplinate(); }\n" % prefix.config
            )
        with open("quuxifier.c", "w", encoding="utf-8") as f:
            f.write('#include "quux.h"\nint main(void) { return quuxify(); }\n')

        cc = c_compiler()
        cc("-fPIC", "-O0", "-I%s" % garply.include, "-c", "quux.c", "-o", "quux.o")

        mkdirp(prefix.lib64)
        if sys.platform == "darwin":
            lib = "libquux.dylib"
            garply_lib = os.path.join(garply.lib64, "libgarply.dylib")
            cc(
                "-dynamiclib",
                "-install_name",
                "@rpath/" + lib,
                "-o",
                lib,
                "quux.o",
                "-Wl,-rpath,%s" % garply.lib64,
                garply_lib,
            )
        else:
            lib = "libquux.so"
            garply_lib = os.path.join(garply.lib64, "libgarply.so")
            cc(
                "-shared",
                "-Wl,-soname,%s" % lib,
                "-o",
                lib,
                "quux.o",
                "-Wl,-rpath,%s" % garply.lib64,
                garply_lib,
            )
        cc(
            "-o",
            "quuxifier",
            "quuxifier.c",
            "-Wl,-rpath,%s" % prefix.lib64,
            "-Wl,-rpath,%s" % garply.lib64,
            lib,
        )
        copy(lib, os.path.join(prefix.lib64, lib))
        os.link(os.path.join(prefix.lib64, lib), os.path.join(prefix.lib64, lib + ".3.0"))
        copy("quuxifier", os.path.join(prefix.lib64, "quuxifier"))

        mkdirp("%s/quux" % prefix.include)
        copy("quux.h", "%s/quux/quux.h" % prefix.include)
        mkdirp(prefix.bin)
        os.symlink("%s/quuxifier" % prefix.lib64, "%s/quuxifier" % prefix.bin)
        os.symlink("%s/garplinator" % garply.lib64, "%s/garplinator" % prefix.bin)
