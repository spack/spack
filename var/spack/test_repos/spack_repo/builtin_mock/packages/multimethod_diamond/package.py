# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

from ..multimethod_diamond_parent import package as mp
from ..multimethod_inheritor import package as mi


class MultimethodDiamond(mi.MultimethodInheritor, mp.MultimethodDiamondParent):
    """This package is designed for use with Spack's multimethod test.
    It has a bunch of test cases for the @when decorator that the
    test uses.
    """

    @when("@4.0")
    def diamond_inheritance(self):
        return "subclass"
