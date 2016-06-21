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

class Mesa(Package):
    """Mesa is an open-source implementation of the OpenGL
    specification - a system for rendering interactive 3D graphics."""

    homepage = "http://www.mesa3d.org"
    url      = "ftp://ftp.freedesktop.org/pub/mesa/older-versions/8.x/8.0.5/MesaLib-8.0.5.tar.gz"
    # url      = "ftp://ftp.freedesktop.org/pub/mesa/10.4.4/MesaLib-10.4.4.tar.gz"

    # version('10.4.4', '8d863a3c209bf5116b2babfccccc68ce')
    version('8.0.5', 'cda5d101f43b8784fa60bdeaca4056f2')

    # mesa 7.x, 8.x, 9.x
    depends_on("libdrm@2.4.33")
    depends_on("llvm@3.0")
    depends_on("libxml2+python")

    # patch("llvm-fixes.patch") # using newer llvm

    # mesa 10.x
    # depends_on("py-mako")
    # depends_on("flex")
    # depends_on("bison")
    # depends_on("dri2proto")
    # depends_on("libxcb")
    # depends_on("libxshmfence")


    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)

        make()
        make("install")
