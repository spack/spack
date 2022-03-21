# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from llnl.util.filesystem import install, mkdirp

from spack.directives import depends_on, version
from spack.package import Package
from spack.pkg.patches.llvm import Llvm as LLVM
from spack.version import Version


class ClangTools(Package):
    """Copy binaries like clang-format out of an LLVM installation and into a
    clean directory for which a module can safely be generated."""

    has_code = False
    homepage = LLVM.homepage

    # Add a clang-format version for every LLVM version
    for llvm_ver in LLVM.versions:
        clang_tools_ver = Version(str(llvm_ver) + "p2")
        version(clang_tools_ver)
        depends_on(
            "llvm@{}".format(llvm_ver), when="@{}".format(clang_tools_ver), type="build"
        )

    def install(self, spec, prefix):
        for utility in (
            ("bin", "clang-format"),
            ("bin", "clang-tidy"),
            ("bin", "git-clang-format"),
            ("share", "clang", "clang-format-diff.py"),
        ):
            source_dir = spec["llvm"].prefix
            destination_dir = spec.prefix
            for component in utility[:-1]:
                source_dir = source_dir.join(component)
                destination_dir = destination_dir.join(component)
            mkdirp(destination_dir)
            install(source_dir.join(utility[-1]), destination_dir.join(utility[-1]))
