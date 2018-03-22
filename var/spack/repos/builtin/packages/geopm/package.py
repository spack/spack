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


class Geopm(Package):

    """GEOPM is an extensible power management framework targeting HPC.
    The GEOPM package provides libgeopm, libgeopmpolicy and applications
    geopmctl and geopmpolicy. GEOPM is designed to be extended for new control
    algorithms and new hardware power management features via its plugin
    infrastructure.

    Note: GEOPM interfaces with hardware using Model Specific Registers (MSRs).
    For propper usage make sure MSRs are made available directly or via the
    msr-safe kernel module by your administrator."""

    homepage = "https://geopm.github.io"
    url      = "https://github.com/geopm/geopm/releases/download/v0.4.0/geopm-0.4.0.tar.gz"

    # Add additional proper versions and checksums here. "spack checksum geopm"
    version('0.4.0', 'd4cc8fffe521296dab379857d7e2064d')
    version('0.3.0', '568fd37234396fff134f8d57b60f2b83')
    version('master', git='https://github.com/geopm/geopm.git', branch='master')
    version('develop', git='https://github.com/geopm/geopm.git', branch='dev')

    # Variants reflecting most ./configure --help options
    variant('debug', default=False, description='Enable debug.')
    variant('coverage', default=False, description='Enable for test coverage support and enable debug.')
    variant('procfs', default=True, description='Use procfs depending on operating systems.')
    variant('mpi', default=True, description='To disable dependent MPI components.')
    variant('fortran', default=True, description='Build fortran interface.')
    variant('doc', default=True, description='Create man pages with ronn.')
    variant('openmp', default=True, description='Build with OpenMP.')
    variant('ompt', default=False, description='Use OpenMP Tool interface.')
    variant('hwloc', default=True, description='Build with hwloc.')
    variant('gnu-ld', default=False, description='Assume C uses gnu-ld.')
    variant('python', default=False, description='Using this option python dependencies are build using spack. These are required for running. It is assumed they are installed on the system. Use this only if this is not the case. (Long build time).')

    # Added dependencies.
    depends_on('m4', type='build')
    depends_on('automake', type='build')
    depends_on('autoconf', type='build')
    depends_on('libtool', type='build')
    depends_on('numactl', type='build')
    depends_on('mpi', when='+mpi', type=('build', 'run'))
    depends_on('hwloc', type=('build', 'run'))

    # python dependcies for running:
    depends_on('py-pandas', type='run', when='+python')
    depends_on('py-numpy', type='run', when='+python')
    depends_on('py-natsort', type='run', when='+python')
    depends_on('py-matplotlib', type='run', when='+python')

    parallel = False

    def install(self, spec, prefix):
        spec = self.spec
        args = []

        args.append('--prefix=%s' % prefix)

        if '+debug' in spec:
            args.append('--enable-debug')

        if '+coverage' in spec:
            args.append('--enable-coverage')

        if '+overhead' in spec:
            args.append('--enable-overhead')

        if '~procfs' in spec:
            args.append('--disable-procfs')

        if '~mpi' in spec:
            args.append('--disable-mpi')
        else:
            args.extend([
                '--with-mpi-bin={0}'.format(spec['mpi'].prefix.bin),
                '--with-mpicc={0}'.format(spec['mpi'].mpicc),
                '--with-mpicxx={0}'.format(spec['mpi'].mpicxx),
                '--with-mpifc={0}'.format(spec['mpi'].mpifc),
                '--with-mpif77={0}'.format(spec['mpi'].mpif77),
            ])

        if '~fortran' in spec:
            args.append('--disable-fortran')

        if '~doc' in spec:
            args.append('--disable-doc')

        if '~openmp' in spec:
            args.append('--disable-openmp')

        if '+ompt' in spec:
            args.append('--enable-ompt')

        if '+gnu-ld' in spec:
            args.append('--with-gnu-ld')

        if '+hwloc' in spec:
            args.append('--with-hwloc={0}'.format(spec['hwloc'].prefix))
        # else:
        #     args.append('--without-hwloc')

        bash = which('bash')
        bash('./autogen.sh')
        configure(*args)
        make()
        make('install')
