# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class Unifycr(AutotoolsPackage):
    """User level file system that enables applications to use node-local
    storage as burst buffers for shared files. Supports scalable and efficient
    aggregation of I/O bandwidth from burst buffers while having the same life
    cycle as a batch-submitted job.
    UnifyCR is designed to support common I/O workloads, including
    checkpoint/restart. While primarily designed for N-N write/read, UnifyCR
    compliments its functionality with the support for N-1 write/read."""

    homepage = "https://github.com/LLNL/UnifyCR"
    git      = "https://github.com/LLNL/UnifyCR.git"
    url      = "https://github.com/LLNL/UnifyCR/archive/v0.1.1.tar.gz"

    version('develop', branch='dev', preferred=True)
    version('0.1.1', sha256='f0628f661d5eff67a55ba2bf254dc38636525c5e191d5f32b9e128294b8f8051')

    variant('debug', default='False', 
            description='Enable debug build options')
    variant('hdf5', default='True',
            description='Build with HDF5 (currently serial only)')
    variant('numa', default='True',
            description='Build with NUMA')
    variant('verbose', default='False', 
            description='Add VERBOSE arguments to make')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')

    # Required dependencies
    # Latest version of GOTCHA has API changes that break UnifyCR.
    # Updates to UnifyCR are coming in order to fix this.
    depends_on('gotcha@0.0.2')
    depends_on('leveldb')
    depends_on('mpi')
    depends_on('pkg-config@0.9.0:')

    # Optional dependencies
    # UnifyCR's integration with HDF5 is still a WIP and is currently
    # configured for serial only. HDF5 is parallel by default. Once fully
    # integrated and UnifyCR users can choose to configure with serial/parallel
    # HDF5, the ability for the user to choose needs to made available here as
    # well.
    # If using custom packages.yaml, can put `variante: ~mpi` under hdf5 or if
    # you don't want to restrict other packages using parallel hdf5, identify
    # the path to h5cc using the a pattern similar to `hdf5@<version>~mpi:
    # path/to/h5cc` for serial HDF5.

    # TODO: Implement capability for user to choose serial/parallel HDF5

    # v0.1.1 not HDF5 compatible; can change when v0.1.1 is no longer supported
    depends_on('hdf5~mpi', when='@0.1.2: +hdf5')
    depends_on('numactl',  when='+numa')

    # we depend on numactl, which does't currently build on darwin
    conflicts('platform=darwin', when='+numa')

    # Parallel disabled to prevent tests from being run out-of-order when
    # installed with the --test={root, all} option. Can potentially change if
    # we add a +test configure option and variant.
    parallel = False
    build_directory = 'spack-build'

    def configure_args(self):
        spec = self.spec
        config_args = []

        if spec.satisfies('@0.1.1'):
            env['CC'] = spec['mpi'].mpicc

        config_args.extend(self.with_or_without('numa'))
        config_args.extend(self.with_or_without('hdf5'))

        if '+debug' in spec:
            config_args.append('--enable-debug')

        if '+verbose' in spec:
            config_args.append('--disable-silent-rules')
        else:
            config_args.append('--enable-silent-rules')

        return config_args

#   @when('@develop') TODO: uncomment when we `make dist` a stable release
    def autoreconf(self, spec, prefix):
        bash = which('bash')
        bash('./autogen.sh')
