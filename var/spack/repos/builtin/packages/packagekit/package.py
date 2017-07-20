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


class Packagekit(AutotoolsPackage):
    """PackageKit is a system designed to make installing and updating
    software on your computer easier."""

    homepage = "https://www.freedesktop.org/software/PackageKit/"
    url      = "https://www.freedesktop.org/software/PackageKit/releases/PackageKit-1.1.4.tar.xz"

    version('1.1.4', 'd1a000a33c7c935522af7a01dea012bf')

    variant('gtk', default=False, description='Build GTK+-3 module functionality')

    depends_on('glib@2.46.0:')
    depends_on('sqlite')
    depends_on('polkit@0.98:')
    depends_on('systemd')
    depends_on('gobject-introspection')
    depends_on('bash-completion@2.0:')
    depends_on('gtkplus', when='+gtk')

    depends_on('pkg-config@0.9.0:', type='build')
    depends_on('intltool@0.35.0:', type='build')
    depends_on('gettext', type='build')
    depends_on('msgpack-c', type='build')
    depends_on('python@2.7:', type='build')

    # requires XML::Parser perl module
    # depends_on('perl@5.8.1:', type='build')

    def configure_args(self):
        args = []

        if '+gtk' in self.spec:
            args.append('--enable-gtk-module')
        else:
            args.append('--disable-gtk-module')

        return args
