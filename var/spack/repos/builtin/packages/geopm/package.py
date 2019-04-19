# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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
    url      = "https://github.com/geopm/geopm/releases/download/v1.0.0/geopm-1.0.0.tar.gz"
    git      = "https://github.com/geopm/geopm.git"

    # Add additional proper versions and checksums here. "spack checksum geopm"
    version('develop', branch='dev')
    version('master', branch='master')
    version('1.0.0',     sha256='24fe72265a7e44d62bdfe49467c49f0b7a649131ddda402d763c00a49765e1cb')

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
    variant('gnu-ld', default=False, description='Assume C compiler uses gnu-ld.')

    # Added dependencies.
    depends_on('ruby-ronn', type='build', when='+doc')
    depends_on('mpi@2.2:', when='+mpi')

    depends_on('py-matplotlib@2.2.2:2.2.3', type=('build', 'run'))
    depends_on('py-cycler@0.10.0:', type=('build', 'run'))
    depends_on('py-numpy@1.14.3:', type=('build', 'run'))
    depends_on('py-setuptools@39.2.0:', type=('build', 'run'))
    depends_on('py-natsort@5.3.2:', type=('build', 'run'))
    depends_on('py-psutil@5.4.8:', type=('build', 'run'))
    depends_on('py-pandas@0.22.0:', type=('build', 'run'))
    depends_on('py-tables@3.4.3:', type=('build', 'run'))

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
        args.extend(self.with_or_without('gnu-ld'))

        return args
