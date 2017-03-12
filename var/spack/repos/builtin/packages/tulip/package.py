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
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install tulip
#
# You can edit this file again by typing:
#
#     spack edit tulip
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class Tulip(CMakePackage):
    """Tulip is an information visualization framework dedicated to
        the analysis and visualization of relational data."""

    extends('python')

    homepage = "http://tulip.labri.fr/"
    url      = "https://sourceforge.net/projects/auber/files/tulip/tulip-4.10.0/tulip-4.10.0_src.tar.gz"

    version('4.10.0', '8c6ac45b8125a2a68eb1e165511e340b')

    depends_on('qt')
    depends_on('freetype')
    depends_on('zlib')
    depends_on('glew')
    depends_on('jpeg')
    depends_on('libpng')
    depends_on('doxygen')
    depends_on('libxml2')
    depends_on('py-pyqt')
    depends_on('python@2.5:2.8')

