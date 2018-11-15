# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from six import string_types

from spack import *
import spack.architecture

from spack.pkg.builtin.mock.multimethod_base import MultimethodBase


class Multimethod(MultimethodBase):
    """This package is designed for use with Spack's multimethod test.
       It has a bunch of test cases for the @when decorator that the
       test uses.
    """

    homepage = 'http://www.example.com/'
    url      = 'http://www.example.com/example-1.0.tar.gz'

    #
    # These functions are only valid for versions 1, 2, and 3.
    #
    @when('@1.0')
    def no_version_2(self):
        return 1

    @when('@3.0')
    def no_version_2(self):
        return 3

    @when('@4.0')
    def no_version_2(self):
        return 4

    #
    # These functions overlap, so there is ambiguity, but we'll take
    # the first one.
    #
    @when('@:4')
    def version_overlap(self):
        return 1

    @when('@2:')
    def version_overlap(self):
        return 2

    #
    # More complicated case with cascading versions.
    #
    def mpi_version(self):
        return 0

    @when('^mpi@3:')
    def mpi_version(self):
        return 3

    @when('^mpi@2:')
    def mpi_version(self):
        return 2

    @when('^mpi@1:')
    def mpi_version(self):
        return 1

    #
    # Use these to test whether the default method is called when no
    # match is found.  This also tests whether we can switch methods
    # on compilers
    #
    def has_a_default(self):
        return 'default'

    @when('%gcc')
    def has_a_default(self):
        return 'gcc'

    @when('%intel')
    def has_a_default(self):
        return 'intel'

    #
    # Make sure we can switch methods on different target
    #
    platform = spack.architecture.platform()
    targets = list(platform.targets.values())
    if len(targets) > 1:
        targets = targets[:-1]

    for target in targets:
        @when('target=' + target.name)
        def different_by_target(self):
            if isinstance(self.spec.architecture.target, string_types):
                return self.spec.architecture.target
            else:
                return self.spec.architecture.target.name
    #
    # Make sure we can switch methods on different dependencies
    #

    @when('^mpich')
    def different_by_dep(self):
        return 'mpich'

    @when('^zmpi')
    def different_by_dep(self):
        return 'zmpi'

    #
    # Make sure we can switch on virtual dependencies
    #
    def different_by_virtual_dep(self):
        return 1

    @when('^mpi@2:')
    def different_by_virtual_dep(self):
        return 2

    #
    # Make sure methods with a default implementation in a superclass
    # will invoke that method when none in the subclass match.
    #
    @when("@2:")
    def base_method(self):
        return "subclass_method"
