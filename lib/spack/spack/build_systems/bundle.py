# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import spack.builder
import spack.directives
import spack.package_base

from typing import Tuple


class BundlePackage(spack.package_base.PackageBase):
    """General purpose bundle, or no-code, package class."""

    #: This attribute is used in UI queries that require to know which
    #: build-system class we are using
    build_system_class = "BundlePackage"

    #: Legacy buildsystem attribute used to deserialize and install old specs
    legacy_buildsystem = "bundle"

    #: Bundle packages do not have associated source or binary code.
    has_code = False

    spack.directives.build_system("bundle")

    phases: Tuple[str, ...] = ("promote")

    def promote(self, spec, prefix):
        # Update the explicit dependencies
        for _, cond_dict in self.dependencies.items():
            for cond, dep in cond_dict.items():
                if dep.explicit and cond in spec:
                    spack.store.db.update_explicit(spec[dep.spec.name], True)



@spack.builder.builder("bundle")
class BundleBuilder(spack.builder.Builder):
    phases = ("install",)

    def install(self, pkg, spec, prefix):
        pass
