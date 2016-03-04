from spack import *


class Netcdf(Package):
    """NetCDF is a set of software libraries and self-describing, machine-independent
    data formats that support the creation, access, and sharing of array-oriented
    scientific data."""

    homepage = "http://www.unidata.ucar.edu/software/netcdf/"
    url      = "ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-4.3.3.tar.gz"

    version('4.4.0', 'cffda0cbd97fdb3a06e9274f7aef438e')
    version('4.3.3', '5fbd0e108a54bd82cb5702a73f56d2ae')

    variant('mpi', default=True, description='Enables MPI parallelism')
    variant('hdf4',    default=False, description="Enable HDF4 support")

    # Dependencies:
    depends_on("curl")  # required for DAP support
    depends_on("hdf", when='+hdf4')
    depends_on("hdf5+mpi~cxx", when='+mpi')  # required for NetCDF-4 support
    depends_on("hdf5~mpi", when='~mpi')  # required for NetCDF-4 support
    depends_on("zlib")  # required for NetCDF-4 support

    def install(self, spec, prefix):
        # Environment variables
        CPPFLAGS = []
        LDFLAGS  = []
        LIBS     = []

        config_args = [
            "--prefix=%s" % prefix,
            "--enable-fsync",
            "--enable-v2",
            "--enable-utilities",
            "--enable-shared",
            "--enable-static",
            "--enable-largefile",
            # necessary for HDF5 support
            "--enable-netcdf-4",
            "--enable-dynamic-loading",
            # necessary for DAP support
            "--enable-dap"
        ]

        if '+mpi' in spec:
            config_args.append('--enable-parallel4')

        CPPFLAGS.append("-I%s/include" % spec['hdf5'].prefix)
        LDFLAGS.append( "-L%s/lib"     % spec['hdf5'].prefix)

        # HDF4 support
        # As of NetCDF 4.1.3, "--with-hdf4=..." is no longer a valid option
        # You must use the environment variables CPPFLAGS and LDFLAGS
        if '+hdf4' in spec:
            config_args.append("--enable-hdf4")
            CPPFLAGS.append("-I%s/include" % spec['hdf'].prefix)
            LDFLAGS.append( "-L%s/lib"     % spec['hdf'].prefix)
            LIBS.append(    "-l%s"         % "jpeg")

        if 'szip' in spec:
            CPPFLAGS.append("-I%s/include" % spec['szip'].prefix)
            LDFLAGS.append( "-L%s/lib"     % spec['szip'].prefix)
            LIBS.append(    "-l%s"         % "sz")

        # Fortran support
        # In version 4.2+, NetCDF-C and NetCDF-Fortran have split.
        # Use the netcdf-fortran package to install Fortran support.

        config_args.append('CPPFLAGS=%s' % ' '.join(CPPFLAGS))
        config_args.append('LDFLAGS=%s'  % ' '.join(LDFLAGS))
        config_args.append('LIBS=%s'     % ' '.join(LIBS))

        configure(*config_args)
        make()
        make("install")
