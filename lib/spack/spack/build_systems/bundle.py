# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import spack.builder
import spack.directives
import spack.package_base


class BundlePackageNoDep(spack.package_base.PackageBaseNoDep):
    """General purpose bundle, or no-code, package class."""

    #: This attribute is used in UI queries that require to know which
    #: build-system class we are using
    build_system_class = "BundlePackage"

    #: Legacy buildsystem attribute used to deserialize and install old specs
    legacy_buildsystem = "bundle"

    #: Bundle packages do not have associated source or binary code.
    has_code = False

    spack.directives.build_system("bundle")


class BundlePackage(BundlePackageNoDep):
    spack.package_base.add_base_deps()


@spack.builder.builder("bundle")
class BundleBuilder(spack.builder.Builder):
    phases = ("install",)

    def install(self, pkg, spec, prefix):
        pass
