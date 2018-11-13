# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xcompmgr(AutotoolsPackage):
    """xcompmgr is a sample compositing manager for X servers supporting the
    XFIXES, DAMAGE, RENDER, and COMPOSITE extensions.  It enables basic
    eye-candy effects."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xcompmgr"
    url      = "https://www.x.org/archive/individual/app/xcompmgr-1.1.7.tar.gz"

    version('1.1.7', '4992895c8934bbc99bb2447dfe5081f2')

    depends_on('libxcomposite')
    depends_on('libxfixes')
    depends_on('libxdamage')
    depends_on('libxrender')
    depends_on('libxext')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
