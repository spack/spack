# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


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
