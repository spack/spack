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
#
from spack import *


class LxdeLxterminal(AutotoolsPackage):
    """LXDE Terminal Emulator"""

    homepage = "https://wiki.lxde.org/en/LXTerminal"
    url      = "https://downloads.sourceforge.net/project/lxde/LXTerminal%20%28terminal%20emulator%29/LXTerminal%200.2.0/lxterminal-0.2.0.tar.gz"

    version('0.2.0', 'e80ad1b6e26212f3d43908c2ad87ba4d')

    depends_on('libtool', type='build')
    depends_on('pkg-config', type='build')
    depends_on('binutils', type='build')
    depends_on('intltool', type='build')
    depends_on('perl-xml-parser', type='build')
    depends_on('perl', type='build')
    depends_on('libx11')
    depends_on('gtkplus')
    depends_on('glib')
    depends_on('lxde-menu-cache')
    depends_on('vte')
