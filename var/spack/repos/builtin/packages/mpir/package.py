# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
