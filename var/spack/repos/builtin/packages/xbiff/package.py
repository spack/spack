# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xbiff(AutotoolsPackage):
    """xbiff provides graphical notification of new e-mail.
    It only handles mail stored in a filesystem accessible file,
    not via IMAP, POP or other remote access protocols."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xbiff"
    url      = "https://www.x.org/archive/individual/app/xbiff-1.0.3.tar.gz"

    version('1.0.3', '779c888cb45da82a612e7f47971df9ab')

    depends_on('libxaw')
    depends_on('libxmu')
    depends_on('libxext')
    depends_on('libx11')

    depends_on('xbitmaps', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
