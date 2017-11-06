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


class Libxc(Package):
    """Libxc is a library of exchange-correlation functionals for
    density-functional theory."""

    homepage = "http://www.tddft.org/programs/octopus/wiki/index.php/Libxc"
    url      = "http://www.tddft.org/programs/octopus/down.php?file=libxc/libxc-2.2.2.tar.gz"

    version('3.0.0', '8227fa3053f8fc215bd9d7b0d36de03c')
    version('2.2.2', 'd9f90a0d6e36df6c1312b6422280f2ec')
    version('2.2.1', '38dc3a067524baf4f8521d5bb1cd0b8f')

    @property
    def libs(self):
        """Libxc can be queried for the following parameters:

        - "static": returns the static library version of libxc
            (by default the shared version is returned)

        :return: list of matching libraries
        """
        query_parameters = self.spec.last_query.extra_parameters

        libraries = ['libxc']

        # Libxc installs both shared and static libraries.
        # If a client ask for static explicitly then return
        # the static libraries
        shared = False if 'static' in query_parameters else True

        # Libxc has a fortran90 interface: give clients the
        # possibility to query for it
        if 'fortran' in query_parameters:
            libraries = ['libxcf90'] + libraries

        return find_libraries(
            libraries, root=self.prefix, shared=shared, recurse=True
        )

    def install(self, spec, prefix):
        # Optimizations for the Intel compiler, suggested by CP2K
        optflags = '-O2'
        if self.compiler.name == 'intel':
            optflags += ' -xAVX -axCORE-AVX2 -ipo'
            if which('xiar'):
                env['AR'] = 'xiar'

        if 'CFLAGS' in env and env['CFLAGS']:
            env['CFLAGS'] += ' ' + optflags
        else:
            env['CFLAGS'] = optflags

        if 'FCFLAGS' in env and env['FCFLAGS']:
            env['FCFLAGS'] += ' ' + optflags
        else:
            env['FCFLAGS'] = optflags

        configure('--prefix={0}'.format(prefix),
                  '--enable-shared')

        make()

        # libxc provides a testsuite, but many tests fail
        # http://www.tddft.org/pipermail/libxc/2013-February/000032.html
        # make('check')

        make('install')
