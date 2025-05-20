# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import spack.builder
import spack.package_base
from spack.package import Prefix, Spec, build_system


class BundlePackage(spack.package_base.PackageBase):
    """General purpose bundle, or no-code, package class."""

    #: This attribute is used in UI queries that require to know which
    #: build-system class we are using
    build_system_class = "BundlePackage"

    #: Legacy buildsystem attribute used to deserialize and install old specs
    legacy_buildsystem = "bundle"

    #: Bundle packages do not have associated source or binary code.
    has_code = False

    build_system("bundle")


@spack.builder.builder("bundle")
class BundleBuilder(spack.builder.Builder):
    phases = ("install",)

    def install(self, pkg: BundlePackage, spec: Spec, prefix: Prefix) -> None:
        pass
