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


class Gource(AutotoolsPackage):
    """Software version control visualization."""

    homepage = "http://gource.io"
    url = "https://github.com/acaudwell/Gource/releases/download/gource-0.44/gource-0.44.tar.gz"

    version('0.44', '79cda1bfaad16027d59cce55455bfab88b57c69d')

    depends_on('automake',   type='build')
    depends_on('autoconf',   type='build')
    depends_on('libtool',    type='build')
    depends_on('glm',        type='build')
    depends_on('pkg-config', type='build')

    depends_on('freetype@2.0:')
    depends_on('pcre')
    depends_on('boost@1.46:+filesystem+system')
    depends_on('glew')
    depends_on('jpeg')
    depends_on('libpng')
    depends_on('pcre')
    depends_on('sdl2')
    depends_on('sdl2-image')

    parallel = False
    force_autoreconf = True

    def url_for_version(self, version):
        tmp = 'https://github.com/acaudwell/Gource/releases/download/gource-{0}/gource-{0}.tar.gz'  # NOQA: ignore=E501
        return tmp.format(version.dotted)

    def configure_args(self):
        spec = self.spec
        return [
            '--disable-dependency-tracking',
            '--without-x',
            '--with-boost=%s' % spec['boost'].prefix
        ]
