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


class Geopm(AutotoolsPackage):

    """GEOPM is an extensible power management framework targeting HPC.
    The GEOPM package provides libgeopm, libgeopmpolicy and applications
    geopmctl and geopmpolicy, as well as tools for postprocessing.
    GEOPM is designed to be extended for new control algorithms and new
    hardware power management features via its plugin infrastructure.

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
    variant('coverage', default=False, description='Enable test coverage support, enables debug by default.')
    variant('procfs', default=True, description='Enable procfs (disable for OSes not using procfs).')
    variant('mpi', default=True, description='Enable MPI dependent components.')
    variant('fortran', default=True, description='Build fortran interface.')
    # TODO: add explicit ruby-ronn dependency. For +doc.
    # This is currently done by the install process and should be handled
    # as configure option --with-ronn=/path/to/ronn.
    # Changes are required in the GEOPM install! To be done in future version.
    variant('doc', default=True, description='Create man pages with ruby-ronn.')
    variant('openmp', default=True, description='Build with OpenMP.')
    variant('ompt', default=False, description='Use OpenMP Tools Interface.')
    variant('hwloc', default=True, description='Build with hwloc.')
    variant('gnu-ld', default=False, description='Assume C compiler uses gnu-ld.')

    # Added dependencies.
    depends_on('m4', type='build')
    depends_on('automake', type='build')
    depends_on('autoconf', type='build')
    depends_on('libtool', type='build')
    depends_on('numactl', type=('build', 'run'))
    depends_on('mpi', when='+mpi', type=('build', 'run'))
    # TODO: check if hwloc@specific-version still required with future openmpi
    depends_on('hwloc@1.11.9', when='+hwloc', type=('build', 'run'))
    depends_on('py-pandas', type='run')
    depends_on('py-numpy', type='run')
    depends_on('py-natsort', type='run')
    depends_on('py-matplotlib', type='run')

    parallel = False

    def configure_args(self):
        spec = self.spec
        args = []

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
        else:
            args.append('--without-hwloc')

        return args
