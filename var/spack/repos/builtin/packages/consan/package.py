# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Consan(MakefilePackage):
    """Pairwise RNA structural alignment, both unconstrained and constrained on alignment
    pins"""

    homepage = "http://eddylab.org/software/consan/"
    url = "http://eddylab.org/software/consan/consan-1.2.tar.gz"

    license("GPL-2.0-only", checked_by="A-N-Other")

    version("1.2", sha256="c9bc9878927a2eaef54aee91be9edd6cf2d01819cba6b6165978cea08c308b24")

    def edit(self, spec, prefix):
        # multiple individual Makefiles to edit
        filter_file(r"^CC\s+=.*", f"CC = {spack_cc}", join_path("src", "Makefile"))
        filter_file(r"^CC\s+=.*", f"CC = {spack_cc}", join_path("src", "squid", "Makefile"))
        filter_file(r"^CC\s+=.*", f"CC = {spack_cc}", join_path("src", "utilities", "Makefile"))
        filter_file(r"^CC\s+=.*", f"CC = {spack_cc}", join_path("src", "boot", "Makefile"))
        filter_file(r"^CC\s+=.*", f"CC = {spack_cc}", join_path("src", "conus-1.1", "Makefile"))

    def flag_handler(self, name, flags):
        # need to set -fcommon to prevent complaints about multiple definitions
        if name == "cflags":
            comp_spec = self.spec.compiler
            if any(
                comp_spec.satisfies(c)
                for c in ["gcc@10:", "clang@11:", "cce@11:", "aocc@3:", "oneapi"]
            ):
                flags.append("-fcommon")
        return flags, None, None

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        for f in ("scompare", "sfold", "strain_ml"):
            install(join_path("src", f), prefix.bin)
        install(join_path("src", "boot", "bstats"), prefix.bin)
        for f in ("comppair", "pModel"):
            install(join_path("src", "utilities", f), prefix.bin)
        for f in ("conus_train", "conus_compare"):
            install(join_path("src", "conus-1.1", f), prefix.bin)
