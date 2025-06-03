# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from spack_repo.builder_test.packages.callbacks import package as callbacks

from spack.package import *


class Inheritance(callbacks.Callbacks):
    """Package used to verify that inheritance among packages work as expected"""

    pass


class GenericBuilder(callbacks.GenericBuilder):
    def install(self, pkg, spec, prefix):
        super().install(pkg, spec, prefix)
        os.environ["INHERITANCE_INSTALL_CALLED"] = "1"
        os.environ["INSTALL_VALUE"] = "INHERITANCE"

    @run_before("install")
    def derived_before_install(self):
        os.environ["DERIVED_BEFORE_INSTALL_CALLED"] = "1"
        os.environ["TEST_VALUE"] = "0"
