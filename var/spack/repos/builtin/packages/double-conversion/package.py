# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class DoubleConversion(CMakePackage):
    """This project (double-conversion) provides binary-decimal and decimal-binary
    routines for IEEE doubles.

    The library consists of efficient conversion routines that have been
    extracted from the V8 JavaScript engine. The code has been refactored
    and improved so that it can be used more easily in other projects.

    There is extensive documentation in src/double-conversion.h. Other examples
    can be found in test/cctest/test-conversions.cc.
    """

    homepage = "https://github.com/google/double-conversion"
    url      = "https://github.com/google/double-conversion/archive/v2.0.1.zip"

    version('2.0.1', '5be77f780841af528e92986d46620b1e')
    version('2.0.0', '045f7927246c368b57dcdb844ec61211')
    version('1.1.5', 'ddf782373e2630c07b2691c31cee0b24')
    version('1.1.4', '5df72704406d93cd54c73d73f02e2744')
    version('1.1.3', 'b312152c8c66c80449d5e0325b94502e')

    def cmake_args(self):
        return ['-DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=true']
