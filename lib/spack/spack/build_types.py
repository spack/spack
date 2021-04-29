# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Build types can add different flags depending on the compiler.
"""


class BuildTypeBase(object):
    """A build type base provides base functions to look up flags for a compiler.
    """
    default = None

    def __init__(self, spec):
        self.spec = spec
        self.default = []

    @property
    def name(self):
        """get the name for the class
        """
        return self.__class__.__name__

    def get_compiler_flags(self, group):
        """
        Get multiple flags from a compiler via a named group.
        """
        if not hasattr(self, group):
            return self.default

        attrs = []
        for attr in getattr(self, group):
            attrs += getattr(self.spec.compiler, attr, self.default)
        return attrs

    def get_package_flags(self, group, package):
        """
        Get multiple flags from a package via a named group
        """
        # Cut out early if we don't have flags or a packages
        if not hasattr(self, group) or package not in self.spec:
            return self.default

        attrs = []
        for attr in getattr(self, group):
            attrs += getattr(self.spec[package].package, attr, self.default)
        return attrs

    def get_flags(self, group=None):
        """
        Given a spack build type (e.g., debug) subclass, return extra flags.

        Each compiler can define flags attribute associated with a buildtype.
        Each package can also defined flags for build types. Eventually
        compilers will be packages so we will not need the first.
        """
        # A build type can define a list of flags for a group attribute
        if group == "cudaflags":
            return self.get_package_flags("cuda_attrs", "cuda")
        elif group in ["cflags", "cxxflags", "fflags"]:
            return self.get_compiler_flags("compiler_attrs")

        # If we don't have a group, or matching group, return default (no flags)
        return self.default


class BasicDebug(BuildTypeBase):
    """
    The debug build type corresponds with the user asking for
    spack_build_type=debug
    """
    compiler_attrs = ['debug_flag']
    cuda_attrs = ['debug_flag']


class DebugOptimized(BuildTypeBase):
    compiler_attrs = ['debug_flag', 'debug_optimize_flag']
    cuda_attrs = ['debug_flag']


class DebugMax(BuildTypeBase):
    compiler_attrs = ['debug_max_flag']
    cuda_attrs = ['debug_flag']


debug_types = {"debug", "debug+opt"}
build_types = {'debug': BasicDebug, 'debug+opt': DebugOptimized,
               'debug+max': DebugMax}


def get_build_type(spec):
    """Get a build type for a spec.

    The variant value has to be a string, not a BuiltType
    So we have a getter method that gets the class associated with the string
    """
    build_type = spec.variants['spack_build_type'].value
    if build_type:
        return build_types[build_type](spec)
