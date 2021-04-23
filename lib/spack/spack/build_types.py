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

    def __init__(self, compiler):
        self.compiler = compiler

    @property
    def name(self):
        """get the name for the class
        """
        # TODO spack has a module that handles conversions from class names
        # to lower case names
        return self.__class__.__name__

    def get_flags(self):
        """Given a spack build type (e.g., debug) subclass, return extra flags.

        Each compiler can define a flag attribute associated with a buildtype.
        """
        # The build type can define a default value
        default = self.default
        return getattr(self.compiler, self.attr, default)


class Debug(BuildTypeBase):
    """
    The debug build type corresponds with the user asking for
    spack_build_type=debug
    """
    # If the compiler does not have a preference, give -g
    default = "-g"
    attr = 'debug_flag'


build_types = {'debug': Debug}


def get_build_type(spec):
    """Get a build type for a spec.

    The variant value has to be a string, not a BuiltType
    So we have a getter method that gets the class associated with the string
    """
    build_type = spec.variants['spack_build_type'].value
    if build_type:
        return build_types[build_type](spec.compiler)
