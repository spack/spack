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


class Jasper(AutotoolsPackage):
    """Library for manipulating JPEG-2000 images"""

    homepage = "https://www.ece.uvic.ca/~frodo/jasper/"
    url = "https://www.ece.uvic.ca/~frodo/jasper/software/jasper-1.900.1.zip"

    version('1.900.1', 'a342b2b4495b3e1394e161eb5d85d754')

    variant('shared', default=True,
            description='Builds shared versions of the libraries')
    variant('debug', default=False,
            description='Builds debug versions of the libraries')

    depends_on('libjpeg-turbo')

    # Fixes a bug (still in upstream as of v.1.900.1) where an assertion fails
    # when certain JPEG-2000 files with an alpha channel are processed
    # see: https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=469786
    patch('fix_alpha_channel_assert_fail.patch')

    def configure_args(self):
        spec = self.spec
        args = ['--mandir={0}'.format(spec.prefix.man)]

        if '+shared' in spec:
            args.append('--enable-shared')

        if '+debug' not in spec:
            args.append('--disable-debug')

        return args
