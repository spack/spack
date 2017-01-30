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


class Mesa(AutotoolsPackage):
    """Mesa is an open-source implementation of the OpenGL
    specification - a system for rendering interactive 3D graphics."""

    homepage = "http://www.mesa3d.org"
    url      = "http://ftp.iij.ad.jp/pub/X11/x.org/pub/mesa/12.0.3/mesa-12.0.3.tar.gz"

    version('12.0.3', '60c5f9897ddc38b46f8144c7366e84ad')

    # General dependencies
    depends_on('python@2.6.4:')
    depends_on('py-mako@0.3.4:')
    depends_on('flex@2.5.35:', type='build')
    depends_on('bison@2.4.1:', type='build')

    # For DRI and hardware acceleration
    depends_on('libpthread-stubs')
    depends_on('libdrm')
    depends_on('openssl')
    depends_on('libxcb@1.9.3:')
    depends_on('libxshmfence@1.1:')
    depends_on('libx11')
    depends_on('libxext')
    depends_on('libxdamage')
    depends_on('libxfixes')

    depends_on('glproto@1.4.14:', type='build')
    depends_on('dri2proto@2.6:', type='build')
    depends_on('dri3proto@1.0:', type='build')
    depends_on('presentproto@1.0:', type='build')
    depends_on('pkg-config@0.9.0:', type='build')

    # TODO: Add package for systemd, provides libudev
    # Using the system package manager to install systemd didn't work for me
