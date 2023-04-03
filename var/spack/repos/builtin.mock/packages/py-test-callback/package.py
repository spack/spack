# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.pkg.builtin.mock.python as mp
from spack.package import *


class PyTestCallback(mp.Python):
    """A package for testing stand-alone test methods as a callback."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/test-callback-1.0.tar.gz"

    version("1.0", "00000000000000000000000000000110")
    version("2.0", "00000000000000000000000000000120")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)

    def test(self):
        super(PyTestCallback, self).test()

        print("PyTestCallback test")
