from spack import *
import os

class Ior(Package):
    """The IOR software is used for benchmarking parallel file systems
    using POSIX, MPI-IO, or HDF5 interfaces."""

    homepage = "http://www.nersc.gov/users/computational-systems/cori/nersc-8-procurement/trinity-nersc-8-rfp/nersc-8-trinity-benchmarks/ior/"
    url      = "https://github.com/LLNL/ior/archive/3.0.1.tar.gz"

    version('3.0.1', '71150025e0bb6ea1761150f48b553065')

    variant('hdf5',  default=False, description='support IO with HDF5 backend')
    variant('ncmpi', default=False, description='support IO with NCMPI backend')

    depends_on('mpi')
    depends_on('hdf5+mpi',   when='+hdf5')
    depends_on('netcdf+mpi', when='+ncmpi')


    def install(self, spec, prefix):
        os.system('./bootstrap')

        config_args = [
            'MPICC=%s' % spec['mpi'].prefix.bin + '/mpicc',
            '--prefix=%s' % prefix,
        ]

        if '+hdf5' in spec:
            config_args.append('--with-hdf5')

        if '+ncmpi' in spec:
            config_args.append('--with-ncmpi')

        configure(*config_args)

        make()
        make('install')
