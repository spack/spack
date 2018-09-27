##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
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


class Fluxbox(AutotoolsPackage):
    """Fluxbox is a windowmanager for X that was based on the Blackbox 0.61.1 code.

    It is very light on resources and easy to handle but yet full of features
    to make an easy, and extremely fast, desktop experience.
    """

    homepage = "http://fluxbox.org/"
    url      = "http://sourceforge.net/projects/fluxbox/files/fluxbox/1.3.7/fluxbox-1.3.7.tar.gz"

    version('1.3.7', 'd99d7710f9daf793e0246dae5304b595')

    depends_on('pkgconfig', type='build')
    depends_on('freetype')
    depends_on('libxrender')
    depends_on('libxext')
    depends_on('expat')
    depends_on('libx11')
