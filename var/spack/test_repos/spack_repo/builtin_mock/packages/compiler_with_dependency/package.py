# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os.path

from spack_repo.builtin_mock.build_systems.compiler import CompilerPackage
from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class CompilerWithDependency(CompilerPackage, Package):
    """Simple compiler package with a dependency on fftw. Modeled after GCC mock,
    to test externals with non-compiler dependencies"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/cc-1.0.tar.gz"

    version("14.0.1", md5="abcdef0123456789abcdef0123456789")
    version("14.0", md5="abcdef0123456789abcdef0123456789")
    version("12.1.0", md5="abcdef0123456789abcdef0123456789")
    version("10.2.1", md5="abcdef0123456789abcdef0123456789")
    version("9.4.1", md5="abcdef0123456789abcdef0123456789")
    version("9.4.0", md5="abcdef0123456789abcdef0123456789")
    version("3.0", md5="def0123456789abcdef0123456789abc")
    version("2.0", md5="abcdef0123456789abcdef0123456789")
    version("1.0", md5="0123456789abcdef0123456789abcdef")

    with default_args(deprecated=True):
        version("12.4.0", md5="abcdef0123456789abcdef0123456789")

    variant(
        "languages",
        default="c,c++,fortran",
        values=("c", "c++", "fortran"),
        multi=True,
        description="Compilers and runtime libraries to build",
    )

    # This variant is here so that we can test having externals using the non-default value
    variant("binutils", default=True, description="")

    provides("c", "cxx", when="languages=c,c++")
    provides("c", when="languages=c")
    provides("cxx", when="languages=c++")
    provides("fortran", when="languages=fortran")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("fftw")
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
                when=f"%[deptypes=build virtuals={language}] {spec.name}@{spec.versions}",
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
                when=f"%[deptypes=build virtuals=fortran] {spec.name}@{spec.versions}",
                type="link",
                description=f"Add a dependency on '{gfortran_str}' for nodes compiled with "
                f"{spec} and using the 'fortran' language",
            )
        # The version of gcc-runtime is the same as the %gcc used to "compile" it
        pkg("gcc-runtime").requires(
            f"@{spec.versions}", when=f"%[deptypes=build] {spec.name}@{spec.versions}"
        )

        # If a node used %gcc@X.Y its dependencies must use gcc-runtime@:X.Y
        # (technically @:X is broader than ... <= @=X but this should work in practice)
        pkg("*").propagate(
            f"gcc@:{spec.version}", when=f"%[deptypes=build] {spec.name}@{spec.versions}"
        )
