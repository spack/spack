# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.pkg.builtin.mock.python as mp
from spack.package import *


class PyTestCallback(mp.Python):
    """A package for testing stand-alone test methods as a callback."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/test-callback-1.0.tar.gz"

    # TODO (post-34236): "test" -> "test_callback" once remove "test" support
    install_time_test_callbacks = ["test"]

    version("1.0", "00000000000000000000000000000110")
    version("2.0", "00000000000000000000000000000120")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)

    # TODO (post-34236): "test" -> "test_callback" once remove "test" support
    def test(self):
        super().test()

        print("PyTestCallback test")
