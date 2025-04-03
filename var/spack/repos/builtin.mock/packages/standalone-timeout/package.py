# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class StandaloneTimeout(Package):
    """This package exercises the stand-alone test timeout feature."""

    homepage = "http://www.example.com/simple_timeout"
    url = "http://www.unit-test-should-replace-this-url/simple_timeout-1.0.tar.gz"

    version("1.0", md5="123456789abcdef0123456789abcdefg")
    version("0.9", md5="0123456789abcdef0123456789abcdef")

    def test_timeout(self):
        """simple timeout test"""
        import time

        # Make sure the value here exceeds the value in the unit test.
        time.sleep(20)

        print("Ran test_timeout")
