# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Randrproto(AutotoolsPackage):
    """X Resize and Rotate Extension (RandR).

    This extension defines a protocol for clients to dynamically change X
    screens, so as to resize, rotate and reflect the root window of a screen.
    """

    homepage = "http://cgit.freedesktop.org/xorg/proto/randrproto"
    url      = "https://www.x.org/archive/individual/proto/randrproto-1.5.0.tar.gz"

    version('1.5.0', sha256='8f8a716d6daa6ba05df97d513960d35a39e040600bf04b313633f11679006fab')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
