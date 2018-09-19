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


class Gmp(AutotoolsPackage):
    """GMP is a free library for arbitrary precision arithmetic, operating
    on signed integers, rational numbers, and floating-point numbers."""

    homepage = "https://gmplib.org"
    url      = "https://ftpmirror.gnu.org/gmp/gmp-6.1.2.tar.bz2"

    version('6.1.2',  '8ddbb26dc3bd4e2302984debba1406a5')
    version('6.1.1',  '4c175f86e11eb32d8bf9872ca3a8e11d')
    version('6.1.0',  '86ee6e54ebfc4a90b643a65e402c4048')
    version('6.0.0a', 'b7ff2d88cae7f8085bd5006096eed470')
    version('6.0.0',  '6ef5869ae735db9995619135bd856b84')
    version('5.1.3', 'a082867cbca5e898371a97bb27b31fea')
    # Old version needed for a binary package in ghc-bootstrap
    version('4.3.2',  'dd60683d7057917e34630b4a787932e8')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
    depends_on('m4', type='build')

    # gmp's configure script seems to be broken; it sometimes misdetects
    # shared library support. Regenerating it fixes the issue.
    force_autoreconf = True

    def configure_args(self):
        args = ['--enable-cxx']
        # This flag is necessary for the Intel build to pass `make check`
        if self.spec.compiler.name == 'intel':
            args.append('CXXFLAGS=-no-ftz')

        return args
