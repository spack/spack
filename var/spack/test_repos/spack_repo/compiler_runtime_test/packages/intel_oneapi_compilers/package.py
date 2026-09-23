# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from spack_repo.builtin_mock.build_systems.compiler import CompilerPackage

from spack.package import *


class IntelOneapiCompilers(CompilerPackage, Package):
    """Injects a link dependency on the corresponding runtime package."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/intel-oneapi-compilers-1.0.tar.gz"

    version("2.0", md5="abcdef0123456789abcdef0123456789")
    version("1.0", md5="0123456789abcdef0123456789abcdef")

    provides("c")
    provides("cxx")

    compiler_languages = ["c", "cxx"]
    c_names = ["icx"]
    cxx_names = ["icpx"]
    compiler_version_regex = r"([0-9.]+)"
    compiler_version_argument = "-dumpversion"

    compiler_wrapper_link_paths = {
        "c": os.path.join("intel-oneapi-compilers", "icx"),
        "cxx": os.path.join("intel-oneapi-compilers", "icpx"),
    }

    depends_on("gcc", type="run")

    @classmethod
    def runtime_constraints(cls, *, spec, pkg):
        for language in ("c", "cxx", "fortran"):
            pkg("*").depends_on(
                f"intel-oneapi-runtime@{spec.version}:",
                when=f"%[deptypes=build virtuals={language}] {spec.name}@{spec.versions}",
                type="link",
                description="Inject intel-oneapi-runtime when oneapi is used as "
                f"a {language} compiler",
            )

        # The version of intel-oneapi-runtime is the same as the %oneapi used to "compile" it
        pkg("intel-oneapi-runtime").requires(
            f"@{spec.versions}", when=f"%[deptypes=build] {spec.name}@{spec.versions}"
        )

        # If the compiler depends on gcc@X.Y, the runtime must depend on gcc-runtime@X.Y
        if spec.satisfies("%gcc"):
            try:
                gcc = spec["gcc"]
                pkg("intel-oneapi-runtime").requires(
                    f"@{spec.versions} %gcc-runtime@{gcc.version}",
                    when=f"%[deptypes=build] {spec.name}/{spec.dag_hash()}",
                )
            except (RuntimeError, KeyError):
                # Externals may not have gcc as a dependency, but still satisfy %gcc
                pass

        # If a node used %intel-oneapi-runtime@X.Y its dependencies must use @:X.Y
        # (technically @:X is broader than ... <= @=X but this should work in practice)
        pkg("*").propagate(
            f"intel-oneapi-compilers@:{spec.version}",
            when=f"%[deptypes=build] {spec.name}@{spec.versions}",
        )
