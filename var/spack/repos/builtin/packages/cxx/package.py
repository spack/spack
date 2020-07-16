# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

class Cxx(Package):
    """Virtual package for the C++ language."""
    homepage = 'https://isocpp.org/std/the-standard'
    virtual = True

    def test(self):
        test_source = os.path.join(self.test_dir, 'data', 'cxx')

        for test in os.listdir(test_source):
            filepath = os.path.join(test_source, test)
            exe_name = '%s.exe' % test

            cxx_exe = os.environ['CXX']

            # standard options
            cxx_opts = [self.cxx11_flag] if 'c++11' in test else []

            cxx_opts += ['-o', exe_name, filepath]
            compiled = self.run_test(cxx_exe, options=cxx_opts, installed=True)

            if compiled:
                expected = ['Hello world', 'YES!']
                self.run_test(exe_name, expected=expected)
