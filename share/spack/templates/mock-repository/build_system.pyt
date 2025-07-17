# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from typing import Tuple

from spack.package import Builder, PackageBase, Prefix, Spec, build_system, register_builder


class Package(PackageBase):
    build_system_class = "Package"
    default_buildsystem = "{{ build_system_name }}"
    build_system("{{ build_system_name }}")


@register_builder("{{ build_system_name }}")
class GenericBuilder(Builder):
    phases = ("install",)
    package_methods: Tuple[str, ...] = ()
    package_attributes: Tuple[str, ...] = ()

    def install(self, pkg: Package, spec: Spec, prefix: Prefix) -> None:
        raise NotImplementedError
