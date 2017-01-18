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


class Bdftopcf(AutotoolsPackage):
    """bdftopcf is a font compiler for the X server and font server.  Fonts
    in Portable Compiled Format can be read by any architecture, although
    the file is structured to allow one particular architecture to read
    them directly without reformatting.  This allows fast reading on the
    appropriate machine, but the files are still portable (but read more
    slowly) on other machines."""

    homepage = "http://cgit.freedesktop.org/xorg/app/bdftopcf"
    url      = "https://www.x.org/archive/individual/app/bdftopcf-1.0.5.tar.gz"

    version('1.0.5', '456416d33e0d41a96b5a3725d99e1be3')

    depends_on('libxfont')

    depends_on('pkg-config@0.9.0:', type='build')
    depends_on('util-macros', type='build')
