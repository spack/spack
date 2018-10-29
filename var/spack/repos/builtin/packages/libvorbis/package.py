# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libvorbis(AutotoolsPackage):
    """Ogg Vorbis is a fully open, non-proprietary, patent-and-royalty-free,
    general-purpose compressed audio format for mid to high quality (8kHz-
    48.0kHz, 16+ bit, polyphonic) audio and music at fixed and variable
    bitrates from 16 to 128 kbps/channel."""

    homepage = "https://xiph.org/vorbis/"
    url      = "http://downloads.xiph.org/releases/vorbis/libvorbis-1.3.5.tar.gz"

    version('1.3.5', '7220e089f3be3412a2317d6fde9e3944')

    depends_on('libogg')

    depends_on('pkgconfig', type='build')

    # `make check` crashes when run in parallel
    parallel = False
