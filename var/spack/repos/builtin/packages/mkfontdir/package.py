# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Mkfontdir(AutotoolsPackage):
    """mkfontdir creates the fonts.dir files needed by the legacy X server
    core font system.   The current implementation is a simple wrapper script
    around the mkfontscale program, which must be built and installed first."""

    homepage = "http://cgit.freedesktop.org/xorg/app/mkfontdir"
    url      = "https://www.x.org/archive/individual/app/mkfontdir-1.0.7.tar.gz"

    version('1.0.7', '52a5bc129f3f3ac54e7115608cec3cdc')

    depends_on('mkfontscale', type='run')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
