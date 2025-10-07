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

from ._checks import BuilderWithDefaults, execute_build_time_tests


class PerlPackage(PackageBase):
    """Specialized class for packages that are built using Perl."""

    build_system_class = "PerlPackage"
    default_buildsystem = "perl"

    build_system("perl")
    extends("perl", when="build_system=perl")

    def test_use(self):
        pass


@register_builder("perl")
class PerlBuilder(BuilderWithDefaults):
    phases = ("configure", "build", "install")
    package_methods = ("check", "test_use")
    package_attributes = ()
    build_time_test_callbacks = ["check"]

    def configure(self, pkg: PerlPackage, spec: Spec, prefix: Prefix) -> None:
        pass

    def build(self, pkg: PerlPackage, spec: Spec, prefix: Prefix) -> None:
        pass

    def install(self, pkg: PerlPackage, spec: Spec, prefix: Prefix) -> None:
        pass

    def check(self):
        pass

    # Ensure that tests run after build (if requested):
    run_after("build")(execute_build_time_tests)
