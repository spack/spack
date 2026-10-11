# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os
import sys

from spack_repo.builtin_mock.build_systems.generic import Package
from spack_repo.builtin_mock.packages.garply.package import c_compiler

from spack.package import *


class Corge(Package):
    """A toy package to test dependencies"""

    homepage = "https://www.example.com"
    has_code = False
    version("3.0.0")

    depends_on("quux")

    def install(self, spec, prefix):
        # Trivial C sources. The library embeds its install path both as an
        # rpath (relocated by relocate_elf_binaries) and as a hard-coded
        # .rodata string (relocated by relocate_text_bin), so both relocation
        # code paths are exercised.
        quux = spec["quux"].prefix
        garply = spec["garply"].prefix
        with open("corge.h", "w", encoding="utf-8") as f:
            f.write("int corgegate(void);\n")
        with open("corge.c", "w", encoding="utf-8") as f:
            f.write(
                '#include "corge.h"\n#include "quux/quux.h"\n'
                'const char *corge_config = "%s";\n'
                "int corgegate(void) { return quuxify(); }\n" % prefix.config
            )
        with open("corgegator.c", "w", encoding="utf-8") as f:
            f.write('#include "corge.h"\nint main(void) { return corgegate(); }\n')

        cc = c_compiler()
        cc("-fPIC", "-O0", "-I%s" % quux.include, "-c", "corge.c", "-o", "corge.o")

        mkdirp(prefix.lib64)
        if sys.platform == "darwin":
            lib = "libcorge.dylib"
            quux_lib = os.path.join(quux.lib64, "libquux.dylib")
            cc("-dynamiclib", "-install_name", "@rpath/" + lib, "-o", lib, "corge.o", quux_lib)
        else:
            lib = "libcorge.so"
            quux_lib = os.path.join(quux.lib64, "libquux.so")
            garply_lib = os.path.join(garply.lib64, "libgarply.so")
            cc("-shared", "-Wl,-soname,%s" % lib, "-o", lib, "corge.o", quux_lib, garply_lib)
        cc(
            "-o",
            "corgegator",
            "corgegator.c",
            "-Wl,-rpath,%s" % prefix.lib64,
            "-Wl,-rpath,%s" % quux.lib64,
            "-Wl,-rpath,%s" % garply.lib64,
            lib,
        )
        copy(lib, os.path.join(prefix.lib64, lib))
        os.link(os.path.join(prefix.lib64, lib), os.path.join(prefix.lib64, lib + ".3.0"))
        copy("corgegator", os.path.join(prefix.lib64, "corgegator"))

        mkdirp("%s/corge" % prefix.include)
        copy("corge.h", "%s/corge/corge.h" % prefix.include)
        mkdirp(prefix.bin)
        os.symlink("%s/corgegator" % prefix.lib64, "%s/corgegator" % prefix.bin)
        os.symlink("%s/quuxifier" % quux.lib64, "%s/quuxifier" % prefix.bin)
        os.symlink("%s/garplinator" % garply.lib64, "%s/garplinator" % prefix.bin)
