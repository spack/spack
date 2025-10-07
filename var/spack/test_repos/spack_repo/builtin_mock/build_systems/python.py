# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import (
    PackageBase,
    Prefix,
    Spec,
    build_system,
    extends,
    register_builder,
    run_after,
)

from ._checks import BuilderWithDefaults, execute_install_time_tests


class PythonExtension(PackageBase):
    def test_imports(self) -> None:
        pass


class PythonPackage(PythonExtension):
    build_system_class = "PythonPackage"
    default_buildsystem = "python_pip"
    install_time_test_callbacks = ["test_imports"]

    build_system("python_pip")
    extends("python", when="build_system=python_pip")


@register_builder("python_pip")
class PythonPipBuilder(BuilderWithDefaults):
    phases = ("install",)
    package_methods = ("test_imports",)
    package_attributes = ("archive_files", "build_directory", "install_time_test_callbacks")
    install_time_test_callbacks = ["test_imports"]

    @property
    def build_directory(self) -> str:
        return self.pkg.stage.source_path

    def install(self, pkg: PythonPackage, spec: Spec, prefix: Prefix) -> None:
        pass

    run_after("install")(execute_install_time_tests)
