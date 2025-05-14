# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from spack.package import *

from ..callbacks.package import Callbacks
from ..callbacks.package import GenericBuilder as CallbacksGenericBuilder


class Inheritance(Callbacks):
    """Package used to verify that inheritance among packages work as expected"""

    pass


class GenericBuilder(CallbacksGenericBuilder):
    def install(self, pkg, spec, prefix):
        super().install(pkg, spec, prefix)
        os.environ["INHERITANCE_INSTALL_CALLED"] = "1"
        os.environ["INSTALL_VALUE"] = "INHERITANCE"

    @run_before("install")
    def derived_before_install(self):
        os.environ["DERIVED_BEFORE_INSTALL_CALLED"] = "1"
        os.environ["TEST_VALUE"] = "0"
