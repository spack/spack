# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import spack.builder
import spack.package


class BundlePackage(spack.package.PackageBase):
    """General purpose bundle, or no-code, package class."""
    #: This attribute is used in UI queries that require to know which
    #: build-system class we are using
    build_system_class = 'BundlePackage'

    build_system = 'bundle'
    #: Bundle packages do not have associated source or binary code.
    has_code = False


@spack.builder.builder('bundle')
class BundleBuilder(spack.builder.Builder):
    phases = ('install',)

    class PackageWrapper(spack.builder.BuildWrapper):
        def install(self, spec, prefix):
            pass
