##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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


class Libxvmc(AutotoolsPackage):
    """X.org libXvMC library."""

    homepage = "https://cgit.freedesktop.org/xorg/lib/libXvMC"
    url      = "https://www.x.org/archive/individual/lib/libXvMC-1.0.9.tar.gz"

    version('1.0.9', 'a28c0780373537f4774565309b31a69e')

    depends_on('libx11@1.6:')
    depends_on('libxext')
    depends_on('libxv')

    depends_on('xextproto', type='build')
    depends_on('videoproto', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
