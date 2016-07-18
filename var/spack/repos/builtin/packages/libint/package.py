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


class Libint(Package):
    """Libint is a high-performance library for computing
    Gaussian integrals in quantum mechanics."""

    homepage = "https://github.com/evaleev/libint"
    url      = "https://github.com/evaleev/libint/archive/v2.1.0.tar.gz"

    version('2.1.0', 'd0dcb985fe32ddebc78fe571ce37e2d6')
    version('1.1.6', '990f67b55f49ecc18f32c58da9240684')

    # Build dependencies
    depends_on('autoconf@2.52:', type='build')
    depends_on('automake',       type='build')
    depends_on('libtool',        type='build')

    # Libint 2 dependencies
    depends_on('boost', when='@2:')
    depends_on('gmp',   when='@2:')

    def url_for_version(self, version):
        base_url = "https://github.com/evaleev/libint/archive"
        if version == Version('1.0.0'):
            return "{0}/LIBINT_1_00.tar.gz".format(base_url)
        elif version < Version('2.1.0'):
            return "{0}/release-{1}.tar.gz".format(base_url, version.dashed)
        else:
            return "{0}/v{1}.tar.gz".format(base_url, version)

    def install(self, spec, prefix):
        # Generate configure
        libtoolize()
        aclocal('-I', 'lib/autoconf')
        autoconf()

        # Optimizations for the Intel compiler, suggested by CP2K
        optflags = '-O2'
        if self.compiler.name == 'intel':
            optflags += ' -xAVX -axCORE-AVX2 -ipo'
            if which('xiar'):
                env['AR'] = 'xiar'

        env['CFLAGS']   = optflags
        env['CXXFLAGS'] = optflags

        config_args = [
            '--prefix={0}'.format(prefix),
            '--with-cc-optflags={0}'.format(optflags),
            '--with-cxx-optflags={0}'.format(optflags)
        ]

        # Options required by CP2K, removed in libint 2
        if self.version < Version('2.0.0'):
            config_args.extend([
                '--with-libint-max-am=5',
                '--with-libderiv-max-am1=4'
            ])

        configure(*config_args)
        make()

        # Testing suite was added in libint 2
        if self.version >= Version('2.0.0'):
            make('check')

        make('install')
