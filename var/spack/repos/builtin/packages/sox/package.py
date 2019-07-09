# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Sox(AutotoolsPackage):
    """SoX, the Swiss Army knife of sound processing programs."""

    homepage = "http://sox.sourceforge.net/Main/HomePage"
    url      = "https://downloads.sourceforge.net/project/sox/sox/14.4.2/sox-14.4.2.tar.bz2"

    version('14.4.2', 'ba804bb1ce5c71dd484a102a5b27d0dd')

    variant('mp3',
            default=False,
            description='Build with mp3 support')

    depends_on('bzip2')
    depends_on('flac')
    depends_on('id3lib')
    depends_on('libvorbis')
    depends_on('opus')
    depends_on('lame', when='+mp3')
    depends_on('libmad', when='+mp3')
