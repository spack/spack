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


class Xproto(AutotoolsPackage):
    """X Window System Core Protocol.

    This package provides the headers and specification documents defining
    the X Window System Core Protocol, Version 11.

    It also includes a number of headers that aren't purely protocol related,
    but are depended upon by many other X Window System packages to provide
    common definitions and porting layer."""

    homepage = "http://cgit.freedesktop.org/xorg/proto/x11proto"
    url      = "https://www.x.org/archive/individual/proto/xproto-7.0.31.tar.gz"

    version('7.0.31', '04b925bf9e472c80f9212615cd684f1e')
    version('7.0.29', '16a78dd2c5ad73011105c96235f6a0af')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')

    def install(self, spec, prefix):
        # Installation fails in parallel
        # See https://github.com/spack/spack/issues/4805
        make('install', parallel=False)
