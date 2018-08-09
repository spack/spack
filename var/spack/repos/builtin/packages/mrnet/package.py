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


class Mrnet(AutotoolsPackage):
    """The MRNet Multi-Cast Reduction Network."""

    homepage = "http://paradyn.org/mrnet"
    url      = "http://ftp.cs.wisc.edu/pub/paradyn/mrnet/mrnet_5.0.1.tar.gz"
    git      = "https://github.com/dyninst/mrnet.git"
    list_url = "http://ftp.cs.wisc.edu/paradyn/mrnet"

    version('5.0.1-3', branch='master')
    version('5.0.1-2', commit='20b1eacfc6d680d9f6472146d2dfaa0f900cc2e9')
    version('5.0.1', '17f65738cf1b9f9b95647ff85f69ecdd')
    version('4.1.0', '5a248298b395b329e2371bf25366115c')
    version('4.0.0', 'd00301c078cba57ef68613be32ceea2f')

    variant('cti', default=False,
            description="Build the MRNet with the CTI startup option")
    variant('lwthreads', default=False,
            description="Also build the MRNet LW threadsafe libraries")
    parallel = False

    depends_on("boost")
    depends_on("cti", when='+cti')

    def configure_args(self):
        spec = self.spec
        config_args = ['--enable-shared']

        # Build the MRNet LW thread safe libraries when the
        # lwthreads variant is present
        if '+lwthreads' in spec:
            config_args.append('--enable-ltwt-threadsafe')
        # Build the MRNet with CTI based start-up when
        # the cti variant is present
        if '+cti' in spec:
            config_args.append('--with-startup=cray-cti')
            cti = self.spec['cti'].prefix
            config_args.append('--with-craycti-inc=-I%s/include' % cti)
            config_args.append('--with-craycti-lib=-I%s/lib' % cti)
        return config_args
