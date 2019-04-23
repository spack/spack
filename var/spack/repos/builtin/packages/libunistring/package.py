# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libunistring(AutotoolsPackage):
    """This library provides functions for manipulating Unicode strings
    and for manipulating C strings according to the Unicode standard."""

    homepage = "https://www.gnu.org/software/libunistring/"
    url      = "https://ftpmirror.gnu.org/libunistring/libunistring-0.9.7.tar.xz"

    version('0.9.10', sha256='eb8fb2c3e4b6e2d336608377050892b54c3c983b646c561836550863003c05d7')
    version('0.9.7', '82e0545363d111bfdfec2ddbfe62ffd3')
    version('0.9.6', 'cb09c398020c27edac10ca590e9e9ef3')
