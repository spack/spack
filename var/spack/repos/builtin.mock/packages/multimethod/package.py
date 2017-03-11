##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
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
    targets = platform.targets.values()
    if len(targets) > 1:
        targets = targets[:-1]

    for target in targets:
        @when('target=' + target.name)
        def different_by_target(self):
            if isinstance(self.spec.architecture.target, basestring):
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
