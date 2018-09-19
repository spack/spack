##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
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
