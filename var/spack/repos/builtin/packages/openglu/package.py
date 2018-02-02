##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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


class Openglu(Package):
    """Placeholder for external OpenGL utility library (GLU) from hardware
       vendors"""

    homepage = "https://www.opengl.org/resources/libraries"
    url      = "https://www.opengl.org/resources/libraries"

    # URL here is arbitrary, just so that spack's fetcher does not throw
    # an error
    version('1.3', 'bbc57d4fe3bd3fb095bdbef6fcb977c4',
            url='https://www.mesa3d.org/archive/glu/glu-9.0.0.tar.gz')

    provides('glu@:1.3', when='@1.3:')
    provides('glu@:1.2', when='@1.2:')
    provides('glu@:1.1', when='@1.1:')
    provides('glu@:1.', when='@1.0:')

    def install(self, spec, prefix):
        msg = """This package is intended to be a placeholder for system-provided
        OpenGL utility (GLU) libraries from hardware vendors.  Please
        download and install the GLU drivers/libraries for your
        graphics hardware separately, and then set that up as an
        external package.  An example of a working packages.yaml:

        packages:
          openglu:
            paths:
              openglu@1.3: /opt/opengl
            buildable: False

        In that case, /opt/opengl/ should contain these two folders:

        include/GL/       (opengl headers, including "glu.h")
        lib               (opengl libraries, including "libGLU.so")

        On Apple Darwin (OS X, macOS) systems, this package is
        normally installed as part of the XCode Command Line Tools in
        /usr/X11R6, so a working packages.yaml would be

        packages:
          openglu:
            paths:
              openglu@1.3: /usr/X11R6
            buildable: False

        In that case, /usr/X11R6 should contain

        include/GL       (GLU headers, including "glu.h")
        lib              (GLU libraries, including "libGLU.dylib")

        """

        raise InstallError(msg)
