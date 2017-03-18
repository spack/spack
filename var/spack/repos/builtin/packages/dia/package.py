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


class Dia(Package):
    """Dia is a program for drawing structured diagrams."""
    homepage  = 'https://wiki.gnome.org/Apps/Dia'
    url       = 'https://ftp.gnome.org/pub/gnome/sources/dia/0.97/dia-0.97.3.tar.xz'

    version('0.97.3',    '0e744a0f6a6c4cb6a089e4d955392c3c')

    depends_on('intltool', type='build')
    depends_on('gtkplus@2.6.0:')
    depends_on('cairo')
    depends_on('libpng')
    depends_on('libxslt')
    depends_on('python')
    depends_on('swig')

    # TODO: Optional dependencies, not yet supported by Spack
    # depends_on('libart')
    # depends_on('py-gtk', type=('build', 'run'))

    def url_for_version(self, version):
        """Handle Dia's version-based custom URLs."""
        return 'https://ftp.gnome.org/pub/gnome/source/dia/%s/dia-%s.tar.xz' % (version.up_to(2), version)

    def install(self, spec, prefix):

        # configure, build, install:
        options = ['--prefix=%s' % prefix,
                   '--with-cairo',
                   '--with-xslt-prefix=%s' % spec['libxslt'].prefix,
                   '--with-python',
                   '--with-swig']

        configure(*options)
        make()
        make('install')
