# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Scrnsaverproto(AutotoolsPackage):
    """MIT Screen Saver Extension.

    This extension defines a protocol to control screensaver features
    and also to query screensaver info on specific windows."""

    homepage = "http://cgit.freedesktop.org/xorg/proto/scrnsaverproto"
    url      = "https://www.x.org/archive/individual/proto/scrnsaverproto-1.2.2.tar.gz"

    version('1.2.2', '21704f1bad472d94abd22fea5704bb48')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
