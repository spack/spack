# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class Unifyfs(AutotoolsPackage):
    """User level file system that enables applications to use node-local
    storage as burst buffers for shared files. Supports scalable and efficient
    aggregation of I/O bandwidth from burst buffers while having the same life
    cycle as a batch-submitted job.
    UnifyFS is designed to support common I/O workloads, including
    checkpoint/restart. While primarily designed for N-N write/read, UnifyFS
    compliments its functionality with the support for N-1 write/read."""

    homepage = "https://github.com/LLNL/UnifyFS"
    git      = "https://github.com/LLNL/UnifyFS.git"
    url      = "https://github.com/LLNL/UnifyFS/releases/download/v0.2.0/unifycr-0.2.0.tar.gz"
    maintainers = ['CamStan']

    version('develop', branch='dev', preferred=True)
    version('0.2.0', sha256='7439b0e885234bc64e8cbb449d8abfadd386692766b6f00647a7b6435efb2066')

    variant('hdf5', default='False', description='Build with parallel HDF5 (install with `^hdf5~mpi` for serial)')
    variant('fortran', default='False', description='Build with gfortran support')
    variant('numa', default='False', description='Build with NUMA')
    variant('pmpi', default='False', description='Enable transparent mount/unmount at MPI_Init/Finalize')
    variant('pmi', default='False', description='Enable PMI2 build options')
    variant('pmix', default='False', description='Enable PMIx build options')

    depends_on('autoconf',  type='build')
    depends_on('automake',  type='build')
    depends_on('libtool',   type='build')
    depends_on('m4',        type='build')
    depends_on('pkgconfig', type='build')

    # Required dependencies
    depends_on('flatcc')
    # Latest version of GOTCHA has API changes that break UnifyFS.
    # Updates to UnifyFS are coming in order to fix this.
    depends_on('gotcha@0.0.2')
    depends_on('leveldb')
    depends_on('margo')
    depends_on('mercury+bmi+sm')
    depends_on('mpi')

    # Optional dependencies
    depends_on('hdf5', when='+hdf5')
    depends_on('numactl',  when='+numa')

    conflicts('^mercury~bmi')
    conflicts('^mercury~sm')
    # UnifyFS depends on numactl, which doesn't currently build on darwin.
    conflicts('platform=darwin', when='+numa')
    # Known compatibility issues with ifort and xlf. Fixes coming.
    conflicts('%intel', when='+fortran')
    conflicts('%xl', when='+fortran')

    # Parallel disabled to prevent tests from being run out-of-order when
    # installed with the --test={root, all} option.
    parallel = False
    debug_build = False
    build_directory = 'spack-build'

    # Only builds properly with debug symbols when flag_handler =
    # build_system_flags.
    # Override the default behavior in order to set debug_build which is used
    # to set the --disable-silent-rules option when configuring.
    def flag_handler(self, name, flags):
        if name in ('cflags', 'cppflags'):
            if '-g' in flags:
                self.debug_build = True
        return (None, None, flags)

    def configure_args(self):
        spec = self.spec
        args = []

        # UnifyFS's configure requires the exact path for HDF5
        def hdf5_compiler_path(name):
            if '~mpi' in spec[name]:  # serial HDF5
                return spec[name].prefix.bin.h5cc
            else:  # parallel HDF5
                return spec[name].prefix.bin.h5pcc

        args.extend(self.with_or_without('numa',
                                         lambda x: spec['numactl'].prefix))
        args.extend(self.with_or_without('hdf5', hdf5_compiler_path))

        if '+fortran' in spec:
            args.append('--enable-fortran')

        if '+pmpi' in spec:
            args.append('--enable-mpi-mount')

        if '+pmi' in spec:
            args.append('--enable-pmi')

        if '+pmix' in spec:
            args.append('--enable-pmix')

        if self.debug_build:
            args.append('--disable-silent-rules')
        else:
            args.append('--enable-silent-rules')

        return args

    @when('@develop')
    def autoreconf(self, spec, prefix):
        bash = which('bash')
        bash('./autogen.sh')
