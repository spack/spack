# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libunistring(AutotoolsPackage):
    """This library provides functions for manipulating Unicode strings
    and for manipulating C strings according to the Unicode standard."""

    homepage = "https://www.gnu.org/software/libunistring/"
    url      = "https://ftpmirror.gnu.org/libunistring/libunistring-0.9.10.tar.xz"

    version('0.9.10', sha256='eb8fb2c3e4b6e2d336608377050892b54c3c983b646c561836550863003c05d7')
    version('0.9.9',  sha256='a4d993ecfce16cf503ff7579f5da64619cee66226fb3b998dafb706190d9a833')
    version('0.9.8',  sha256='7b9338cf52706facb2e18587dceda2fbc4a2a3519efa1e15a3f2a68193942f80')
    version('0.9.7', '82e0545363d111bfdfec2ddbfe62ffd3')
    version('0.9.6', 'cb09c398020c27edac10ca590e9e9ef3')

    depends_on('libiconv')

    # glibc 2.28+ removed libio.h and thus _IO_ftrylockfile
    patch('removed_libio.patch', when='@:0.9.9')
