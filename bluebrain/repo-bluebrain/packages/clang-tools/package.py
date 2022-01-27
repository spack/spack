# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from llnl.util.filesystem import install, mkdirp

from spack.directives import depends_on, version
from spack.package import Package
from spack.pkg.patches.llvm import Llvm as LLVM


class ClangTools(Package):
    """Copy binaries like clang-format out of an LLVM installation and into a
    clean directory for which a module can safely be generated."""

    has_code = False
    homepage = LLVM.homepage

    # Add a clang-format version for every LLVM version
    for llvm_ver in LLVM.versions:
        version(llvm_ver)
        depends_on(
            "llvm@{}".format(llvm_ver), when="@{}".format(llvm_ver), type="build"
        )

    def install(self, spec, prefix):
        mkdirp(spec.prefix.bin)
        for utility in ("clang-format", "clang-tidy"):
            install(
                spec["llvm"].prefix.bin.join(utility), spec.prefix.bin.join(utility)
            )
