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

    version('develop', branch='dev', preferred=True)
    version('0.1.1', tag='v0.1.1')

    variant('debug', default='False', description='Enable debug build options')
    variant('hdf5', default='False', description='Build with parallel HDF5 (install with `^hdf5~mpi` for serial)')
    variant('numa', default='False', description='Build with NUMA')

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
    depends_on('pkgconfig')

    # Optional dependencies

    # UnifyCR's integration with HDF5 is still a WIP and is currently
    # configured for serial only. HDF5 is parallel by default.
    #
    # To build with serial HDF5, use `spack install unifycr+hdf5 ^hdf5~mpi`
    #
    # Once UnifyCR is compatible with parallel HDF5, excluding `^hdf5~mpi` from
    # the install line will build UnifyCR with parallel HDF5.

    # v0.1.1 not HDF5 compatible; can change when v0.1.1 is no longer supported
    depends_on('hdf5', when='@0.1.2: +hdf5')
    depends_on('numactl',  when='+numa')

    # we depend on numactl, which does't currently build on darwin
    conflicts('platform=darwin', when='+numa')
    conflicts('+hdf5', when='@:0.1.1')

    # Parallel disabled to prevent tests from being run out-of-order when
    # installed with the --test={root, all} option. Can potentially change if
    # we add a +test configure option and variant.
    parallel = False
    build_directory = 'spack-build'

    def configure_args(self):
        spec = self.spec
        args = []

        if spec.satisfies('@0.1.1'):
            env['CC'] = spec['mpi'].mpicc

        # UnifyCR's configure requires the exact path for HDF5
        def hdf5_compiler_path(name):
            if '~mpi' in spec[name]:  # serial HDF5
                return spec[name].prefix.bin.h5cc
            else:  # parallel HDF5
                return spec[name].prefix.bin.h5pcc

        args.extend(self.with_or_without('numa',
                                         lambda x: spec['numactl'].prefix))
        args.extend(self.with_or_without('hdf5', hdf5_compiler_path))

        if '+debug' in spec:
            args.append('--enable-debug')

        if spack.config.get('config:debug'):
            args.append('--disable-silent-rules')
        else:
            args.append('--enable-silent-rules')

        return args

#    @when('@develop') TODO: uncomment when we `make dist` a stable release
    def autoreconf(self, spec, prefix):
        bash = which('bash')
        bash('./autogen.sh')
