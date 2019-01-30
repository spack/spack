# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Bigreqsproto(AutotoolsPackage):
    """Big Requests Extension.

    This extension defines a protocol to enable the use of requests
    that exceed 262140 bytes in length."""

    homepage = "http://cgit.freedesktop.org/xorg/proto/bigreqsproto"
    url      = "https://www.x.org/archive/individual/proto/bigreqsproto-1.1.2.tar.gz"

    version('1.1.2', '9b83369ac7a5eb2bf54c8f34db043a0e')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
