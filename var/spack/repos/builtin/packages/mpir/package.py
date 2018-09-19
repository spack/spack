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


class Mpir(Package):
    """Multiple Precision Integers and Rationals."""

    homepage = "https://github.com/wbhart/mpir"
    url      = "https://github.com/wbhart/mpir/archive/mpir-2.7.0.tar.gz"
    git      = "https://github.com/wbhart/mpir.git"

    version('develop', branch='master')
    version('2.7.0', '985b5d57bd0e74c74125ee885b9c8f71')
    version('2.6.0', 'ec17d6a7e026114ceb734b2466aa0a91')

    # This setting allows mpir to act as a drop-in replacement for gmp
    variant('gmp_compat',        default=False,
            description='Compile with GMP library compatibility')

    # Build dependencies
    depends_on('autoconf', type='build')

    # Other dependencies
    depends_on('yasm')

    def install(self, spec, prefix):
        # We definitely don't want to have MPIR build its
        # own version of YASM. This tries to install it
        # to a system directory.
        options = ['--prefix={0}'.format(prefix),
                   '--with-system-yasm']

        if '+gmp_compat' in spec:
            options.extend(['--enable-gmpcompat'])

        configure(*options)
        make()
        if self.run_tests:
            make('check')
        make('install')
