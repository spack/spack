# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
    git      = "https://github.com/geopm/geopm.git"

    # Add additional proper versions and checksums here. "spack checksum geopm"
    version('develop', branch='dev')
    version('master', branch='master')
    version('0.5.0', '61b454bc74d4606fe84818aef16c1be4')
    version('0.4.0', 'd4cc8fffe521296dab379857d7e2064d')
    version('0.3.0', '568fd37234396fff134f8d57b60f2b83')

    # Variants reflecting most ./configure --help options
    variant('debug', default=False, description='Enable debug.')
    variant('coverage', default=False, description='Enable test coverage support, enables debug by default.')
    variant('overhead', default=False, description='Enable GEOPM to calculate and display time spent in GEOPM API calls.')
    variant('procfs', default=True, description='Enable procfs (disable for OSes not using procfs).')
    variant('mpi', default=True, description='Enable MPI dependent components.')
    variant('fortran', default=True, description='Build fortran interface.')
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
    depends_on('ruby-ronn', type='build', when='+doc')
    depends_on('doxygen', type='build', when='+doc')
    depends_on('numactl')
    depends_on('mpi', when='+mpi')
    # TODO: check if hwloc@specific-version still required with future openmpi
    depends_on('hwloc@1.11.9', when='+hwloc')
    depends_on('json-c')
    depends_on('py-pandas', type='run')
    depends_on('py-numpy', type='run')
    depends_on('py-natsort', type='run')
    depends_on('py-matplotlib', type='run')

    parallel = False

    def configure_args(self):
        args = []
        args.extend(self.enable_or_disable('debug'))
        args.extend(self.enable_or_disable('coverage'))
        args.extend(self.enable_or_disable('overhead'))
        args.extend(self.enable_or_disable('procfs'))
        args.extend(self.enable_or_disable('mpi'))
        args.extend(self.enable_or_disable('fortran'))
        args.extend(self.enable_or_disable('doc'))
        args.extend(self.enable_or_disable('openmp'))
        args.extend(self.enable_or_disable('ompt'))
        args.extend(self.with_or_without('hwloc', activation_value='prefix'))
        args.extend(self.with_or_without('gnu-ld'))

        return args
