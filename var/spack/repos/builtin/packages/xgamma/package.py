# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xgamma(AutotoolsPackage):
    """xgamma allows X users to query and alter the gamma correction of a
    monitor via the X video mode extension (XFree86-VidModeExtension)."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xgamma"
    url      = "https://www.x.org/archive/individual/app/xgamma-1.0.6.tar.gz"

    version('1.0.6', 'ac4f91bf1d9aa0433152ba6196288cc6')

    depends_on('libx11')
    depends_on('libxxf86vm')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
