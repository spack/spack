# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Videoproto(AutotoolsPackage):
    """X Video Extension.

    This extension provides a protocol for a video output mechanism,
    mainly to rescale video playback in the video controller hardware."""

    homepage = "http://cgit.freedesktop.org/xorg/proto/videoproto"
    url      = "https://www.x.org/archive/individual/proto/videoproto-2.3.3.tar.gz"

    version('2.3.3', 'd984100603ee2420072f27bb491f4b7d')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
