# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import spack.builder
import spack.package

# Decorator for the generic build system
generic = spack.builder.BuilderMeta.make_decorator(build_system='generic')


@spack.builder.builder('generic')
class GenericBuilder(spack.builder.Builder):
    """A builder for a generic build system, that require packagers
    to implement an "install" phase.
    """
    #: A generic package has only the "install" phase
    phases = ('install',)

    class PackageWrapper(spack.builder.BuildWrapper):
        # This will be used as a registration decorator in user
        # packages, if need be
        generic.run_after('install')(spack.package.PackageBase.sanity_check_prefix)
        # On macOS, force rpaths for shared library IDs and remove duplicate rpaths
        generic.run_after('install')(spack.package.PackageBase.apply_macos_rpath_fixups)


class Package(spack.package.PackageBase):
    """General purpose class with a single ``install`` phase that needs to be
    coded by packagers.
    """
    #: This attribute is used in UI queries that require to know which
    #: build-system class we are using
    build_system_class = 'Package'
    #: Build system used by this package (will become a variant)
    build_system = 'generic'
