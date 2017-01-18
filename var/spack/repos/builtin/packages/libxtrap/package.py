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


class Libxtrap(AutotoolsPackage):
    """libXTrap is the Xlib-based client API for the DEC-XTRAP extension.

    XTrap was a proposed standard extension for X11R5 which facilitated the
    capturing of server protocol and synthesizing core input events.

    Digital participated in the X Consortium's xtest working group which chose
    to evolve XTrap functionality into the XTEST & RECORD extensions for X11R6.

    As X11R6 was released in 1994, XTrap has now been deprecated for over
    15 years, and uses of it should be quite rare."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libXTrap"
    url      = "https://www.x.org/archive/individual/lib/libXTrap-1.0.1.tar.gz"

    version('1.0.1', 'fde266b82ee14da3e4f4f81c9584c1ea')

    depends_on('libx11')
    depends_on('libxt')
    depends_on('libxext')

    depends_on('trapproto', type='build')
    depends_on('xextproto', type='build')
    depends_on('pkg-config@0.9.0:', type='build')
    depends_on('util-macros', type='build')
