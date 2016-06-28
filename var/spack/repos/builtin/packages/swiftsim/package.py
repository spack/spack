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

import llnl.util.tty as tty


class Swiftsim(Package):
    """
    SPH With Inter-dependent Fine-grained Tasking (SWIFT) provides
    astrophysicists with a state of the art framework to perform
    particle based simulations.
    """

    homepage = 'http://icc.dur.ac.uk/swift/'
    url = 'http://gitlab.cosma.dur.ac.uk/swift/swiftsim/repository/archive.tar.gz?ref=v0.3.0'

    version('0.3.0', git='https://gitlab.cosma.dur.ac.uk/swift/swiftsim.git', commit='254cc1b563b2f88ddcf437b1f71da123bb9db733')

    variant('mpi', default=True, description='Enable distributed memory parallelism')

    # Build dependencies
    depends_on('autoconf')
    depends_on('automake')
    depends_on('libtool')
    depends_on('m4')
    # link-time / run-time dependencies
    depends_on('mpi', when='+mpi')
    depends_on('metis')
    depends_on('hdf5~mpi', when='~mpi')
    depends_on('hdf5+mpi', when='+mpi')

    def setup_environment(self, spack_env, run_env):
        # Needed to be able to download from the Durham gitlab repository
        tty.warn('Setting "GIT_SSL_NO_VERIFY=1"')
        tty.warn('This is needed to clone SWIFT repository')
        spack_env.set('GIT_SSL_NO_VERIFY', 1)

    def install(self, spec, prefix):
        # Generate configure from configure.ac
        # and Makefile.am
        libtoolize()
        aclocal()
        autoconf()
        autogen = Executable('./autogen.sh')
        autogen()

        # Configure and install
        options = ['--prefix=%s' % prefix,
                   '--enable-mpi' if '+mpi' in spec else '--disable-mpi',
                   '--enable-optimization']
        configure(*options)
        make()
        make("install")
