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


class Wcslib(AutotoolsPackage):
    """WCSLIB a C implementation of the coordinate transformations
    defined in the FITS WCS papers."""

    homepage = "http://www.atnf.csiro.au/people/mcalabre/WCS/wcslib/"
    url      = "ftp://ftp.atnf.csiro.au/pub/software/wcslib/wcslib-5.18.tar.bz2"

    version('5.18', '67a78354be74eca4f17d3e0853d5685f')

    variant('cfitsio', default=False, description='Include CFITSIO support')
    variant('x',       default=False, description='Use the X Window System')

    depends_on('gmake', type='build')
    depends_on('flex@2.5.9:', type='build')
    depends_on('cfitsio', when='+cfitsio')
    depends_on('libx11', when='+x')

    def configure_args(self):
        spec = self.spec

        # TODO: Add PGPLOT package
        args = ['--without-pgplot']

        if '+cfitsio' in spec:
            args.extend([
                '--with-cfitsio',
                '--with-cfitsiolib={0}'.format(
                    spec['cfitsio'].libs.directories[0]),
                '--with-cfitsioinc={0}'.format(
                    spec['cfitsio'].headers.directories[0]),
            ])
        else:
            args.append('--without-cfitsio')

        if '+x' in spec:
            args.append('--with-x')
        else:
            args.append('--without-x')

        return args
