# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import (
    BuilderWithDefaults,
    PackageBase,
    Prefix,
    Spec,
    build_system,
    depends_on,
    execute_install_time_tests,
    register_builder,
    run_after,
)

from ._checks import execute_build_time_tests


class MakefilePackage(PackageBase):
    build_system_class = "MakefilePackage"
    default_buildsystem = "makefile"

    build_system("makefile")
    depends_on("gmake", type="build", when="build_system=makefile")


@register_builder("makefile")
class MakefileBuilder(BuilderWithDefaults):
    phases = ("edit", "build", "install")
    package_methods = ("check", "installcheck")
    package_attributes = (
        "build_time_test_callbacks",
        "install_time_test_callbacks",
        "build_directory",
    )

    build_time_test_callbacks = ["check"]
    install_time_test_callbacks = ["installcheck"]

    @property
    def build_directory(self) -> str:
        """Return the directory containing the main Makefile."""
        return self.pkg.stage.source_path

    def edit(self, pkg: MakefilePackage, spec: Spec, prefix: Prefix) -> None:
        pass

    def build(self, pkg: MakefilePackage, spec: Spec, prefix: Prefix) -> None:
        pass

    def install(self, pkg: MakefilePackage, spec: Spec, prefix: Prefix) -> None:
        pass

    def check(self) -> None:
        pass

    def installcheck(self) -> None:
        pass

    run_after("build")(execute_build_time_tests)
    run_after("install")(execute_install_time_tests)
