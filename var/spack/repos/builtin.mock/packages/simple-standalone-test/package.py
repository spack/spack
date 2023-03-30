# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SimpleStandaloneTest(Package):
    """This package has a simple stand-alone test features."""

    homepage = "http://www.example.com/simple_test"
    url = "http://www.unit-test-should-replace-this-url/simple_test-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    provides("standalone-test")

    def test_echo(self):
        """simple stand-alone test"""
        echo = which("echo")
        echo("testing echo", output=str.split, error=str.split)
