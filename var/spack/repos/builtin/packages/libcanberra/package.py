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


class Libcanberra(AutotoolsPackage):
    """libcanberra is an implementation of the XDG Sound Theme and
    Name Specifications, for generating event sounds on free desktops,
    such as GNOME."""

    homepage = "http://0pointer.de/lennart/projects/libcanberra/"
    url      = "http://0pointer.de/lennart/projects/libcanberra/libcanberra-0.30.tar.xz"

    version('0.30', '34cb7e4430afaf6f447c4ebdb9b42072')

    # TODO: Add variants and dependencies for the following audio support:
    # ALSA, OSS, PulseAudio, udev, GStreamer, null, GTK3+ , tdb

    variant('gtk', default=False, description='Enable optional GTK+ support')

    depends_on('libxrender',    when='+gtk')
    depends_on('libxext',       when='+gtk')
    depends_on('libx11',        when='+gtk')
    depends_on('libxinerama',   when='+gtk')
    depends_on('libxrandr',     when='+gtk')
    depends_on('libxcursor',    when='+gtk')
    depends_on('libxcomposite', when='+gtk')
    depends_on('libxdamage',    when='+gtk')
    depends_on('libxfixes',     when='+gtk')
    depends_on('libxcb',        when='+gtk')
    depends_on('libxau',        when='+gtk')
    depends_on('gtkplus',       when='+gtk')

    depends_on('libvorbis')

    depends_on('pkg-config@0.9.0:', type='build')

    def configure_args(self):
        args = ['--enable-static']

        if '+gtk' in self.spec:
            args.append('--enable-gtk')
        else:
            args.append('--disable-gtk')

        return args
