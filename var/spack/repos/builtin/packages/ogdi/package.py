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


class Ogdi(AutotoolsPackage):
    """OGDI is the Open Geographic Datastore Interface. OGDI is an application
    programming interface (API) that uses a standardized access methods to work
    in conjunction with GIS software packages (the application) and various
    geospatial data products."""

    homepage = "http://ogdi.sourceforge.net/"
    url      = "https://sourceforge.net/projects/ogdi/files/ogdi/3.2.0/ogdi-3.2.0.tar.gz"

    version('3.2.0', '6fca8f38b2c1e4abb02a4dbedc8bab68')

    depends_on('gmake', type='build')
    depends_on('proj')
    depends_on('zlib')
    depends_on('expat')

    parallel = False

    # FIXME: Known installation issues on macOS
    # https://github.com/OSGeo/homebrew-osgeo4mac/blob/master/Formula/ogdi.rb

    def configure_args(self):
        # Set the TOPDIR environment variable to point to the home directory
        # of the OGDI source tree.
        env['TOPDIR'] = self.stage.source_path
        env['CFLAGS'] = self.compiler.pic_flag

        spec = self.spec

        return [
            '--with-proj={0}'.format(spec['proj'].prefix),
            '--with-zlib={0}'.format(spec['zlib'].prefix),
            '--with-expat={0}'.format(spec['expat'].prefix),
        ]
