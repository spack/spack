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


class Mxml(AutotoolsPackage):
    """Mini-XML is a small XML library that you can use to read and write XML
    and XML-like data files in your application without requiring large
    non-standard libraries.
    """

    homepage = "http://michaelrsweet.github.io/mxml/"
    url      = "https://github.com/michaelrsweet/mxml/releases/download/release-2.10/mxml-2.10.tar.gz"

    version('2.10', '8804c961a24500a95690ef287d150abe')
    version('2.9', 'e21cad0f7aacd18f942aa0568a8dee19')
    version('2.8', 'd85ee6d30de053581242c4a86e79a5d2')
    version('2.7', '76f2ae49bf0f5745d5cb5d9507774dc9')
    version('2.6', '68977789ae64985dddbd1a1a1652642e')
    version('2.5', 'f706377fba630b39fa02fd63642b17e5')

    def url_for_version(self, version):
        if version <= Version('2.7'):
            return 'https://github.com/michaelrsweet/mxml/archive/release-{0}.tar.gz'.format(version)
        else:
            return 'https://github.com/michaelrsweet/mxml/releases/download/release-{0}/mxml-{0}.tar.gz'.format(version)

    def configure_args(self):
        return [
            # ADIOS build with -fPIC, so we need it too (avoid linkage issue)
            'CFLAGS={0}'.format(self.compiler.pic_flag),
            # Default is non-shared, but avoid any future surprises
            '--disable-shared',
        ]
