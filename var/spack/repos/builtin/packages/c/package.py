# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class C(Package):
    """Virtual package for C compilers."""

    homepage = "http://open-std.org/JTC1/SC22/WG14/www/standards"
    virtual = True

    def test_c(self):
        """Compile and run 'Hello world'"""

        test_source = self.test_suite.current_test_data_dir

        cc_exe = os.environ["CC"]
        cc_exe = which(join_path(self.prefix.bin, cc_exe))
        if cc_exe is None:
            raise SkipTest(f"{os.environ['CC']} not found in {self.version}")

        for test in os.listdir(test_source):
            with test_part(self, f"test_c_{test}", f"Test {test}"):
                filepath = test_source.join(test)
                exe_name = f"{test}.exe"
                cc_opts = ["-o", exe_name, filepath]
                comp_exe = which(join_path(self.prefix.bin, cc_exe))
                if comp_exe is None:
                    raise SkipTest(f"{str(cc_exe)} not found in {self.version}")
                compiled = cc_exe(*cc_opts)

                if compiled:
                    expected = ["Hello world", "YES!"]
                    exe = which(join_path(self.prefix.bin, exe_name))
                    if exe is None:
                        raise SkipTest(f"{exe} not found in {self.version}")
                    out = exe(output=str.split, error=str.split)
                    check_outputs(expected, out)
                else:
                    assert False, "Did not compile"
