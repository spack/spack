# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class XorgGtest(AutotoolsPackage):
    """Provides a Google Test environment for starting and stopping
    a X server for testing purposes."""

    homepage = "https://people.freedesktop.org/~cndougla/xorg-gtest/"
    url      = "https://www.x.org/archive/individual/test/xorg-gtest-0.7.1.tar.bz2"

    version('0.7.1', '31beb4d7d2b4eba7f9265fa0cb4c6428')

    depends_on('libx11')
    depends_on('libxi')
    depends_on('xorg-server')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')

    # TODO: may be missing evemu package?
    # TODO: what is the difference between xorg-gtest and googletest packages?
