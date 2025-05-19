# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from typing import Tuple

from spack.package import PackageBase, Prefix, Spec, build_system, register_builder, run_after

from ._checks import BuilderWithDefaults, apply_macos_rpath_fixups, execute_install_time_tests


class Package(PackageBase):
    """General purpose class with a single ``install`` phase that needs to be
    coded by packagers.
    """

    #: This attribute is used in UI queries that require to know which
    #: build-system class we are using
    build_system_class = "Package"
    #: Legacy buildsystem attribute used to deserialize and install old specs
    legacy_buildsystem = "generic"

    build_system("generic")


@register_builder("generic")
class GenericBuilder(BuilderWithDefaults):
    """A builder for a generic build system, that require packagers
    to implement an "install" phase.
    """

    #: A generic package has only the "install" phase
    phases = ("install",)

    #: Names associated with package methods in the old build-system format
    legacy_methods: Tuple[str, ...] = ()

    #: Names associated with package attributes in the old build-system format
    legacy_attributes: Tuple[str, ...] = ("archive_files", "install_time_test_callbacks")

    #: Callback names for post-install phase tests
    install_time_test_callbacks = []

    # On macOS, force rpaths for shared library IDs and remove duplicate rpaths
    run_after("install", when="platform=darwin")(apply_macos_rpath_fixups)

    # unconditionally perform any post-install phase tests
    run_after("install")(execute_install_time_tests)

    def install(self, pkg: Package, spec: Spec, prefix: Prefix) -> None:
        raise NotImplementedError
