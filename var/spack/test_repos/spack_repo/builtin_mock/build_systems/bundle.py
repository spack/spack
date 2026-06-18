# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import Builder, PackageBase, Prefix, Spec, build_system, register_builder


class BundlePackage(PackageBase):
    """General purpose bundle, or no-code, package class."""

    build_system_class = "BundlePackage"
    default_buildsystem = "bundle"
    has_code = False

    build_system("bundle")


@register_builder("bundle")
class BundleBuilder(Builder):
    phases = ("install",)

    def install(self, pkg: BundlePackage, spec: Spec, prefix: Prefix) -> None:
        pass
