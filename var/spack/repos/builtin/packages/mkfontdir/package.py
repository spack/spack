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


class Mkfontdir(AutotoolsPackage):
    """mkfontdir creates the fonts.dir files needed by the legacy X server
    core font system.   The current implementation is a simple wrapper script
    around the mkfontscale program, which must be built and installed first."""

    homepage = "http://cgit.freedesktop.org/xorg/app/mkfontdir"
    url      = "https://www.x.org/archive/individual/app/mkfontdir-1.0.7.tar.gz"

    version('1.0.7', '52a5bc129f3f3ac54e7115608cec3cdc')

    depends_on('mkfontscale', type='run')

    depends_on('pkg-config@0.9.0:', type='build')
    depends_on('util-macros', type='build')
