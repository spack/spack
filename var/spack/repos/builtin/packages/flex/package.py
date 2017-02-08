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


class Flex(AutotoolsPackage):
    """Flex is a tool for generating scanners."""

    homepage = "https://github.com/westes/flex"
    url = "https://github.com/westes/flex/releases/download/v2.6.1/flex-2.6.1.tar.gz"

    version('2.6.3', 'a5f65570cd9107ec8a8ec88f17b31bb1')
    # Problematic version:
    # See issue #2554; https://github.com/westes/flex/issues/113
    # version('2.6.2', 'cc6d76c333db7653d5caf423a3335239')
    version('2.6.1', '05bcd8fb629e0ae130311e8a6106fa82')
    version('2.6.0', '760be2ee9433e822b6eb65318311c19d')
    version('2.5.39', '5865e76ac69c05699f476515592750d7')

    depends_on('bison',         type='build')
    depends_on('gettext@0.19:', type='build')
    depends_on('help2man',      type='build')

    # Older tarballs don't come with a configure script
    depends_on('m4',       type='build')
    depends_on('autoconf', type='build', when='@:2.6.0')
    depends_on('automake', type='build', when='@:2.6.0')
    depends_on('libtool',  type='build', when='@:2.6.0')

    def url_for_version(self, version):
        url = "https://github.com/westes/flex"
        if version >= Version('2.6.1'):
            url += "/releases/download/v{0}/flex-{0}.tar.gz".format(version)
        elif version == Version('2.6.0'):
            url += "/archive/v{0}.tar.gz".format(version)
        elif version >= Version('2.5.37'):
            url += "/archive/flex-{0}.tar.gz".format(version)
        else:
            url += "/archive/flex-{0}.tar.gz".format(version.dashed)

        return url
