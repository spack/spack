##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
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

    depends_on('pkg-config@0.9.0:', type='build')

    # `make check` crashes when run in parallel
    parallel = False
