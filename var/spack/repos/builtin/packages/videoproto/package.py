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


class Videoproto(AutotoolsPackage):
    """X Video Extension.

    This extension provides a protocol for a video output mechanism,
    mainly to rescale video playback in the video controller hardware."""

    homepage = "http://cgit.freedesktop.org/xorg/proto/videoproto"
    url      = "https://www.x.org/archive/individual/proto/videoproto-2.3.3.tar.gz"

    version('2.3.3', 'd984100603ee2420072f27bb491f4b7d')

    depends_on('pkg-config@0.9.0:', type='build')
    depends_on('util-macros', type='build')
