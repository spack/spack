# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xpr(AutotoolsPackage):
    """xpr takes as input a window dump file produced by xwd
    and formats it for output on various types of printers."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xpr"
    url      = "https://www.x.org/archive/individual/app/xpr-1.0.4.tar.gz"

    version('1.0.4', '6adfa60f458474c0c226454c233fc32f')

    depends_on('libxmu')
    depends_on('libx11')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
