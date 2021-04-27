# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *

import spack.pkg.builtin.mock.multimethod_inheritor as mi
import spack.pkg.builtin.mock.multimethod_diamond_parent as mp


class MultimethodDiamond(mi.MultimethodInheritor, mp.MultimethodDiamondParent):
    """This package is designed for use with Spack's multimethod test.
       It has a bunch of test cases for the @when decorator that the
       test uses.
    """

    @when('@4.0')
    def diamond_inheritance(self):
        return 'subclass'
