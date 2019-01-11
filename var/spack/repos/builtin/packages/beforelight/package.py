# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Beforelight(AutotoolsPackage):
    """The beforelight program is a sample implementation of a screen saver
    for X servers supporting the MIT-SCREEN-SAVER extension.   It is only
    recommended for use as a code sample, as it does not include features
    such as screen locking or configurability."""

    homepage = "http://cgit.freedesktop.org/xorg/app/beforelight"
    url      = "https://www.x.org/archive/individual/app/beforelight-1.0.5.tar.gz"

    version('1.0.5', 'f0433eb6df647f36bbb5b38fb2beb22a')

    depends_on('libx11')
    depends_on('libxscrnsaver')
    depends_on('libxt')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
