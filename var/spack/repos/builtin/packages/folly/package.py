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


class Folly(AutotoolsPackage):
    """Folly (acronymed loosely after Facebook Open Source Library) is a
    library of C++11 components designed with practicality and efficiency
    in mind.

    Folly contains a variety of core library components used extensively at
    Facebook. In particular, it's often a dependency of Facebook's other open
    source C++ efforts and place where those projects can share code.
    """

    homepage = "https://github.com/facebook/folly"
    url = "https://github.com/facebook/folly/archive/v2017.06.05.00.tar.gz"

    version('2017.06.05.00', 'a25e8d646702c3e0c1400f591e485a33')
    version('2016.11.14.00', '88550acdb4d4b331c0ca9922039c8727')
    version('2016.11.07.00', '2f605b20ad539bccdbfd361daa92081e')
    version('2016.10.31.00', 'ab3049302792f8470cef64f3a29eedec')
    version('2016.10.24.00', '0445efb7c16b5c32dfbb173157e54866')
    version('2016.10.17.00', 'b7e01934a45c5036fab8fdc70e9eaf4d')

    depends_on('m4', type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
    depends_on('pkgconfig', type='build')

    # TODO: folly requires gcc 4.9+ and a version of boost compiled with
    # TODO: C++14 support (but there's no neat way to check that these
    # TODO: constraints are met right now)
    depends_on('boost')

    depends_on('gflags')
    depends_on('glog')
    depends_on('double-conversion')
    depends_on('libevent')

    configure_directory = 'folly'
