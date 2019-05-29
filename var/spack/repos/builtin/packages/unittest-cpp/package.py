# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class UnittestCpp(CMakePackage):
    """UnitTest++ is a lightweight unit testing framework for C++. It was
    designed to do test-driven development on a wide variety of platforms.
    Simplicity, portability, speed, and small footprint are all very
    important aspects of UnitTest++. UnitTest++ is mostly standard C++ and
    makes minimal use of advanced library and language features, which
    means it should be easily portable to just about any platform."""

    homepage = "https://github.com/unittest-cpp/unittest-cpp/wiki"
    url      = "https://github.com/unittest-cpp/unittest-cpp/archive/v1.6.0.tar.gz"

    version('2.0.0', 'edaccca3e61d977881bdf1e0cf372243')
    version('1.6.0', '50f2500f76efd5b9312f19186b66b329')
