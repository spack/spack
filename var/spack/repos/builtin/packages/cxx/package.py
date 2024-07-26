# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Cxx(Package):
    """Virtual package for the C++ language."""

    homepage = "https://isocpp.org/std/the-standard"
    virtual = True

    def test_c(self):
        """Compile and run 'Hello World'"""
        test_source = self.test_suite.current_test_data_dir

        cxx_exe = os.environ["CXX"]
        cxx_exe = which(join_path(self.prefix.bin, cxx_exe))
        if cxx_exe is None:
            raise SkipTest(f"{os.environ['CXX']} not found in {self.version}")

        for test in os.listdir(test_source):
            with test_part(self, f"test_cxx_{test}", f"Test {test}"):
                filepath = os.path.join(test_source, test)
                exe_name = f"{test}.exe"
                # standard options
                # Hack to get compiler attributes
                # TODO: remove this when compilers are dependencies
                c_name = clang if self.spec.satisfies("llvm+clang") else self.name
                c_spec = spack.spec.CompilerSpec(c_name, self.spec.version)
                c_cls = spack.compilers.class_for_compiler_name(c_name)
                compiler = c_cls(c_spec, None, None, ["fakecc", "fakecxx"])
                cxx_opts = [compiler.cxx11_flag] if "c++11" in test else []
                cxx_opts += ["-o", exe_name, filepath]
                compiled = cxx_exe(*cxx_opts)

                if compiled:
                    expected = ["Hello world", "YES!"]
                    exe_run = which(join_path(self.prefix.bin, exe_name))
                    if exe_run is None:
                        raise SkipTest(f"{exe_run} not found in {self.version}")
                    out = exe_run(output=str.split, error=str.split)
                    assert expected in out
                else:
                    assert False, "Did not compile"
