# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libxv(AutotoolsPackage):
    """libXv - library for the X Video (Xv) extension to the
    X Window System."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libXv"
    url      = "https://www.x.org/archive/individual/lib/libXv-1.0.10.tar.gz"

    version('1.0.10', 'e7182673b4bbe3ca00ac932e22edc038')

    depends_on('libx11@1.6:')
    depends_on('libxext')

    depends_on('xextproto', type='build')
    depends_on('videoproto', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
