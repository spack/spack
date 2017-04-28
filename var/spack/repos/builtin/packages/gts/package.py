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


class Gts(AutotoolsPackage):
    """GTS stands for the GNU Triangulated Surface Library.

    It is an Open Source Free Software Library intended to provide a set of
    useful functions to deal with 3D surfaces meshed with interconnected
    triangles. The source code is available free of charge under the Free
    Software LGPL license.

    The code is written entirely in C with an object-oriented approach
    based mostly on the design of GTK+. Careful attention is paid to
    performance related issues as the initial goal of GTS is to provide a
    simple and efficient library to scientists dealing with 3D computational
    surface meshes.
    """

    homepage = "http://gts.sourceforge.net/index.html"
    url = "http://gts.sourceforge.net/tarballs/gts-snapshot-121130.tar.gz"

    version('121130', '023ebb6b13b8707534182a3ef0d12908')

    depends_on('glib')
