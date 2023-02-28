# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Fortran(Package):
    """Virtual package for the Fortran language."""

    homepage = "https://wg5-fortran.org/"
    virtual = True

    def test_hello(self):
        """build and run hello examples"""
        test_source = self.test_suite.current_test_data_dir
        expected = ["Hello world", "YES!"]

        for test in os.listdir(test_source):
            exe_name = "%s.exe" % test

            filepath = os.path.join(test_source, test)
            fc = which(os.environ["FC"])
            fc("-o", exe_name, filepath)

            exe = which(exe_name)
            out = exe(output=str.split, error=str.split)
            checkoutputs(expected, out)
