# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os.path

from spack.package import *


class Gcc(CompilerPackage, Package):
    """Simple compiler package."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/gcc-1.0.tar.gz"

    version("14.0", md5="abcdef0123456789abcdef0123456789")
    version("3.0", md5="def0123456789abcdef0123456789abc")
    version("2.0", md5="abcdef0123456789abcdef0123456789")
    version("1.0", md5="0123456789abcdef0123456789abcdef")

    variant(
        "languages",
        default="c,c++,fortran",
        values=("c", "c++", "fortran"),
        multi=True,
        description="Compilers and runtime libraries to build",
    )

    provides("c", "cxx", when="languages=c,c++")
    provides("c", when="languages=c")
    provides("cxx", when="languages=c++")
    provides("fortran", when="languages=fortran")

    depends_on("c", type="build")

    c_names = ["gcc"]
    cxx_names = ["g++"]
    fortran_names = ["gfortran"]
    compiler_prefixes = [r"\w+-\w+-\w+-"]
    compiler_suffixes = [r"-mp-\d+(?:\.\d+)?", r"-\d+(?:\.\d+)?", r"\d\d"]
    compiler_version_regex = r"(?<!clang version)\s?([0-9.]+)"
    compiler_version_argument = ("-dumpfullversion", "-dumpversion")

    compiler_wrapper_link_paths = {
        "c": os.path.join("gcc", "gcc"),
        "cxx": os.path.join("gcc", "g++"),
        "fortran": os.path.join("gcc", "gfortran"),
    }

    def install(self, spec, prefix):
        # Create the minimal compiler that will fool `spack compiler find`
        mkdirp(prefix.bin)
        with open(prefix.bin.gcc, "w", encoding="utf-8") as f:
            f.write('#!/bin/bash\necho "%s"' % str(spec.version))
        set_executable(prefix.bin.gcc)

    def _cc_path(self):
        if self.spec.satisfies("languages=c"):
            return str(self.spec.prefix.bin.gcc)
        return None

    def _cxx_path(self):
        if self.spec.satisfies("languages=c++"):
            return os.path.join(self.spec.prefix.bin, "g++")
        return None

    def _fortran_path(self):
        if self.spec.satisfies("languages=fortran"):
            return str(self.spec.prefix.bin.gfortran)
        return None

    @classmethod
    def runtime_constraints(cls, *, spec, pkg):
        """Callback function to inject runtime-related rules into the solver.

        Rule-injection is obtained through method calls of the ``pkg`` argument.

        Documentation for this function is temporary. When the API will be in its final state,
        we'll document the behavior at https://spack.readthedocs.io/en/latest/

        Args:
            spec: spec that will inject runtime dependencies
            pkg: object used to forward information to the solver
        """
        for language in ("c", "cxx", "fortran"):
            pkg("*").depends_on(
                f"gcc-runtime@{spec.version}:",
                when=f"%[virtuals={language}] {spec.name}@{spec.versions}",
                type="link",
                description=f"Inject gcc-runtime when gcc is used as a {language} compiler",
            )

        gfortran_str = "libgfortran@5"
        if spec.satisfies("gcc@:6"):
            gfortran_str = "libgfortran@3"
        elif spec.satisfies("gcc@7"):
            gfortran_str = "libgfortran@4"

        for fortran_virtual in ("fortran-rt", gfortran_str):
            pkg("*").depends_on(
                fortran_virtual,
                when=f"%[virtuals=fortran] {spec.name}@{spec.versions}",
                type="link",
                description=f"Add a dependency on '{gfortran_str}' for nodes compiled with "
                f"{spec} and using the 'fortran' language",
            )
        # The version of gcc-runtime is the same as the %gcc used to "compile" it
        pkg("gcc-runtime").requires(f"@{spec.versions}", when=f"%{spec.name}@{spec.versions}")

        # If a node used %gcc@X.Y its dependencies must use gcc-runtime@:X.Y
        # (technically @:X is broader than ... <= @=X but this should work in practice)
        pkg("*").propagate(f"gcc@:{spec.version}", when=f"%{spec.name}@{spec.versions}")
