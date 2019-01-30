# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libxrender(AutotoolsPackage):
    """libXrender - library for the Render Extension to the X11 protocol."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libXrender"
    url      = "https://www.x.org/archive/individual/lib/libXrender-0.9.10.tar.gz"

    version('0.9.10', '98a14fc11aee08b4a1769426ab4b23a3')
    version('0.9.9',  '0c797c4f2a7b782896bc223e6dac4333')

    depends_on('libx11@1.6:')

    depends_on('renderproto@0.9:', type=('build', 'link'))
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
