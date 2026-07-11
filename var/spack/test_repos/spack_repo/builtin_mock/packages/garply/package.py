# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os
import sys

from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


def c_compiler():
    """Return a C compiler, ignoring Spack's compiler wrapper on PATH."""
    if sys.platform == "darwin":
        return which("/usr/bin/clang")
    path = ":".join(s for s in os.environ["PATH"].split(os.pathsep) if "lib/spack/env" not in s)
    return which("gcc", path=path)


class Garply(Package):
    """Toy package for testing dependencies"""

    homepage = "https://www.example.com"
    has_code = False
    version("3.0.0")

    def install(self, spec, prefix):
        # The library embeds its install path twice: as an rpath (relocated by
        # relocate_elf_binaries, in the ELF dynamic section) and as a hard-coded
        # .rodata string (relocated by relocate_text_bin / BinaryFilePrefixReplacer),
        # so both relocation code paths are exercised.
        with open("garply.h", "w", encoding="utf-8") as f:
            f.write("int garplinate(void);\n")
        with open("garply.c", "w", encoding="utf-8") as f:
            f.write(
                '#include "garply.h"\n'
                'const char *garply_config = "%s";\n'
                "int garplinate(void) { return 3; }\n" % prefix.config
            )
        with open("garplinator.c", "w", encoding="utf-8") as f:
            f.write('#include "garply.h"\nint main(void) { return garplinate(); }\n')

        cc = c_compiler()
        cc("-fPIC", "-O0", "-c", "garply.c", "-o", "garply.o")

        mkdirp(prefix.lib64)
        if sys.platform == "darwin":
            lib = "libgarply.dylib"
            cc("-dynamiclib", "-install_name", "@rpath/" + lib, "-o", lib, "garply.o")
            cc("-o", "garplinator", "garplinator.c", "-Wl,-rpath,%s" % prefix.lib64, lib)
            copy(lib, os.path.join(prefix.lib64, lib))
            os.link(os.path.join(prefix.lib64, lib), os.path.join(prefix.lib64, lib + ".3.0"))
        else:
            lib = "libgarply.so"
            cc("-shared", "-Wl,-soname,%s" % lib, "-o", lib, "garply.o")
            cc("-o", "garplinator", "garplinator.c", "-Wl,-rpath,%s" % prefix.lib64, lib)
            copy(lib, os.path.join(prefix.lib64, lib))
            os.link(os.path.join(prefix.lib64, lib), os.path.join(prefix.lib64, lib + ".3.0"))
        copy("garplinator", os.path.join(prefix.lib64, "garplinator"))

        mkdirp("%s/garply" % prefix.include)
        copy("garply.h", "%s/garply/garply.h" % prefix.include)
        mkdirp(prefix.bin)
        os.symlink("%s/garplinator" % prefix.lib64, "%s/garplinator" % prefix.bin)
