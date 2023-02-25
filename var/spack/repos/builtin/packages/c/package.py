# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class C(Package):
    """Virtual package for C compilers."""

    homepage = "http://open-std.org/JTC1/SC22/WG14/www/standards"
    virtual = True

    def test_c_exes(self):
        """build and run C examples"""
        test_source = self.test_suite.current_test_data_dir

        for test in os.listdir(test_source):
            with test_part(
                self, "test_{0}".format(test), purpose="build and run {0}".format(test)
            ):
                filepath = test_source.join(test)
                exe_name = "{0}.exe".format(test)

                cc = which(os.environ["CC"])
                cc("-o", exe_name, filepath)

                exe = which(exe_name)
                out = exe(output=str.split, error=str.split)
                for expected in ["Hello world", "YES!"]:
                    assert expected in out
